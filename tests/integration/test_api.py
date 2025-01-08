import pytest
import os
from dotenv import load_dotenv
from evaengine import EvaEngine, EvalResponse
from evaengine.exceptions import EvaluationError, AuthenticationError

load_dotenv()

TEST_TWEET = {
    "input_tweet": "What's your favorite programming language?",
    "output_tweet": "Python is amazing for its simplicity and readability!"
}

TEST_PROJECT_TWEET = {
    "input_tweet": "Just launched my new AI project!"
}

@pytest.mark.asyncio
class TestEvaEngineIntegration:
    """Integration tests for EvaEngine API"""

    async def test_evaluate_tweet(self, eva_client):
        """Test tweet evaluation endpoint"""
        result = await eva_client.evaluate_tweet(
            input_tweet=TEST_TWEET["input_tweet"],
            output_tweet=TEST_TWEET["output_tweet"]
        )
        
        # Verify response is EvalResponse instance
        assert isinstance(result, EvalResponse)
        assert hasattr(result, 'truth')  # Check attributes instead of dict keys
        assert hasattr(result, 'accuracy')
        assert hasattr(result, 'creativity')
        assert hasattr(result, 'engagement')
        
        # Verify score ranges
        assert 0 <= result.truth.score <= 100
        assert 0 <= result.accuracy.score <= 100
        assert 0 <= result.creativity.score <= 100
        assert 0 <= result.engagement.score <= 100
        assert 0 <= result.final_score <= 100
        
        # Verify rationales exist
        assert result.truth.rationale
        assert result.accuracy.rationale
        assert result.creativity.rationale
        assert result.engagement.rationale

    async def test_evaluate_tweet_virtual(self, eva_client):
        """Test virtual evaluation endpoint"""
        result = await eva_client.evaluate_tweet_virtual(
            input_tweet=TEST_TWEET["input_tweet"],
            output_tweet=TEST_TWEET["output_tweet"]
        )
        
        assert isinstance(result, EvalResponse)
        assert 0 <= result.final_score <= 100

    async def test_get_scores(self, eva_client):
        """Test historical scores endpoint"""
        results = await eva_client.get_scores()
        
        # Verify it returns a list of EvalResponse objects
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], EvalResponse)
            assert results[0].original_tweet
            assert results[0].responded_tweet
            assert 0 <= results[0].final_score <= 100

    async def test_get_suggested_tweet(self, eva_client):
        """Test tweet suggestion endpoint"""
        suggestion = await eva_client.get_suggested_tweet(
            input_tweet=TEST_PROJECT_TWEET["input_tweet"]
        )
        
        assert isinstance(suggestion, str)
        assert len(suggestion) > 0

