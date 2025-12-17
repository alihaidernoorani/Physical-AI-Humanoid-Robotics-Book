from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from src.config.settings import settings

# Import the limiter from the main app
from ...main import limiter


router = APIRouter()


class HealthCheck(BaseModel):
    status: str
    version: str
    api_title: str
    dependencies: Dict[str, Any]


@router.get("/health", response_model=HealthCheck)
@limiter.limit("1000 per minute")
async def health_check():
    # Check dependencies status
    dependencies_status = {
        "qdrant": "unknown",  # This would be checked in a real implementation
        "neon_db": "unknown",  # This would be checked in a real implementation
        "openai": "unknown"    # This would be checked in a real implementation
    }

    return HealthCheck(
        status="healthy",
        version=settings.api_version,
        api_title=settings.api_title,
        dependencies=dependencies_status
    )