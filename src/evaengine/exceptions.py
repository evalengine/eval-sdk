class EvaEngineError(Exception):
    """Base exception for EvaEngine errors"""
    pass

class AuthenticationError(EvaEngineError):
    """Raised when authentication fails"""
    pass

class EvaluationError(EvaEngineError):
    """Raised when tweet evaluation fails"""
    pass

class ConfigurationError(EvaEngineError):
    """Raised when configuration is invalid"""
    pass