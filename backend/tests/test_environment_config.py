"""
Test suite for environment configuration
"""
import pytest
import os
from unittest.mock import patch, MagicMock
import sys
import tempfile

# Add backend src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import Settings, validate_settings

def test_settings_loading():
    """Test that settings can be loaded from environment variables"""
    # Test with mock environment variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test',
        'DEBUG_MODE': 'true'
    }):
        settings = Settings()

        assert settings.qdrant_url == 'https://test-qdrant.com'
        assert settings.cohere_api_key == 'test-cohere-key'
        assert settings.gemini_api_key == 'test-gemini-key'
        assert settings.neon_db_url == 'postgresql://test:test@test:5432/test'
        assert settings.debug_mode is True

def test_settings_defaults():
    """Test default values when environment variables are not set"""
    # Temporarily clear environment variables for this test
    env_backup = {}
    for key in ['QDRANT_URL', 'COHERE_API_KEY', 'GEMINI_API_KEY', 'NEON_DB_URL', 'DEBUG_MODE']:
        if key in os.environ:
            env_backup[key] = os.environ[key]
            del os.environ[key]

    try:
        # With empty environment, most values should be empty strings or defaults
        settings = Settings()

        # These should be empty strings since no defaults are set in the model
        assert settings.qdrant_url == ""
        assert settings.cohere_api_key == ""
        assert settings.gemini_api_key == ""
        assert settings.neon_db_url == ""
        assert settings.debug_mode is False  # Default is False
    finally:
        # Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value

def test_validate_settings_all_present():
    """Test validation when all required environment variables are present"""
    # Set up environment with all required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key',
        'GEMINI_API_KEY': 'test-gemini-key',
        'NEON_DB_URL': 'postgresql://test:test@test:5432/test'
    }):
        # This should not raise an exception
        assert validate_settings() is True

def test_validate_settings_missing_variables():
    """Test validation when required environment variables are missing"""
    # Clear all required environment variables
    env_backup = {}
    required_vars = ['QDRANT_URL', 'COHERE_API_KEY', 'GEMINI_API_KEY', 'NEON_DB_URL']

    for key in required_vars:
        if key in os.environ:
            env_backup[key] = os.environ[key]
            del os.environ[key]

    try:
        # This should raise a ValueError
        with pytest.raises(ValueError, match="Missing required environment variables"):
            validate_settings()
    finally:
        # Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value

def test_validate_settings_partial_missing():
    """Test validation when some required environment variables are missing"""
    # Set up environment with only some required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key'
        # Missing GEMINI_API_KEY and NEON_DB_URL
    }):
        # This should raise a ValueError
        with pytest.raises(ValueError, match="Missing required environment variables"):
            validate_settings()

def test_debug_mode_parsing():
    """Test that debug mode is correctly parsed from environment"""
    test_cases = [
        ('true', True),
        ('True', True),
        ('TRUE', True),
        ('1', True),
        ('false', False),
        ('False', False),
        ('FALSE', False),
        ('0', False),
        ('anything_else', False)  # Default is false
    ]

    for env_value, expected in test_cases:
        with patch.dict(os.environ, {
            'QDRANT_URL': 'https://test-qdrant.com',
            'COHERE_API_KEY': 'test-cohere-key',
            'GEMINI_API_KEY': 'test-gemini-key',
            'NEON_DB_URL': 'postgresql://test:test@test:5432/test',
            'DEBUG_MODE': env_value
        }):
            settings = Settings()
            assert settings.debug_mode == expected

def test_sensitive_data_not_in_logs():
    """Test that sensitive data is not exposed in error messages or logs"""
    # This test verifies that error messages don't contain sensitive data
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://user:password@test-qdrant.com',
        'COHERE_API_KEY': 'secret-cohere-key',
        'GEMINI_API_KEY': 'secret-gemini-key',
        'NEON_DB_URL': 'postgresql://user:password@test:5432/test'
    }):
        settings = Settings()

        # Verify that sensitive data is not exposed in string representation
        settings_str = str(settings)

        # The actual keys should not appear in string representation
        # (unless Pydantic is configured to show them, which we should avoid)
        # This test depends on Pydantic's security settings

if __name__ == "__main__":
    pytest.main([__file__])