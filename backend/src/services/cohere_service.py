import cohere
from typing import List
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class CohereService:
    def __init__(self):
        # Initialize Cohere client with API key from settings
        if not settings.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(settings.cohere_api_key)
        self.model = "embed-multilingual-v3.0"  # Using multilingual model for broader language support
        self.input_type = "search_document"  # Optimize embeddings for search

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type=self.input_type
            )

            embeddings = [embedding for embedding in response.embeddings]
            logger.info(f"Generated embeddings for {len(texts)} text(s)")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type=self.input_type
            )

            embedding = response.embeddings[0]
            logger.info(f"Generated embedding for text of length {len(text)}")
            return embedding

        except Exception as e:
            logger.error(f"Error generating single embedding: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Check if Cohere service is accessible by generating a test embedding
        """
        try:
            test_text = "health check"
            self.generate_single_embedding(test_text)
            return True
        except Exception as e:
            logger.error(f"Cohere health check failed: {str(e)}")
            return False

# Create a singleton instance
cohere_service = CohereService()