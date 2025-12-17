"""
Test suite for missing environment variables error reporting
"""
import pytest
import os
from unittest.mock import patch
import sys

# Add backend src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import validate_settings

def test_validate_settings_with_missing_vars():
    """Test that validate_settings raises proper error with missing environment variables"""
    # Clear all required environment variables
    env_backup = {}
    required_vars = ['QDRANT_URL', 'COHERE_API_KEY', 'GEMINI_API_KEY', 'NEON_DB_URL']

    for key in required_vars:
        if key in os.environ:
            env_backup[key] = os.environ[key]
            del os.environ[key]

    try:
        # This should raise a ValueError
        with pytest.raises(ValueError) as exc_info:
            validate_settings()

        # Check that the error message mentions missing environment variables
        error_message = str(exc_info.value)
        assert "Missing required environment variables" in error_message

        # Check that all required variables are mentioned in the error
        for var in required_vars:
            assert var in error_message
    finally:
        # Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value

def test_validate_settings_with_partial_missing_vars():
    """Test that validate_settings raises proper error with partially missing environment variables"""
    # Set up environment with only some required variables
    with patch.dict(os.environ, {
        'QDRANT_URL': 'https://test-qdrant.com',
        'COHERE_API_KEY': 'test-cohere-key'
        # Missing GEMINI_API_KEY and NEON_DB_URL
    }):
        with pytest.raises(ValueError) as exc_info:
            validate_settings()

        error_message = str(exc_info.value)
        assert "Missing required environment variables" in error_message
        assert "GEMINI_API_KEY" in error_message
        assert "NEON_DB_URL" in error_message

def test_config_object_with_missing_vars():
    """Test that the config object handles missing variables gracefully"""
    from src.config import Settings

    # Temporarily clear environment variables for this test
    env_backup = {}
    all_vars = ['QDRANT_URL', 'QDRANT_API_KEY', 'COHERE_API_KEY', 'GEMINI_API_KEY', 'NEON_DB_URL', 'DEBUG_MODE']

    for key in all_vars:
        if key in os.environ:
            env_backup[key] = os.environ[key]
            del os.environ[key]

    try:
        # Creating the Settings object should not fail, but values will be empty
        settings = Settings()

        # Values should be empty strings or defaults
        assert settings.qdrant_url == ""
        assert settings.cohere_api_key == ""
        assert settings.gemini_api_key == ""
        assert settings.neon_db_url == ""
        assert settings.debug_mode is False  # Default value
    finally:
        # Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value

def test_error_message_format():
    """Test that error messages for missing variables are properly formatted"""
    # Clear only one required variable
    env_backup = os.environ.get('GEMINI_API_KEY')
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']

    try:
        with pytest.raises(ValueError) as exc_info:
            validate_settings()

        error_message = str(exc_info.value)
        assert "GEMINI_API_KEY" in error_message
        assert "Missing required environment variables" in error_message
    finally:
        if env_backup:
            os.environ['GEMINI_API_KEY'] = env_backup

def test_multiple_missing_variables_error():
    """Test error message when multiple variables are missing"""
    # Clear multiple required variables
    env_backup = {}
    vars_to_clear = ['GEMINI_API_KEY', 'NEON_DB_URL']

    for key in vars_to_clear:
        if key in os.environ:
            env_backup[key] = os.environ[key]
            del os.environ[key]

    try:
        with pytest.raises(ValueError) as exc_info:
            validate_settings()

        error_message = str(exc_info.value)
        for var in vars_to_clear:
            assert var in error_message

        # Should contain multiple variables in the error message
        assert "GEMINI_API_KEY" in error_message
        assert "NEON_DB_URL" in error_message
    finally:
        # Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value

if __name__ == "__main__":
    pytest.main([__file__])