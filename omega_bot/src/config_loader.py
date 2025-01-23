import os
import yaml
from typing import Dict, Any
from .exceptions import ConfigurationError

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config['defaults']
        except FileNotFoundError:
            raise ConfigurationError(f"Config file not found at {self.config_path}")
        except Exception as e:
            raise ConfigurationError(f"Error loading config: {str(e)}")
