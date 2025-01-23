import pytest
from unittest.mock import Mock
from src.image_generator import ImageGenerator
from src.exceptions import ImageGenerationError

@pytest.fixture
def mock_client(monkeypatch):
    mock = Mock()
    monkeypatch.setattr("openai.OpenAI", lambda api_key: mock)
    return mock

def test_invalid_prompt_length():
    generator = ImageGenerator("fake-key")
    with pytest.raises(ImageGenerationError):
        generator.generate_image("a" * 4001)
