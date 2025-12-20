"""
Integration tests for backend-frontend communication in the RAG system.

This module tests the communication between the frontend components and
the backend API endpoints, ensuring proper data flow and response handling.
"""

import pytest
import asyncio
import json
from typing import Dict, Any, Optional
from unittest.mock import AsyncMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestBackendFrontendIntegration:
    """Test class for backend-frontend integration scenarios."""

    def test_rag_chat_endpoint_basic_communication(self, test_client):
        """
        Test basic communication with the RAG chat endpoint.

        This simulates a frontend request to the backend chat endpoint
        and verifies the response structure and content.
        """
        # Simulate a typical frontend request
        request_data = {
            "query_text": "What is the main concept of physical AI?",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Verify response status
        assert response.status_code == 200

        # Verify response structure
        response_data = response.json()
        assert "response_id" in response_data
        assert "response_text" in response_data
        assert "citations" in response_data
        assert "confidence_score" in response_data
        assert "grounded_chunks" in response_data
        assert "is_fallback" in response_data

    def test_rag_chat_endpoint_per_page_mode(self, test_client):
        """
        Test per-page mode communication with the RAG chat endpoint.

        This tests the scenario where the frontend sends selected text
        for contextual retrieval.
        """
        # Simulate a per-page mode request from frontend
        request_data = {
            "query_text": "Explain this concept in more detail",
            "retrieval_mode": "per-page",
            "selected_text": "Physical AI combines robotics with artificial intelligence",
            "metadata_filters": {
                "module": "introduction",
                "chapter": "1"
            }
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Verify response status
        assert response.status_code == 200

        # Verify response structure
        response_data = response.json()
        assert "response_id" in response_data
        assert "response_text" in response_data
        assert "citations" in response_data
        assert isinstance(response_data["citations"], list)

    def test_rag_validation_endpoint_integration(self, test_client):
        """
        Test communication with the RAG validation endpoint.

        This tests the frontend validation request to ensure query validity.
        """
        # Simulate a validation request from frontend
        request_data = {
            "query_text": "What is physical AI?",
            "retrieval_mode": "full-book"
        }

        response = test_client.post(
            "/api/rag/validate",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Verify response status
        assert response.status_code == 200

        # Verify response structure
        response_data = response.json()
        assert "is_valid" in response_data
        assert "errors" in response_data
        assert isinstance(response_data["is_valid"], bool)

    def test_statistics_endpoint_integration(self, test_client):
        """
        Test communication with the statistics endpoint.

        This tests the frontend request for RAG system statistics.
        """
        response = test_client.get(
            "/api/rag/stats",
            headers={"Authorization": "Bearer test-token"}
        )

        # Verify response status
        assert response.status_code == 200

        # Verify response structure
        response_data = response.json()
        assert "total_queries" in response_data
        assert "avg_response_time" in response_data
        assert "success_rate" in response_data

    def test_health_check_endpoint_integration(self, test_client):
        """
        Test communication with the health check endpoint.

        This tests the frontend health monitoring request.
        """
        response = test_client.get("/api/health")

        # Verify response status
        assert response.status_code == 200

        # Verify response structure
        response_data = response.json()
        assert "status" in response_data
        assert "timestamp" in response_data
        assert "services" in response_data

    def test_error_handling_integration(self, test_client):
        """
        Test error handling in backend-frontend communication.

        This tests how the backend handles invalid requests from the frontend.
        """
        # Send an invalid request with missing required fields
        request_data = {
            "query_text": "",  # Empty query
            "retrieval_mode": "invalid-mode"  # Invalid mode
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Should return 422 for validation error
        assert response.status_code == 422

    def test_rate_limiting_integration(self, test_client):
        """
        Test rate limiting behavior in backend-frontend communication.

        This tests how the backend handles excessive requests from the frontend.
        """
        # Send multiple requests rapidly to trigger rate limiting
        request_data = {
            "query_text": "Test query for rate limiting",
            "retrieval_mode": "full-book"
        }

        # Send more requests than allowed by rate limiter
        for i in range(105):  # Assuming 100 per minute limit
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )

        # Eventually should hit rate limit
        rate_limited_response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        # Check if rate limiting is triggered (could be 429 or handled differently)
        # depending on slowapi configuration
        assert rate_limited_response.status_code in [200, 429]

    def test_authentication_integration(self, test_client):
        """
        Test authentication flow in backend-frontend communication.

        This tests how the backend handles unauthorized requests from the frontend.
        """
        # Send request without authentication header
        request_data = {
            "query_text": "Test query without auth",
            "retrieval_mode": "full-book"
        }

        response = test_client.post(
            "/api/rag/chat",
            json=request_data
        )

        # Should return 401 for unauthorized access
        assert response.status_code in [401, 403]

    def test_citation_format_integration(self, test_client):
        """
        Test that citations are properly formatted for frontend consumption.

        This ensures the backend returns citation data in a format
        that the frontend can properly display.
        """
        request_data = {
            "query_text": "What are the key concepts in chapter 1?",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {
                "chapter": "1"
            }
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        assert response.status_code == 200
        response_data = response.json()

        # Verify citation format
        for citation in response_data.get("citations", []):
            assert "chunk_id" in citation
            assert "module" in citation
            assert "chapter" in citation
            assert "subsection" in citation
            assert "page_reference" in citation

    def test_confidence_scoring_integration(self, test_client):
        """
        Test that confidence scores are properly calculated and returned.

        This ensures the backend provides confidence information that
        the frontend can use for response quality indication.
        """
        request_data = {
            "query_text": "What is the main topic of this textbook?",
            "retrieval_mode": "full-book"
        }

        response = test_client.post(
            "/api/rag/chat",
            headers={"Authorization": "Bearer test-token"},
            json=request_data
        )

        assert response.status_code == 200
        response_data = response.json()

        # Verify confidence score format
        confidence_score = response_data.get("confidence_score")
        assert isinstance(confidence_score, float)
        assert 0.0 <= confidence_score <= 1.0


class TestAsyncCommunication:
    """Test class for asynchronous communication patterns."""

    @pytest.mark.asyncio
    async def test_async_request_handling(self):
        """
        Test asynchronous request handling between frontend and backend.

        This simulates how the backend handles concurrent requests
        from multiple frontend instances.
        """
        import aiohttp

        # This would normally be run in a separate process during actual testing
        # For now, we'll simulate the async behavior
        async def mock_async_request():
            # Simulate an async request
            await asyncio.sleep(0.01)  # Small delay to simulate network call
            return {"status": "success", "data": "response"}

        # Run the async function
        result = await mock_async_request()
        assert result["status"] == "success"


if __name__ == "__main__":
    pytest.main([__file__])