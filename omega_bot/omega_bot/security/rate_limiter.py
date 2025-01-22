"""
Rate Limiter Module
Handles request rate limiting for the bot.

Author: Omega-Open-AI
Date: 2025-01-22
"""

import time
from typing import Dict, Tuple
from collections import defaultdict

from omega_bot.data.settings_manager import SettingsManager
from omega_bot.utils.error_handler import BotError

class RateLimiter:
    """Rate limiter implementation for controlling request frequency."""

    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the rate limiter with configuration."""
        self.settings = SettingsManager(config_path)
        
        # Load rate limit settings
        self.max_requests_per_minute = self.settings.get("rate_limit.max_requests_per_minute", 5)
        self.max_requests_per_day = self.settings.get("rate_limit.max_requests_per_day", 50)
        self.cooldown_period = self.settings.get("rate_limit.cooldown_period", 3600)  # 1 hour in seconds
        
        # Initialize tracking dictionaries
        self._minute_tracking: Dict[int, Tuple[int, float]] = defaultdict(lambda: (0, time.time()))
        self._daily_tracking: Dict[int, Tuple[int, float]] = defaultdict(lambda: (0, time.time()))
        self._cooldowns: Dict[int, float] = {}

    def can_process(self, user_id: int) -> bool:
        """Check if a user can make a request."""
        current_time = time.time()
        
        # Check if user is in cooldown
        if user_id in self._cooldowns:
            if current_time < self._cooldowns[user_id]:
                return False
            else:
                del self._cooldowns[user_id]
        
        # Check minute limit
        minute_count, minute_start = self._minute_tracking[user_id]
        if current_time - minute_start >= 60:
            # Reset minute counter if more than a minute has passed
            self._minute_tracking[user_id] = (1, current_time)
        else:
            if minute_count >= self.max_requests_per_minute:
                self._add_cooldown(user_id)
                return False
            self._minute_tracking[user_id] = (minute_count + 1, minute_start)
        
        # Check daily limit
        daily_count, daily_start = self._daily_tracking[user_id]
        if current_time - daily_start >= 86400:  # 24 hours in seconds
            # Reset daily counter if more than a day has passed
            self._daily_tracking[user_id] = (1, current_time)
        else:
            if daily_count >= self.max_requests_per_day:
                self._add_cooldown(user_id)
                return False
            self._daily_tracking[user_id] = (daily_count + 1, daily_start)
        
        return True

    def _add_cooldown(self, user_id: int) -> None:
        """Add a user to cooldown."""
        self._cooldowns[user_id] = time.time() + self.cooldown_period

    def get_limits(self) -> Dict[str, int]:
        """Get current rate limit settings."""
        return {
            "per_minute": self.max_requests_per_minute,
            "per_day": self.max_requests_per_day,
            "cooldown_period": self.cooldown_period
        }

    def reset_user(self, user_id: int) -> None:
        """Reset rate limits for a specific user."""
        if user_id in self._minute_tracking:
            del self._minute_tracking[user_id]
        if user_id in self._daily_tracking:
            del self._daily_tracking[user_id]
        if user_id in self._cooldowns:
            del self._cooldowns[user_id]
