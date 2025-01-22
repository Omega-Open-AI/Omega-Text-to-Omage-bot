import pytest
from pathlib import Path
import shutil
from src.config import BotConfig
from src.model_downloader import ModelDownloader
from src.image_generator import ImageGenerator
from src.settings_manager import SettingsManager

@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for tests."""
    yield tmp_path
    # Cleanup after tests
    if tmp_path.exists():
        shutil.rmtree(tmp_path)

@pytest.fixture
def models_dir(temp_dir):
    """Create a temporary models directory."""
    models_dir = temp_dir / "models"
    models_dir.mkdir()
    return models_dir

@pytest.fixture
def model_downloader(models_dir):
    """Provide a ModelDownloader instance."""
    return ModelDownloader(str(models_dir))

@pytest.fixture
def image_generator(model_downloader):
    """Provide an ImageGenerator instance."""
    return ImageGenerator(model_downloader)

@pytest.fixture
def settings_manager(temp_dir):
    """Provide a SettingsManager instance."""
    settings_file = temp_dir / "settings.json"
    return SettingsManager(str(settings_file))

# Last Updated: 2025-01-22 19:53:20
# Created By: Omega-Open-AI