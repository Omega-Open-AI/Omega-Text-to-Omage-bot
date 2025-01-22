import pytest
from pathlib import Path
from src.image_generator import ImageGenerator, GenerationError
from src.config import GenerationSettings

@pytest.mark.asyncio
async def test_device_selection(image_generator):
    """Test device selection logic."""
    assert image_generator.device in ["cuda", "cpu"]

@pytest.mark.asyncio
async def test_generate_image_invalid_model(image_generator):
    """Test generation with invalid model."""
    with pytest.raises(GenerationError):
        await image_generator.generate_image(
            prompt="test prompt",
            model_id="nonexistent_model"
        )

@pytest.mark.asyncio
async def test_get_model_info(image_generator):
    """Test getting model information."""
    with pytest.raises(GenerationError):
        await image_generator.get_model_info("nonexistent_model")

# Last Updated: 2025-01-22 19:53:20
# Created By: Omega-Open-AI