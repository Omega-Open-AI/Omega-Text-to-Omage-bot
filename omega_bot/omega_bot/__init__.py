"""
Omega Text to Image Bot
A Telegram bot for generating images from text descriptions using AI models.
"""

from omega_bot.core.bot import OmegaBot
from omega_bot.core.generator import ImageGenerator
from omega_bot.core.models import ModelDownloader
from omega_bot.data.settings_manager import SettingsManager
from omega_bot.security.rate_limiter import RateLimiter
from omega_bot.utils.error_handler import BotError

__version__ = "1.0.0"
__author__ = "Omega-Open-AI"
__license__ = "MIT"

# Export main classes for easier imports
__all__ = [
    "OmegaBot",
    "ImageGenerator",
    "ModelDownloader",
    "SettingsManager",
    "RateLimiter",
    "BotError"
]
