import os
from datetime import datetime
from typing import Dict, Optional, List

class ModelInfo:
    def __init__(self, name: str, model_id: str, description: str, civitai_url: str = None):
        self.name = name
        self.model_id = model_id
        self.description = description
        self.civitai_url = civitai_url
        self.default_positive_prompt = "highly detailed, high quality"
        self.default_negative_prompt = "low quality, ugly, deformed"

class GenerationSettings:
    def __init__(self):
        self.steps = int(os.getenv("NUM_INFERENCE_STEPS", "30"))
        self.cfg_scale = float(os.getenv("GUIDANCE_SCALE", "7.5"))
        self.width = int(os.getenv("IMAGE_SIZE", "512"))
        self.height = int(os.getenv("IMAGE_SIZE", "512"))
        self.sampler = os.getenv("DEFAULT_SAMPLER", "DPM++ 2M Karras")
        self.safety_checker = os.getenv("SAFETY_CHECKER", "false").lower() == "true"

class UserSettings:
    def __init__(self, preferred_model: str, preferred_settings: GenerationSettings,
                 lora_weights: Dict[str, float], nsfw_enabled: bool):
        self.preferred_model = preferred_model
        self.preferred_settings = preferred_settings
        self.lora_weights = lora_weights
        self.nsfw_enabled = nsfw_enabled

class BotConfig:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    MODELS_DIR = os.getenv("MODELS_DIR", "/models")
    TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/omega_bot")
    DEFAULT_MODEL = "flux"
    MAX_DAILY_GENERATIONS = int(os.getenv("MAX_DAILY_GENERATIONS", "50"))

    @staticmethod
    def is_user_allowed(user_id: int) -> bool:
        allowed_users = os.getenv("ALLOWED_USERS", "").split(",")
        return not allowed_users or str(user_id) in allowed_users

AVAILABLE_MODELS = {
    "flux": ModelInfo(
        name="FLUX - Dev",
        model_id="flux",
        description="Advanced model for realistic generations",
        civitai_url="https://civitai.com/api/download/models/flux"
    ),
    # Additional models can be added here
}

# Last Updated: 2025-01-22 19:35:43
# Created By: Omega-Open-AI

# Modal Configuration
import modal
from pathlib import Path
import os
from .bot import OmegaBot
from .config import BotConfig

stub = modal.Stub("omega-image-bot")

image = (
    modal.Image.debian_slim()
    .pip_install(
        "python-telegram-bot",
        "diffusers",
        "transformers",
        "torch",
        "accelerate"
    )
    .pip_install_from_requirements("requirements.txt")
)

@stub.function(
    image=image,
    gpu="A10G",
    timeout=600,
    secret=modal.Secret.from_name("omega-bot-secrets")
)
def run_bot():
    """Run the Telegram bot in the cloud."""
    bot = OmegaBot()
    bot.run()

@stub.local_entrypoint()
def main():
    """Local development entrypoint."""
    if not os.getenv("TELEGRAM_TOKEN"):
        raise ValueError("TELEGRAM_TOKEN environment variable not set")
    run_bot.remote()

# Last Updated: 2025-01-22 19:51:41
# Created By: Omega-Open-AI
