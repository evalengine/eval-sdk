import pytest
import pytest_asyncio
import os
from dotenv import load_dotenv
from evaengine import EvaEngine

load_dotenv()

@pytest_asyncio.fixture
async def eva_client():
    """Fixture to provide an EvaEngine client"""
    api_key = os.getenv("X_API_KEY")
    base_url = os.getenv("EVA_API_URL", "https://api.evaengine.ai")
    
    if not api_key:
        pytest.skip("X_API_KEY environment variable not set")
    
    async with EvaEngine(api_key=api_key, base_url=base_url) as client:
        yield client 