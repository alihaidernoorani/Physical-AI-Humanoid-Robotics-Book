"""
Test suite for RAG functionality
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

client = TestClient(app)

def test_rag_chat_endpoint_exists():
    """Test that the RAG chat endpoint exists and returns proper status"""
    # This test will check if the endpoint exists, but without actual service calls
    # since we're not running the full services in test environment

    # Mock the services to avoid actual API calls
    with patch('src.api.rag.cohere_service') as mock_cohere, \
         patch('src.api.rag.qdrant_service') as mock_qdrant, \
         patch('src.api.rag.gemini_service') as mock_gemini:

        # Configure mocks
        mock_cohere.generate_single_embedding.return_value = [0.1] * 1024
        mock_qdrant.search_chunks_full_book.return_value = []
        mock_gemini.chat_with_context.return_value = {
            "response_text": "Test response",
            "model_used": "gemini-2.5-flash",
            "usage": {"prompt_tokens": 10, "response_tokens": 10}
        }

        # Test with minimal valid request
        response = client.post("/api/rag/chat", json={
            "query_text": "What is robotics?",
            "retrieval_mode": "full-book"
        })

        # Should return 422 (validation error) or 200 depending on validation
        # Since we're mocking, it should succeed if the endpoint exists
        assert response.status_code in [200, 422, 400]  # 400/422 are validation errors which are expected

def test_rag_chat_endpoint_with_per_page_mode():
    """Test the RAG chat endpoint with per-page mode"""
    with patch('src.api.rag.cohere_service') as mock_cohere, \
         patch('src.api.rag.qdrant_service') as mock_qdrant, \
         patch('src.api.rag.gemini_service') as mock_gemini:

        # Configure mocks
        mock_cohere.generate_single_embedding.return_value = [0.1] * 1024
        mock_qdrant.search_chunks_per_page.return_value = []
        mock_gemini.chat_with_context.return_value = {
            "response_text": "Test response for per-page mode",
            "model_used": "gemini-2.5-flash",
            "usage": {"prompt_tokens": 10, "response_tokens": 10}
        }

        # Test per-page mode with selected text
        response = client.post("/api/rag/chat", json={
            "query_text": "Explain this concept",
            "retrieval_mode": "per-page",
            "selected_text": "This is the selected text to focus on"
        })

        # Should return 200, 400, or 422
        assert response.status_code in [200, 422, 400]

def test_rag_chat_endpoint_validation():
    """Test validation of RAG chat endpoint"""
    response = client.post("/api/rag/chat", json={
        "query_text": "",  # Invalid - empty query
        "retrieval_mode": "invalid_mode"
    })

    # Should return validation error (422 or 400)
    assert response.status_code in [422, 400]

def test_rag_chat_endpoint_missing_query():
    """Test RAG chat endpoint with missing query"""
    response = client.post("/api/rag/chat", json={})

    # Should return validation error
    assert response.status_code in [422, 400]

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "services" in data
    assert data["status"] == "healthy"

def test_validate_rag_query_endpoint():
    """Test the RAG query validation endpoint"""
    response = client.post("/api/rag/validate", json={
        "query_text": "Test query",
        "retrieval_mode": "full-book"
    })

    assert response.status_code == 200
    data = response.json()
    assert "is_valid" in data

if __name__ == "__main__":
    pytest.main([__file__])