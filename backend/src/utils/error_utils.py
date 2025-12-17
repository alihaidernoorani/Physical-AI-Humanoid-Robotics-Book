from typing import Dict, Any, Optional
import logging
from datetime import datetime
import traceback
from fastapi import HTTPException, status
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class RAGError(Exception):
    """Base exception class for RAG-related errors"""
    def __init__(self, message: str, error_code: str = "RAG_ERROR", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class EmbeddingGenerationError(RAGError):
    """Exception raised when embedding generation fails"""
    def __init__(self, message: str = "Failed to generate embeddings", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "EMBEDDING_GENERATION_ERROR", details)

class VectorSearchError(RAGError):
    """Exception raised when vector search fails"""
    def __init__(self, message: str = "Failed to perform vector search", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VECTOR_SEARCH_ERROR", details)

class AIClientError(RAGError):
    """Exception raised when AI client (Gemini) fails"""
    def __init__(self, message: str = "AI client error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AI_CLIENT_ERROR", details)

class ValidationError(RAGError):
    """Exception raised when validation fails"""
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class APIResponse(BaseModel):
    """Standard API response model"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.utcnow()

def create_error_response(message: str, error_code: str = "GENERAL_ERROR",
                         status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                         details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized error response
    """
    error_response = {
        "success": False,
        "message": message,
        "error": {
            "code": error_code,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    return error_response

def create_success_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized success response
    """
    response = {
        "success": True,
        "message": message,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat()
    }

    return response

def log_error(error: Exception, context: str = "", user_id: Optional[str] = None) -> str:
    """
    Log error with context and return an error ID for tracking
    """
    import uuid

    error_id = str(uuid.uuid4())
    error_type = type(error).__name__
    error_message = str(error)
    error_traceback = traceback.format_exc()

    error_context = {
        "error_id": error_id,
        "error_type": error_type,
        "error_message": error_message,
        "context": context,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    logger.error(f"Error ID: {error_id} | Context: {context} | Type: {error_type} | Message: {error_message}")
    logger.debug(f"Full traceback for error {error_id}: {error_traceback}")

    return error_id

def handle_exception(error: Exception, context: str = "", user_id: Optional[str] = None,
                    default_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> HTTPException:
    """
    Convert an exception to an appropriate HTTPException
    """
    error_id = log_error(error, context, user_id)

    # Map specific exceptions to appropriate HTTP status codes
    if isinstance(error, RAGError):
        if isinstance(error, ValidationError):
            status_code = status.HTTP_400_BAD_REQUEST
        elif isinstance(error, EmbeddingGenerationError):
            status_code = status.HTTP_502_BAD_GATEWAY
        elif isinstance(error, VectorSearchError):
            status_code = status.HTTP_502_BAD_GATEWAY
        elif isinstance(error, AIClientError):
            status_code = status.HTTP_502_BAD_GATEWAY
        else:
            status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(error, HTTPException):
        # If it's already an HTTPException, return it as is
        return error
    else:
        # For all other exceptions, use the default or 500
        status_code = default_status_code

    detail = f"An error occurred (ID: {error_id}). Please contact support if the issue persists."

    return HTTPException(
        status_code=status_code,
        detail=detail
    )

def validate_and_sanitize_input(input_data: Dict[str, Any],
                               required_fields: Optional[List[str]] = None,
                               max_lengths: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
    """
    Validate and sanitize input data
    """
    required_fields = required_fields or []
    max_lengths = max_lengths or {}

    # Check required fields
    missing_fields = []
    for field in required_fields:
        if field not in input_data or input_data[field] is None or input_data[field] == "":
            missing_fields.append(field)

    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    # Sanitize and validate field lengths
    sanitized_data = {}
    for key, value in input_data.items():
        # Type validation
        if not isinstance(value, (str, int, float, bool, type(None), list, dict)):
            raise ValidationError(f"Invalid type for field '{key}': {type(value)}")

        # Length validation for strings
        if isinstance(value, str):
            if key in max_lengths and len(value) > max_lengths[key]:
                raise ValidationError(f"Field '{key}' exceeds maximum length of {max_lengths[key]} characters")

            # Basic sanitization for strings
            sanitized_value = value.strip()
            sanitized_data[key] = sanitized_value
        else:
            sanitized_data[key] = value

    return sanitized_data

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers to the same logger
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Global error handler for uncaught exceptions
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Global exception handler for uncaught exceptions
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Call the default handler for keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))