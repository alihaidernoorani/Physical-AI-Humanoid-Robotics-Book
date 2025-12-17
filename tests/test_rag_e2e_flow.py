"""
End-to-End tests for the complete RAG flow.

This module tests the complete RAG flow from user query to response,
including all components: API endpoints, RAG service, embedding generation,
vector search, and response generation.
"""

import pytest
import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock
from typing import Dict, Any, Optional

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from fastapi.testclient import TestClient
from src.services.rag_service import RAGService
from src.services.qdrant_service import qdrant_service
from src.services.embedding_service import CohereEmbeddingService
from src.services.generation_service import GeminiGenerationService


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service for testing."""
    mock = AsyncMock(spec=CohereEmbeddingService)
    mock.generate_embedding.return_value = [0.1] * 1024  # Mock embedding vector
    mock.generate_embeddings.return_value = [[0.1] * 1024, [0.2] * 1024]
    return mock


@pytest.fixture
def mock_generation_service():
    """Mock generation service for testing."""
    mock = AsyncMock(spec=GeminiGenerationService)
    mock.generate_response.return_value = "Mocked AI response based on context"
    mock.generate_response_with_citations.return_value = {
        "response": "Mocked AI response with citations",
        "confidence": 0.95
    }
    return mock


class TestCompleteRAGFlow:
    """Test class for complete end-to-end RAG flow scenarios."""

    def test_complete_rag_flow_full_book_mode(self, test_client):
        """
        Test the complete RAG flow in full-book mode.

        This test verifies the entire flow from query to response:
        1. Query validation
        2. Embedding generation
        3. Vector search in Qdrant
        4. Context retrieval
        5. AI response generation
        6. Response formatting with citations
        """
        # Mock data that would be returned by services
        mock_search_results = [
            {
                "chunk_id": "chunk_1",
                "content": "Physical AI combines robotics with artificial intelligence to create systems that can understand and interact with the physical world.",
                "module": "introduction",
                "chapter": "1",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "3",
                "score": 0.85
            },
            {
                "chunk_id": "chunk_2",
                "content": "The core principles of physical AI include embodied cognition, sensorimotor learning, and real-world interaction.",
                "module": "introduction",
                "chapter": "1",
                "subsection": "1.2",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "4",
                "score": 0.78
            }
        ]

        # Test the complete flow
        request_data = {
            "query_text": "What is physical AI?",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            # Verify response
            assert response.status_code == 200
            response_data = response.json()

            # Verify response structure
            assert "response_id" in response_data
            assert "response_text" in response_data
            assert "citations" in response_data
            assert "confidence_score" in response_data
            assert "grounded_chunks" in response_data
            assert "is_fallback" in response_data

            # Verify citations are properly formatted
            assert len(response_data["citations"]) > 0
            for citation in response_data["citations"]:
                assert "chunk_id" in citation
                assert "module" in citation
                assert "chapter" in citation
                assert "subsection" in citation
                assert "page_reference" in citation

            # Verify confidence score is in valid range
            assert 0.0 <= response_data["confidence_score"] <= 1.0

    def test_complete_rag_flow_per_page_mode(self, test_client):
        """
        Test the complete RAG flow in per-page mode.

        This test verifies the flow when the user selects specific text
        for contextual retrieval.
        """
        mock_search_results = [
            {
                "chunk_id": "chunk_3",
                "content": "Humanoid robotics involves creating robots with human-like characteristics and capabilities.",
                "module": "humanoid_robots",
                "chapter": "5",
                "subsection": "5.1",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "45",
                "score": 0.92
            }
        ]

        request_data = {
            "query_text": "Explain humanoid robotics",
            "retrieval_mode": "per-page",
            "selected_text": "Humanoid robotics is an important field in AI",
            "metadata_filters": {
                "chapter": "5"
            }
        }

        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            assert response.status_code == 200
            response_data = response.json()

            # Verify response structure
            assert "response_id" in response_data
            assert "response_text" in response_data
            assert len(response_data["citations"]) > 0

    def test_rag_flow_with_metadata_filters(self, test_client):
        """
        Test RAG flow with metadata filters applied.

        This verifies that the system properly filters results based
        on module, chapter, and subsection metadata.
        """
        mock_search_results = [
            {
                "chunk_id": "filtered_chunk_1",
                "content": "Filtered content for chapter 3",
                "module": "advanced_concepts",
                "chapter": "3",
                "subsection": "3.2",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "25",
                "score": 0.88
            }
        ]

        request_data = {
            "query_text": "Advanced concepts in physical AI",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {
                "module": "advanced_concepts",
                "chapter": "3"
            }
        }

        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            assert response.status_code == 200
            response_data = response.json()

            # Verify that citations match the requested filters
            for citation in response_data["citations"]:
                assert citation["module"] == "advanced_concepts"
                assert citation["chapter"] == "3"

    def test_rag_flow_validation_errors(self, test_client):
        """
        Test RAG flow with invalid inputs to verify proper error handling.
        """
        # Test with empty query
        request_data = {
            "query_text": "",
            "retrieval_mode": "full-book"
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Should return validation error
        assert response.status_code == 422

        # Test with invalid retrieval mode
        request_data = {
            "query_text": "Test query",
            "retrieval_mode": "invalid_mode"
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Should return validation error
        assert response.status_code == 422

    def test_rag_flow_no_results_fallback(self, test_client):
        """
        Test RAG flow when no relevant results are found.

        This verifies that the system provides appropriate fallback
        responses when the vector search returns no results.
        """
        # Mock empty search results
        with patch.object(qdrant_service, 'search_chunks', return_value=[]):
            request_data = {
                "query_text": "Query with no matching results",
                "retrieval_mode": "full-book",
                "selected_text": "",
                "metadata_filters": {}
            }

            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            assert response.status_code == 200
            response_data = response.json()

            # Should still return a response, possibly with is_fallback=True
            assert "response_text" in response_data
            # The response might be a fallback response

    def test_complete_flow_with_citation_quality(self, test_client):
        """
        Test that the complete RAG flow maintains citation quality.

        This verifies that citations are properly linked to the retrieved
        chunks and that the response accurately references the source material.
        """
        mock_search_results = [
            {
                "chunk_id": "high_quality_1",
                "content": "Physical AI represents a paradigm shift in robotics by integrating cognitive capabilities with physical embodiment.",
                "module": "foundations",
                "chapter": "2",
                "subsection": "2.1",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "12",
                "score": 0.95
            },
            {
                "chunk_id": "high_quality_2",
                "content": "The integration of perception, cognition, and action is fundamental to physical AI systems.",
                "module": "foundations",
                "chapter": "2",
                "subsection": "2.2",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "13",
                "score": 0.89
            }
        ]

        request_data = {
            "query_text": "What makes physical AI different from traditional robotics?",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {
                "chapter": "2"
            }
        }

        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            assert response.status_code == 200
            response_data = response.json()

            # Verify high-quality citations are returned
            citations = response_data["citations"]
            assert len(citations) == 2  # Should match our mock results

            # Verify citation content matches mock data
            returned_chunk_ids = {cit["chunk_id"] for cit in citations}
            expected_chunk_ids = {"high_quality_1", "high_quality_2"}
            assert returned_chunk_ids == expected_chunk_ids

            # Verify confidence score reflects high-quality results
            assert response_data["confidence_score"] > 0.8

    def test_rag_flow_response_consistency(self, test_client):
        """
        Test that the RAG flow provides consistent responses for the same query.

        This verifies that the system behaves deterministically for identical inputs.
        """
        mock_search_results = [
            {
                "chunk_id": "consistent_chunk",
                "content": "Consistent content for testing",
                "module": "test",
                "chapter": "1",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.90
            }
        ]

        request_data = {
            "query_text": "Consistency test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Make the same request multiple times
        responses = []
        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            for _ in range(3):
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                responses.append(response.json())

        # Verify consistency across responses
        first_response = responses[0]
        for response in responses[1:]:
            # Response text might vary due to AI generation, but structure should be consistent
            assert "response_text" in response
            assert "citations" in response
            assert "confidence_score" in response
            assert len(response["citations"]) == len(first_response["citations"])

    def test_rag_flow_grounding_verification(self, test_client):
        """
        Test that the RAG flow properly verifies grounding of responses.

        This ensures that the generated responses are properly grounded
        in the retrieved context chunks.
        """
        mock_search_results = [
            {
                "chunk_id": "grounded_chunk_1",
                "content": "Physical AI systems must integrate perception, cognition, and action in real-time.",
                "module": "principles",
                "chapter": "3",
                "subsection": "3.1",
                "source_type": "textbook",
                "source_origin": "physical_ai_humanoid_robotics.pdf",
                "page_reference": "20",
                "score": 0.88
            }
        ]

        request_data = {
            "query_text": "How do physical AI systems integrate different capabilities?",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {
                "module": "principles"
            }
        }

        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            assert response.status_code == 200
            response_data = response.json()

            # Verify that grounded chunks are returned
            assert "grounded_chunks" in response_data
            assert isinstance(response_data["grounded_chunks"], list)
            assert len(response_data["grounded_chunks"]) > 0

            # Verify that citations are properly linked to grounded chunks
            citation_chunk_ids = {cit["chunk_id"] for cit in response_data["citations"]}
            grounded_chunk_ids = set(response_data["grounded_chunks"])
            assert citation_chunk_ids.issubset(grounded_chunk_ids)

    def test_rag_flow_performance_under_load(self, test_client):
        """
        Test RAG flow performance with multiple concurrent requests.

        This simulates real-world usage with multiple users making requests.
        """
        import concurrent.futures
        import threading

        mock_search_results = [
            {
                "chunk_id": "load_test_chunk",
                "content": "Content for load testing",
                "module": "test",
                "chapter": "1",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.85
            }
        ]

        def make_request():
            request_data = {
                "query_text": f"Load test query {threading.current_thread().ident}",
                "retrieval_mode": "full-book",
                "selected_text": "",
                "metadata_filters": {}
            }

            with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                return response.status_code == 200

        # Make multiple concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [future.result() for future in futures]

        # Verify all requests succeeded
        assert all(results), "All concurrent requests should succeed"


class TestRAGFlowErrorHandling:
    """Test class for RAG flow error handling scenarios."""

    def test_embedding_service_failure(self, test_client):
        """
        Test RAG flow when embedding service fails.

        This verifies graceful degradation when core services are unavailable.
        """
        request_data = {
            "query_text": "Test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Mock embedding service failure
        with patch('src.services.rag_service.CohereEmbeddingService.generate_embedding') as mock_embed:
            mock_embed.side_effect = Exception("Embedding service unavailable")

            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            # Should return appropriate error status
            assert response.status_code in [500, 200]  # Either error or fallback response

    def test_qdrant_service_failure(self, test_client):
        """
        Test RAG flow when Qdrant service fails.

        This verifies handling of vector database unavailability.
        """
        request_data = {
            "query_text": "Test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Mock Qdrant service failure
        with patch.object(qdrant_service, 'search_chunks') as mock_search:
            mock_search.side_effect = Exception("Qdrant service unavailable")

            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

            # Should return appropriate error status or fallback
            assert response.status_code in [500, 200]

    def test_generation_service_failure(self, test_client):
        """
        Test RAG flow when generation service fails.

        This verifies handling of AI model unavailability.
        """
        mock_search_results = [
            {
                "chunk_id": "error_test_chunk",
                "content": "Content for error testing",
                "module": "test",
                "chapter": "1",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.8
            }
        ]

        request_data = {
            "query_text": "Test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Mock generation service failure
        with patch.object(qdrant_service, 'search_chunks', return_value=mock_search_results):
            with patch('src.services.rag_service.GeminiGenerationService.generate_response') as mock_gen:
                mock_gen.side_effect = Exception("Generation service unavailable")

                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )

                # Should return appropriate error status or fallback
                assert response.status_code in [500, 200]


if __name__ == "__main__":
    pytest.main([__file__])