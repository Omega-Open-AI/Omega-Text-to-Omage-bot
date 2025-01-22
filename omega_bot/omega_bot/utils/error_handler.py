"""
Error Handler Module
Custom error handling for the bot.

Author: Omega-Open-AI
Date: 2025-01-22
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

class BotError(Exception):
    """Base exception class for bot-related errors."""
    
    def __init__(self, message: str, error_code: Optional[int] = None):
        """Initialize the error with a message and optional error code."""
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
        
        # Log the error
        logger.error(f"Bot Error {f"[{error_code}]" if error_code else ""}: {message}")

class ValidationError(BotError):
    """Raised when input validation fails."""
    def __init__(self, message: str):
        super().__init__(message, error_code=400)

class RateLimitError(BotError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str):
        super().__init__(message, error_code=429)

class ModelError(BotError):
    """Raised when there's an error with model operations."""
    def __init__(self, message: str):
        super().__init__(message, error_code=500)

class ConfigurationError(BotError):
    """Raised when there's a configuration-related error."""
    def __init__(self, message: str):
        super().__init__(message, error_code=501)

def handle_error(error: Exception) -> str:
    """Convert exceptions to user-friendly messages."""
    if isinstance(error, ValidationError):
        return f"?? Invalid input: {str(error)}"
    elif isinstance(error, RateLimitError):
        return f"? Rate limit exceeded: {str(error)}"
    elif isinstance(error, ModelError):
        return f"?? Model error: {str(error)}"
    elif isinstance(error, ConfigurationError):
        return f"?? Configuration error: {str(error)}"
    elif isinstance(error, BotError):
        return f"? Error: {str(error)}"
    else:
        # For unexpected errors
        logger.exception("Unexpected error occurred")
        return "An unexpected error occurred. Please try again later."
