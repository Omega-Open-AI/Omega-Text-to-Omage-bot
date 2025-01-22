# omega_bot/security/input_validation.py
from typing import Optional, Dict, Any
import re
from dataclasses import dataclass
from ..utils.error_handler import ValidationError, SecurityError
from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class PromptValidationRules:
    min_length: int = 3
    max_length: int = 500
    allowed_chars: str = r"[a-zA-Z0-9\s\-_.,!?()'\"]+"
    forbidden_words: set = frozenset(["hack", "exploit", "nsfw"])

class InputValidator:
    def __init__(self, rules: Optional[PromptValidationRules] = None):
        self.rules = rules or PromptValidationRules()
        
    def validate_prompt(self, prompt: str) -> str:
        """Validate and sanitize user input prompt."""
        if not isinstance(prompt, str):
            raise ValidationError("Prompt must be a string")
            
        if not (self.rules.min_length <= len(prompt) <= self.rules.max_length):
            raise ValidationError(
                f"Prompt length must be between {self.rules.min_length} "
                f"and {self.rules.max_length} characters"
            )
            
        if not re.match(f"^{self.rules.allowed_chars}$", prompt):
            raise ValidationError("Prompt contains invalid characters")
            
        for word in self.rules.forbidden_words:
            if word.lower() in prompt.lower():
                raise SecurityError(f"Prompt contains forbidden word: {word}")
                
        return prompt.strip()

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user settings."""
        required_keys = {"model_id", "steps", "cfg_scale", "width", "height"}
        if not all(key in settings for key in required_keys):
            raise ValidationError(f"Missing required settings: {required_keys - settings.keys()}")
            
        # Validate numeric ranges
        if not (1 <= settings["steps"] <= 50):
            raise ValidationError("Steps must be between 1 and 50")
        if not (1.0 <= settings["cfg_scale"] <= 20.0):
            raise ValidationError("CFG scale must be between 1.0 and 20.0")
        if not (64 <= settings["width"] <= 1024):
            raise ValidationError("Width must be between 64 and 1024")
        if not (64 <= settings["height"] <= 1024):
            raise ValidationError("Height must be between 64 and 1024")
            
        return settings
