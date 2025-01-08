from typing import Optional
from http import HTTPStatus

class EvaEngineError(Exception):
    """Base exception for EvaEngine errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, raw_error: Optional[Exception] = None):
        super().__init__(message)
        self.status_code = status_code
        self.raw_error = raw_error

class AuthenticationError(EvaEngineError):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed", raw_error: Optional[Exception] = None):
        super().__init__(message, HTTPStatus.UNAUTHORIZED, raw_error)

class EvaluationError(EvaEngineError):
    """Raised when tweet evaluation fails"""
    def __init__(self, message: str, status_code: Optional[int] = None, raw_error: Optional[Exception] = None):
        super().__init__(f"Tweet evaluation failed: {message}", status_code, raw_error)

class ConfigurationError(EvaEngineError):
    """Raised when configuration is invalid"""
    def __init__(self, message: str, raw_error: Optional[Exception] = None):
        super().__init__(f"Invalid configuration: {message}", None, raw_error)

class NetworkError(EvaEngineError):
    """Raised when network communication fails"""
    def __init__(self, message: str, status_code: Optional[int] = None, raw_error: Optional[Exception] = None):
        super().__init__(f"Network error: {message}", status_code, raw_error)

class APIError(EvaEngineError):
    """Raised when API returns an error response"""
    def __init__(self, message: str, status_code: int, raw_error: Optional[Exception] = None):
        super().__init__(f"API error: {message}", status_code, raw_error)