from typing import Dict, Any, List, Optional
from src.models.rag_models import RAGQuery, KnowledgeChunk, ChatResponse
from src.utils.metadata_utils import validate_metadata
from src.utils.error_utils import ValidationError
import re

def validate_rag_query(query: RAGQuery) -> Dict[str, Any]:
    """
    Validate RAG query parameters
    """
    errors = []

    # Validate query text length
    if len(query.query_text) < 1 or len(query.query_text) > 1000:
        errors.append("Query text must be between 1 and 1000 characters")

    # Validate retrieval mode
    if query.retrieval_mode not in ["full-book", "per-page"]:
        errors.append("Retrieval mode must be either 'full-book' or 'per-page'")

    # Validate selected text for per-page mode
    if query.retrieval_mode == "per-page" and (not query.selected_text or len(query.selected_text.strip()) == 0):
        errors.append("Selected text is required for per-page retrieval mode")

    # Validate user_id format if provided (simple format check)
    if query.user_id and not re.match(r'^[a-zA-Z0-9_-]{1,50}$', query.user_id):
        errors.append("User ID must be 1-50 alphanumeric characters, underscores, or hyphens")

    # Validate metadata filters
    if query.metadata_filters:
        for key, value in query.metadata_filters.items():
            if not isinstance(key, str) or not isinstance(value, str):
                errors.append("Metadata filter keys and values must be strings")
            elif len(key) > 50 or len(value) > 100:
                errors.append("Metadata filter keys must be <= 50 chars and values <= 100 chars")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def validate_knowledge_chunk(chunk: KnowledgeChunk) -> Dict[str, Any]:
    """
    Validate knowledge chunk parameters
    """
    errors = []

    # Validate chunk_id
    if not chunk.chunk_id or len(chunk.chunk_id) == 0:
        errors.append("Chunk ID is required")

    # Validate content length (50-2000 characters as per constitution)
    if len(chunk.content) < 50:
        errors.append("Content must be at least 50 characters long")
    elif len(chunk.content) > 2000:
        errors.append("Content must not exceed 2000 characters")

    # Validate embedding
    if not chunk.embedding or len(chunk.embedding) == 0:
        errors.append("Embedding is required")
    elif not all(isinstance(val, (int, float)) for val in chunk.embedding):
        errors.append("All embedding values must be numeric")

    # Validate metadata fields (module, chapter, subsection)
    if not chunk.module or len(chunk.module.strip()) == 0:
        errors.append("Module is required")
    elif len(chunk.module) > 200:
        errors.append("Module name must not exceed 200 characters")

    if not chunk.chapter or len(chunk.chapter.strip()) == 0:
        errors.append("Chapter is required")
    elif len(chunk.chapter) > 200:
        errors.append("Chapter name must not exceed 200 characters")

    if not chunk.subsection or len(chunk.subsection.strip()) == 0:
        errors.append("Subsection is required")
    elif len(chunk.subsection) > 200:
        errors.append("Subsection name must not exceed 200 characters")

    # Validate source_type
    valid_source_types = ["textbook", "diagram", "exercise", "example", "definition", "theorem", "code", "figure"]
    if chunk.source_type not in valid_source_types:
        errors.append(f"Source type must be one of {valid_source_types}")

    # Validate source_origin
    if not chunk.source_origin or len(chunk.source_origin.strip()) == 0:
        errors.append("Source origin is required")

    # Validate page_reference
    if not chunk.page_reference or len(chunk.page_reference.strip()) == 0:
        errors.append("Page reference is required")

    # Validate embedding array size (typically 1024 for Cohere embeddings)
    if len(chunk.embedding) < 100 or len(chunk.embedding) > 4096:
        errors.append("Embedding vector size is not within expected range (100-4096)")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def validate_chat_response(response: ChatResponse) -> Dict[str, Any]:
    """
    Validate chat response parameters
    """
    errors = []

    # Validate response_id
    if not response.response_id or len(response.response_id) == 0:
        errors.append("Response ID is required")

    # Validate query_id (if provided)
    if response.query_id and len(response.query_id) == 0:
        errors.append("Query ID must be a valid non-empty string if provided")

    # Validate response_text
    if not response.response_text or len(response.response_text.strip()) == 0:
        errors.append("Response text is required")
    elif len(response.response_text) > 5000:
        errors.append("Response text must not exceed 5000 characters")

    # Validate citations
    if response.citations and len(response.citations) > 0:
        for citation in response.citations:
            if not citation.chunk_id or len(citation.chunk_id) == 0:
                errors.append("Each citation must have a valid chunk_id")
            if not citation.module or len(citation.module) == 0:
                errors.append("Each citation must have a valid module")
            if not citation.chapter or len(citation.chapter) == 0:
                errors.append("Each citation must have a valid chapter")

    # Validate confidence_score (0.0-1.0)
    if response.confidence_score < 0.0 or response.confidence_score > 1.0:
        errors.append("Confidence score must be between 0.0 and 1.0")

    # Validate grounded_chunks
    if response.grounded_chunks and not all(isinstance(chunk_id, str) and len(chunk_id) > 0 for chunk_id in response.grounded_chunks):
        errors.append("All grounded chunk IDs must be non-empty strings")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def validate_embedding_data(embedding: List[float]) -> Dict[str, Any]:
    """
    Validate embedding data structure and values
    """
    errors = []

    if not embedding or len(embedding) == 0:
        errors.append("Embedding cannot be empty")
    elif not all(isinstance(val, (int, float)) for val in embedding):
        errors.append("All embedding values must be numeric")
    elif len(embedding) < 100 or len(embedding) > 4096:
        errors.append("Embedding vector size is not within expected range (100-4096)")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "vector_size": len(embedding) if embedding else 0
    }

