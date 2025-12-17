"""
Comprehensive unit tests for backend services
"""
import pytest
import os
from unittest.mock import patch, MagicMock
import sys
import json

# Add backend src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.services.qdrant_service import QdrantService
from src.services.cohere_service import CohereService
from src.services.gemini_service import GeminiService


def test_qdrant_service_initialization():
    """Test Qdrant service initialization"""
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'QDRANT_API_KEY': 'test-api-key'
    }):
        service = QdrantService()
        assert service is not None
        # Verify that the client was created (either with auth or without)
        assert hasattr(service, 'client')


def test_cohere_service_initialization():
    """Test Cohere service initialization"""
    with patch.dict(os.environ, {
        'COHERE_API_KEY': 'test-cohere-key'
    }):
        service = CohereService()
        assert service is not None
        # Verify that the client was created
        assert hasattr(service, 'client')


def test_gemini_service_initialization():
    """Test Gemini service initialization"""
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test-gemini-key'
    }):
        service = GeminiService()
        assert service is not None
        # Verify that the model was created
        assert hasattr(service, 'model')


def test_qdrant_health_check():
    """Test Qdrant service health check"""
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com'
    }):
        service = QdrantService()

        # Mock the health check response
        with patch.object(service.client, 'health', return_value={'title': 'qdrant - vector database', 'version': '1.0.0'}):
            is_healthy = service.health_check()
            assert is_healthy is True


def test_cohere_health_check():
    """Test Cohere service health check"""
    with patch.dict(os.environ, {
        'COHERE_API_KEY': 'test-cohere-key'
    }):
        service = CohereService()

        # Mock the embed text response
        with patch.object(service.client, 'embed', return_value=MagicMock(embeddings=[[0.1, 0.2, 0.3]])):
            is_healthy = service.health_check()
            assert is_healthy is True


def test_gemini_health_check():
    """Test Gemini service health check"""
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test-gemini-key'
    }):
        service = GeminiService()

        # Mock the generate content response
        mock_response = MagicMock()
        mock_response.text = "Test response"
        with patch.object(service.model, 'generate_content', return_value=mock_response):
            is_healthy = service.health_check()
            assert is_healthy is True


def test_cohere_embedding_generation():
    """Test Cohere service embedding generation"""
    with patch.dict(os.environ, {
        'COHERE_API_KEY': 'test-cohere-key'
    }):
        service = CohereService()

        test_text = "This is a test sentence for embedding."
        mock_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]

        # Mock the embed text response
        mock_result = MagicMock()
        mock_result.embeddings = [mock_embedding]
        with patch.object(service.client, 'embed', return_value=mock_result):
            embedding = service.generate_single_embedding(test_text)
            assert embedding == mock_embedding
            assert len(embedding) == len(mock_embedding)


def test_qdrant_search_methods():
    """Test Qdrant service search methods"""
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com'
    }):
        service = QdrantService()

        test_embedding = [0.1, 0.2, 0.3]
        mock_results = [
            {
                'id': 'test-id-1',
                'payload': {
                    'module': 'Module 1',
                    'chapter': 'Chapter 1',
                    'subsection': '1.1',
                    'page_reference': 'p.15',
                    'content': 'Test content 1'
                },
                'score': 0.95
            },
            {
                'id': 'test-id-2',
                'payload': {
                    'module': 'Module 2',
                    'chapter': 'Chapter 2',
                    'subsection': '2.1',
                    'page_reference': 'p.30',
                    'content': 'Test content 2'
                },
                'score': 0.85
            }
        ]

        # Mock the search response
        mock_search_result = [
            MagicMock(id='test-id-1', payload=mock_results[0]['payload'], score=0.95),
            MagicMock(id='test-id-2', payload=mock_results[1]['payload'], score=0.85)
        ]

        with patch.object(service.client, 'search', return_value=mock_search_result):
            # Test full-book search
            results = service.search_chunks_full_book(test_embedding, limit=2)
            assert len(results) == 2
            assert results[0]['module'] == 'Module 1'
            assert results[1]['module'] == 'Module 2'

            # Test per-page search
            per_page_results = service.search_chunks_per_page(test_embedding, test_embedding, limit=2)
            assert len(per_page_results) == 2


