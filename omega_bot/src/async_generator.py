import aiohttp
import asyncio
from .config_loader import ConfigLoader
from .exceptions import ImageGenerationError

class AsyncImageGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.config = ConfigLoader().config
        self.base_url = "https://api.openai.com/v1/images/generations"

    async def generate_batch(self, prompts: list[str]) -> list[str]:
        async with aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }) as session:
            tasks = [self._generate_single(session, p) for p in prompts]
            return await asyncio.gather(*tasks)

    async def _generate_single(self, session: aiohttp.ClientSession, prompt: str) -> str:
        params = {
            "model": self.config["model"],
            "prompt": prompt,
            "size": self.config["size"],
            "quality": self.config["quality"],
            "n": 1
        }

        for attempt in range(self.config["max_retries"]):
            try:
                async with session.post(self.base_url, json=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data["data"][0]["url"]
            except Exception as e:
                if attempt == self.config["max_retries"] - 1:
                    raise ImageGenerationError(f"Async failed after {self.config['max_retries']} attempts: {str(e)}")
                await asyncio.sleep(self.config["retry_delay"] * (2 ** attempt))
