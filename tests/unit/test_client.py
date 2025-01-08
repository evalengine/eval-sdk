import pytest
from evaengine import EvaEngine
from evaengine.exceptions import ConfigurationError, EvaluationError

class TestEvaEngineUnit:
    """Unit tests for EvaEngine client"""

    def test_client_initialization(self):
        """Test client initialization with API key"""
        client = EvaEngine(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.evaengine.ai"

    def test_client_initialization_custom_url(self):
        """Test client initialization with custom base URL"""
        client = EvaEngine(api_key="test-key", base_url="https://custom.api.com/")
        assert client.base_url == "https://custom.api.com"

    def test_client_initialization_no_key(self):
        """Test client initialization without API key"""
        with pytest.raises(ConfigurationError, match="API key is required"):
            EvaEngine(api_key="")