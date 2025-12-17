from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    qdrant_cluster_id: Optional[str] = os.getenv("QDRANT_CLUSTER_ID")

    # Cohere Configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    # Google Gemini Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    # Neon Postgres Configuration
    neon_db_url: str = os.getenv("NEON_DB_URL", "")

    # Debug Configuration
    debug_mode: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # Security Configuration
    secret_key: str = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")

    # Application Configuration
    app_name: str = "RAG Backend API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a single instance of settings
settings = Settings()

def validate_settings():
    """
    Validate that all required environment variables are set
    """
    required_vars = [
        "QDRANT_URL",
        "COHERE_API_KEY",
        "GEMINI_API_KEY",
        "NEON_DB_URL",
        "SECRET_KEY"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return True