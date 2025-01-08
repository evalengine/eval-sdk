import aiohttp
from typing import Optional, Dict, Any, List, Callable, TypeVar, ParamSpec
from functools import wraps
from .models import EvalResponse
from .exceptions import (
    AuthenticationError,
    EvaluationError,
    ConfigurationError,
    NetworkError,
    APIError,
    EvaEngineError
)

P = ParamSpec("P")
T = TypeVar("T")

def handle_api_errors(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to handle common API errors"""
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise AuthenticationError("Invalid API key") from e
            elif e.status == 400:
                raise EvaluationError(f"Invalid request: {str(e)}", e.status) from e
            else:
                raise APIError(f"API request failed: {str(e)}", e.status) from e
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error: {str(e)}") from e
        except Exception as e:
            raise EvaEngineError(f"Unexpected error: {str(e)}", raw_error=e) from e
    return wrapper

class EvaEngine:
    def __init__(self, api_key: str, base_url: Optional[str] = "https://api.evaengine.ai"):
        if not api_key:
            raise ConfigurationError("API key is required")
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

    @handle_api_errors
    async def _make_request(self, method: str, endpoint: str, json: Optional[Dict] = None) -> Any:
        if not self.session:
            raise ConfigurationError("Client session not initialized")
        
        async with self.session.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            json=json
        ) as response:
            response.raise_for_status()
            return await response.json()

    @handle_api_errors
    async def evaluate_tweet(self, input_tweet: str, output_tweet: str) -> EvalResponse:
        """
        Evaluate a tweet response against an original tweet.
        
        Args:
            input_tweet: The original tweet text
            output_tweet: The response tweet to evaluate
            
        Returns:
            EvalResponse object containing scores and analysis
            
        Raises:
            ConfigurationError: If client is not properly initialized
            EvaluationError: If evaluation fails
            AuthenticationError: If API key is invalid
            NetworkError: If there are connection issues
            APIError: For other API-related errors
        """
        if not input_tweet or not output_tweet:
            raise EvaluationError("Both input_tweet and output_tweet are required")
            
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

    @handle_api_errors
    async def evaluate_tweet_virtual(self, input_tweet: str, output_tweet: str) -> EvalResponse:
        """
        Evaluate a tweet response using virtual scoring.
        
        Args:
            input_tweet: The original tweet text
            output_tweet: The response tweet to evaluate
            
        Returns:
            EvalResponse object containing virtual scores
            
        Raises:
            ConfigurationError: If client is not properly initialized
            EvaluationError: If evaluation fails
            AuthenticationError: If API key is invalid
            NetworkError: If there are connection issues
            APIError: For other API-related errors
        """
        if not input_tweet or not output_tweet:
            raise EvaluationError("Both input_tweet and output_tweet are required")
            
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

    @handle_api_errors
    async def get_scores(self) -> List[EvalResponse]:
        """
        Get available scoring metrics.
        
        Returns:
            List of EvalResponse objects containing historical scores
            
        Raises:
            ConfigurationError: If client is not properly initialized
            AuthenticationError: If API key is invalid
            NetworkError: If there are connection issues
            APIError: For other API-related errors
        """
        data = await self._make_request("GET", "/api/eval/scores")
        return [EvalResponse(**score) for score in data["scores"]]

    @handle_api_errors
    async def get_suggested_tweet(self, input_tweet: str) -> str:
        """
        Get a suggested tweet response.
        
        Args:
            input_tweet: The original tweet to respond to
            
        Returns:
            Suggested response tweet
            
        Raises:
            ConfigurationError: If client is not properly initialized
            EvaluationError: If suggestion fails
            AuthenticationError: If API key is invalid
            NetworkError: If there are connection issues
            APIError: For other API-related errors
        """
        if not input_tweet:
            raise EvaluationError("input_tweet is required")
            
        data = await self._make_request(
            "POST",
            "/api/eval/suggested-tweet",
            {"input_tweet": input_tweet}
        )
        
        if "suggested_tweet" not in data:
            raise EvaluationError("Invalid response format: missing suggested_tweet")
        return data["suggested_tweet"]

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()