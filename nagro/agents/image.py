"""Image generation agent for NAGRO 4.1."""

from __future__ import annotations
from typing import Any, AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.config import settings


class ImageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "image",
            "You are NAGRO 4.1's image generation specialist. "
            "Help users create stunning visuals by refining their prompts "
            "and generating high-quality images."
        )

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        image_result = await self._generate_image(message)
        if image_result.get("success"):
            urls = image_result["urls"]
            url_list = "\n".join(f"- {url}" for url in urls)
            response = (
                f"🎨 **NAGRO 4.1 - Image Generated Successfully**\n\n"
                f"**Prompt:** {message}\n\n"
                f"**Generated Images:**\n{url_list}\n\n"
            )
            if image_result.get("revised_prompt"):
                response += f"**Enhanced Prompt:** {image_result['revised_prompt']}\n"
            return response

        return await self._text_response(message, history, llm_client, llm_type)

    async def _text_response(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        enhanced = (
            f"The user wants to generate an image. "
            f"No image API is configured, so help them refine their prompt "
            f"and explain what the image would look like.\n\n"
            f"User's request: {message}\n\n"
            f"Provide:\n"
            f"1. An enhanced, detailed prompt for image generation\n"
            f"2. A vivid text description of what the image would look like\n"
            f"3. Suggestions for style, lighting, composition\n"
            f"4. Note that they need to configure an image API key to generate actual images"
        )
        messages = history + [{"role": "user", "content": enhanced}]
        return await self._call_llm(llm_client, llm_type, messages)

    async def _generate_image(self, prompt: str) -> dict:
        provider = settings.nagro_image_provider

        if provider == "openai" and settings.openai_api_key:
            return await self._generate_openai(prompt)
        elif provider == "stability" and settings.stability_api_key:
            return await self._generate_stability(prompt)
        elif provider == "replicate" and settings.replicate_api_key:
            return await self._generate_replicate(prompt)

        return {"success": False, "error": "No image generation API configured"}

    async def _generate_openai(self, prompt: str) -> dict:
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return {
                "success": True,
                "urls": [img.url for img in response.data],
                "revised_prompt": response.data[0].revised_prompt,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _generate_stability(self, prompt: str) -> dict:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers={
                        "Authorization": f"Bearer {settings.stability_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "text_prompts": [{"text": prompt, "weight": 1}],
                        "cfg_scale": 7,
                        "height": 1024,
                        "width": 1024,
                        "steps": 30,
                        "samples": 1,
                    },
                )
                response.raise_for_status()
                data = response.json()
                images = data.get("artifacts", [])
                return {
                    "success": True,
                    "urls": [f"data:image/png;base64,{img['base64']}" for img in images],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _generate_replicate(self, prompt: str) -> dict:
        try:
            import replicate
            output = await replicate.async_run(
                "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
                input={"prompt": prompt, "width": 1024, "height": 1024},
            )
            urls = list(output) if output else []
            return {"success": True, "urls": urls}
        except Exception as e:
            return {"success": False, "error": str(e)}
