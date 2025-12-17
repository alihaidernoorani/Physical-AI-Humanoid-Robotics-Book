from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import status
from src.models.rag_models import ChatResponse, Citation, RAGResponse
from src.utils.error_utils import APIResponse, create_success_response, create_error_response

def format_rag_response(
    response_text: str,
    citations: List[Dict[str, Any]],
    confidence_score: float,
    grounded_chunks: List[str],
    is_fallback: bool = False,
    query_id: Optional[str] = None
) -> RAGResponse:
    """
    Format a RAG response with proper structure
    """
    # Convert raw citation dicts to Citation models
    formatted_citations = []
    for citation_data in citations:
        citation = Citation(
            chunk_id=citation_data.get("chunk_id", ""),
            module=citation_data.get("module", ""),
            chapter=citation_data.get("chapter", ""),
            subsection=citation_data.get("subsection", ""),
            page_reference=citation_data.get("page_reference", "")
        )
        formatted_citations.append(citation)

    return RAGResponse(
        response_id=f"resp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}",
        response_text=response_text,
        citations=formatted_citations,
        confidence_score=confidence_score,
        grounded_chunks=grounded_chunks,
        is_fallback=is_fallback
    )

def format_chat_response(
    response_text: str,
    query_id: Optional[str] = None,
    citations: Optional[List[Dict[str, Any]]] = None,
    confidence_score: float = 0.0,
    grounded_chunks: Optional[List[str]] = None,
    is_fallback: bool = False
) -> ChatResponse:
    """
    Format a chat response with proper structure
    """
    return ChatResponse(
        response_id=f"chat_resp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}",
        query_id=query_id,
        response_text=response_text,
        citations=citations or [],
        confidence_score=confidence_score,
        grounded_chunks=grounded_chunks or [],
        created_at=datetime.utcnow(),
        is_fallback=is_fallback
    )

def format_api_response(
    success: bool,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a standard API response
    """
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

    if data is not None:
        response["data"] = data

    if error is not None:
        response["error"] = error

    return response

def format_success_response(
    message: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a successful API response
    """
    return format_api_response(success=True, message=message, data=data)

def format_error_response(
    message: str,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format an error API response
    """
    error_info = {
        "message": message
    }

    if error_code:
        error_info["code"] = error_code

    if details:
        error_info["details"] = details

    return format_api_response(success=False, message=message, error=error_info)

def format_health_response(
    status: str,
    services: Dict[str, bool],
    additional_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a health check response
    """
    response_data = {
        "status": status,
        "services": services,
        "timestamp": datetime.utcnow().isoformat()
    }

    if additional_info:
        response_data.update(additional_info)

    return format_success_response("Health check successful", response_data)

def format_citation_list(
    chunks: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """
    Format a list of chunks into proper citation format
    """
    citations = []
    for chunk in chunks:
        citation = {
            "chunk_id": chunk.get("chunk_id", ""),
            "module": chunk.get("module", ""),
            "chapter": chunk.get("chapter", ""),
            "subsection": chunk.get("subsection", ""),
            "page_reference": chunk.get("page_reference", ""),
            "content_preview": chunk.get("content", "")[:200] + "..." if len(chunk.get("content", "")) > 200 else chunk.get("content", "")
        }
        citations.append(citation)

    return citations

def format_embedding_response(
    chunk_id: str,
    embedding: List[float],
    metadata: Dict[str, str]
) -> Dict[str, Any]:
    """
    Format an embedding generation response
    """
    return {
        "chunk_id": chunk_id,
        "embedding": embedding,
        "metadata": metadata,
        "vector_size": len(embedding) if embedding else 0,
        "timestamp": datetime.utcnow().isoformat()
    }

def format_indexing_response(
    indexed_count: int,
    failed_count: int,
    results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Format a content indexing response
    """
    return {
        "indexed_count": indexed_count,
        "failed_count": failed_count,
        "results": results,
        "total_processed": indexed_count + failed_count,
        "success_rate": indexed_count / (indexed_count + failed_count) if (indexed_count + failed_count) > 0 else 0,
        "timestamp": datetime.utcnow().isoformat()
    }

def format_user_settings_response(
    user_id: str,
    learning_level: str,
    preferred_language: str,
    last_accessed_module: Optional[str] = None,
    custom_preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a user settings response
    """
    settings_data = {
        "user_id": user_id,
        "learning_level": learning_level,
        "preferred_language": preferred_language,
        "last_accessed_module": last_accessed_module,
        "custom_preferences": custom_preferences or {},
        "timestamp": datetime.utcnow().isoformat()
    }

    return format_success_response("User settings retrieved successfully", settings_data)

def format_translation_response(
    original_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
    from_cache: bool = False
) -> Dict[str, Any]:
    """
    Format a translation response
    """
    translation_data = {
        "original_text": original_text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language,
        "from_cache": from_cache,
        "timestamp": datetime.utcnow().isoformat()
    }

    return format_success_response("Translation completed successfully", translation_data)

def format_confidence_indicator(confidence_score: float) -> str:
    """
    Format a confidence score into a human-readable indicator
    """
    if confidence_score >= 0.8:
        return "high"
    elif confidence_score >= 0.6:
        return "medium"
    elif confidence_score >= 0.4:
        return "low"
    else:
        return "very_low"

def format_query_response_time(start_time: datetime) -> float:
    """
    Calculate and format query response time in milliseconds
    """
    end_time = datetime.utcnow()
    response_time_ms = (end_time - start_time).total_seconds() * 1000
    return round(response_time_ms, 2)

def format_api_error(
    error_message: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a standardized API error response
    """
    error_data = {
        "error": error_message,
        "status_code": status_code,
        "timestamp": datetime.utcnow().isoformat()
    }

    if error_code:
        error_data["error_code"] = error_code

    if details:
        error_data["details"] = details

    return error_data

def create_paginated_response(
    items: List[Any],
    page: int,
    page_size: int,
    total_count: int
) -> Dict[str, Any]:
    """
    Create a paginated response
    """
    total_pages = (total_count + page_size - 1) // page_size
    has_next = page < total_pages
    has_prev = page > 1

    response_data = {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev
        }
    }

    return format_success_response("Paginated results retrieved successfully", response_data)