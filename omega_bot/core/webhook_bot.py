"""
Webhook-based implementation of the Omega Text to Image Bot.
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from omega_bot.core.bot import OmegaBot
from omega_bot.modal.metrics import (
    GENERATION_TIME,
    GENERATION_FAILURES,
    RATE_LIMITS_HIT
)

logger = logging.getLogger(__name__)

class OmegaWebhookBot(OmegaBot):
    """Webhook-based implementation of the Omega bot."""

    async def setup_webhook(self) -> Application:
        """Set up the webhook application."""
        try:
            # Create application
            application = Application.builder().token(self.token).build()
            
            # Add command handlers
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("generate", self.generate_image))
            
            return application

        except Exception as e:
            logger.error(f"Failed to set up webhook: {str(e)}")
            raise

    async def generate_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Override generate_image to include metrics."""
        try:
            if not self.rate_limiter.can_process(update.effective_user.id):
                RATE_LIMITS_HIT.inc()
                await update.message.reply_text(
                    "🚫 Rate limit exceeded. Please try again later."
                )
                return

            with GENERATION_TIME.time():
                await super().generate_image(update, context)

        except Exception as e:
            GENERATION_FAILURES.inc()
            logger.error(f"Error generating image: {str(e)}")
            await update.message.reply_text(
                "❌ An error occurred while generating the image. Please try again later."
            )

    async def run_webhook(self, update_data: dict) -> None:
        """Process a webhook update."""
        try:
            application = await self.setup_webhook()
            update = Update.de_json(update_data, application.bot)
            await application.process_update(update)
        except Exception as e:
            logger.error(f"Error processing webhook update: {str(e)}")
            raise
