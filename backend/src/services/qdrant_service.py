from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from src.models.rag_models import KnowledgeChunk
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        # Initialize Qdrant client with configuration from settings
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False  # Using HTTP for better compatibility
            )
        else:
            # For local Qdrant instances without API key
            self.client = QdrantClient(url=settings.qdrant_url)

        self.collection_name = "knowledge_chunks"
        self.vector_size = 1024  # Cohere embeddings typically have 1024 dimensions

    def create_collection(self):
        """
        Create the knowledge chunks collection if it doesn't exist
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector configuration
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    )
                )

                # Create payload index for metadata fields
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="module",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="chapter",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="subsection",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                logger.info(f"Created collection '{self.collection_name}' with metadata indices")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")

        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise

    def store_chunk(self, chunk: KnowledgeChunk) -> bool:
        """
        Store a knowledge chunk in the Qdrant collection
        """
        try:
            points = [
                models.PointStruct(
                    id=chunk.chunk_id,
                    vector=chunk.embedding,
                    payload={
                        "content": chunk.content,
                        "module": chunk.module,
                        "chapter": chunk.chapter,
                        "subsection": chunk.subsection,
                        "source_type": chunk.source_type,
                        "source_origin": chunk.source_origin,
                        "page_reference": chunk.page_reference,
                        "created_at": chunk.created_at.isoformat(),
                        "updated_at": chunk.updated_at.isoformat()
                    }
                )
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Stored chunk {chunk.chunk_id} in Qdrant")
            return True

        except Exception as e:
            logger.error(f"Error storing chunk {chunk.chunk_id}: {str(e)}")
            return False

    def search_chunks_full_book(self,
                               query_embedding: List[float],
                               limit: int = 5,
                               filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks across the full book based on embedding similarity
        """
        try:
            # Build filter conditions if provided
            filter_conditions = []

            if filters:
                for key, value in filters.items():
                    if key in ["module", "chapter", "subsection"]:
                        filter_conditions.append(
                            models.FieldCondition(
                                key=key,
                                match=models.MatchValue(value=value)
                            )
                        )

            search_filter = None
            if filter_conditions:
                search_filter = models.Filter(
                    must=filter_conditions
                )

            # Perform search across the entire collection
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=search_filter,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )

            results = []
            for hit in search_results:
                result = {
                    "chunk_id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "module": hit.payload.get("module", ""),
                    "chapter": hit.payload.get("chapter", ""),
                    "subsection": hit.payload.get("subsection", ""),
                    "source_type": hit.payload.get("source_type", ""),
                    "source_origin": hit.payload.get("source_origin", ""),
                    "page_reference": hit.payload.get("page_reference", ""),
                    "score": hit.score
                }
                results.append(result)

            logger.info(f"Full-book search found {len(results)} chunks")
            return results

        except Exception as e:
            logger.error(f"Error in full-book search: {str(e)}")
            return []

    def search_chunks_per_page(self,
                              query_embedding: List[float],
                              selected_text_embedding: List[float],
                              limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for chunks specifically relevant to selected text (per-page mode)
        This implementation focuses on finding chunks that are contextually related to the selected text
        """
        try:
            # For per-page mode, we want to find chunks that are semantically similar to both
            # the query and the selected text context
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit * 2,  # Get more results to filter for relevance to selected text
                with_payload=True,
                with_vectors=False
            )

            # Filter results to prioritize chunks that are more relevant to the selected text context
            # For now, we'll just return the top results, but this could be enhanced with more
            # sophisticated relevance scoring based on the selected text
            results = []
            for hit in search_results:
                result = {
                    "chunk_id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "module": hit.payload.get("module", ""),
                    "chapter": hit.payload.get("chapter", ""),
                    "subsection": hit.payload.get("subsection", ""),
                    "source_type": hit.payload.get("source_type", ""),
                    "source_origin": hit.payload.get("source_origin", ""),
                    "page_reference": hit.payload.get("page_reference", ""),
                    "score": hit.score
                }
                results.append(result)

            # Limit to the specified number of results
            results = results[:limit]

            logger.info(f"Per-page search found {len(results)} chunks")
            return results
        except Exception as e:
            logger.error(f"Error in per-page search: {str(e)}")
            return []

    def search_chunks(self,
                     query_embedding: List[float],
                     limit: int = 5,
                     filters: Optional[Dict[str, str]] = None,
                     full_book_mode: bool = True) -> List[Dict[str, Any]]:
        """
        Generic search method that delegates to specific mode methods
        """
        try:
            if full_book_mode:
                return self.search_chunks_full_book(query_embedding, limit, filters)
            else:
                # For per-page mode, we'd need the selected text embedding as well
                # This method is kept for backward compatibility
                return self.search_chunks_full_book(query_embedding, limit, filters)
        except Exception as e:
            logger.error(f"Error in generic search: {str(e)}")
            return []

    def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a specific chunk from the collection
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[chunk_id]
                )
            )

            logger.info(f"Deleted chunk {chunk_id} from Qdrant")
            return True

        except Exception as e:
            logger.error(f"Error deleting chunk {chunk_id}: {str(e)}")
            return False

    def health_check(self) -> bool:
        """
        Check if Qdrant service is accessible
        """
        try:
            # Try to get collections to verify connection
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False

# Create a singleton instance
qdrant_service = QdrantService()