def validate_content_chunk(content: str, min_length: int = 50, max_length: int = 2000) -> Dict[str, Any]:
    """
    Validate content chunk parameters
    """
    errors = []

    if not content or len(content.strip()) == 0:
        errors.append("Content cannot be empty")
    elif len(content) < min_length:
        errors.append(f"Content must be at least {min_length} characters")
    elif len(content) > max_length:
        errors.append(f"Content must not exceed {max_length} characters")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "length": len(content) if content else 0
    }

def validate_metadata_fields(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate metadata fields for knowledge chunks
    """
    return validate_metadata(metadata)

def validate_retrieval_params(query: str, mode: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate retrieval parameters
    """
    errors = []

    # Validate query
    if not query or len(query.strip()) == 0:
        errors.append("Query cannot be empty")
    elif len(query) > 1000:
        errors.append("Query must not exceed 1000 characters")

    # Validate mode
    if mode not in ["full-book", "per-page"]:
        errors.append("Mode must be either 'full-book' or 'per-page'")

    # Validate selected_text for per-page mode
    if mode == "per-page" and (not selected_text or len(selected_text.strip()) == 0):
        errors.append("Selected text is required for per-page mode")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def validate_api_request(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
    """
    Validate API request data
    """
    errors = []

    # Check for required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Required field '{field}' is missing")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def sanitize_user_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    if not text:
        return ""

    # Remove potential script tags
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    # Remove potential javascript: urls
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    # Remove potential vbscript: urls
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

    return sanitized.strip()

def validate_chunk_list(chunks: List[KnowledgeChunk]) -> Dict[str, Any]:
    """
    Validate a list of knowledge chunks
    """
    errors = []
    valid_chunks = []
    invalid_chunks = []

    for i, chunk in enumerate(chunks):
        validation_result = validate_knowledge_chunk(chunk)
        if validation_result["is_valid"]:
            valid_chunks.append(chunk)
        else:
            invalid_chunks.append({
                "index": i,
                "chunk_id": getattr(chunk, 'chunk_id', f'unknown_{i}'),
                "errors": validation_result["errors"]
            })
            errors.extend([f"Chunk {i} ({chunk.chunk_id}): {error}" for error in validation_result["errors"]])

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "valid_count": len(valid_chunks),
        "invalid_count": len(invalid_chunks),
        "valid_chunks": valid_chunks,
        "invalid_chunks": invalid_chunks
    }