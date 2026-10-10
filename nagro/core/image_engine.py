"""
NAGRO 4.1 — Self-Built Image Generation Engine

No Stable Diffusion. No DALL-E. No external AI models.
Generates images procedurally using NAGRO's own algorithms.
Uses only Pillow (PIL) — pure Python image processing.
"""

from __future__ import annotations
import math
import random
import hashlib
import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime

from nagro.core.config import settings


def _seed_from_prompt(prompt: str) -> int:
    return int(hashlib.md5(prompt.encode()).hexdigest()[:8], 16)


def generate_image(
    prompt: str,
    negative_prompt: str = "",
    width: int | None = None,
    height: int | None = None,
    steps: int | None = None,
    guidance_scale: float = 0.0,
    seed: int | None = None,
) -> dict:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
    except ImportError:
        return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}

    w = width or settings.nagro_image_width
    h = height or settings.nagro_image_height
    s = seed if seed is not None else _seed_from_prompt(prompt)
    rng = random.Random(s)

    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)

    prompt_lower = prompt.lower()

    warm = any(k in prompt_lower for k in ["fire", "sun", "warm", "red", "orange", "hot", "flame", "sunset"])
    cool = any(k in prompt_lower for k in ["ice", "cold", "water", "blue", "ocean", "sky", "cool", "sea"])
    nature = any(k in prompt_lower for k in ["nature", "forest", "tree", "green", "garden", "leaf", "mountain"])
    dark = any(k in prompt_lower for k in ["dark", "night", "black", "shadow", "space", "galaxy", "stars"])
    neon = any(k in prompt_lower for k in ["neon", "cyber", "cyberpunk", "glow", "electric", "futuristic"])

    if warm:
        palette = [(255, 69, 0), (255, 140, 0), (255, 215, 0), (220, 20, 60), (255, 99, 71)]
    elif cool:
        palette = [(0, 105, 148), (0, 150, 199), (77, 195, 255), (0, 191, 255), (135, 206, 250)]
    elif nature:
        palette = [(34, 139, 34), (0, 128, 0), (60, 179, 113), (46, 139, 87), (144, 238, 144)]
    elif dark:
        palette = [(20, 20, 40), (40, 20, 60), (60, 20, 80), (80, 40, 120), (100, 50, 150)]
    elif neon:
        palette = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 100)]
    else:
        palette = [(rng.randint(50, 255), rng.randint(50, 255), rng.randint(50, 255)) for _ in range(5)]

    bg1, bg2 = palette[0], palette[1]
    for y in range(h):
        r = int(bg1[0] + (bg2[0] - bg1[0]) * y / h)
        g = int(bg1[1] + (bg2[1] - bg1[1]) * y / h)
        b = int(bg1[2] + (bg2[2] - bg1[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    for _ in range(rng.randint(15, 40)):
        shape = rng.choice(["circle", "rect", "line", "triangle", "diamond"])
        color = rng.choice(palette)
        alpha_color = color + (rng.randint(80, 200),)

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        cx, cy = rng.randint(0, w), rng.randint(0, h)
        size = rng.randint(20, min(w, h) // 3)

        if shape == "circle":
            odraw.ellipse([cx - size, cy - size, cx + size, cy + size], fill=alpha_color, outline=color)
        elif shape == "rect":
            odraw.rectangle([cx - size, cy - size // 2, cx + size, cy + size // 2], fill=alpha_color, outline=color)
        elif shape == "line":
            x2, y2 = cx + rng.randint(-200, 200), cy + rng.randint(-200, 200)
            odraw.line([(cx, cy), (x2, y2)], fill=color, width=rng.randint(2, 6))
        elif shape == "triangle":
            pts = [(cx, cy - size), (cx - size, cy + size), (cx + size, cy + size)]
            odraw.polygon(pts, fill=alpha_color, outline=color)
        elif shape == "diamond":
            pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
            odraw.polygon(pts, fill=alpha_color, outline=color)

        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    for _ in range(rng.randint(5, 12)):
        points = [(rng.randint(0, w), rng.randint(0, h)) for _ in range(rng.randint(3, 6))]
        draw.line(points, fill=rng.choice(palette), width=rng.randint(1, 3))

    try:
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
    except Exception:
        pass

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    draw.text((10, h - 20), "NAGRO 4.1", fill=(255, 255, 255), font=font)

    output_dir = Path("outputs/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nagro_{timestamp}_{s}.png"
    filepath = output_dir / filename
    img.save(str(filepath), "PNG")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "success": True,
        "base64": img_base64,
        "file_path": str(filepath),
        "width": w,
        "height": h,
        "prompt": prompt,
        "seed": s,
        "engine": "NAGRO 4.1 Procedural Engine",
    }


def is_image_model_loaded() -> bool:
    return True


def unload_image_model():
    pass
