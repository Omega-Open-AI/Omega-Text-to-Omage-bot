import pytest
from unittest.mock import MagicMock, AsyncMock
from telegram import Update, User, Message, Chat
from telegram.ext import ContextTypes
from src.bot import OmegaBot

@pytest.fixture
def mock_update():
    """Create a mock Telegram update."""
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 123
    update.effective_user.first_name = "Test User"
    update.message = MagicMock(spec=Message)
    update.message.chat = MagicMock(spec=Chat)
    update.message.reply_text = AsyncMock()
    update.message.reply_photo = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    """Create a mock context."""
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []
    return context

@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    """Test the start command."""
    bot = OmegaBot()
    await bot.start(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "Hi Test User!" in call_args
    assert "/generate" in call_args

@pytest.mark.asyncio
async def test_generate_command_no_prompt(mock_update, mock_context):
    """Test generate command without prompt."""
    bot = OmegaBot()
    await bot.generate(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once_with(
        "Please provide a prompt!"
    )

# Last Updated: 2025-01-22 19:53:20
# Created By: Omega-Open-AI