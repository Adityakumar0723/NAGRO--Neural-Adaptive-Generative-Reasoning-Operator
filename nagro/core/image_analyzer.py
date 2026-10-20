"""
NAGRO 4.1 — Self-Built Image Analyzer
No external AI APIs. Uses Pillow (PIL) for image analysis.
Analyzes: colors, dimensions, brightness, contrast, patterns, composition.
"""
from __future__ import annotations
import base64
import math
from io import BytesIO
from collections import Counter


def analyze_image(image_data: bytes) -> dict:
    """Analyze an uploaded image and return detailed analysis."""
    try:
        from PIL import Image, ImageStat, ImageFilter
    except ImportError:
        return {"success": False, "error": "Pillow not installed"}

    try:
        img = Image.open(BytesIO(image_data))
    except Exception as e:
        return {"success": False, "error": f"Cannot open image: {e}"}

    width, height = img.size
    mode = img.mode
    fmt = img.format or "Unknown"

    rgb = img.convert("RGB")
    stat = ImageStat.Stat(rgb)

    avg_r, avg_g, avg_b = [int(x) for x in stat.mean]
    brightness = (avg_r * 299 + avg_g * 587 + avg_b * 114) / 1000

    std_r, std_g, std_b = stat.stddev
    contrast = (std_r + std_g + std_b) / 3

    dominant_colors = _get_dominant_colors(rgb, n=5)
    color_names = [_name_color(r, g, b) for r, g, b in dominant_colors]

    brightness_label = _brightness_label(brightness)
    contrast_label = _contrast_label(contrast)

    aspect = _aspect_ratio(width, height)
    orientation = "Landscape" if width > height else ("Portrait" if height > width else "Square")
    megapixels = round((width * height) / 1_000_000, 2)
    file_size_kb = round(len(image_data) / 1024, 1)

    color_temp = _color_temperature(avg_r, avg_g, avg_b)
    saturation = _estimate_saturation(rgb)
    sharpness = _estimate_sharpness(rgb)
    complexity = _estimate_complexity(rgb)

    description = _build_description(
        width, height, orientation, brightness_label, contrast_label,
        color_names, color_temp, saturation, sharpness, complexity
    )

    analysis_text = _build_analysis_text(
        width, height, fmt, megapixels, file_size_kb, orientation, aspect,
        brightness, brightness_label, contrast, contrast_label,
        avg_r, avg_g, avg_b, dominant_colors, color_names,
        color_temp, saturation, sharpness, complexity, description
    )

    return {
        "success": True,
        "analysis": analysis_text,
        "data": {
            "dimensions": {"width": width, "height": height},
            "format": fmt,
            "mode": mode,
            "megapixels": megapixels,
            "file_size_kb": file_size_kb,
            "orientation": orientation,
            "aspect_ratio": aspect,
            "brightness": round(brightness, 1),
            "brightness_label": brightness_label,
            "contrast": round(contrast, 1),
            "contrast_label": contrast_label,
            "avg_color": {"r": avg_r, "g": avg_g, "b": avg_b},
            "dominant_colors": [
                {"r": r, "g": g, "b": b, "name": n}
                for (r, g, b), n in zip(dominant_colors, color_names)
            ],
            "color_temperature": color_temp,
            "saturation": saturation,
            "sharpness": sharpness,
            "complexity": complexity,
        },
    }


