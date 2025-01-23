class ImageGenerationError(Exception):
    """Base exception for image generation failures"""
    pass

class ConfigurationError(Exception):
    """Raised when config loading fails"""
    pass

class SecurityError(Exception):
    """Raised for path sanitization issues"""
    pass
