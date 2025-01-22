"""
Model Manager Module
Handles model configurations and management.

Author: Omega-Open-AI
Date: 2025-01-22
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any

from omega_bot.utils.error_handler import BotError

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages AI model configurations and settings."""

    def __init__(self, config_path: str = "config/models.json"):
        """Initialize the model manager with configuration."""
        self.config_path = Path(config_path)
        self.models: Dict[str, Any] = {}
        self.default_model: str = ""
        self.model_directory: str = ""
        
        self._load_config()

    def _load_config(self) -> None:
        """Load model configurations from JSON file."""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
                self.models = config.get("models", {})
                self.default_model = config.get("default_model", "")
                self.model_directory = config.get("model_directory", "models")
                
            if not self.models:
                raise BotError("No models defined in configuration")
                
            logger.info(f"Loaded {len(self.models)} model configurations")
            
        except FileNotFoundError:
            raise BotError(f"Model configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise BotError(f"Invalid model configuration JSON: {str(e)}")
        except Exception as e:
            raise BotError(f"Error loading model configuration: {str(e)}")

    def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration for a specific model."""
        model_name = model_name or self.default_model
        
        if not model_name:
            raise BotError("No model name provided and no default model set")
            
        if model_name not in self.models:
            raise BotError(f"Model not found: {model_name}")
            
        return self.models[model_name]

    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """Get list of all available models."""
        return self.models

    def get_model_directory(self) -> str:
        """Get the directory where model files are stored."""
        return self.model_directory

    def validate_model_config(self, config: Dict[str, Any]) -> bool:
        """Validate a model configuration."""
        required_fields = ["name", "type", "version", "checkpoint"]
        return all(field in config for field in required_fields)

    def add_model(self, model_name: str, config: Dict[str, Any]) -> None:
        """Add a new model configuration."""
        if not self.validate_model_config(config):
            raise BotError("Invalid model configuration")
            
        self.models[model_name] = config
        self._save_config()

    def remove_model(self, model_name: str) -> None:
        """Remove a model configuration."""
        if model_name not in self.models:
            raise BotError(f"Model not found: {model_name}")
            
        del self.models[model_name]
        self._save_config()

    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            config = {
                "models": self.models,
                "default_model": self.default_model,
                "model_directory": self.model_directory
            }
            
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
                
            logger.info("Saved model configuration")
            
        except Exception as e:
            raise BotError(f"Error saving model configuration: {str(e)}")