def _get_dominant_colors(img, n=5):
    small = img.resize((100, 100))
    pixels = list(small.getdata())
    quantized = [(r // 32 * 32, g // 32 * 32, b // 32 * 32) for r, g, b in pixels]
    counter = Counter(quantized)
    return [color for color, _ in counter.most_common(n)]


def _name_color(r, g, b):
    colors = {
        "Red": (255, 0, 0), "Green": (0, 128, 0), "Blue": (0, 0, 255),
        "Yellow": (255, 255, 0), "Cyan": (0, 255, 255), "Magenta": (255, 0, 255),
        "White": (255, 255, 255), "Black": (0, 0, 0), "Gray": (128, 128, 128),
        "Orange": (255, 165, 0), "Pink": (255, 192, 203), "Purple": (128, 0, 128),
        "Brown": (139, 69, 19), "Navy": (0, 0, 128), "Teal": (0, 128, 128),
        "Maroon": (128, 0, 0), "Olive": (128, 128, 0), "Lime": (0, 255, 0),
        "Coral": (255, 127, 80), "Gold": (255, 215, 0), "Beige": (245, 245, 220),
        "Sky Blue": (135, 206, 235), "Dark Green": (0, 100, 0),
    }
    best_name = "Unknown"
    best_dist = float('inf')
    for name, (cr, cg, cb) in colors.items():
        dist = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        if dist < best_dist:
            best_dist = dist
            best_name = name
    return best_name


def _brightness_label(brightness):
    if brightness < 50:
        return "Very Dark"
    elif brightness < 100:
        return "Dark"
    elif brightness < 160:
        return "Medium"
    elif brightness < 210:
        return "Bright"
    else:
        return "Very Bright"


def _contrast_label(contrast):
    if contrast < 30:
        return "Low"
    elif contrast < 60:
        return "Medium"
    elif contrast < 90:
        return "High"
    else:
        return "Very High"


def _aspect_ratio(w, h):
    g = math.gcd(w, h)
    rw, rh = w // g, h // g
    common = {(16, 9): "16:9", (4, 3): "4:3", (1, 1): "1:1",
              (3, 2): "3:2", (21, 9): "21:9", (9, 16): "9:16",
              (3, 4): "3:4", (2, 3): "2:3"}
    return common.get((rw, rh), f"{rw}:{rh}")


def _color_temperature(r, g, b):
    if r > b + 40:
        return "Warm"
    elif b > r + 40:
        return "Cool"
    else:
        return "Neutral"


def _estimate_saturation(img):
    try:
        hsv = img.convert("HSV")
        stat = ImageStat.Stat(hsv)
        sat = stat.mean[1]
        if sat < 50:
            return "Low"
        elif sat < 120:
            return "Medium"
        else:
            return "High"
    except Exception:
        return "Unknown"


def _estimate_sharpness(img):
    try:
        from PIL import ImageFilter
        gray = img.convert("L")
        edges = gray.filter(ImageFilter.FIND_EDGES)
        from PIL import ImageStat
        stat = ImageStat.Stat(edges)
        edge_mean = stat.mean[0]
        if edge_mean < 10:
            return "Soft/Blurry"
        elif edge_mean < 30:
            return "Normal"
        else:
            return "Sharp"
    except Exception:
        return "Unknown"


def _estimate_complexity(img):
    try:
        small = img.resize((50, 50))
        pixels = list(small.convert("RGB").getdata())
        quantized = set((r // 64, g // 64, b // 64) for r, g, b in pixels)
        unique = len(quantized)
        if unique < 10:
            return "Simple"
        elif unique < 30:
            return "Moderate"
        else:
            return "Complex"
    except Exception:
        return "Unknown"


def _build_description(w, h, orientation, brightness, contrast,
                       color_names, temp, saturation, sharpness, complexity):
    unique_colors = list(dict.fromkeys(color_names))[:3]
    color_str = ", ".join(unique_colors)

    parts = [
        f"This is a {orientation.lower()} image ({w}×{h} pixels)",
        f"with {brightness.lower()} brightness and {contrast.lower()} contrast.",
        f"The dominant colors are **{color_str}**,",
        f"giving it a **{temp.lower()}** tone.",
    ]
    if saturation != "Unknown":
        parts.append(f"Color saturation is {saturation.lower()}.")
    if sharpness != "Unknown":
        parts.append(f"The image appears {sharpness.lower()}.")
    if complexity != "Unknown":
        parts.append(f"Visual complexity is {complexity.lower()}.")

    return " ".join(parts)


def _build_analysis_text(w, h, fmt, mp, size_kb, orientation, aspect,
                         brightness, b_label, contrast, c_label,
                         avg_r, avg_g, avg_b, dom_colors, color_names,
                         temp, saturation, sharpness, complexity, desc):
    unique_colors = list(dict.fromkeys(color_names))[:5]
    color_swatches = " | ".join(
        f"**{n}** (rgb({r},{g},{b}))" for (r, g, b), n in zip(dom_colors[:5], unique_colors)
    )

    return (
        f"## Image Analysis\n\n"
        f"{desc}\n\n"
        f"---\n\n"
        f"### Technical Details\n\n"
        f"| Property | Value |\n"
        f"|----------|-------|\n"
        f"| **Dimensions** | {w} × {h} pixels |\n"
        f"| **Megapixels** | {mp} MP |\n"
        f"| **Format** | {fmt} |\n"
        f"| **File Size** | {size_kb} KB |\n"
        f"| **Orientation** | {orientation} |\n"
        f"| **Aspect Ratio** | {aspect} |\n\n"
        f"### Color Analysis\n\n"
        f"| Property | Value |\n"
        f"|----------|-------|\n"
        f"| **Brightness** | {b_label} ({brightness:.0f}/255) |\n"
        f"| **Contrast** | {c_label} ({contrast:.0f}) |\n"
        f"| **Temperature** | {temp} |\n"
        f"| **Saturation** | {saturation} |\n"
        f"| **Average Color** | rgb({avg_r}, {avg_g}, {avg_b}) |\n\n"
        f"**Dominant Colors:** {color_swatches}\n\n"
        f"### Image Quality\n\n"
        f"| Property | Value |\n"
        f"|----------|-------|\n"
        f"| **Sharpness** | {sharpness} |\n"
        f"| **Complexity** | {complexity} |\n\n"
        f"---\n"
        f"*Analyzed by NAGRO 4.1 Image Analyzer — 100% self-built, no external AI APIs.*"
    )
