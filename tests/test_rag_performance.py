"""
Performance tests for RAG response times.

This module tests the performance characteristics of the RAG system,
including response times under various conditions, throughput, and
scalability metrics.
"""

import pytest
import time
import asyncio
from typing import Dict, Any, List
from unittest.mock import patch
import statistics

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestRAGPerformance:
    """Test class for RAG system performance metrics."""

    def test_basic_response_time(self, test_client):
        """
        Test basic response time for RAG queries.

        Verifies that the system responds within acceptable time limits
        under normal conditions.
        """
        mock_search_results = [
            {
                "chunk_id": "perf_chunk_1",
                "content": "Performance test content for measuring response times",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.85
            }
        ]

        request_data = {
            "query_text": "Performance test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        start_time = time.time()
        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )
        end_time = time.time()

        response_time = end_time - start_time

        # Verify response is successful
        assert response.status_code == 200

        # Verify response time is within acceptable limits (e.g., 5 seconds)
        assert response_time <= 5.0, f"Response time {response_time}s exceeds 5s limit"
        print(f"Basic response time: {response_time:.3f}s")

    def test_response_time_percentiles(self, test_client):
        """
        Test response time percentiles to understand performance distribution.

        Measures p50, p90, p95, and p99 response times across multiple requests.
        """
        mock_search_results = [
            {
                "chunk_id": "percentile_chunk",
                "content": "Content for percentile testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.8
            }
        ]

        request_data = {
            "query_text": "Percentile performance test",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        response_times = []
        num_requests = 20  # Reduced for testing purposes

        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            for i in range(num_requests):
                start_time = time.time()
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                end_time = time.time()

                if response.status_code == 200:
                    response_times.append(end_time - start_time)

        # Calculate percentiles
        if len(response_times) > 0:
            p50 = statistics.median(response_times)
            p90 = sorted(response_times)[int(0.9 * len(response_times))] if len(response_times) > 1 else response_times[0]
            p95 = sorted(response_times)[int(0.95 * len(response_times))] if len(response_times) > 1 else response_times[0]

            print(f"Response time - P50: {p50:.3f}s, P90: {p90:.3f}s, P95: {p95:.3f}s")

            # Verify performance targets
            assert p50 <= 3.0, f"P50 response time {p50}s exceeds 3s target"
            assert p90 <= 5.0, f"P90 response time {p90}s exceeds 5s target"

    def test_concurrent_request_performance(self, test_client):
        """
        Test performance under concurrent requests.

        Measures how the system handles multiple simultaneous requests.
        """
        import concurrent.futures
        import threading

        mock_search_results = [
            {
                "chunk_id": "concurrent_chunk",
                "content": "Content for concurrent testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.75
            }
        ]

        def make_request(request_id: int):
            request_data = {
                "query_text": f"Concurrent request {request_id}",
                "retrieval_mode": "full-book",
                "selected_text": "",
                "metadata_filters": {}
            }

            start_time = time.time()
            with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
            end_time = time.time()

            return {
                "response_time": end_time - start_time,
                "status_code": response.status_code,
                "request_id": request_id
            }

        # Execute concurrent requests
        num_concurrent = 10
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_concurrent)]
            results = [future.result() for future in futures]

        # Analyze results
        successful_responses = [r for r in results if r["status_code"] == 200]
        response_times = [r["response_time"] for r in successful_responses]

        if len(response_times) > 0:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times) if response_times else 0

            print(f"Concurrent performance - Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s, Success rate: {len(successful_responses)}/{num_concurrent}")

            # Verify performance under load
            assert len(successful_responses) >= num_concurrent * 0.9, f"Success rate too low: {len(successful_responses)}/{num_concurrent}"
            assert avg_response_time <= 5.0, f"Average response time {avg_response_time}s exceeds 5s limit under load"

    def test_large_query_response_time(self, test_client):
        """
        Test response time with large/complex queries.

        Verifies performance with longer, more complex user queries.
        """
        mock_search_results = [
            {
                "chunk_id": "large_query_chunk_1",
                "content": "Detailed content about physical AI and humanoid robotics for testing large query performance",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.88
            },
            {
                "chunk_id": "large_query_chunk_2",
                "content": "Additional detailed content to test how the system handles complex queries with multiple context chunks",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.2",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "2",
                "score": 0.82
            },
            {
                "chunk_id": "large_query_chunk_3",
                "content": "More content to increase the complexity of the retrieval and generation process for performance testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.3",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "3",
                "score": 0.79
            }
        ]

        # Complex query that might require more processing
        complex_query = (
            "Can you provide a comprehensive explanation of how physical AI integrates "
            "perception, cognition, and action in humanoid robotics systems, "
            "including the challenges and benefits of this approach compared to "
            "traditional robotics, with specific examples from the textbook, "
            "and also explain how this relates to sensorimotor learning and "
            "embodied cognition principles?"
        )

        request_data = {
            "query_text": complex_query,
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        start_time = time.time()
        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )
        end_time = time.time()

        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time <= 10.0, f"Complex query response time {response_time}s exceeds 10s limit"
        print(f"Complex query response time: {response_time:.3f}s")

    def test_response_time_with_filters(self, test_client):
        """
        Test response time when using metadata filters.

        Verifies that filtering doesn't significantly impact performance.
        """
        mock_search_results = [
            {
                "chunk_id": "filtered_perf_chunk",
                "content": "Content for filtered performance testing",
                "module": "filtered_module",
                "chapter": "filtered_chapter",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.85
            }
        ]

        request_data = {
            "query_text": "Filtered performance test",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {
                "module": "filtered_module",
                "chapter": "filtered_chapter"
            }
        }

        start_time = time.time()
        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )
        end_time = time.time()

        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time <= 5.0, f"Filtered query response time {response_time}s exceeds 5s limit"
        print(f"Filtered query response time: {response_time:.3f}s")

    def test_throughput_measurement(self, test_client):
        """
        Test system throughput (requests per second).

        Measures how many requests the system can handle per second.
        """
        mock_search_results = [
            {
                "chunk_id": "throughput_chunk",
                "content": "Content for throughput testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.8
            }
        ]

        request_data = {
            "query_text": "Throughput test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Measure throughput over a time period
        start_time = time.time()
        request_count = 0
        time_limit = 5.0  # 5 seconds to measure throughput

        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            while time.time() - start_time < time_limit:
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                if response.status_code == 200:
                    request_count += 1
                else:
                    break  # Stop if we get an error

        elapsed_time = time.time() - start_time
        throughput = request_count / elapsed_time if elapsed_time > 0 else 0

        print(f"Throughput: {request_count} requests in {elapsed_time:.2f}s = {throughput:.2f} RPS")

        # Verify minimum throughput target
        assert throughput >= 1.0, f"Throughput {throughput:.2f} RPS is below minimum 1 RPS target"

    def test_memory_usage_during_requests(self, test_client):
        """
        Test memory usage patterns during request processing.

        While we can't directly measure memory in this test, we can
        verify that the system handles multiple requests without
        obvious memory leaks by checking response consistency.
        """
        mock_search_results = [
            {
                "chunk_id": "memory_test_chunk",
                "content": "Content for memory usage testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.8
            }
        ]

        request_data = {
            "query_text": "Memory usage test",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Make multiple requests and verify consistent response structure
        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            for i in range(10):
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                assert response.status_code == 200
                response_data = response.json()

                # Verify consistent response structure
                assert "response_text" in response_data
                assert "citations" in response_data
                assert "confidence_score" in response_data

    def test_response_time_degradation_over_time(self, test_client):
        """
        Test for response time degradation over extended usage.

        Checks if response times increase significantly as the system
        processes more requests (potential memory leaks or resource exhaustion).
        """
        mock_search_results = [
            {
                "chunk_id": "degradation_test_chunk",
                "content": "Content for degradation testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.8
            }
        ]

        request_data = {
            "query_text": "Degradation test query",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        response_times = []
        num_requests = 15  # Number of requests to make

        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            for i in range(num_requests):
                start_time = time.time()
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                end_time = time.time()

                if response.status_code == 200:
                    response_time = end_time - start_time
                    response_times.append(response_time)

        if len(response_times) >= 10:  # Need enough data points for comparison
            early_batch = response_times[:5]  # First 5 requests
            late_batch = response_times[-5:]  # Last 5 requests

            avg_early = sum(early_batch) / len(early_batch)
            avg_late = sum(late_batch) / len(late_batch)

            degradation_factor = avg_late / avg_early if avg_early > 0 else 1

            print(f"Early requests avg: {avg_early:.3f}s, Late requests avg: {avg_late:.3f}s")
            print(f"Degradation factor: {degradation_factor:.2f}x")

            # Verify no significant degradation (within 2x)
            assert degradation_factor <= 2.0, f"Performance degraded by {degradation_factor:.2f}x over time"


class TestPerformanceBoundaries:
    """Test class for performance boundary conditions."""

    def test_maximum_response_time_boundary(self, test_client):
        """
        Test that response times don't exceed maximum acceptable limits.

        Verifies system behavior under maximum acceptable response time boundaries.
        """
        mock_search_results = [
            {
                "chunk_id": "boundary_chunk",
                "content": "Content for boundary testing" * 100,  # Large content
                "module": "performance",
                "chapter": "boundary",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.8
            }
        ] * 10  # Multiple chunks

        request_data = {
            "query_text": "Boundary condition test with potentially large response",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        start_time = time.time()
        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            response = test_client.post(
                "/api/rag/chat",
                headers={"Authorization": "Bearer test-token"},
                json=request_data
            )
        end_time = time.time()

        response_time = end_time - start_time

        # Even with large content, response should be reasonable
        assert response.status_code == 200
        assert response_time <= 15.0, f"Response time {response_time}s exceeds 15s boundary"
        print(f"Boundary test response time: {response_time:.3f}s")

    def test_minimum_performance_requirements(self, test_client):
        """
        Test that the system meets minimum performance requirements.

        Verifies that basic performance targets are met.
        """
        mock_search_results = [
            {
                "chunk_id": "min_perf_chunk",
                "content": "Content for minimum performance testing",
                "module": "performance",
                "chapter": "test",
                "subsection": "1.1",
                "source_type": "textbook",
                "source_origin": "test.pdf",
                "page_reference": "1",
                "score": 0.85
            }
        ]

        request_data = {
            "query_text": "Minimum performance requirement test",
            "retrieval_mode": "full-book",
            "selected_text": "",
            "metadata_filters": {}
        }

        # Run multiple requests to get average performance
        response_times = []
        num_samples = 5

        with patch('src.services.qdrant_service.QdrantService.search_chunks', return_value=mock_search_results):
            for _ in range(num_samples):
                start_time = time.time()
                response = test_client.post(
                    "/api/rag/chat",
                    headers={"Authorization": "Bearer test-token"},
                    json=request_data
                )
                end_time = time.time()

                if response.status_code == 200:
                    response_times.append(end_time - start_time)

        if response_times:
            avg_response_time = sum(response_times) / len(response_times)

            # Minimum performance requirement: average response time under 3 seconds
            assert avg_response_time <= 3.0, f"Average response time {avg_response_time:.3f}s exceeds minimum requirement of 3s"
            print(f"Average response time: {avg_response_time:.3f}s (target: <=3s)")


if __name__ == "__main__":
    pytest.main([__file__])