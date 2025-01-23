import openai
import time
from typing import Optional
from .config_loader import ConfigLoader
from .exceptions import ImageGenerationError

class ImageGenerator:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.config = ConfigLoader().config

    def _validate_prompt(self, prompt: str):
        if len(prompt) > 4000:
            raise ImageGenerationError("Prompt exceeds 4000 character limit")
        if not prompt.strip():
            raise ImageGenerationError("Prompt cannot be empty")

    def generate_image(self, prompt: str, **kwargs) -> str:
        self._validate_prompt(prompt)
        
        params = {
            "model": kwargs.get("model") or self.config["model"],
            "size": kwargs.get("size") or self.config["size"],
            "quality": kwargs.get("quality") or self.config["quality"],
            "n": 1
        }

        for attempt in range(self.config["max_retries"]):
            try:
                response = self.client.images.generate(
                    prompt=prompt,
                    **params
                )
                return response.data[0].url
            except Exception as e:
                if attempt == self.config["max_retries"] - 1:
                    raise ImageGenerationError(f"Failed after {self.config['max_retries']} attempts: {str(e)}")
                delay = self.config["retry_delay"] * (2 ** attempt)
                time.sleep(delay)
