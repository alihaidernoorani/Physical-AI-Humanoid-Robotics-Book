"""
Rate limiting configuration for the RAG backend system
"""
from slowapi import errors
from slowapi.util import get_remote_address
from fastapi import HTTPException, Request
from typing import Callable

# Define rate limit configurations
RATE_LIMITS = {
    "chat_endpoint": "100 per minute",  # 100 requests per minute per IP for chat
    "embeddings_endpoint": "200 per minute",  # 200 requests per minute per IP for embeddings
    "health_endpoint": "1000 per minute",  # Higher rate for health checks
    "default": "50 per minute"  # Default rate limit
}

def get_rate_limit_for_endpoint(endpoint_name: str) -> str:
    """
    Get the appropriate rate limit for a given endpoint
    """
    return RATE_LIMITS.get(endpoint_name, RATE_LIMITS["default"])

def handle_rate_limit_error(request: Request, exc: errors.RateLimitExceeded):
    """
    Custom handler for rate limit exceeded errors
    """
    return HTTPException(
        status_code=429,
        detail={
            "error": "Rate limit exceeded",
            "message": f"Too many requests from this IP address. Limit: {exc.limit} per {exc.limit.period}.",
            "retry_after": exc.limit.period,
            "timestamp": "datetime.utcnow().isoformat()"
        }
    )