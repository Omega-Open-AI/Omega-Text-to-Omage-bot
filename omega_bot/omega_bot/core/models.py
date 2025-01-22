import os
import logging
from pathlib import Path
import httpx
from tqdm import tqdm
from .error_handler import ModelError, handle_errors
from .config import BotConfig, AVAILABLE_MODELS

logger = logging.getLogger(__name__)

class ModelDownloader:
    def __init__(self, models_dir: str = BotConfig.MODELS_DIR):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self._initialize_models()

    def _initialize_models(self) -> None:
        """Create model directories if they don't exist."""
        for model_id in AVAILABLE_MODELS:
            (self.models_dir / model_id).mkdir(exist_ok=True)

    @handle_errors()
    async def download_model(self, model_id: str) -> Path:
        """Download a model from Civitai or other sources."""
        if model_id not in AVAILABLE_MODELS:
            raise ModelError(f"Unknown model: {model_id}")

        model_info = AVAILABLE_MODELS[model_id]
        model_path = self.models_dir / model_id / "model.safetensors"

        if model_path.exists():
            logger.info(f"Model {model_id} already exists")
            return model_path

        if not model_info.civitai_url:
            raise ModelError(f"No download URL for model: {model_id}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(model_info.civitai_url, follow_redirects=True)
                response.raise_for_status()
                
                total_size = int(response.headers.get("content-length", 0))
                with tqdm(total=total_size, unit="iB", unit_scale=True) as progress_bar:
                    with open(model_path, "wb") as f:
                        for data in response.iter_bytes():
                            f.write(data)
                            progress_bar.update(len(data))

            logger.info(f"Successfully downloaded model: {model_id}")
            return model_path

        except Exception as e:
            raise ModelError(f"Failed to download model {model_id}: {str(e)}")

    @handle_errors()
    async def get_model_path(self, model_id: str) -> Path:
        """Get the path to a downloaded model."""
        model_path = self.models_dir / model_id / "model.safetensors"
        if not model_path.exists():
            raise ModelError(f"Model not found: {model_id}")
        return model_path

    @handle_errors()
    async def list_available_models(self) -> list[str]:
        """List all available models."""
        return list(AVAILABLE_MODELS.keys())

# Last Updated: 2025-01-22 19:51:41
# Created By: Omega-Open-AI