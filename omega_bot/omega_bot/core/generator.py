"""
Image Generator Module
Handles image generation using Stable Diffusion models.

Author: Omega-Open-AI
Date: 2025-01-22
"""

import os
import logging
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

from omega_bot.data.settings_manager import SettingsManager
from omega_bot.utils.error_handler import BotError
from omega_bot.data.model_manager import ModelManager

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Handles image generation using various AI models."""

    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the image generator with configuration."""
        self.settings = SettingsManager(config_path)
        self.model_manager = ModelManager()
        
        # Load generation settings
        self.max_size = self.settings.get("generation.max_image_size", 1024)
        self.default_model = self.settings.get("generation.default_model", "stable-diffusion-v1.5")
        self.timeout = self.settings.get("generation.timeout", 300)
        
        # Initialize output directory
        self.output_dir = Path(self.settings.get("storage.output_dir", "output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize the pipeline
        self._pipeline = None

    async def _load_model(self, model_name: Optional[str] = None) -> None:
        """Load the Stable Diffusion model."""
        try:
            model_name = model_name or self.default_model
            model_info = self.model_manager.get_model_info(model_name)
            
            if not model_info:
                raise BotError(f"Model {model_name} not found in configuration")
            
            # Load model in a separate thread to avoid blocking
            def load_pipeline():
                return StableDiffusionPipeline.from_pretrained(
                    model_info["checkpoint"],
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    safety_checker=model_info.get("requires_safety_checker", True),
                )
            
            loop = asyncio.get_event_loop()
            self._pipeline = await loop.run_in_executor(None, load_pipeline)
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self._pipeline = self._pipeline.to("cuda")
                
            logger.info(f"Successfully loaded model: {model_name}")
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            raise BotError(f"Failed to load model: {str(e)}")

    async def generate(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate an image from the given prompt."""
        try:
            # Load model if not loaded or different model requested
            if self._pipeline is None or (model_name and model_name != self.default_model):
                await self._load_model(model_name)

            # Get model parameters
            model_info = self.model_manager.get_model_info(model_name or self.default_model)
            params = {**model_info["default_parameters"], **(parameters or {})}

            # Generate the image
            logger.info(f"Generating image for prompt: {prompt}")
            image = self._pipeline(
                prompt,
                num_inference_steps=params.get("num_inference_steps", 50),
                guidance_scale=params.get("guidance_scale", 7.5),
                negative_prompt=params.get("negative_prompt", ""),
                width=self.max_size,
                height=self.max_size,
            ).images[0]

            # Save the generated image
            output_path = self.output_dir / f"generated_{os.urandom(8).hex()}.png"
            image.save(output_path)
            logger.info(f"Image saved to: {output_path}")

            return str(output_path)

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise BotError(f"Image generation failed: {str(e)}")

    def __del__(self):
        """Cleanup resources."""
        if self._pipeline is not None and torch.cuda.is_available():
            try:
                self._pipeline = self._pipeline.to("cpu")
                torch.cuda.empty_cache()
            except Exception as e:
                logger.warning(f"Error cleaning up GPU resources: {str(e)}")
