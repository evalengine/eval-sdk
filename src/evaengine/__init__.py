from .client import EvaEngine
from .models import EvalResponse, TweetPair, ScoreDetail
from .exceptions import EvaEngineError, AuthenticationError, EvaluationError

__version__ = "0.1.1"

__all__ = [
    "EvaEngine",
    "EvalResponse",
    "TweetPair",
    "ScoreDetail",
    "EvaEngineError",
    "AuthenticationError",
    "EvaluationError"
]
