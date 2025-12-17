"""
Test suite for dual retrieval modes functionality
"""
import pytest
import os
from unittest.mock import patch, MagicMock
import sys
import json

# Add backend src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi.testclient import TestClient
from main import app

def test_rag_query_full_book_mode():
    """Test RAG query in full-book mode"""
    # Set up environment with required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        client = TestClient(app)

        # Mock the services
        with patch('src.api.rag.qdrant_service') as mock_qdrant, \
             patch('src.api.rag.cohere_service') as mock_cohere, \
             patch('src.api.rag.gemini_service') as mock_gemini:

            # Setup mock responses
            mock_qdrant.search_full_book.return_value = [
                {
                    'module': 'Module 1',
                    'chapter': 'Chapter 1',
                    'subsection': '1.1 Introduction',
                    'page_reference': 'p.15',
                    'text': 'Sample text from the textbook',
                    'confidence_score': 0.95
                }
            ]
            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]
            mock_gemini.generate_response.return_value = {
                'text': 'This is a response based on the full book content.',
                'confidence_score': 0.92,
                'is_fallback': False
            }

            # Make request in full-book mode
            response = client.post("/api/rag/query", json={
                "query_text": "Test question for full book mode",
                "retrieval_mode": "full-book"
            })

            assert response.status_code == 200
            data = response.json()

            # Verify the response structure
            assert "response_text" in data
            assert "citations" in data
            assert "confidence_score" in data
            assert "is_fallback" in data

            # Verify that full-book search was called
            mock_qdrant.search_full_book.assert_called_once()

def test_rag_query_per_page_mode():
    """Test RAG query in per-page mode"""
    # Set up environment with required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        client = TestClient(app)

        # Mock the services
        with patch('src.api.rag.qdrant_service') as mock_qdrant, \
             patch('src.api.rag.cohere_service') as mock_cohere, \
             patch('src.api.rag.gemini_service') as mock_gemini:

            # Setup mock responses
            mock_qdrant.search_per_page.return_value = [
                {
                    'module': 'Module 1',
                    'chapter': 'Chapter 1',
                    'subsection': '1.1 Selected Content',
                    'page_reference': 'p.20',
                    'text': 'Selected text content',
                    'confidence_score': 0.88
                }
            ]
            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]
            mock_gemini.generate_response.return_value = {
                'text': 'This is a response based on the selected text.',
                'confidence_score': 0.85,
                'is_fallback': False
            }

            # Make request in per-page mode with selected text
            response = client.post("/api/rag/query", json={
                "query_text": "Test question for per page mode",
                "retrieval_mode": "per-page",
                "selected_text": "This is the selected text for testing"
            })

            assert response.status_code == 200
            data = response.json()

            # Verify the response structure
            assert "response_text" in data
            assert "citations" in data
            assert "confidence_score" in data
            assert "is_fallback" in data

            # Verify that per-page search was called
            mock_qdrant.search_per_page.assert_called_once()

def test_rag_query_invalid_mode():
    """Test RAG query with invalid mode returns error"""
    # Set up environment with required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        client = TestClient(app)

        # Make request with invalid mode
        response = client.post("/api/rag/query", json={
            "query_text": "Test question",
            "retrieval_mode": "invalid-mode"
        })

        assert response.status_code == 422  # Validation error

def test_rag_query_per_page_without_selected_text():
    """Test RAG query in per-page mode without selected text"""
    # Set up environment with required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        client = TestClient(app)

        # Mock the services
        with patch('src.api.rag.qdrant_service') as mock_qdrant, \
             patch('src.api.rag.cohere_service') as mock_cohere, \
             patch('src.api.rag.gemini_service') as mock_gemini:

            # Setup mock responses
            mock_qdrant.search_per_page.return_value = []
            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]
            mock_gemini.generate_response.return_value = {
                'text': 'Fallback response when no context available.',
                'confidence_score': 0.3,
                'is_fallback': True
            }

            # Make request in per-page mode without selected text
            response = client.post("/api/rag/query", json={
                "query_text": "Test question without selected text",
                "retrieval_mode": "per-page"
                # No selected_text provided
            })

            assert response.status_code == 200
            data = response.json()

            # Should still return a response, but potentially with lower confidence
            assert "response_text" in data
            assert data["is_fallback"] is True

def test_rag_query_mode_switching():
    """Test that switching between modes works correctly"""
    # Set up environment with required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        client = TestClient(app)

        # Mock the services
        with patch('src.api.rag.qdrant_service') as mock_qdrant, \
             patch('src.api.rag.cohere_service') as mock_cohere, \
             patch('src.api.rag.gemini_service') as mock_gemini:

            # Setup mock responses
            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]

            # Full book mode response
            mock_qdrant.search_full_book.return_value = [
                {
                    'module': 'Full Book Module',
                    'chapter': 'Full Book Chapter',
                    'subsection': 'Full Book Section',
                    'page_reference': 'p.100',
                    'text': 'Full book content',
                    'confidence_score': 0.9
                }
            ]
            mock_gemini.generate_response.return_value = {
                'text': 'Response from full book content.',
                'confidence_score': 0.88,
                'is_fallback': False
            }

            # Test full book mode
            response1 = client.post("/api/rag/query", json={
                "query_text": "Test question",
                "retrieval_mode": "full-book"
            })
            assert response1.status_code == 200
            mock_qdrant.search_full_book.assert_called_once()
            mock_qdrant.reset_mock()

            # Per page mode response
            mock_qdrant.search_per_page.return_value = [
                {
                    'module': 'Per Page Module',
                    'chapter': 'Per Page Chapter',
                    'subsection': 'Per Page Section',
                    'page_reference': 'p.50',
                    'text': 'Per page content',
                    'confidence_score': 0.85
                }
            ]
            mock_gemini.generate_response.return_value = {
                'text': 'Response from per page content.',
                'confidence_score': 0.82,
                'is_fallback': False
            }

            # Test per page mode
            response2 = client.post("/api/rag/query", json={
                "query_text": "Test question",
                "retrieval_mode": "per-page",
                "selected_text": "Selected content for testing"
            })
            assert response2.status_code == 200
            mock_qdrant.search_per_page.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])