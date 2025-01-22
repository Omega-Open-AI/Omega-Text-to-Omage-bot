import pytest
from pathlib import Path
from src.model_downloader import ModelDownloader, ModelError

@pytest.mark.asyncio
async def test_initialize_models(models_dir):
    """Test model directory initialization."""
    downloader = ModelDownloader(str(models_dir))
    assert models_dir.exists()
    assert (models_dir / "flux").exists()

@pytest.mark.asyncio
async def test_list_available_models(model_downloader):
    """Test listing available models."""
    models = await model_downloader.list_available_models()
    assert isinstance(models, list)
    assert "flux" in models

@pytest.mark.asyncio
async def test_get_model_path_nonexistent(model_downloader):
    """Test getting path of nonexistent model."""
    with pytest.raises(ModelError):
        await model_downloader.get_model_path("nonexistent_model")

# Last Updated: 2025-01-22 19:53:20
# Created By: Omega-Open-AI