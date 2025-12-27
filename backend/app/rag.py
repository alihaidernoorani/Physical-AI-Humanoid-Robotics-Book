from typing import Dict, List, Any, Optional, Literal
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from cohere.errors import ApiError
from .config import settings

logger = logging.getLogger(__name__)

# Type alias for input_type parameter
InputType = Literal["search_query", "search_document"]


class CohereEmbeddingService:
    """
    Service for generating embeddings using Cohere's embed-v3 model.
    Supports dynamic input_type for optimal search performance.
    """

    # Cohere API timeout in seconds
    API_TIMEOUT = 30

    def __init__(self):
        self.client = cohere.Client(
            api_key=settings.cohere_api_key,
            timeout=self.API_TIMEOUT
        )
        self.model = settings.embedding_model  # embed-multilingual-v3.0 or embed-english-v3.0

    def generate_single_embedding(
        self,
        text: str,
        input_type: InputType = "search_query"
    ) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: The text to embed
            input_type: "search_query" for queries, "search_document" for documents

        Returns:
            List of float values representing the embedding vector
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type=input_type  # Required for embed-v3 models
            )
            return response.embeddings[0]
        except ApiError as e:
            logger.error(f"Cohere API error generating embedding: {str(e)}")
            raise
        except TimeoutError as e:
            logger.error(f"Cohere API timeout generating embedding: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating embedding: {str(e)}")
            raise

    def generate_batch_embeddings(
        self,
        texts: List[str],
        input_type: InputType = "search_document"
    ) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of texts to embed
            input_type: "search_query" for queries, "search_document" for documents

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        try:
            # Cohere supports up to 96 texts per batch
            batch_size = 96
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=input_type  # Required for embed-v3 models
                )
                all_embeddings.extend(response.embeddings)

            return all_embeddings
        except ApiError as e:
            logger.error(f"Cohere API error generating batch embeddings: {str(e)}")
            raise
        except TimeoutError as e:
            logger.error(f"Cohere API timeout generating batch embeddings: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating batch embeddings: {str(e)}")
            raise


class QdrantRetrievalService:
    """
    Service for vector retrieval using Qdrant with relevance score filtering.
    """

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        self.relevance_threshold = settings.relevance_threshold  # Default: 0.7
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """
        Create the collection if it doesn't exist.
        """
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")
        except Exception:
            # Create collection with appropriate vector size
            # Cohere embed-v3 produces 1024-dim vectors
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
            )
            logger.info(f"Created collection {self.collection_name}")

    def _format_result(self, result) -> Dict:
        """Format a single search result."""
        return {
            "chunk_id": str(result.id),
            "content": result.payload.get("content", ""),
            "score": result.score,
            "module": result.payload.get("metadata", {}).get("module", ""),
            "chapter": result.payload.get("metadata", {}).get("chapter", ""),
            "subsection": result.payload.get("metadata", {}).get("subsection", ""),
            "page_reference": result.payload.get("metadata", {}).get("page_reference", "")
        }

    def _filter_by_relevance(self, results: List[Dict]) -> List[Dict]:
        """Filter results by relevance threshold."""
        filtered = [r for r in results if r["score"] >= self.relevance_threshold]
        if len(filtered) < len(results):
            logger.info(
                f"Filtered {len(results) - len(filtered)} results below "
                f"relevance threshold {self.relevance_threshold}"
            )
        return filtered

    def search_chunks_full_book(
        self,
        query_embedding: List[float],
        limit: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for relevant chunks in the full book with relevance filtering.
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

            # Perform search (request more than limit to account for filtering)
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit * 2,  # Request extra to account for filtering
                query_filter=qdrant_filters,
                with_payload=True
            )

            # Format and filter results
            formatted_results = [self._format_result(r) for r in results]
            filtered_results = self._filter_by_relevance(formatted_results)

            # Return up to the requested limit
            final_results = filtered_results[:limit]

            logger.info(f"Found {len(final_results)} relevant results for full-book search")
            return final_results

        except Exception as e:
            logger.error(f"Error in full-book search: {str(e)}")
            return []

    def search_chunks_per_page(
        self,
        query_embedding: List[float],
        selected_text_embedding: List[float],
        limit: int = 5
    ) -> List[Dict]:
        """
        Search for relevant chunks using both query and selected text embeddings.
        """
        try:
            # Search using the selected text embedding
            selected_text_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=selected_text_embedding,
                limit=limit,
                with_payload=True
            )

            # Search using the query embedding
            query_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            # Combine and deduplicate results
            all_results = {}

            for result in selected_text_results:
                all_results[result.id] = self._format_result(result)

            for result in query_results:
                if result.id not in all_results:
                    all_results[result.id] = self._format_result(result)

            # Sort by score, filter by relevance, and return top results
            sorted_results = sorted(all_results.values(), key=lambda x: x["score"], reverse=True)
            filtered_results = self._filter_by_relevance(sorted_results)
            final_results = filtered_results[:limit]

            logger.info(f"Found {len(final_results)} relevant results for per-page search")
            return final_results

        except Exception as e:
            logger.error(f"Error in per-page search: {str(e)}")
            return []

    def health_check(self) -> bool:
        """Check if Qdrant service is healthy."""
        try:
            self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False


class RAGService:
    """
    Main RAG service that combines Cohere embedding and Qdrant retrieval.
    Handles graceful degradation when no relevant context is found.
    """

    def __init__(self):
        self.cohere_service = CohereEmbeddingService()
        self.qdrant_service = QdrantRetrievalService()

    def retrieve_context(
        self,
        query: str,
        retrieval_mode: str = "full-book",
        selected_text: Optional[str] = None,
        metadata_filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Retrieve context chunks based on the query and mode.

        Args:
            query: The user's question
            retrieval_mode: "full-book" or "per-page"
            selected_text: Required for per-page mode
            metadata_filters: Optional filters for module/chapter

        Returns:
            List of relevant context chunks, empty if none found above threshold
        """
        try:
            # Generate embedding for the query using search_query input_type
            query_embedding = self.cohere_service.generate_single_embedding(
                query,
                input_type="search_query"
            )

            if retrieval_mode == "full-book":
                results = self.qdrant_service.search_chunks_full_book(
                    query_embedding=query_embedding,
                    limit=5,
                    filters=metadata_filters
                )
            else:  # per-page mode
                if not selected_text:
                    logger.warning("Selected text is required for per-page retrieval mode")
                    return []

                # Generate embedding for selected text (also search_query for retrieval)
                selected_text_embedding = self.cohere_service.generate_single_embedding(
                    selected_text,
                    input_type="search_query"
                )

                results = self.qdrant_service.search_chunks_per_page(
                    query_embedding=query_embedding,
                    selected_text_embedding=selected_text_embedding,
                    limit=5
                )

            # Log if no relevant results found
            if not results:
                logger.info(f"No relevant context found for query: {query[:50]}...")

            return results

        except Exception as e:
            logger.error(f"Error in retrieve_context: {str(e)}")
            return []

    def health_check(self) -> bool:
        """Check if RAG service is healthy."""
        return self.qdrant_service.health_check()


# Create a singleton instance
rag_service = RAGService()
