"""
Omega Text to Image Bot
Core bot implementation for handling Telegram interactions and image generation.

Author: Omega-Open-AI
Date: 2025-01-22
"""

import logging
import os
from typing import Optional, Dict, Any

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from omega_bot.core.generator import ImageGenerator
from omega_bot.data.settings_manager import SettingsManager
from omega_bot.security.rate_limiter import RateLimiter
from omega_bot.utils.error_handler import BotError

logger = logging.getLogger(__name__)

class OmegaBot:
    """Main bot class for handling Telegram commands and image generation."""

    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the bot with configuration."""
        self.settings = SettingsManager(config_path)
        self.generator = ImageGenerator()
        self.rate_limiter = RateLimiter()
        
        # Initialize bot token from environment or config
        self.token = os.getenv("BOT_TOKEN") or self.settings.get("bot.token")
        if not self.token:
            raise BotError("Bot token not found in environment or config")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command."""
        user = update.effective_user
        welcome_message = (
            f"?? Hi {user.first_name}!\n\n"
            "I'm Omega, your AI Image Generation Bot. ??\n"
            "Send me a text description, and I'll create an image for you.\n\n"
            "Commands:\n"
            "/generate <description> - Generate an image\n"
            "/settings - View current settings\n"
            "/help - Show help message"
        )
        await update.message.reply_text(welcome_message)

    async def generate_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /generate command."""
        try:
            # Check rate limit
            if not self.rate_limiter.can_process(update.effective_user.id):
                await update.message.reply_text(
                    "?? Rate limit exceeded. Please try again later."
                )
                return

            # Get the prompt from the command
            prompt = " ".join(context.args)
            if not prompt:
                await update.message.reply_text(
                    "Please provide a description for the image.\n"
                    "Example: /generate a beautiful sunset over mountains"
                )
                return

            # Send processing message
            processing_message = await update.message.reply_text(
                "?? Generating your image... Please wait."
            )

            # Generate the image
            image_path = await self.generator.generate(prompt)

            # Send the generated image
            with open(image_path, "rb") as image:
                await update.message.reply_photo(
                    photo=image,
                    caption=f"?? Generated image for: {prompt}"
                )

            # Clean up
            os.remove(image_path)
            await processing_message.delete()

        except BotError as e:
            await update.message.reply_text(f"Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            await update.message.reply_text(
                "? An error occurred while generating the image. Please try again later."
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command."""
        help_text = (
            "?? Omega Bot Help\n\n"
            "Commands:\n"
            "/start - Start the bot\n"
            "/generate <description> - Generate an image from text\n"
            "/settings - View current settings\n"
            "/help - Show this help message\n\n"
            "Tips:\n"
            "- Be descriptive in your prompts\n"
            "- Images are generated in 1024x1024 resolution\n"
            "- Generation usually takes 10-30 seconds\n"
            "- Daily limits apply to ensure fair usage"
        )
        await update.message.reply_text(help_text)

    def run(self) -> None:
        """Run the bot."""
        try:
            # Create application and add handlers
            application = Application.builder().token(self.token).build()
            
            # Add command handlers
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("generate", self.generate_image))
            
            # Start the bot
            logger.info("Starting Omega Bot...")
            application.run_polling()

        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            raise BotError(f"Bot startup failed: {str(e)}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create and run the bot
    bot = OmegaBot()
    bot.run()
