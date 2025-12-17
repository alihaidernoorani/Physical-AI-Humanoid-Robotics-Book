"""
Integration tests to verify that full-book mode retrieves from entire textbook
and per-page mode only retrieves from selected text
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

def test_full_book_mode_retrieves_from_entire_textbook():
    """Test that full-book mode retrieves from the entire textbook content"""
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

            # Setup mock response for full-book search that includes multiple modules/chapters
            full_book_results = [
                {
                    'module': 'Module 1',
                    'chapter': 'Chapter 1',
                    'subsection': '1.1 Introduction',
                    'page_reference': 'p.15',
                    'text': 'Introduction content from the textbook',
                    'confidence_score': 0.95
                },
                {
                    'module': 'Module 2',
                    'chapter': 'Chapter 3',
                    'subsection': '3.2 Advanced Topics',
                    'page_reference': 'p.45',
                    'text': 'Advanced content from a different chapter',
                    'confidence_score': 0.88
                },
                {
                    'module': 'Module 3',
                    'chapter': 'Chapter 5',
                    'subsection': '5.1 Conclusions',
                    'page_reference': 'p.80',
                    'text': 'Conclusion content from the end of the book',
                    'confidence_score': 0.82
                }
            ]

            mock_qdrant.search_full_book.return_value = full_book_results
            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]
            mock_gemini.generate_response.return_value = {
                'text': 'This response is based on content from multiple chapters across the entire textbook.',
                'confidence_score': 0.88,
                'is_fallback': False
            }

            # Make request in full-book mode
            response = client.post("/api/rag/query", json={
                "query_text": "Give me an overview of the textbook content",
                "retrieval_mode": "full-book"
            })

            assert response.status_code == 200
            data = response.json()

            # Verify the response structure
            assert "response_text" in data
            assert "citations" in data
            assert len(data["citations"]) == 3  # Should have multiple citations from different parts

            # Verify that citations come from different modules/chapters (full-book scope)
            modules = set([citation['module'] for citation in data["citations"]])
            chapters = set([citation['chapter'] for citation in data["citations"]])

            assert len(modules) > 1  # Multiple modules referenced
            assert len(chapters) > 1  # Multiple chapters referenced

            # Verify that full-book search method was called
            mock_qdrant.search_full_book.assert_called_once()
            mock_qdrant.search_per_page.assert_not_called()

def test_per_page_mode_retrieves_only_from_selected_text():
    """Test that per-page mode only retrieves from the selected text"""
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

            # Setup mock response for per-page search that should only return results from selected text
            selected_text_content = "This is the selected text that the per-page mode should focus on."
            per_page_results = [
                {
                    'module': 'Module 1',
                    'chapter': 'Chapter 1',
                    'subsection': '1.1 Selected Content',
                    'page_reference': 'p.20',
                    'text': selected_text_content,
                    'confidence_score': 0.92
                }
            ]

            mock_qdrant.search_per_page.return_value = per_page_results
            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]
            mock_gemini.generate_response.return_value = {
                'text': 'This response is based only on the selected text provided.',
                'confidence_score': 0.85,
                'is_fallback': False
            }

            # Make request in per-page mode with selected text
            selected_text = "This is the specific text that was selected by the user for focused analysis."
            response = client.post("/api/rag/query", json={
                "query_text": "Explain the selected content",
                "retrieval_mode": "per-page",
                "selected_text": selected_text
            })

            assert response.status_code == 200
            data = response.json()

            # Verify the response structure
            assert "response_text" in data
            assert "citations" in data
            assert len(data["citations"]) >= 1

            # Verify that citations are limited in scope (per-page mode)
            # In per-page mode, we should get results only related to the selected text
            for citation in data["citations"]:
                # All citations should be closely related to the selected text
                assert 'Selected' in citation['subsection'] or 'selected' in citation['text'].lower()

            # Verify that per-page search method was called
            mock_qdrant.search_per_page.assert_called_once()
            mock_qdrant.search_full_book.assert_not_called()

def test_mode_based_retrieval_scoping_comparison():
    """Test to compare retrieval scope between modes"""
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

            # Mock data for comparison
            full_book_results = [
                {
                    'module': 'Module 1', 'chapter': 'Chapter 1', 'subsection': '1.1',
                    'page_reference': 'p.15', 'text': 'Intro content', 'confidence_score': 0.9
                },
                {
                    'module': 'Module 2', 'chapter': 'Chapter 3', 'subsection': '3.2',
                    'page_reference': 'p.45', 'text': 'Advanced content', 'confidence_score': 0.85
                },
                {
                    'module': 'Module 3', 'chapter': 'Chapter 5', 'subsection': '5.1',
                    'page_reference': 'p.80', 'text': 'Conclusion content', 'confidence_score': 0.8
                }
            ]

            per_page_results = [
                {
                    'module': 'Module 1', 'chapter': 'Chapter 1', 'subsection': '1.1 Selected',
                    'page_reference': 'p.20', 'text': 'Selected text content', 'confidence_score': 0.92
                }
            ]

            mock_cohere.embed_text.return_value = [0.1, 0.2, 0.3]
            mock_gemini.generate_response.return_value = {
                'text': 'Response based on provided context',
                'confidence_score': 0.85,
                'is_fallback': False
            }

            # Test full-book mode - should access all content
            mock_qdrant.search_full_book.return_value = full_book_results
            response_full = client.post("/api/rag/query", json={
                "query_text": "Compare retrieval modes",
                "retrieval_mode": "full-book"
            })

            assert response_full.status_code == 200
            full_data = response_full.json()

            # Should have citations from multiple modules in full-book mode
            full_modules = set([citation['module'] for citation in full_data["citations"]])
            assert len(full_modules) == 3  # All three modules should be represented

            # Reset mock for per-page test
            mock_qdrant.search_per_page.return_value = per_page_results

            # Test per-page mode - should be limited to selected text
            response_per_page = client.post("/api/rag/query", json={
                "query_text": "Compare retrieval modes",
                "retrieval_mode": "per-page",
                "selected_text": "Selected text for focused retrieval"
            })

            assert response_per_page.status_code == 200
            per_page_data = response_per_page.json()

            # Should have citations limited to the selected context in per-page mode
            per_page_modules = set([citation['module'] for citation in per_page_data["citations"]])
            assert len(per_page_modules) <= 1  # Limited to the selected text scope

            # Verify correct methods were called for each mode
            assert mock_qdrant.search_full_book.call_count == 1
            assert mock_qdrant.search_per_page.call_count == 1

if __name__ == "__main__":
    pytest.main([__file__])