def test_gemini_response_generation():
    """Test Gemini service response generation"""
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test-gemini-key'
    }):
        service = GeminiService()

        query = "What is artificial intelligence?"
        context_chunks = [
            {
                'id': 'chunk-1',
                'payload': {
                    'module': 'Module 1',
                    'chapter': 'Chapter 1',
                    'content': 'Artificial intelligence is the simulation of human intelligence processes by machines.',
                    'page_reference': 'p.10'
                },
                'score': 0.9
            }
        ]

        mock_response_text = "Artificial intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."

        # Mock the generate content response
        mock_response = MagicMock()
        mock_response.text = mock_response_text
        with patch.object(service.model, 'generate_content', return_value=mock_response):
            response = service.chat_with_context(query, context_chunks)
            assert 'response_text' in response
            assert len(response['response_text']) > 0
            assert response['response_text'] == mock_response_text


def test_input_validation_utils():
    """Test input validation utilities"""
    from src.utils.validation_utils import validate_rag_query
    from src.models.rag_models import RAGQuery

    # Test valid query
    valid_query = RAGQuery(
        query_text="What is the main concept?",
        retrieval_mode="full-book"
    )
    validation_result = validate_rag_query(valid_query)
    assert validation_result["is_valid"] is True
    assert len(validation_result["errors"]) == 0

    # Test query with insufficient length
    short_query = RAGQuery(
        query_text="",  # Empty query
        retrieval_mode="full-book"
    )
    validation_result = validate_rag_query(short_query)
    assert validation_result["is_valid"] is False
    assert len(validation_result["errors"]) > 0

    # Test invalid retrieval mode
    invalid_mode_query = RAGQuery(
        query_text="Test query",
        retrieval_mode="invalid-mode"  # Invalid mode
    )
    validation_result = validate_rag_query(invalid_mode_query)
    assert validation_result["is_valid"] is False
    assert "Retrieval mode must be either" in validation_result["errors"][0]

    # Test per-page mode without selected text
    per_page_without_text = RAGQuery(
        query_text="Test query",
        retrieval_mode="per-page",
        selected_text=None  # Missing selected text for per-page mode
    )
    validation_result = validate_rag_query(per_page_without_text)
    assert validation_result["is_valid"] is False
    assert "Selected text is required for per-page" in validation_result["errors"][0]


def test_error_handling_utils():
    """Test error handling utilities"""
    from src.utils.error_utils import log_error, handle_exception
    from fastapi import HTTPException

    # Test error logging
    test_error = ValueError("Test error for logging")
    error_id = log_error(test_error, "test_context", "test_user")
    assert isinstance(error_id, str)
    assert len(error_id) > 0

    # Test exception handling
    test_exception = ValueError("Test exception")
    http_exception = handle_exception(test_exception, "test_context", "test_user")
    assert isinstance(http_exception, HTTPException)
    assert http_exception.status_code == 500


def test_metadata_utils():
    """Test metadata utilities"""
    from src.utils.metadata_utils import calculate_confidence_score, validate_metadata

    # Test confidence score calculation
    scores = [0.9, 0.8, 0.7, 0.6, 0.5]
    confidence = calculate_confidence_score(scores)
    assert isinstance(confidence, float)
    assert 0.0 <= confidence <= 1.0

    # Test metadata validation
    valid_metadata = {
        "module": "Test Module",
        "chapter": "Test Chapter",
        "subsection": "Test Subsection",
        "source_type": "textbook",
        "source_origin": "test_origin",
        "page_reference": "p.1"
    }
    validation_result = validate_metadata(valid_metadata)
    assert validation_result["is_valid"] is True
    assert len(validation_result["errors"]) == 0


if __name__ == "__main__":
    pytest.main([__file__])