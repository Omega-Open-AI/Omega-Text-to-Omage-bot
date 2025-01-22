import pytest
from src.settings_manager import SettingsManager
from src.error_handler import ConfigError

@pytest.mark.asyncio
async def test_get_empty_settings(settings_manager):
    """Test getting settings for new user."""
    settings = await settings_manager.get_user_settings(123)
    assert isinstance(settings, dict)
    assert len(settings) == 0

@pytest.mark.asyncio
async def test_update_and_get_settings(settings_manager):
    """Test updating and retrieving user settings."""
    test_settings = {"preferred_model": "flux", "steps": 30}
    await settings_manager.update_user_settings(123, test_settings)
    
    settings = await settings_manager.get_user_settings(123)
    assert settings == test_settings

@pytest.mark.asyncio
async def test_get_preference(settings_manager):
    """Test getting specific preference."""
    test_settings = {"preferred_model": "flux"}
    await settings_manager.update_user_settings(123, test_settings)
    
    value = await settings_manager.get_user_preference(123, "preferred_model")
    assert value == "flux"

# Last Updated: 2025-01-22 19:53:20
# Created By: Omega-Open-AI