from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from datetime import datetime
import logging

# Import the limiter from the main app
from ...main import limiter

from src.models.rag_models import RAGQuery, RAGResponse
from src.services.qdrant_service import qdrant_service
from src.services.cohere_service import cohere_service
from src.services.gemini_service import gemini_service
from src.utils.metadata_utils import calculate_confidence_score
from src.utils.validation_utils import validate_rag_query
from src.utils.response_utils import format_rag_response, format_api_error
from src.utils.error_utils import handle_exception, log_error
from src.config import settings
from src.middleware.auth_middleware import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)

@router.on_event("startup")
async def startup_event():
    """
    Initialize services on startup
    """
    try:
        # Initialize Qdrant collection
        qdrant_service.create_collection()
        logger.info("Qdrant collection initialized")

        # Verify services are accessible
        if not qdrant_service.health_check():
            logger.error("Qdrant service health check failed")

        if not cohere_service.health_check():
            logger.error("Cohere service health check failed")

        if not gemini_service.health_check():
            logger.error("Gemini service health check failed")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

@router.post("/rag/chat", response_model=RAGResponse, tags=["RAG"])
@limiter.limit("100 per minute")
async def rag_chat_endpoint(query: RAGQuery, current_user: dict = Depends(get_current_user)):
    """
    Process user queries and return contextually relevant responses based on textbook content
    """
    start_time = datetime.utcnow()

    try:
        # Validate the query
        validation_result = validate_rag_query(query)
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid query parameters: {'; '.join(validation_result['errors'])}"
            )

        logger.info(f"Processing RAG query: {query.query_text[:50]}...")

        # Generate embedding for the query
        query_embedding = cohere_service.generate_single_embedding(query.query_text)

        # Perform vector search based on retrieval mode
        if query.retrieval_mode == "full-book":
            # Full-book search with optional metadata filters
            search_results = qdrant_service.search_chunks_full_book(
                query_embedding=query_embedding,
                limit=5,
                filters=query.metadata_filters if query.metadata_filters else None
            )
        else:  # per-page mode
            # Per-page search using selected text
            if not query.selected_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Selected text is required for per-page retrieval mode"
                )

            # For per-page mode, we'll search using the selected text context
            selected_text_embedding = cohere_service.generate_single_embedding(query.selected_text)
            search_results = qdrant_service.search_chunks_per_page(
                query_embedding=query_embedding,
                selected_text_embedding=selected_text_embedding,
                limit=5
            )

        # Calculate confidence score based on relevance scores
        relevance_scores = [result["score"] for result in search_results]
        confidence_score = calculate_confidence_score(relevance_scores) if relevance_scores else 0.0

        # If no relevant chunks found, return a fallback response
        if not search_results or confidence_score < 0.2:
            fallback_response = "I couldn't find relevant information in the textbook to answer your question. Please try rephrasing your question or check other sections of the textbook."
            response = format_rag_response(
                response_text=fallback_response,
                citations=[],
                confidence_score=confidence_score,
                grounded_chunks=[],
                is_fallback=True
            )
            logger.info(f"Fallback response generated with confidence {confidence_score}")
            return response

        # Generate response using Gemini with context
        gemini_response = gemini_service.chat_with_context(
            query=query.query_text,
            context_chunks=search_results
        )

        # Extract citations from search results
        citations = []
        for result in search_results:
            citation = {
                "chunk_id": result["chunk_id"],
                "module": result["module"],
                "chapter": result["chapter"],
                "subsection": result["subsection"],
                "page_reference": result["page_reference"]
            }
            citations.append(citation)

        # Create the final response
        response = format_rag_response(
            response_text=gemini_response["response_text"],
            citations=citations,
            confidence_score=confidence_score,
            grounded_chunks=[result["chunk_id"] for result in search_results],
            is_fallback=False
        )

        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        logger.info(f"RAG query processed successfully in {response_time:.2f}ms with confidence {confidence_score}")

        return response

    except Exception as e:
        error_id = log_error(e, "RAG Chat Endpoint", getattr(query, 'user_id', None))
        raise handle_exception(e, "RAG Chat Endpoint", getattr(query, 'user_id', None))

@router.post("/rag/validate", tags=["RAG"])
async def validate_rag_query_endpoint(query: RAGQuery, current_user: dict = Depends(get_current_user)):
    """
    Validate a RAG query without processing it
    """
    try:
        validation_result = validate_rag_query(query)

        return {
            "is_valid": validation_result["is_valid"],
            "errors": validation_result["errors"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        error_id = log_error(e, "RAG Query Validation")
        raise handle_exception(e, "RAG Query Validation")

@router.get("/rag/stats", tags=["RAG"])
async def get_rag_stats(current_user: dict = Depends(get_current_user)):
    """
    Get statistics about the RAG system
    """
    try:
        # This would typically connect to the database to get stats
        # For now, we'll return basic stats
        stats = {
            "total_chunks_indexed": 0,  # This would come from Qdrant
            "avg_response_time_ms": 0,  # This would come from logs
            "success_rate": 0,  # This would come from logs
            "timestamp": datetime.utcnow().isoformat()
        }

        return {
            "stats": stats,
            "message": "RAG statistics retrieved"
        }
    except Exception as e:
        error_id = log_error(e, "RAG Stats Endpoint")
        raise handle_exception(e, "RAG Stats Endpoint")