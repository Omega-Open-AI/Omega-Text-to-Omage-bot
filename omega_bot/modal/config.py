"""
Modal configuration settings for the Omega Text to Image Bot.
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModalConfig:
    """Configuration settings for Modal deployment."""
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    GPU_TYPE: str = os.getenv("GPU_TYPE", "T4")
    MEMORY_LIMIT: int = int(os.getenv("MEMORY_LIMIT", "4096"))
    VOLUME_NAME: str = "omega-bot-storage"
    SECRETS_NAME: str = "omega-bot-secrets"
    APP_NAME: str = "omega-text-to-image-bot"

    @property
    def webhook_path(self) -> str:
        """Get the full webhook path."""
        return f"{self.WEBHOOK_URL}/webhook"

    def validate(self) -> None:
        """Validate the configuration."""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        if not self.WEBHOOK_URL:
            raise ValueError("WEBHOOK_URL environment variable is required")
