# omega_bot/data/settings_manager.py
from typing import Dict, Any, Optional
import json
from pathlib import Path
import aiofiles
from ..utils.error_handler import BotError
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SettingsManager:
    def __init__(self, settings_file: str = "config/settings.json"):
        self.settings_file = Path(settings_file)
        self.settings: Dict[str, Dict[str, Any]] = {}
        self._ensure_settings_file()
        
    def _ensure_settings_file(self):
        """Ensure settings file exists with default values."""
        if not self.settings_file.exists():
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            default_settings = {
                "telegram_token": "",
                "default_model": "flux",
                "generation_defaults": {
                    "steps": 30,
                    "cfg_scale": 7.5,
                    "width": 512,
                    "height": 512
                }
            }
            with open(self.settings_file, 'w') as f:
                json.dump(default_settings, f, indent=4)
                
    async def get_telegram_token(self) -> str:
        """Get Telegram bot token."""
        async with aiofiles.open(self.settings_file, 'r') as f:
            settings = json.loads(await f.read())
        return settings.get("telegram_token", "")
        
    async def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Get settings for a specific user."""
        try:
            async with aiofiles.open(self.settings_file, 'r') as f:
                all_settings = json.loads(await f.read())
                
            user_settings = all_settings.get("users", {}).get(str(user_id), {})
            return {
                **all_settings["generation_defaults"],
                **user_settings
            }
            
        except Exception as e:
            logger.error(f"Error reading user settings: {str(e)}")
            raise BotError(f"Failed to read settings: {str(e)}")
            
    async def update_user_settings(
        self,
        user_id: int,
        settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update settings for a specific user."""
        try:
            async with aiofiles.open(self.settings_file, 'r') as f:
                all_settings = json.loads(await f.read())
                
            if "users" not in all_settings:
                all_settings["users"] = {}
                
            all_settings["users"][str(user_id)] = settings
            
            async with aiofiles.open(self.settings_file, 'w') as f:
                await f.write(json.dumps(all_settings, indent=4))
                
            return settings
            
        except Exception as e:
            logger.error(f"Error updating user settings: {str(e)}")
            raise BotError(f"Failed to update settings: {str(e)}")
