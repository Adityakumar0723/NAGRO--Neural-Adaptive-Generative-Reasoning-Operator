"""
NAGRO 4.1 — Self-Built Image Analyzer (Advanced)

100% NAGRO's own image analysis engine.
NO external AI models. NO CLIP. NO BLIP. NO transformers. NO open source vision models.
Uses ONLY Pillow (PIL) + pure math for all analysis.

Capabilities:
- Color analysis (dominant colors, palette, temperature, harmony)
- Scene/content type detection (photo, screenshot, diagram, text, art, etc.)
- Brightness, contrast, sharpness, saturation, noise estimation
- Region-based analysis (top/bottom/left/right/center color distribution)
- Texture detection (smooth, grainy, detailed, patterned)
- Mood/atmosphere estimation from color psychology
- Edge density and composition analysis
- Image quality scoring
- Photography/design suggestions
- Histogram analysis
"""
from __future__ import annotations
import math
from io import BytesIO
from collections import Counter


def analyze_image(image_data: bytes) -> dict:
    """Full image analysis — returns detailed markdown report."""
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
    file_size_kb = round(len(image_data) / 1024, 1)
    megapixels = round((width * height) / 1_000_000, 2)

    rgb = img.convert("RGB")

    stat = ImageStat.Stat(rgb)
    avg_r, avg_g, avg_b = [int(x) for x in stat.mean]
    std_r, std_g, std_b = stat.stddev

    brightness = (avg_r * 299 + avg_g * 587 + avg_b * 114) / 1000
    contrast = (std_r + std_g + std_b) / 3

    dominant_colors = _get_dominant_colors(rgb, n=8)
    color_names = [_name_color(r, g, b) for r, g, b in dominant_colors]
    unique_color_names = list(dict.fromkeys(color_names))

    b_label = _brightness_label(brightness)
    c_label = _contrast_label(contrast)
    aspect = _aspect_ratio(width, height)
    orientation = "Landscape" if width > height else ("Portrait" if height > width else "Square")
    color_temp = _color_temperature(avg_r, avg_g, avg_b)
    saturation_val, saturation_label = _estimate_saturation(rgb)
    sharpness_val, sharpness_label = _estimate_sharpness(rgb)
    complexity_val, complexity_label = _estimate_complexity(rgb)
    noise_label = _estimate_noise(rgb)
    texture = _detect_texture(rgb)
    content_type = _detect_content_type(rgb, width, height, complexity_val, sharpness_val, contrast, saturation_val)
    scene_subjects = _detect_scene_subjects(rgb, width, height, avg_r, avg_g, avg_b, brightness, contrast, saturation_val, dominant_colors)
    mood = _detect_mood(avg_r, avg_g, avg_b, brightness, saturation_val, contrast)
    color_harmony = _analyze_color_harmony(dominant_colors)
    regions = _analyze_regions(rgb, width, height)
    histogram_info = _analyze_histogram(rgb)
    has_transparency = mode in ("RGBA", "LA", "PA")
    is_animated = getattr(img, "n_frames", 1) > 1
    quality_score = _calculate_quality_score(brightness, contrast, sharpness_val, noise_label, saturation_val)
    suggestions = _generate_suggestions(b_label, c_label, sharpness_label, saturation_label, noise_label, color_temp, quality_score)

    analysis = _build_full_report(
        width, height, fmt, mode, megapixels, file_size_kb, orientation, aspect,
        brightness, b_label, contrast, c_label, avg_r, avg_g, avg_b,
        dominant_colors, unique_color_names, color_temp, saturation_label,
        sharpness_label, complexity_label, noise_label, texture, content_type,
        mood, color_harmony, regions, histogram_info, has_transparency,
        is_animated, quality_score, suggestions, scene_subjects
    )

    return {
        "success": True,
        "analysis": analysis,
        "data": {
            "dimensions": {"width": width, "height": height},
            "format": fmt, "mode": mode,
            "megapixels": megapixels, "file_size_kb": file_size_kb,
            "orientation": orientation, "aspect_ratio": aspect,
            "brightness": round(brightness, 1), "brightness_label": b_label,
            "contrast": round(contrast, 1), "contrast_label": c_label,
            "color_temperature": color_temp, "saturation": saturation_label,
            "sharpness": sharpness_label, "complexity": complexity_label,
            "noise": noise_label, "texture": texture,
            "content_type": content_type, "mood": mood,
            "color_harmony": color_harmony,
            "quality_score": quality_score,
            "has_transparency": has_transparency,
            "is_animated": is_animated,
            "dominant_colors": [
                {"r": r, "g": g, "b": b, "name": n}
                for (r, g, b), n in zip(dominant_colors[:5], color_names[:5])
            ],
        },
    }


