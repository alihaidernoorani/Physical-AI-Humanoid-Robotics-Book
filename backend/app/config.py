from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_rag")
    cluster_id: str = os.getenv("CLUSTER_ID", "")

    # Cohere Configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "embed-multilingual-v3.0")

    # Google AI (Gemini) Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Neon Postgres Configuration
    database_url: str = os.getenv("DATABASE_URL", "")

    # Application Configuration
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # API Configuration
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    model_config = {"env_file": ".env"}

# Create a singleton instance
settings = Settings()