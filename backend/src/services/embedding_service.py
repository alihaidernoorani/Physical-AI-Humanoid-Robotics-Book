from typing import List, Optional
import numpy as np
import cohere
from src.config.settings import settings


class EmbeddingService:
    """
    Service for generating embeddings for text chunks using Cohere.
    """

    def __init__(self, model_name: str = "embed-english-v3.0"):
        self.model_name = model_name
        self.client = cohere.Client(settings.cohere_api_key)

    def generate_embedding(self, text: str, input_type: str = "search_document") -> List[float]:
        """
        Generate embedding for a single text string.
        """
        response = self.client.embed(
            texts=[text],
            model=self.model_name,
            input_type=input_type
        )
        return response.embeddings[0]  # Convert to list for JSON serialization

    def generate_embeddings_batch(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """
        Generate embeddings for a batch of text strings.
        """
        response = self.client.embed(
            texts=texts,
            model=self.model_name,
            input_type=input_type
        )
        return response.embeddings

    def cosine_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        """
        a = np.array(emb1)
        b = np.array(emb2)
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))


# Example usage
if __name__ == "__main__":
    service = EmbeddingService()

    # Test single embedding
    text = "This is a sample text for embedding."
    embedding = service.generate_embedding(text)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

    # Test batch embedding
    texts = [
        "First sentence for embedding.",
        "Second sentence for embedding.",
        "Third sentence for embedding."
    ]
    embeddings = service.generate_embeddings_batch(texts)
    print(f"Batch embeddings: {len(embeddings)}")
    print(f"First embedding length: {len(embeddings[0])}")