"""Image generation agent for NAGRO 4.1 — self-built procedural engine, no external models."""

from __future__ import annotations
from typing import AsyncIterator

from nagro.agents.base import BaseAgent


class ImageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "image",
            "You are NAGRO 4.1's image generation specialist. "
            "You generate images using NAGRO's own procedural engine. "
            "No Stable Diffusion, no DALL-E — everything is self-built."
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
                f"**Resolution:** {result['width']}x{result['height']}\n"
                f"**Engine:** NAGRO 4.1 Procedural (self-built)\n\n"
                f"*Generated using NAGRO's own procedural image engine. No external AI models.*"
            )

        error = result.get("error", "Unknown error")
        return (
            f"**NAGRO 4.1 — Image Generation**\n\n"
            f"**Prompt:** {message}\n\n"
            f"Error: {error}\n\n"
            f"Make sure Pillow is installed: `pip install Pillow`"
        )

    def _generate_image(self, prompt: str) -> dict:
        try:
            from nagro.core.image_engine import generate_image
            return generate_image(prompt=prompt)
        except ImportError:
            return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}
        except Exception as e:
            return {"success": False, "error": str(e)}
