from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Configuration
    api_title: str = "RAG Chatbot API"
    api_version: str = "1.0.0"
    api_description: str = "Retrieval-Augmented Generation Chatbot for Physical AI & Humanoid Robotics Textbook"

    # Database Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_chunks"

    # Cohere Configuration
    cohere_api_key: str

    # Google Configuration (for Gemini via OpenAI Agents SDK)
    google_api_key: str

    # Neon Postgres Configuration
    neon_db_url: Optional[str] = None

    # Application Configuration
    debug: bool = False
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"

    def model_post_init(self, __context):
        """Validate that required API keys are present"""
        required_keys = ['cohere_api_key', 'google_api_key']
        for key in required_keys:
            value = getattr(self, key)
            if not value or value.strip() == "":
                raise ValueError(f"Required environment variable {key.upper()} is not set")


settings = Settings()