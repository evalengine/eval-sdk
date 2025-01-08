from typing import Optional, Dict, Any, List
import aiohttp
from .models import EvalResponse, TweetPair, ScoreDetail
from .exceptions import EvaEngineError, AuthenticationError

class EvaEngine:
    def __init__(self, api_key: str, base_url: Optional[str] = "https://api.evaengine.ai"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    "X-API-Key": self.api_key,
                    "accept": "application/json",
                    "Content-Type": "application/json"
                }
            )

    async def _make_request(self, method: str, endpoint: str, json: Optional[Dict] = None) -> Any:
        await self._ensure_session()
        
        async with self.session.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            json=json
        ) as response:
            if response.status == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status != 200:
                raise EvaEngineError(f"API request failed: {response.status}")
            
            return await response.json()

    async def evaluate_tweet(self, input_tweet: str, output_tweet: str) -> EvalResponse:
        """
        Evaluate a tweet response against an original tweet.
        
        Args:
            input_tweet: The original tweet text
            output_tweet: The response tweet to evaluate
            
        Returns:
            EvalResponse object containing scores and analysis
        """
        try:
            data = await self._make_request(
                "POST",
                "/api/eval/evaluate-tweet",
                {
                    "input_tweet": input_tweet,
                    "output_tweet": output_tweet
                }
            )
            # Transform response if needed
            if "output_tweet" in data:
                data["responded_tweet"] = data.pop("output_tweet")
            return EvalResponse(**data)
        except Exception as e:
            raise EvaEngineError(f"Evaluation failed: {str(e)}")

    async def evaluate_tweet_virtual(self, input_tweet: str, output_tweet: str) -> EvalResponse:
        """
        Evaluate a tweet response using virtual scoring.
        
        Args:
            input_tweet: The original tweet text
            output_tweet: The response tweet to evaluate
            
        Returns:
            EvalResponse object containing virtual scores
        """
        try:
            data = await self._make_request(
                "POST",
                "/api/eval/virtuals/evaluate-tweet",
                {
                    "input_tweet": input_tweet,
                    "output_tweet": output_tweet
                }
            )
            # Transform response if needed
            if "output_tweet" in data:
                data["responded_tweet"] = data.pop("output_tweet")
            return EvalResponse(**data)
        except Exception as e:
            raise EvaEngineError(f"Virtual evaluation failed: {str(e)}")

    async def get_scores(self) -> List[EvalResponse]:
        """
        Get available scoring metrics.
        
        Returns:
            List of EvalResponse objects containing historical scores
        """
        try:
            data = await self._make_request("GET", "/api/eval/scores")
            return [EvalResponse(**score) for score in data["scores"]]
        except Exception as e:
            raise EvaEngineError(f"Failed to fetch scores: {str(e)}")

    async def get_suggested_tweet(self, input_tweet: str) -> str:
        """
        Get a suggested tweet response.
        
        Args:
            input_tweet: The original tweet to respond to
            
        Returns:
            Suggested response tweet
        """
        try:
            data = await self._make_request(
                "POST",
                "/api/eval/suggested-tweet",
                {"input_tweet": input_tweet}
            )
            return data["suggested_tweet"]
        except Exception as e:
            raise EvaEngineError(f"Failed to get suggestion: {str(e)}")

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()