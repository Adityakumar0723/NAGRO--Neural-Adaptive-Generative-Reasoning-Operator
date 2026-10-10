"""NAGRO 4.1 Local Image Generation Engine — Stable Diffusion on your machine."""

from __future__ import annotations
import io
import base64
import threading
from pathlib import Path

from nagro.core.config import settings

_lock = threading.Lock()
_pipeline = None


def _get_pipeline():
    """Lazy-load the image generation pipeline (singleton)."""
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    with _lock:
        if _pipeline is not None:
            return _pipeline

        import torch
        from diffusers import AutoPipelineForText2Image

        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32

        _pipeline = AutoPipelineForText2Image.from_pretrained(
            settings.nagro_image_model,
            torch_dtype=dtype,
            variant="fp16" if device == "cuda" else None,
        )
        _pipeline = _pipeline.to(device)

        return _pipeline


def generate_image(
    prompt: str,
    negative_prompt: str = "",
    width: int | None = None,
    height: int | None = None,
    steps: int | None = None,
    guidance_scale: float = 0.0,
    seed: int | None = None,
) -> dict:
    """Generate an image from text using local Stable Diffusion."""
    try:
        import torch
        pipe = _get_pipeline()

        width = width or settings.nagro_image_width
        height = height or settings.nagro_image_height
        steps = steps or settings.nagro_image_steps

        generator = None
        if seed is not None:
            generator = torch.Generator(device=pipe.device).manual_seed(seed)

        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt or None,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]

        # Save to output directory
        output_dir = Path("outputs/images")
        output_dir.mkdir(parents=True, exist_ok=True)

        import time
        filename = f"nagro_{int(time.time())}.png"
        filepath = output_dir / filename
        image.save(filepath)

        # Also return base64
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode()

        return {
            "success": True,
            "file_path": str(filepath),
            "base64": b64,
            "width": width,
            "height": height,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def is_image_model_loaded() -> bool:
    """Check if image model is loaded."""
    return _pipeline is not None


def unload_image_model():
    """Unload image model to free VRAM/RAM."""
    global _pipeline
    with _lock:
        if _pipeline is not None:
            del _pipeline
            _pipeline = None
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
