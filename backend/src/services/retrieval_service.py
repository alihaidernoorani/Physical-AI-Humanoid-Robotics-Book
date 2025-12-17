from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
import uuid
from src.config.settings import settings
from src.utils.text_chunker import TextChunk


class RetrievalService:
    """
    Service for storing and retrieving text chunks with embeddings in Qdrant.
    """

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        self.collection_name = settings.qdrant_collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensure the Qdrant collection exists with the correct configuration.
        The vector size is determined by the embedding model used (Cohere embed-english-v3.0 produces 1024-dimensional vectors).
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embed-english-v3.0 produces 1024-dimensional vectors
                    distance=models.Distance.COSINE
                )
            )

    def store_chunks(self, chunks: List[TextChunk], embeddings: List[List[float]]) -> bool:
        """
        Store text chunks with their embeddings in Qdrant.
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point = PointStruct(
                id=chunk.id,
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "module_name": chunk.module_name,
                    "chapter_title": chunk.chapter_title,
                    "section_path": chunk.section_path,
                    "token_count": chunk.token_count
                }
            )
            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return True

    def retrieve_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Retrieve top-k most similar chunks to the query embedding.
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        retrieved_chunks = []
        for result in results:
            chunk_data = {
                "id": result.id,
                "content": result.payload["content"],
                "module_name": result.payload["module_name"],
                "chapter_title": result.payload["chapter_title"],
                "section_path": result.payload["section_path"],
                "token_count": result.payload["token_count"],
                "similarity_score": result.score
            }
            retrieved_chunks.append(chunk_data)

        return retrieved_chunks

    def search_by_text(self, query_text: str, embedding_service, top_k: int = 5) -> List[Dict]:
        """
        Search for similar chunks using text query (generates embedding internally).
        """
        query_embedding = embedding_service.generate_embedding(query_text)
        return self.retrieve_similar(query_embedding, top_k)

    def delete_collection(self):
        """
        Delete the entire collection (useful for re-indexing).
        """
        try:
            self.client.delete_collection(self.collection_name)
            return True
        except:
            return False


# Example usage
if __name__ == "__main__":
    from src.services.embedding_service import EmbeddingService
    from src.utils.text_chunker import TextChunker

    # Initialize services
    retrieval_service = RetrievalService()
    embedding_service = EmbeddingService()
    chunker = TextChunker()

    # Sample text to test
    sample_text = """
    The Robot Operating System (ROS) is a flexible framework for writing robot software.
    It is a collection of tools, libraries, and conventions that aim to simplify the task
    of creating complex and robust robot behavior across a wide variety of robotic platforms.
    ROS provides hardware abstraction, device drivers, libraries, visualizers, message-passing,
    package management, and other capabilities.
    """

    # Chunk the text
    chunks = chunker.chunk_text(sample_text, "The Robotic Nervous System (ROS 2)", "Introduction", "module-1/intro")

    # Generate embeddings
    texts = [chunk.content for chunk in chunks]
    embeddings = embedding_service.generate_embeddings_batch(texts)

    # Store in Qdrant
    retrieval_service.store_chunks(chunks, embeddings)

    print(f"Stored {len(chunks)} chunks in Qdrant collection: {retrieval_service.collection_name}")

    # Test search
    search_results = retrieval_service.search_by_text("robot software framework", embedding_service)
    print(f"Search results: {len(search_results)} chunks found")
    for result in search_results:
        print(f"Score: {result['similarity_score']:.3f}, Content: {result['content'][:100]}...")