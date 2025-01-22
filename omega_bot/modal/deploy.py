"""
Modal deployment configuration for Omega Text to Image Bot.
"""

import json
from modal import Image, Secret, Stub, Volume, web_endpoint, asgi_app
from prometheus_client import make_asgi_app

from .config import ModalConfig
from .metrics import (
    TOTAL_REQUESTS,
    FAILED_REQUESTS,
    GENERATION_TIME,
    MEMORY_USAGE
)

# Initialize configuration
config = ModalConfig()
config.validate()

# Create Modal stub
stub = Stub(config.APP_NAME)

# Create persistent volume
volume = Volume.persisted(config.VOLUME_NAME)

# Create base image
def create_base_image():
    return (
        Image.debian_slim()
        .pip_install([
            "python-telegram-bot>=20.0",
            "diffusers>=0.24.0",
            "transformers>=4.36.0",
            "torch>=2.1.0",
            "Pillow>=10.0.0",
            "PyYAML>=6.0",
            "python-dotenv>=1.0.0",
            "tqdm>=4.66.0",
            "requests>=2.31.0",
            "numpy>=1.24.0",
            "prometheus-client>=0.17.0"
        ])
    )

image = create_base_image()

@stub.function(
    image=image,
    secret=Secret.from_name(config.SECRETS_NAME),
    gpu=config.GPU_TYPE,
    volume=volume,
    memory=config.MEMORY_LIMIT
)
@web_endpoint(method="POST")
async def webhook_handler(raw_body: bytes):
    """Handle webhook requests from Telegram."""
    try:
        TOTAL_REQUESTS.inc()
        with GENERATION_TIME.time():
            from omega_bot.core.webhook_bot import OmegaWebhookBot
            
            # Parse the update
            update_data = json.loads(raw_body)
            
            # Initialize and run bot
            bot = OmegaWebhookBot()
            await bot.run_webhook(update_data)
            
            return {"status": "success"}
    except Exception as e:
        FAILED_REQUESTS.inc()
        raise e

@stub.function(image=image)
@asgi_app()
def metrics():
    """Expose Prometheus metrics."""
    return make_asgi_app()

@stub.function(image=image)
@web_endpoint(method="GET")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
