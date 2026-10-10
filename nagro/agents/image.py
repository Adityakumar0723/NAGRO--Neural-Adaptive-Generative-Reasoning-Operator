"""Image generation agent for NAGRO 4.1 — local Stable Diffusion, no APIs."""

from __future__ import annotations
from typing import AsyncIterator

from nagro.agents.base import BaseAgent


class ImageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "image",
            "You are NAGRO 4.1's image generation specialist. "
            "You generate images locally using Stable Diffusion. "
            "No external APIs needed — everything runs on the user's machine."
        )

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:
        result = self._generate_image(message)

        if result.get("success"):
            return (
                f"**NAGRO 4.1 — Image Generated Successfully**\n\n"
                f"**Prompt:** {message}\n\n"
                f"**Saved to:** `{result['file_path']}`\n"
                f"**Resolution:** {result['width']}x{result['height']}\n\n"
                f"![Generated Image](data:image/png;base64,{result['base64'][:100]}...)\n\n"
                f"*Generated locally using Stable Diffusion. No external APIs used.*"
            )

        error = result.get("error", "Unknown error")
        return await self._text_fallback(message, history, error)

    async def _text_fallback(
        self,
        message: str,
        history: list[dict[str, str]],
        error: str,
    ) -> str:
        """When image model isn't available, provide a detailed text description."""
        enhanced = (
            f"The user wants to generate an image but the image model is not loaded.\n"
            f"Error: {error}\n\n"
            f"User's request: {message}\n\n"
            f"Provide:\n"
            f"1. An enhanced, detailed prompt for image generation\n"
            f"2. A vivid text description of what the image would look like\n"
            f"3. Suggestions for style, lighting, composition\n"
            f"4. Instructions to set up image generation:\n"
            f"   - Run: pip install diffusers torch\n"
            f"   - The image model will auto-download on first use (~2 GB)"
        )
        messages = history + [{"role": "user", "content": enhanced}]
        try:
            return self._generate(messages)
        except FileNotFoundError:
            return (
                f"**NAGRO 4.1 — Image Generation Setup Needed**\n\n"
                f"**Your Prompt:** {message}\n\n"
                f"To generate images locally, install PyTorch and Diffusers:\n"
                f"```bash\n"
                f"pip install torch diffusers transformers accelerate\n"
                f"```\n\n"
                f"The image model (~2 GB) will download automatically on first use.\n"
                f"Everything runs on your machine — no API keys needed."
            )

    def _generate_image(self, prompt: str) -> dict:
        """Generate image using local Stable Diffusion."""
        try:
            from nagro.core.image_engine import generate_image
            return generate_image(prompt=prompt)
        except ImportError:
            return {
                "success": False,
                "error": "Image dependencies not installed. Run: pip install torch diffusers transformers accelerate",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
