from typing import Dict, List, Any, Optional
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from .config import settings

logger = logging.getLogger(__name__)

class CohereEmbeddingService:
    """
    Service for generating embeddings using Cohere's embed-multilingual-v3.0 model
    """
    def __init__(self):
        self.client = cohere.Client(settings.cohere_api_key)
        self.model = settings.embedding_model  # embed-multilingual-v3.0

    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model
            )
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise

class QdrantRetrievalService:
    """
    Service for vector retrieval using Qdrant
    """
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """
        Create the collection if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")
        except:
            # Create collection with appropriate vector size
            # Cohere embed-multilingual-v3.0 produces 1024-dim vectors
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
            )
            logger.info(f"Created collection {self.collection_name}")

    def search_chunks_full_book(self, query_embedding: List[float], limit: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for relevant chunks in the full book
        """
        try:
            # Build filters if provided
            qdrant_filters = None
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    if isinstance(value, list):
                        filter_conditions.append(
                            models.FieldCondition(
                                key=f"metadata.{key}",
                                match=models.MatchAny(any=value)
                            )
                        )
                    else:
                        filter_conditions.append(
                            models.FieldCondition(
                                key=f"metadata.{key}",
                                match=models.MatchValue(value=value)
                            )
                        )

                if filter_conditions:
                    qdrant_filters = models.Filter(must=filter_conditions)

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=qdrant_filters,
                with_payload=True
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    "chunk_id": result.id,
                    "content": result.payload.get("content", ""),
                    "score": result.score,
                    "module": result.payload.get("metadata", {}).get("module", ""),
                    "chapter": result.payload.get("metadata", {}).get("chapter", ""),
                    "subsection": result.payload.get("metadata", {}).get("subsection", ""),
                    "page_reference": result.payload.get("metadata", {}).get("page_reference", "")
                }
                formatted_results.append(formatted_result)

            logger.info(f"Found {len(formatted_results)} results for full-book search")
            return formatted_results

        except Exception as e:
            logger.error(f"Error in full-book search: {str(e)}")
            return []

    def search_chunks_per_page(self, query_embedding: List[float], selected_text_embedding: List[float], limit: int = 5) -> List[Dict]:
        """
        Search for relevant chunks using both query and selected text embeddings
        """
        try:
            # First search using the selected text embedding to find related content
            selected_text_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=selected_text_embedding,
                limit=limit,
                with_payload=True
            )

            # Then search using the query embedding
            query_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            # Combine and deduplicate results, prioritizing those from selected text search
            all_results = {}

            # Add selected text results with higher priority
            for result in selected_text_results:
                all_results[result.id] = {
                    "chunk_id": result.id,
                    "content": result.payload.get("content", ""),
                    "score": result.score,
                    "module": result.payload.get("metadata", {}).get("module", ""),
                    "chapter": result.payload.get("metadata", {}).get("chapter", ""),
                    "subsection": result.payload.get("metadata", {}).get("subsection", ""),
                    "page_reference": result.payload.get("metadata", {}).get("page_reference", "")
                }

            # Add query results if not already present
            for result in query_results:
                if result.id not in all_results:
                    all_results[result.id] = {
                        "chunk_id": result.id,
                        "content": result.payload.get("content", ""),
                        "score": result.score,
                        "module": result.payload.get("metadata", {}).get("module", ""),
                        "chapter": result.payload.get("metadata", {}).get("chapter", ""),
                        "subsection": result.payload.get("metadata", {}).get("subsection", ""),
                        "page_reference": result.payload.get("metadata", {}).get("page_reference", "")
                    }

            # Sort by score and return top results
            sorted_results = sorted(all_results.values(), key=lambda x: x["score"], reverse=True)[:limit]

            logger.info(f"Found {len(sorted_results)} results for per-page search")
            return sorted_results

        except Exception as e:
            logger.error(f"Error in per-page search: {str(e)}")
            return []

    def health_check(self) -> bool:
        """
        Check if Qdrant service is healthy
        """
        try:
            # Try to get collection info
            self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False

class RAGService:
    """
    Main RAG service that combines Cohere embedding and Qdrant retrieval
    """
    def __init__(self):
        self.cohere_service = CohereEmbeddingService()
        self.qdrant_service = QdrantRetrievalService()

    def retrieve_context(self, query: str, retrieval_mode: str = "full-book",
                        selected_text: Optional[str] = None,
                        metadata_filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve context chunks based on the query and mode
        """
        try:
            # Generate embedding for the query
            query_embedding = self.cohere_service.generate_single_embedding(query)

            if retrieval_mode == "full-book":
                # Full-book search with optional metadata filters
                results = self.qdrant_service.search_chunks_full_book(
                    query_embedding=query_embedding,
                    limit=5,
                    filters=metadata_filters
                )
            else:  # per-page mode
                # Per-page search using selected text
                if not selected_text:
                    logger.warning("Selected text is required for per-page retrieval mode")
                    return []

                # Generate embedding for the selected text
                selected_text_embedding = self.cohere_service.generate_single_embedding(selected_text)

                # Perform per-page search
                results = self.qdrant_service.search_chunks_per_page(
                    query_embedding=query_embedding,
                    selected_text_embedding=selected_text_embedding,
                    limit=5
                )

            return results

        except Exception as e:
            logger.error(f"Error in retrieve_context: {str(e)}")
            return []

    def health_check(self) -> bool:
        """
        Check if RAG service is healthy
        """
        return self.qdrant_service.health_check()

# Create a singleton instance
rag_service = RAGService()