# ═══════════════════════════════════════════
#  COLOR ANALYSIS
# ═══════════════════════════════════════════

def _get_dominant_colors(img, n=8):
    small = img.resize((80, 80))
    pixels = list(small.getdata())
    quantized = [(r // 24 * 24, g // 24 * 24, b // 24 * 24) for r, g, b in pixels]
    counter = Counter(quantized)
    return [color for color, _ in counter.most_common(n)]


def _name_color(r, g, b):
    colors = {
        "Red": (220, 30, 30), "Dark Red": (139, 0, 0), "Light Red": (255, 102, 102),
        "Green": (0, 150, 0), "Dark Green": (0, 80, 0), "Light Green": (144, 238, 144),
        "Blue": (30, 30, 220), "Dark Blue": (0, 0, 139), "Light Blue": (135, 206, 250),
        "Sky Blue": (135, 206, 235), "Navy": (0, 0, 100),
        "Yellow": (240, 240, 0), "Gold": (255, 215, 0), "Amber": (255, 191, 0),
        "Orange": (255, 140, 0), "Dark Orange": (200, 100, 0),
        "Cyan": (0, 220, 220), "Teal": (0, 128, 128),
        "Magenta": (220, 0, 220), "Pink": (255, 150, 180), "Hot Pink": (255, 50, 150),
        "Purple": (128, 0, 180), "Violet": (148, 103, 189), "Lavender": (180, 160, 220),
        "White": (250, 250, 250), "Off-White": (240, 235, 220),
        "Light Gray": (192, 192, 192), "Gray": (128, 128, 128), "Dark Gray": (64, 64, 64),
        "Black": (15, 15, 15), "Near Black": (30, 30, 30),
        "Brown": (139, 69, 19), "Dark Brown": (80, 40, 10), "Tan": (210, 180, 140),
        "Beige": (245, 235, 200), "Cream": (255, 253, 208),
        "Olive": (128, 128, 0), "Lime": (50, 205, 50),
        "Coral": (255, 127, 80), "Salmon": (250, 128, 114),
        "Turquoise": (64, 224, 208), "Indigo": (75, 0, 130),
        "Maroon": (128, 0, 0), "Burgundy": (128, 0, 32),
        "Peach": (255, 218, 185), "Mint": (152, 255, 152),
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
    if brightness < 40: return "Very Dark"
    if brightness < 85: return "Dark"
    if brightness < 130: return "Medium-Dark"
    if brightness < 170: return "Medium"
    if brightness < 210: return "Bright"
    return "Very Bright"


def _contrast_label(contrast):
    if contrast < 20: return "Very Low"
    if contrast < 40: return "Low"
    if contrast < 65: return "Medium"
    if contrast < 85: return "High"
    return "Very High"


def _aspect_ratio(w, h):
    g = math.gcd(w, h)
    rw, rh = w // g, h // g
    common = {
        (16, 9): "16:9 (Widescreen)", (4, 3): "4:3 (Standard)", (1, 1): "1:1 (Square)",
        (3, 2): "3:2 (Classic Photo)", (21, 9): "21:9 (Ultrawide)", (9, 16): "9:16 (Phone Vertical)",
        (3, 4): "3:4", (2, 3): "2:3", (5, 4): "5:4", (4, 5): "4:5 (Instagram)",
    }
    return common.get((rw, rh), f"{rw}:{rh}")


def _color_temperature(r, g, b):
    diff = r - b
    if diff > 60: return "Very Warm"
    if diff > 25: return "Warm"
    if diff > -25: return "Neutral"
    if diff > -60: return "Cool"
    return "Very Cool"


def _estimate_saturation(img):
    try:
        from PIL import ImageStat
        hsv = img.convert("HSV")
        stat = ImageStat.Stat(hsv)
        sat = stat.mean[1]
        if sat < 30: return (sat, "Very Low (near grayscale)")
        if sat < 70: return (sat, "Low")
        if sat < 120: return (sat, "Medium")
        if sat < 180: return (sat, "High")
        return (sat, "Very High (vivid)")
    except Exception:
        return (0, "Unknown")


def _estimate_sharpness(img):
    try:
        from PIL import ImageFilter, ImageStat
        gray = img.convert("L")
        edges = gray.filter(ImageFilter.Kernel(
            size=(3, 3),
            kernel=[-1, -1, -1, -1, 8, -1, -1, -1, -1],
            scale=1, offset=128,
        ))
        stat = ImageStat.Stat(edges)
        val = stat.stddev[0]
        if val < 5: return (val, "Very Soft / Blurry")
        if val < 15: return (val, "Soft")
        if val < 30: return (val, "Normal")
        if val < 50: return (val, "Sharp")
        return (val, "Very Sharp / High Detail")
    except Exception:
        return (0, "Unknown")


def _estimate_complexity(img):
    try:
        small = img.resize((60, 60))
        pixels = list(small.convert("RGB").getdata())
        quantized = set((r // 48, g // 48, b // 48) for r, g, b in pixels)
        unique = len(quantized)
        if unique < 8: return (unique, "Very Simple (few colors)")
        if unique < 20: return (unique, "Simple")
        if unique < 40: return (unique, "Moderate")
        if unique < 70: return (unique, "Complex")
        return (unique, "Very Complex (many details)")
    except Exception:
        return (0, "Unknown")


def _estimate_noise(img):
    try:
        from PIL import ImageFilter, ImageStat
        gray = img.convert("L")
        small = gray.resize((200, 200)) if max(gray.size) > 200 else gray
        blurred = small.filter(ImageFilter.GaussianBlur(radius=2))
        diff_pixels = list(zip(small.getdata(), blurred.getdata()))
        noise_sum = sum(abs(a - b) for a, b in diff_pixels)
        avg_noise = noise_sum / len(diff_pixels)
        if avg_noise < 3: return "Very Low (clean)"
        if avg_noise < 7: return "Low"
        if avg_noise < 15: return "Moderate"
        if avg_noise < 25: return "High"
        return "Very High (noisy/grainy)"
    except Exception:
        return "Unknown"


# ═══════════════════════════════════════════
#  CONTENT & SCENE DETECTION
# ═══════════════════════════════════════════

def _detect_texture(img):
    try:
        from PIL import ImageFilter, ImageStat
        gray = img.convert("L").resize((100, 100))
        edges = gray.filter(ImageFilter.FIND_EDGES)
        stat = ImageStat.Stat(edges)
        edge_mean = stat.mean[0]
        edge_std = stat.stddev[0]

        if edge_mean < 5 and edge_std < 8:
            return "Smooth / Flat"
        if edge_mean < 15 and edge_std < 20:
            return "Slightly Textured"
        if edge_mean < 30:
            if edge_std > 40:
                return "Mixed (some areas detailed, some smooth)"
            return "Moderately Textured"
        if edge_mean < 50:
            return "Highly Textured / Detailed"
        return "Very Detailed / Dense Patterns"
    except Exception:
        return "Unknown"


def _detect_content_type(img, w, h, complexity, sharpness, contrast, saturation):
    try:
        from PIL import ImageStat
        gray = img.convert("L")
        stat = ImageStat.Stat(gray)
        gray_std = stat.stddev[0]
        gray_mean = stat.mean[0]

        small = img.resize((50, 50))
        pixels = list(small.getdata())
        unique_pixels = len(set(pixels))

        r_vals = [p[0] for p in pixels]
        g_vals = [p[1] for p in pixels]
        b_vals = [p[2] for p in pixels]
        is_grayscale = all(
            abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20
            for r, g, b in pixels[:100]
        )

        corner_pixels = []
        full = img.resize((100, 100))
        pxs = list(full.getdata())
        for y in range(5):
            for x in range(5):
                corner_pixels.append(pxs[y * 100 + x])
                corner_pixels.append(pxs[y * 100 + (99 - x)])
                corner_pixels.append(pxs[(99 - y) * 100 + x])
                corner_pixels.append(pxs[(99 - y) * 100 + (99 - x)])
        corner_unique = len(set(corner_pixels))
        corner_uniform = corner_unique < 15

        if unique_pixels < 50 and gray_std < 20:
            return "Solid Color / Gradient"

        if unique_pixels < 200 and complexity < 15:
            if contrast > 60:
                return "Text / Document"
            return "Simple Graphic / Icon"

        if w == h and w in (16, 32, 48, 64, 128, 256, 512):
            return "Icon / Favicon"

        if complexity < 12 and contrast > 50 and saturation < 50:
            return "Screenshot / UI"

        if is_grayscale:
            if contrast > 60:
                return "Black & White Photo"
            return "Grayscale Image"

        if complexity < 20 and saturation < 40 and corner_uniform:
            return "Screenshot / Interface"

        if complexity > 50 and sharpness > 25 and saturation > 80:
            return "Photograph (high quality)"

        if complexity > 35 and sharpness > 15:
            return "Photograph"

        if complexity < 25 and saturation > 100:
            return "Digital Art / Illustration"

        if complexity < 20:
            return "Simple Image / Graphic"

        return "Mixed Content Image"
    except Exception:
        return "Image"


def _detect_scene_subjects(img, w, h, avg_r, avg_g, avg_b, brightness, contrast, saturation, dominant_colors):
    """Detect likely subjects/scenes in the image using regional color analysis + heuristics."""
    try:
        from PIL import ImageStat
        subjects = []
        confidence = {}

        half_h = h // 2
        upper = img.crop((0, 0, w, half_h))
        lower = img.crop((0, half_h, w, h))
        up_stat = ImageStat.Stat(upper.convert("RGB"))
        lo_stat = ImageStat.Stat(lower.convert("RGB"))
        ur, ug, ub = [int(x) for x in up_stat.mean]
        lr, lg, lb = [int(x) for x in lo_stat.mean]

        # Sky detection — upper region is blue-ish and bright
        if ub > ur + 20 and ub > 140 and ug > 120 and (ub - ur) > 15:
            subjects.append("sky")
            confidence["sky"] = "high"
        elif ub > ur and ub > 100 and brightness > 100 and ur < 200:
            subjects.append("possible sky or blue background")
            confidence["sky"] = "medium"

        # Sunset/sunrise — upper has orange/pink gradient, warm colors
        if ur > 180 and ug > 100 and ug < 180 and ub < 150 and (ur - ub) > 50:
            subjects.append("sunset or sunrise")
            confidence["sunset"] = "high"

        # Grass/vegetation — strong green in lower region
        if lg > lr + 15 and lg > lb + 15 and lg > 80:
            subjects.append("grass or vegetation")
            confidence["grass"] = "high"
        elif lg > lr and lg > lb and lg > 60:
            subjects.append("possible plants or greenery")
            confidence["grass"] = "medium"

        # Water/ocean — strong blue dominant in lower region
        if lb > lr + 15 and lb > lg + 10 and lb > 100 and lr < 150:
            subjects.append("water, ocean, or lake")
            confidence["water"] = "high"

        # Sand/beach — tan/beige/yellow in lower region
        if lr > 180 and lg > 160 and lb < 160 and abs(lr - lg) < 40 and lr > lb:
            subjects.append("sand or beach")
            confidence["sand"] = "medium"

        # Snow — very bright, low saturation, cool
        if brightness > 200 and saturation < 50 and avg_b >= avg_r:
            subjects.append("snow or ice")
            confidence["snow"] = "high"

        # Night scene — very dark overall with some bright points
        if brightness < 60 and contrast > 40:
            subjects.append("night scene")
            confidence["night"] = "high"

        # Forest/trees — dominant dark green + brown
        if any(_is_green(c) for c in dominant_colors[:3]) and any(_is_brown(c) for c in dominant_colors[:5]):
            subjects.append("forest or trees")
            confidence["forest"] = "high"

        # Fire/flame — strong orange + red + yellow dominant
        warm_count = sum(1 for c in dominant_colors[:5] if _is_warm(c))
        if warm_count >= 3 and avg_r > 150 and avg_g > 80 and avg_g < 180:
            subjects.append("fire, flames, or warm lighting")
            confidence["fire"] = "medium"

        # Skin tones — detect peach/tan ranges prominently
        skin_count = sum(1 for c in dominant_colors[:6] if _is_skin_tone(c))
        if skin_count >= 2:
            subjects.append("likely contains person or portrait")
            confidence["person"] = "medium"

        # Food — warm, saturated, varied colors in center
        center = img.crop((w // 4, h // 4, 3 * w // 4, 3 * h // 4))
        c_stat = ImageStat.Stat(center.convert("RGB"))
        cr, cg, cb = [int(x) for x in c_stat.mean]
        if saturation > 100 and cr > 140 and cg > 100 and warm_count >= 2:
            subjects.append("possibly food or still life")
            confidence["food"] = "low"

        # Flower — high saturation, varied bright colors
        if saturation > 150 and len(set(_name_color(*c) for c in dominant_colors[:5])) >= 4:
            subjects.append("flower or colorful subject")
            confidence["flower"] = "medium"

        # Document/text — mostly white with dark marks
        if brightness > 200 and contrast > 60 and saturation < 30:
            subjects.append("document, paper, or text")
            confidence["document"] = "high"

        # UI/screenshot
        edge_pixels = []
        small = img.resize((100, 100))
        pxs = list(small.getdata())
        for i in range(100):
            edge_pixels.append(pxs[i])
            edge_pixels.append(pxs[9900 + i])
        edge_unique = len(set(edge_pixels))
        if edge_unique < 10 and saturation < 60:
            subjects.append("UI screenshot or interface")
            confidence["ui"] = "high"

        if not subjects:
            subjects.append("abstract or mixed subject")

        return {"subjects": subjects, "confidence": confidence}
    except Exception:
        return {"subjects": [], "confidence": {}}


def _is_green(c):
    r, g, b = c
    return g > r + 20 and g > b + 20 and g > 50


def _is_brown(c):
    r, g, b = c
    return r > g and g > b and r > 60 and r < 180 and (r - b) > 30


def _is_warm(c):
    r, g, b = c
    return r > b + 30 and r > 150


def _is_skin_tone(c):
    r, g, b = c
    return (170 <= r <= 255 and 120 <= g <= 220 and 90 <= b <= 200
            and r > g and g > b and (r - b) < 90)


def _detect_mood(r, g, b, brightness, saturation, contrast):
    moods = []

    if brightness < 70:
        moods.append("Dark / Dramatic")
    elif brightness < 100:
        moods.append("Moody / Subdued")
    elif brightness > 210:
        moods.append("Bright / Airy")
    elif brightness > 180:
        moods.append("Light / Cheerful")

    if saturation > 150:
        moods.append("Vibrant / Energetic")
    elif saturation < 40:
        moods.append("Muted / Calm")

    if r > 180 and g < 100 and b < 100:
        moods.append("Passionate / Intense")
    elif b > 180 and r < 100 and g < 100:
        moods.append("Cool / Serene")
    elif g > 150 and r < 120 and b < 120:
        moods.append("Natural / Fresh")
    elif r > 200 and g > 150 and b < 80:
        moods.append("Warm / Inviting")
    elif r > 180 and g > 100 and b > 180:
        moods.append("Playful / Creative")

    if contrast > 80:
        moods.append("High-Impact")
    elif contrast < 25:
        moods.append("Soft / Dreamy")

    if not moods:
        moods.append("Balanced / Neutral")

    return " • ".join(moods[:3])


def _analyze_color_harmony(colors):
    if len(colors) < 2:
        return "Monochromatic"

    hues = []
    for r, g, b in colors[:6]:
        mx = max(r, g, b)
        mn = min(r, g, b)
        if mx == mn:
            hues.append(0)
        elif mx == r:
            hues.append(((g - b) / (mx - mn)) % 6)
        elif mx == g:
            hues.append((b - r) / (mx - mn) + 2)
        else:
            hues.append((r - g) / (mx - mn) + 4)
    hues = [h * 60 for h in hues]

    if len(set(int(h / 30) for h in hues)) <= 2:
        return "Monochromatic / Analogous"

    diffs = []
    for i in range(len(hues)):
        for j in range(i + 1, len(hues)):
            d = abs(hues[i] - hues[j])
            if d > 180:
                d = 360 - d
            diffs.append(d)

    if any(150 < d < 210 for d in diffs):
        return "Complementary (opposite colors)"
    if any(100 < d < 150 for d in diffs):
        return "Triadic / Split-Complementary"
    if all(d < 60 for d in diffs):
        return "Analogous (neighboring colors)"
    return "Mixed / Complex Palette"


# ═══════════════════════════════════════════
#  REGION & HISTOGRAM ANALYSIS
# ═══════════════════════════════════════════

def _analyze_regions(img, w, h):
    try:
        from PIL import ImageStat
        half_w, half_h = w // 2, h // 2
        regions = {
            "Top": img.crop((0, 0, w, half_h)),
            "Bottom": img.crop((0, half_h, w, h)),
            "Left": img.crop((0, 0, half_w, h)),
            "Right": img.crop((half_w, 0, w, h)),
            "Center": img.crop((w // 4, h // 4, 3 * w // 4, 3 * h // 4)),
        }
        result = {}
        for name, region in regions.items():
            stat = ImageStat.Stat(region.convert("RGB"))
            r, g, b = [int(x) for x in stat.mean]
            bri = (r * 299 + g * 587 + b * 114) / 1000
            result[name] = {
                "color": _name_color(r, g, b),
                "brightness": _brightness_label(bri),
                "rgb": f"({r}, {g}, {b})",
            }
        return result
    except Exception:
        return {}


def _analyze_histogram(img):
    try:
        rgb = img.convert("RGB")
        r_hist = rgb.split()[0].histogram()
        g_hist = rgb.split()[1].histogram()
        b_hist = rgb.split()[2].histogram()

        total = sum(r_hist)

        dark_pct = round(100 * sum(r_hist[:64] + g_hist[:64] + b_hist[:64]) / (total * 3))
        mid_pct = round(100 * sum(r_hist[64:192] + g_hist[64:192] + b_hist[64:192]) / (total * 3))
        light_pct = round(100 * sum(r_hist[192:] + g_hist[192:] + b_hist[192:]) / (total * 3))

        r_peak = r_hist.index(max(r_hist))
        g_peak = g_hist.index(max(g_hist))
        b_peak = b_hist.index(max(b_hist))

        if dark_pct > 60:
            distribution = "Heavily Dark (low-key)"
        elif light_pct > 60:
            distribution = "Heavily Bright (high-key)"
        elif mid_pct > 60:
            distribution = "Concentrated in Midtones"
        else:
            distribution = "Well Distributed"

        clipped_dark = sum(r_hist[:3] + g_hist[:3] + b_hist[:3]) / (total * 3) * 100
        clipped_light = sum(r_hist[253:] + g_hist[253:] + b_hist[253:]) / (total * 3) * 100

        return {
            "dark_pct": dark_pct,
            "mid_pct": mid_pct,
            "light_pct": light_pct,
            "distribution": distribution,
            "r_peak": r_peak, "g_peak": g_peak, "b_peak": b_peak,
            "clipped_shadows": round(clipped_dark, 1),
            "clipped_highlights": round(clipped_light, 1),
        }
    except Exception:
        return {}


# ═══════════════════════════════════════════
#  QUALITY SCORING & SUGGESTIONS
# ═══════════════════════════════════════════

def _calculate_quality_score(brightness, contrast, sharpness, noise, saturation):
    score = 50

    if 80 < brightness < 200:
        score += 10
    elif 60 < brightness < 220:
        score += 5

    if 40 < contrast < 90:
        score += 10
    elif 25 < contrast < 100:
        score += 5

    if sharpness > 20:
        score += 15
    elif sharpness > 10:
        score += 8

    if noise in ("Very Low (clean)", "Low"):
        score += 10
    elif noise == "Moderate":
        score += 3
    elif noise in ("High", "Very High (noisy/grainy)"):
        score -= 5

    if 60 < saturation < 180:
        score += 5

    return min(max(score, 10), 100)


def _generate_suggestions(b_label, c_label, sharpness, saturation, noise, temp, quality):
    tips = []

    if "Very Dark" in b_label or "Dark" in b_label:
        tips.append("Consider increasing brightness/exposure for better visibility")
    if "Very Bright" in b_label:
        tips.append("The image may be overexposed — reducing brightness could recover details")

    if "Very Low" in c_label or "Low" in c_label:
        tips.append("Increasing contrast would make the image more visually striking")
    if "Very High" in c_label:
        tips.append("Very high contrast — some details might be lost in shadows/highlights")

    if "Blurry" in sharpness or "Soft" in sharpness:
        tips.append("The image appears soft — try sharpening or using a higher resolution source")

    if "Very Low" in saturation:
        tips.append("Very low saturation — if this isn't intentional, boosting saturation would add life")
    if "Very High" in saturation:
        tips.append("Very vivid colors — reducing saturation slightly could look more natural")

    if "High" in noise or "Very High" in noise:
        tips.append("Noticeable noise/grain — noise reduction could improve clarity")

    if quality >= 85:
        tips.insert(0, "Excellent image quality overall!")
    elif quality >= 70:
        tips.insert(0, "Good image quality with room for minor improvements")

    if not tips:
        tips.append("Image looks well-balanced — no major improvements needed")

    return tips


# ═══════════════════════════════════════════
#  BUILD FINAL REPORT
# ═══════════════════════════════════════════

def _build_full_report(w, h, fmt, mode, mp, size_kb, orientation, aspect,
                       brightness, b_label, contrast, c_label, avg_r, avg_g, avg_b,
                       dom_colors, unique_color_names, color_temp, saturation,
                       sharpness, complexity, noise, texture, content_type,
                       mood, color_harmony, regions, histogram, has_transparency,
                       is_animated, quality_score, suggestions, scene_subjects=None):

    top3_colors = unique_color_names[:3]
    color_str = ", ".join(top3_colors)

    color_blocks = " | ".join(
        f"**{n}** `rgb({r},{g},{b})`"
        for (r, g, b), n in zip(dom_colors[:5], unique_color_names[:5])
    )

    score_bar = "█" * (quality_score // 10) + "░" * (10 - quality_score // 10)
    score_emoji = "🟢" if quality_score >= 75 else ("🟡" if quality_score >= 50 else "🔴")

    report = f"## 🖼️ NAGRO Image Analysis\n\n"

    # Lead with what we see — subjects first, then technicals
    subject_summary = ""
    if scene_subjects and scene_subjects.get("subjects"):
        subs = scene_subjects["subjects"]
        if subs and subs[0] != "abstract or mixed subject":
            subject_summary = f"**I can see: {', '.join(subs[:4])}.** "

    report += (
        f"{subject_summary}"
        f"This is a **{content_type}** in **{orientation.lower()}** orientation ({w}×{h} pixels). "
        f"The dominant colors are **{color_str}**, giving the image a **{color_temp.lower()}** feel. "
    )
    if mood:
        report += f"The overall mood is **{mood.split(' • ')[0].lower()}**. "
    report += f"Image quality score: **{quality_score}/100** {score_emoji}\n\n"

    if scene_subjects and scene_subjects.get("subjects"):
        subs = scene_subjects["subjects"]
        conf = scene_subjects.get("confidence", {})
        if subs and subs[0] != "abstract or mixed subject":
            report += f"### 👁️ What NAGRO Sees\n\n"
            for s in subs:
                # Find confidence level if available
                lvl = ""
                for key, c in conf.items():
                    if key in s.lower() or s.lower().startswith(key):
                        lvl = f" _(confidence: {c})_"
                        break
                report += f"- **{s.capitalize()}**{lvl}\n"
            report += "\n"

    report += f"---\n\n"

    report += f"### 📊 Technical Details\n\n"
    report += f"| Property | Value |\n|----------|-------|\n"
    report += f"| **Dimensions** | {w} × {h} pixels |\n"
    report += f"| **Resolution** | {mp} Megapixels |\n"
    report += f"| **Format** | {fmt} ({mode}) |\n"
    report += f"| **File Size** | {size_kb} KB |\n"
    report += f"| **Orientation** | {orientation} |\n"
    report += f"| **Aspect Ratio** | {aspect} |\n"
    report += f"| **Content Type** | {content_type} |\n"
    if has_transparency:
        report += f"| **Transparency** | Yes (has alpha channel) |\n"
    if is_animated:
        report += f"| **Animated** | Yes (multiple frames) |\n"
    report += f"\n"

    report += f"### 🎨 Color Analysis\n\n"
    report += f"| Property | Value |\n|----------|-------|\n"
    report += f"| **Color Temperature** | {color_temp} |\n"
    report += f"| **Saturation** | {saturation} |\n"
    report += f"| **Color Harmony** | {color_harmony} |\n"
    report += f"| **Average Color** | rgb({avg_r}, {avg_g}, {avg_b}) |\n\n"
    report += f"**Dominant Colors:** {color_blocks}\n\n"

    report += f"### 💡 Brightness & Contrast\n\n"
    report += f"| Property | Value |\n|----------|-------|\n"
    report += f"| **Brightness** | {b_label} ({brightness:.0f}/255) |\n"
    report += f"| **Contrast** | {c_label} ({contrast:.0f}) |\n"

    if histogram:
        report += f"| **Shadows** | {histogram.get('dark_pct', '?')}% |\n"
        report += f"| **Midtones** | {histogram.get('mid_pct', '?')}% |\n"
        report += f"| **Highlights** | {histogram.get('light_pct', '?')}% |\n"
        report += f"| **Tonal Distribution** | {histogram.get('distribution', '?')} |\n"
        clipped_s = histogram.get('clipped_shadows', 0)
        clipped_h = histogram.get('clipped_highlights', 0)
        if clipped_s > 5:
            report += f"| **⚠️ Shadow Clipping** | {clipped_s}% (lost detail in darks) |\n"
        if clipped_h > 5:
            report += f"| **⚠️ Highlight Clipping** | {clipped_h}% (lost detail in brights) |\n"
    report += f"\n"

    report += f"### 🔍 Image Quality\n\n"
    report += f"| Property | Value |\n|----------|-------|\n"
    report += f"| **Sharpness** | {sharpness} |\n"
    report += f"| **Noise** | {noise} |\n"
    report += f"| **Texture** | {texture} |\n"
    report += f"| **Complexity** | {complexity} |\n"
    report += f"| **Quality Score** | {score_emoji} {quality_score}/100 [{score_bar}] |\n\n"

    if mood:
        report += f"### 🎭 Mood & Atmosphere\n\n"
        report += f"**{mood}**\n\n"

    if regions:
        report += f"### 🗺️ Region Analysis\n\n"
        report += f"| Region | Dominant Color | Brightness |\n|--------|---------------|------------|\n"
        for name, info in regions.items():
            report += f"| **{name}** | {info['color']} {info['rgb']} | {info['brightness']} |\n"
        report += f"\n"

    if suggestions:
        report += f"### 💡 Suggestions\n\n"
        for tip in suggestions:
            report += f"- {tip}\n"
        report += f"\n"

    report += f"---\n*Analyzed by **NAGRO 4.1 Image Analyzer** — 100% self-built engine, zero external AI APIs.*"

    return report
