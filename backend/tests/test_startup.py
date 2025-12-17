"""
Test suite for application startup
"""
import pytest
import os
from unittest.mock import patch
import sys

# Add backend src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from fastapi.testclient import TestClient

def test_startup_with_valid_env_vars():
    """Test application startup with valid environment variables"""
    # Set up environment with all required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        # Create test client - this tests that the app can be created
        client = TestClient(app)

        # Test basic endpoint to ensure app is running
        response = client.get("/")
        assert response.status_code == 200

def test_startup_event():
    """Test that startup event runs without errors"""
    # This test simulates the startup event
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        # Import the startup event function
        from src.api.rag import startup_event

        # Run the startup event - should not raise any exceptions
        # Note: This will mock the actual service health checks
        with patch('src.services.qdrant_service.qdrant_service.create_collection') as mock_create_collection, \
             patch('src.services.qdrant_service.qdrant_service.health_check', return_value=True), \
             patch('src.services.cohere_service.cohere_service.health_check', return_value=True), \
             patch('src.services.gemini_service.gemini_service.health_check', return_value=True):

            # The startup event should complete without errors
            startup_event()

def test_health_check_with_valid_env_vars():
    """Test health check endpoint with valid environment variables"""
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        client = TestClient(app)

        # Mock the service health checks to return True
        with patch('src.services.qdrant_service.qdrant_service.health_check', return_value=True), \
             patch('src.services.cohere_service.cohere_service.health_check', return_value=True), \
             patch('src.services.gemini_service.gemini_service.health_check', return_value=True):

            response = client.get("/api/health")
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "healthy"
            assert data["services"]["qdrant"] == True
            assert data["services"]["cohere"] == True
            assert data["services"]["gemini"] == True

def test_config_validation_on_startup():
    """Test that config validation works during startup"""
    # Test with missing environment variables - should still allow app creation
    # but validation should fail when validate_settings is called
    env_backup = {}
    required_vars = ['QDRANT_URL', 'COHERE_API_KEY', 'GEMINI_API_KEY', 'NEON_DB_URL']

    for key in required_vars:
        if key in os.environ:
            env_backup[key] = os.environ[key]
            del os.environ[key]

    try:
        # App should still be creatable even with missing env vars
        client = TestClient(app)

        # But accessing settings with validation should fail
        from src.config import validate_settings
        with pytest.raises(ValueError):
            validate_settings()
    finally:
        # Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value

if __name__ == "__main__":
    pytest.main([__file__])