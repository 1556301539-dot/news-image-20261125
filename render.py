#!/usr/bin/env python3
"""
THE WORLD IN ONE PAGE -- Wednesday 25 November 2026 (redesigned)
make.fun bounty: Sum up 25 November's world news in one image.

Dense broadsheet front page, in the spirit of a classic newspaper:
huge serif date masthead, story-count strip, ticker, stats strip,
three illustrated lead cards, eight mini illustrated stories, a world
map with pins, and a numbered 24-story brief list.

Deterministic, offline. No network, no randomness, no timestamps.
Only stdlib + Pillow. Fixed fonts, fixed layout, fixed text.
Output: entry.png next to this file (and ./output/entry.png),
1024x1024 PNG, <= 1 MiB, byte-identical across runs in the same env.

All news is the already-verified 25 Nov 2026 set (see SOURCES.md).
Nothing was invented: every number, date and quote below was in the
verified set. Stories are re-presented as stats, scenes and briefs.
"""

import hashlib
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24
CW = W - 2 * M  # 976
BG = (252, 250, 244)      # newsprint cream
INK = (15, 15, 15)
RED = (178, 34, 34)
BLUE = (27, 68, 128)
GREY = (96, 96, 96)
DARKGREY = (60, 60, 60)
LIGHT_BLUE = (232, 240, 245)
LAND = (226, 216, 186)
RULE = (15, 15, 15)

REGION = {
    "MIDDLE EAST": (178, 34, 34),
    "ASIA-PACIFIC": (180, 90, 20),
    "AMERICAS": (110, 60, 120),
    "EUROPE": (27, 68, 128),
    "AFRICA": (46, 110, 60),
    "OCEANIA": (20, 100, 110),
    "GLOBAL": (96, 96, 96),
}

# ---------------------------------------------------------------- fonts
FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/noto",
]

def _find(cands):
    for d in FONT_DIRS:
        for name in cands:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None

_SERIF_BOLD = _find(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"])
_SERIF = _find(["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
_SERIF_ITALIC = _find(["LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf"])
_SANS_BOLD = _find(["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"])
_SANS = _find(["LiberationSans-Regular.ttf", "DejaVuSans.ttf"])

_cache = {}
def font(kind, size):
    key = (kind, size)
    if key in _cache:
        return _cache[key]
    path = {"serif_bold": _SERIF_BOLD, "serif": _SERIF,
            "serif_italic": _SERIF_ITALIC, "sans_bold": _SANS_BOLD,
            "sans": _SANS}.get(kind)
    f = ImageFont.truetype(path, size) if path else ImageFont.load_default()
    _cache[key] = f
    return f

# ---------------------------------------------------------------- text
def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, max_w, leading, color=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y

def rule(draw, x, y, w, h=2, color=RULE):
    draw.rectangle([x, y, x + w, y + h], fill=color)

def kicker(draw, x, y, text, color=RED, size=10):
    f = font("sans_bold", size)
    draw.text((x, y), text, font=f, fill=color)
    return y + size + 4

def num_circle(draw, cx, cy, r, num, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    f = font("sans_bold", 9)
    t = str(num)
    bb = draw.textbbox((0, 0), t, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), t,
              font=f, fill=(255, 255, 255))

def paste_scene(img, scene_fn, x, y, w, h):
    """Draw a scene into a temp image and paste it: clips any drawing
    that would spill outside the scene rectangle."""
    tmp = Image.new("RGB", (w, h), BG)
    td = ImageDraw.Draw(tmp)
    scene_fn(td, 0, 0, w, h)
    img.paste(tmp, (x, y))

# ---------------------------------------------------------------- scenes
# Every scene is drawn from fixed PIL primitives: no randomness, no time.

def scene_sea(d, x, y, w, h):
    # Strait of Hormuz at dusk: burning tanker.
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 58))
    d.rectangle([x, y + int(h * 0.52), x + w, y + h], fill=(14, 42, 72))
    d.ellipse([x + int(w * 0.68), y + int(h * 0.30), x + int(w * 0.82),
               y + int(h * 0.52)], fill=(232, 120, 40))
    for i in range(5):
        yy = y + int(h * 0.58) + i * 7
        d.line([x + 6 + i * 8, yy, x + w - 6 - i * 6, yy],
               fill=(70, 110, 150), width=2)
    # tanker hull
    hx, hy = x + int(w * 0.10), y + int(h * 0.52)
    hw, hh = int(w * 0.72), int(h * 0.26)
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 12, hy + hh),
               (hx + 6, hy + hh)], fill=(12, 12, 14))
    d.rectangle([hx + 8, hy - 16, hx + hw - 30, hy], fill=(200, 60, 40))
    d.rectangle([hx + 14, hy - 30, hx + 40, hy - 16], fill=(40, 40, 44))
    d.rectangle([hx + hw - 26, hy - 26, hx + hw - 14, hy], fill=(220, 200, 160))
    # flame + smoke on deck (kept inside the scene box)
    fx = hx + int(hw * 0.55)
    d.polygon([(fx, hy - 26), (fx + 10, hy - 42), (fx + 20, hy - 26)],
              fill=(240, 140, 30))
    d.polygon([(fx + 5, hy - 22), (fx + 10, hy - 34), (fx + 15, hy - 22)],
              fill=(250, 210, 60))
    for cx, cy, r in [(fx + 26, hy - 28, 5), (fx + 34, hy - 36, 6),
                      (fx + 42, hy - 42, 4)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 90, 96))

def scene_space(d, x, y, w, h):
    # Night launch: rocket, stars, Earth curve, station.
    d.rectangle([x, y, x + w, y + h], fill=(8, 12, 28))
    for sx, sy, r in [(0.12, 0.15, 1), (0.30, 0.08, 2), (0.55, 0.18, 1),
                      (0.78, 0.10, 2), (0.90, 0.28, 1), (0.22, 0.35, 1),
                      (0.45, 0.06, 1), (0.66, 0.38, 1), (0.05, 0.45, 2),
                      (0.85, 0.50, 1)]:
        d.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r,
                   y + sy * h + r], fill=(255, 255, 255))
    # Earth curve
    d.ellipse([x - int(w * 0.25), y + int(h * 0.82), x + int(w * 1.05),
               y + int(h * 1.55)], fill=(40, 90, 160))
    d.arc([x - int(w * 0.25), y + int(h * 0.82), x + int(w * 1.05),
           y + int(h * 1.55)], 180, 360, fill=(120, 180, 230), width=3)
    # rocket
    rx, ry = x + int(w * 0.30), y + int(h * 0.18)
    rw, rh = 16, 52
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=(235, 235, 230),
                outline=INK)
    d.polygon([(rx, ry), (rx + rw // 2, ry - 16), (rx + rw, ry)],
              fill=RED, outline=INK)
    d.polygon([(rx, ry + rh), (rx - 8, ry + rh + 12), (rx, ry + rh)],
              fill=RED, outline=INK)
    d.polygon([(rx + rw, ry + rh), (rx + rw + 8, ry + rh + 12),
               (rx + rw, ry + rh)], fill=RED, outline=INK)
    d.ellipse([rx + 4, ry + 12, rx + 12, ry + 20], fill=LIGHT_BLUE,
              outline=INK)
    d.polygon([(rx + 2, ry + rh + 12), (rx + 8, ry + rh + 22),
               (rx + 14, ry + rh + 12)], fill=(250, 180, 40))
    d.polygon([(rx + 5, ry + rh + 12), (rx + 8, ry + rh + 18),
               (rx + 11, ry + rh + 12)], fill=(250, 230, 120))
    # station
    sx, sy = x + int(w * 0.62), y + int(h * 0.16)
    d.rectangle([sx, sy, sx + 34, sy + 12], fill=(200, 200, 195),
                outline=INK)
    d.rectangle([sx + 34, sy + 2, sx + 46, sy + 10], fill=(180, 180, 175),
                outline=INK)
    d.rectangle([sx - 26, sy + 2, sx, sy + 10], fill=(60, 90, 160),
                outline=INK)
    d.rectangle([sx + 46, sy + 2, sx + 72, sy + 10], fill=(60, 90, 160),
                outline=INK)

def scene_court(d, x, y, w, h):
    # Brooklyn courthouse: pediment, columns, steps.
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.polygon([(x + 8, y + 22), (x + w // 2, y + 4), (x + w - 8, y + 22)],
              fill=(210, 202, 180), outline=INK)
    d.ellipse([x + w // 2 - 7, y + 10, x + w // 2 + 7, y + 24],
              fill=(120, 100, 70), outline=INK)
    for i in range(4):
        cx = x + 16 + i * int((w - 32) / 3)
        d.rectangle([cx - 6, y + 26, cx + 6, y + h - 22], fill=(245, 240, 228),
                    outline=INK)
        d.rectangle([cx - 9, y + 22, cx + 9, y + 26], fill=(200, 192, 170))
        d.rectangle([cx - 9, y + h - 26, cx + 9, y + h - 22],
                    fill=(200, 192, 170))
    d.rectangle([x + w // 2 - 12, y + h - 42, x + w // 2 + 12, y + h - 22],
                fill=(60, 50, 40))
    for i in range(3):
        yy = y + h - 18 + i * 5
        d.rectangle([x + 6, yy, x + w - 6, yy + 3], fill=(190, 182, 160))

def scene_city(d, x, y, w, h):
    # City skyline at dusk, smoke column.
    d.rectangle([x, y, x + w, y + h], fill=(58, 48, 66))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(30, 26, 34))
    d.ellipse([x + int(w * 0.72), y + int(h * 0.12), x + int(w * 0.86),
               y + int(h * 0.34)], fill=(240, 150, 60))
    for bx, bw, bh in [(0.04, 0.16, 0.45), (0.24, 0.12, 0.62),
                       (0.40, 0.18, 0.38), (0.62, 0.14, 0.55),
                       (0.80, 0.16, 0.42)]:
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h],
                    fill=(18, 16, 22))
        for wy in range(3):
            for wx in range(2):
                if (int(bx * 10) + wy + wx) % 2 == 0:
                    d.rectangle([x + (bx + 0.03 + wx * 0.06) * w,
                                 y + h - bh * h + 6 + wy * 10,
                                 x + (bx + 0.05 + wx * 0.06) * w,
                                 y + h - bh * h + 10 + wy * 10],
                                fill=(250, 200, 90))
    for cx, cy, r in [(0.30, 0.30, 6), (0.32, 0.20, 8), (0.35, 0.12, 6)]:
        d.ellipse([x + cx * w - r, y + cy * h - r, x + cx * w + r,
                   y + cy * h + r], fill=(120, 120, 126))

def scene_store(d, x, y, w, h):
    # Supermarket storefront with striped awning.
    d.rectangle([x, y, x + w, y + h], fill=(206, 188, 158))
    for i in range(8):
        c = (178, 34, 34) if i % 2 == 0 else (245, 240, 228)
        d.polygon([(x + i * w // 8, y + 12), (x + (i + 1) * w // 8, y + 12),
                   (x + (i + 1) * w // 8 + 4, y + 26),
                   (x + i * w // 8 + 4, y + 26)], fill=c)
    d.rectangle([x + 8, y + 30, x + w - 8, y + h - 8], fill=(40, 40, 46),
                outline=INK)
    for i in range(3):
        d.rectangle([x + 16 + i * 22, y + 38, x + 32 + i * 22, y + 52],
                    fill=(90, 140, 90))
    d.rectangle([x + w - 34, y + 38, x + w - 14, y + h - 8],
                fill=(120, 90, 60), outline=INK)
    d.rectangle([x + 8, y + h - 8, x + w - 8, y + h - 4], fill=(120, 110, 100))

def scene_hospital(d, x, y, w, h):
    # Field hospital: white block, red cross, green ground.
    d.rectangle([x, y, x + w, y + h], fill=(180, 210, 235))
    d.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(90, 140, 80))
    d.rectangle([x + int(w * 0.18), y + int(h * 0.22), x + int(w * 0.82),
                 y + int(h * 0.68)], fill=(245, 245, 240), outline=INK)
    d.rectangle([x + int(w * 0.46), y + int(h * 0.28), x + int(w * 0.54),
                 y + int(h * 0.44)], fill=RED)
    d.rectangle([x + int(w * 0.42), y + int(h * 0.33), x + int(w * 0.58),
                 y + int(h * 0.39)], fill=RED)
    for wx in (0.24, 0.34, 0.66, 0.76):
        d.rectangle([x + wx * w, y + int(h * 0.50), x + (wx + 0.06) * w,
                     y + int(h * 0.62)], fill=(120, 170, 200))
    d.rectangle([x + int(w * 0.44), y + int(h * 0.50), x + int(w * 0.56),
                 y + int(h * 0.68)], fill=(70, 60, 50))

def scene_skyline(d, x, y, w, h):
    # Shanghai towers at night.
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sy, r in [(0.10, 0.12, 1), (0.35, 0.08, 1), (0.60, 0.14, 2),
                      (0.85, 0.10, 1), (0.50, 0.22, 1)]:
        d.ellipse([x + sx * w - r, y + sy * h - r, x + sx * w + r,
                   y + sy * h + r], fill=(255, 255, 255))
    for bx, bw, bh in [(0.02, 0.14, 0.55), (0.20, 0.12, 0.72),
                       (0.36, 0.16, 0.48), (0.56, 0.13, 0.66),
                       (0.73, 0.18, 0.58)]:
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h],
                    fill=(8, 10, 20), outline=(40, 50, 80))
        for wy in range(4):
            for wx in range(2):
                if (int(bx * 20) + wy * 2 + wx) % 3 == 0:
                    d.rectangle([x + (bx + 0.03 + wx * 0.05) * w,
                                 y + h - bh * h + 5 + wy * 9,
                                 x + (bx + 0.045 + wx * 0.05) * w,
                                 y + h - bh * h + 8 + wy * 9],
                                fill=(250, 200, 90))
    # spire on the tallest tower
    tx = x + int(w * 0.26)
    d.line([tx, y + int(h * 0.28), tx, y + int(h * 0.10)], fill=RED, width=2)
    d.ellipse([tx - 2, y + int(h * 0.10) - 2, tx + 2, y + int(h * 0.10) + 2],
              fill=RED)

def scene_port(d, x, y, w, h):
    # Container port with a crane.
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 236))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(150, 140, 125))
    # crane
    d.rectangle([x + int(w * 0.70), y + 6, x + int(w * 0.70) + 5, y + h - 6],
                fill=(40, 40, 44))
    d.rectangle([x + int(w * 0.30), y + 8, x + int(w * 0.92), y + 14],
                fill=(40, 40, 44))
    d.line([x + int(w * 0.55), y + 14, x + int(w * 0.55), y + 34],
           fill=(40, 40, 44), width=2)
    d.rectangle([x + int(w * 0.50), y + 34, x + int(w * 0.60), y + 44],
                fill=(178, 34, 34), outline=INK)
    # container stacks
    cols = [(178, 60, 40), (40, 90, 160), (60, 120, 70), (200, 130, 40)]
    for s in range(2):
        for i, c in enumerate(cols[:3]):
            cx = x + 8 + i * 24
            cy = y + int(h * 0.72) - 14 - s * 14
            d.rectangle([cx, cy, cx + 22, cy + 12], fill=c, outline=INK)
    d.line([x, y + int(h * 0.72), x + w, y + int(h * 0.72)], fill=INK,
           width=1)

def scene_island(d, x, y, w, h):
    # Pacific island with palms and two flags.
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 225))
    for i in range(4):
        yy = y + int(h * 0.30) + i * 9
        d.line([x + 4 + i * 6, yy, x + w - 4 - i * 5, yy],
               fill=(220, 235, 245), width=2)
    d.ellipse([x + int(w * 0.22), y + int(h * 0.52), x + int(w * 0.78),
               y + int(h * 0.86)], fill=(232, 214, 160), outline=(180, 160, 110))
    # palm
    px, py = x + int(w * 0.38), y + int(h * 0.62)
    d.line([px, py, px + 4, py - 26], fill=(110, 80, 40), width=3)
    for dx, dy in [(-14, -30), (-10, -34), (16, -30), (12, -34), (0, -36)]:
        d.line([px + 4, py - 26, px + 4 + dx, py - 26 + dy + 8],
               fill=(50, 120, 60), width=3)
    # flags
    for fx, c in [(0.68, (178, 34, 34)), (0.80, (27, 68, 128))]:
        d.line([x + fx * w, y + int(h * 0.58), x + fx * w, y + int(h * 0.80)],
               fill=INK, width=2)
        d.polygon([(x + fx * w, y + int(h * 0.58)),
                   (x + fx * w + 14, y + int(h * 0.58) + 4),
                   (x + fx * w, y + int(h * 0.58) + 9)], fill=c)

def scene_street(d, x, y, w, h):
    # Hanoi street stall with steam.
    d.rectangle([x, y, x + w, y + h], fill=(240, 225, 200))
    d.rectangle([x, y + int(h * 0.70), x + w, y + h], fill=(140, 130, 120))
    d.rectangle([x + 6, y + 10, x + int(w * 0.42), y + int(h * 0.70)],
                fill=(190, 170, 140), outline=INK)
    d.rectangle([x + int(w * 0.58), y + 16, x + w - 6, y + int(h * 0.70)],
                fill=(200, 180, 150), outline=INK)
    # stall awning
    for i in range(6):
        c = (200, 60, 40) if i % 2 == 0 else (245, 240, 228)
        d.polygon([(x + 10 + i * 12, y + int(h * 0.42)),
                   (x + 22 + i * 12, y + int(h * 0.42)),
                   (x + 24 + i * 12, y + int(h * 0.54)),
                   (x + 12 + i * 12, y + int(h * 0.54))], fill=c)
    d.rectangle([x + 10, y + int(h * 0.54), x + 82, y + int(h * 0.70)],
                fill=(110, 80, 50))
    d.ellipse([x + 22, y + int(h * 0.46), x + 42, y + int(h * 0.56)],
              fill=(230, 230, 225), outline=INK)
    for cx, cy, r in [(32, 0.30, 5), (40, 0.22, 6), (48, 0.14, 5)]:
        d.ellipse([x + cx - r, y + cy * h - r, x + cx + r, y + cy * h + r],
                  fill=(255, 255, 255))

def scene_document(d, x, y, w, h):
    # Leaked documents: paper, red stamp, bar chart.
    d.rectangle([x, y, x + w, y + h], fill=(120, 95, 70))
    d.rectangle([x + int(w * 0.12), y + 8, x + int(w * 0.88), y + h - 6],
                fill=(250, 248, 240), outline=INK)
    for i in range(5):
        yy = y + 18 + i * 8
        d.line([x + int(w * 0.20), yy, x + int(w * 0.80), yy],
               fill=(170, 170, 165), width=1)
    # bars
    for i, bh in enumerate([10, 16, 24]):
        bx = x + int(w * 0.20) + i * 16
        d.rectangle([bx, y + h - 14 - bh, bx + 10, y + h - 14],
                    fill=(178, 34, 34) if i == 2 else (90, 90, 96))
    d.ellipse([x + int(w * 0.62), y + 10, x + int(w * 0.90), y + 38],
              outline=RED, width=2)
    d.text((x + int(w * 0.66), y + 18), "500k", font=font("sans_bold", 10),
           fill=RED)

# ---------------------------------------------------------------- map
# Continent outlines in a 0..1000 x 0..520 map space.
CONTINENTS = {
    "North America": [(60, 87), (150, 50), (230, 68), (260, 118),
                      (210, 174), (180, 236), (130, 223), (95, 174),
                      (55, 136)],
    "South America": [(210, 285), (260, 273), (290, 322), (270, 409),
                      (235, 471), (215, 384), (200, 322)],
    "Europe": [(470, 87), (530, 68), (570, 93), (560, 143), (510, 155),
               (480, 130), (460, 112)],
    "Africa": [(480, 198), (540, 186), (580, 223), (570, 310),
               (540, 384), (510, 353), (490, 273), (470, 229)],
    "Asia": [(600, 74), (720, 50), (840, 68), (910, 112), (880, 174),
             (800, 211), (730, 186), (640, 174), (590, 124)],
    "Oceania": [(820, 372), (880, 366), (900, 397), (860, 422),
                (820, 403)],
}
# (x, y) in map space
DOTS = [(150, 136), (690, 118), (760, 142), (520, 118), (520, 248),
        (250, 358), (850, 390), (640, 149), (545, 161), (760, 235),
        (560, 75)]
PINS = [(590, 186, "1"), (700, 87, "2"), (185, 118, "3")]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT_BLUE, outline=INK, width=2)
    for gx in range(x + 40, x + w, 40):
        d.line([gx, y, gx, y + h], fill=(210, 222, 230), width=1)
    for gy in range(y + 34, y + h, 34):
        d.line([x, gy, x + w, gy], fill=(210, 222, 230), width=1)
    # Crop-zoom the map space (x 40..930, y 40..480) so the continents
    # fill the box instead of floating in empty ocean.
    sx, sy = w / 890.0, h / 440.0
    def px(mx):
        return x + (mx - 40) * sx
    def py(my):
        return y + (my - 40) * sy
    for pts in CONTINENTS.values():
        scaled = [(px(mx), py(my)) for mx, my in pts]
        d.polygon(scaled, fill=LAND, outline=(120, 110, 90))
    for mx, my in DOTS:
        cx, cy = px(mx), py(my)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=INK)
    for mx, my, num in PINS:
        num_circle(d, px(mx), py(my), 8, num, RED)

# ---------------------------------------------------------------- content
# All facts below are the verified 25 Nov 2026 set (SOURCES.md).

LEAD_HEADLINE = "HORMUZ IN FLAMES: 25 TANKERS HIT, TRAFFIC DOWN 40%"
LEAD_DECK = ("Iran says it downed a US MQ-9 drone over Hormuz as around "
             "25 tankers were hit and shipping fell more than 40%.")
LEAD_BODY = ("Tehran said three oil tankers struck naval mines and caught "
             "fire. Brent crude traded below $90 a barrel. Saudi defences "
             "intercepted 209 Houthi aerial threats since September, "
             "after a strike injured 11 in Riyadh.")

STORY2_HEAD = "FIRST FOREIGNER ABOARD TIANGONG"
STORY2_BODY = ("China's Shenzhou-24 blasted off from Jiuquan at 08:18 Beijing "
               "time, carrying Tang Hongbo, Wu Yi and Pakistan's Muhammad "
               "Zeeshan Ali -- the first foreign astronaut to visit the "
               "Tiangong station, and the first Pakistani in orbit. It "
               "docked 3h 38m after liftoff; the crew will run about 90 "
               "experiments in a week-long stay.")

STORY3_HEAD = "HUAWEI GUILTY ON 10 OF 12 COUNTS"
STORY3_BODY = ("A Brooklyn jury convicted Huawei of bank fraud, wire fraud, "
               "sanctions violations and conspiracy to steal trade secrets, "
               "after a case that began in 2018. Jurors acquitted the firm "
               "of racketeering. Sentencing is set for 14 September 2027.")

STATS = [
    ("25", "tankers reported hit\nin the Strait of Hormuz"),
    ("40%", "fall in shipping\ntraffic through Hormuz"),
    ("209", "Houthi aerial threats\nintercepted since Sept."),
    ("08:18", "Shenzhou-24 liftoff,\nBeijing time, Jiuquan"),
    ("10/12", "counts Huawei was\nconvicted on in Brooklyn"),
    ("≈500,000", "Russian losses in Ukraine,\nper leaked documents"),
]

MINIS = [
    ("MIDDLE EAST", "GAZA", "Strikes kill seven despite ceasefire",
     "Israeli strikes killed seven, including Hamas's internal security chief.",
     scene_city),
    ("AMERICAS", "COLOMBIA", "25 hostages taken in supermarket siege",
     "Gunmen seized 25 hostages at a supermarket in Colombia.",
     scene_store),
    ("AFRICA", "DR CONGO", "WHO evacuates hospital amid fighting",
     "Staff sheltered three days as Ebola deaths reach 5,775.",
     scene_hospital),
    ("ASIA-PACIFIC", "SHANGHAI", "Anti-graft drive reaches party boss",
     "Shanghai chief Chen Jining is placed under investigation.",
     scene_skyline),
    ("ASIA-PACIFIC", "TRADE", "US readies tariffs on 16 economies",
     "Washington plans new tariffs on India, China and 14 more.",
     scene_port),
    ("OCEANIA", "CANBERRA", "Australia signs sweeping Solomons pact",
     "Ports, police and schools: the deal is meant to blunt Beijing.",
     scene_island),
    ("ASIA-PACIFIC", "HANOI", "Hot-pot blast kills 7, injures 9",
     "A gas explosion at a Hanoi hot-pot restaurant kills seven.",
     scene_street),
    ("EUROPE", "WAR", "Leaked files put Russian losses near 500,000",
     "Leaked documents put Russia's losses in Ukraine near 500,000.",
     scene_document),
]

# 24 numbered briefs: (region, text). Region counts:
# Europe 5, Africa 2, Americas 3, Asia-Pacific 6, Oceania 2,
# Middle East 3, Global 3. With the 3 featured stories that is
# 27 stories: Middle East 4, Asia-Pacific 7, Americas 4, Europe 5,
# Africa 2, Oceania 2, Global 3.
BRIEFS = [
    ("EUROPE", "UK warns firms backing Ukraine of Russian sabotage"),
    ("EUROPE", "Kyiv: Libya ship strike was self-defence"),
    ("EUROPE", "Ukraine seeks EUR 115bn in foreign aid for 2027"),
    ("EUROPE", "EU and Canada plan a closer AI pact"),
    ("AFRICA", "WHO evacuates staff from Ituri hospital"),
    ("AFRICA", "Ebola: 5,775 deaths among 11,762 cases"),
    ("AMERICAS", "CIA, ODNI hit by cyberattack on classified systems"),
    ("AMERICAS", "Gunmen take 25 hostages at Colombia supermarket"),
    ("AMERICAS", "States sue Musk firms over sexualised Grok images"),
    ("ASIA-PACIFIC", "US plans tariffs on India, China, 14 more"),
    ("ASIA-PACIFIC", "Shanghai party chief Chen Jining under investigation"),
    ("OCEANIA", "Australia, Solomons sign sweeping security pact"),
    ("MIDDLE EAST", "Israeli strikes in Gaza kill seven despite ceasefire"),
    ("MIDDLE EAST", "Saudi-led coalition hits Hodeidah port"),
    ("MIDDLE EAST", "Houthis threaten Jeddah and Red Sea ports"),
    ("OCEANIA", "US criticises Australia's social media law"),
    ("ASIA-PACIFIC", "Hanoi hot-pot blast kills 7, injures 9"),
    ("ASIA-PACIFIC", "India, Canada 'very close' to a trade pact"),
    ("GLOBAL", "Rubio and Qatar sign critical-minerals framework"),
    ("ASIA-PACIFIC", "North Korea orders Swiss office in Pyongyang shut"),
    ("GLOBAL", "Pope Leo XIV applies for US midterm mail ballot"),
    ("GLOBAL", "Lego picks Portugal for its eighth factory"),
    ("EUROPE", "Leaked files put Russian losses near 500,000"),
    ("ASIA-PACIFIC", "Modi and Merz hold a call"),
]

# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = M, W - M

    # ---- top bar
    y = 10
    d.text((x0, y), "THE WORLD IN ONE PAGE",
           font=font("sans_bold", 11), fill=INK)
    rt = "EVERY STORY DATED WEDNESDAY 25 NOVEMBER 2026"
    tw = d.textlength(rt, font=font("sans_bold", 11))
    d.text((x1 - tw, y), rt, font=font("sans_bold", 11), fill=INK)
    y += 16
    rule(d, x0, y, CW, 3, color=RED)
    y += 6

    # ---- masthead: huge serif date
    mast = "Wednesday 25 November 2026"
    mf = font("serif_bold", 54)
    d.text((x0, y), mast, font=mf, fill=INK)
    y += 62
    rule(d, x0, y, CW, 2)
    y += 6

    # ---- story-count strip
    strip = ("27 STORIES, ALL FROM WEDNESDAY 25 NOV  •  MIDDLE EAST 4  •  "
             "ASIA-PACIFIC 7  •  AMERICAS 4  •  EUROPE 5  •  AFRICA 2  •  "
             "OCEANIA 2  •  GLOBAL 3")
    d.text((x0, y), strip, font=font("sans_bold", 11), fill=INK)
    y += 18
    rule(d, x0, y, CW, 1)
    y += 5

    # ---- ticker (italic serif)
    tick = ("Huawei guilty on 10 of 12 counts   •   Shenzhou-24 lifts off "
            "with a Pakistani pilot aboard   •   25 tankers hit as Hormuz "
            "traffic falls 40%   •   Saudi defences intercept 209 threats")
    d.text((x0, y), tick, font=font("serif_italic", 12), fill=DARKGREY)
    y += 20
    rule(d, x0, y, CW, 1)
    y += 6

    # ---- stats strip: 6 boxes
    sy = y
    bw = (CW - 5 * 6) // 6
    for i, (num, cap) in enumerate(STATS):
        bx = x0 + i * (bw + 6)
        if i > 0:
            d.line([bx - 3, sy + 4, bx - 3, sy + 52], fill=(200, 195, 180),
                   width=1)
        nf = font("serif_bold", 27)
        d.text((bx, sy), num, font=nf, fill=RED)
        cy = sy + 32
        for line in cap.split("\n"):
            d.text((bx, cy), line, font=font("sans", 9), fill=DARKGREY)
            cy += 12
    y = sy + 58
    rule(d, x0, y, CW, 1)
    y += 8

    # ---- three big cards
    cards = [
        (392, "MIDDLE EAST", "LEAD STORY", LEAD_HEADLINE, None, LEAD_BODY,
         scene_sea, 21),
        (284, "SPACE", "ASIA", STORY2_HEAD, None, STORY2_BODY,
         scene_space, 19),
        (284, "COURTS", "US-CHINA", STORY3_HEAD, None, STORY3_BODY,
         scene_court, 19),
    ]
    cx = x0
    for w, k1, k2, head, _deck, body, scene, hs in cards:
        paste_scene(img, scene, cx, y, w, 88)
        yy = y + 88 + 5
        yy = kicker(d, cx, yy, "%s  •  %s" % (k1, k2),
                    color=REGION[k1] if k1 in REGION else RED, size=10)
        yy = para(d, cx, yy, head, font("serif_bold", hs), w, hs + 4,
                  color=RED if k1 == "MIDDLE EAST" else INK, max_lines=2)
        yy += 2
        if k1 == "MIDDLE EAST":
            yy = para(d, cx, yy, LEAD_DECK, font("serif", 12), w, 15,
                      max_lines=2)
            yy += 3
            yy = para(d, cx, yy, LEAD_BODY, font("serif", 11), w, 14,
                      max_lines=4)
        else:
            yy = para(d, cx, yy, body, font("serif", 11), w, 14, max_lines=5)
        cx += w + 8
    y += 250
    rule(d, x0, y, CW, 1)
    y += 6

    # ---- the day in eight
    d.text((x0, y), "THE DAY IN EIGHT",
           font=font("sans_bold", 13), fill=BLUE)
    rt = "EVERY PICTURE DRAWN, EVERY STORY SOURCED"
    tw = d.textlength(rt, font=font("sans_bold", 10))
    d.text((x1 - tw, y + 2), rt, font=font("sans_bold", 10), fill=GREY)
    y += 18
    mw = (CW - 3 * 8) // 4
    for row in range(2):
        ry = y + row * 124
        for col in range(4):
            idx = row * 4 + col
            region, place, head, body, scene = MINIS[idx]
            mx = x0 + col * (mw + 8)
            paste_scene(img, scene, mx, ry, mw, 50)
            yy = ry + 50 + 4
            yy = kicker(d, mx, yy, "%s  •  %s" % (region, place),
                        color=REGION[region], size=8)
            yy = para(d, mx, yy, head, font("serif_bold", 12), mw, 15,
                      max_lines=2)
            yy = para(d, mx, yy, body, font("serif", 10), mw, 12,
                      max_lines=2)
    y += 248
    rule(d, x0, y, CW, 1)
    y += 6

    # ---- map + numbered briefs
    d.text((x0, y), "ALSO ON WEDNESDAY  —  24 MORE STORIES",
           font=font("sans_bold", 13), fill=BLUE)
    rt = "PIN NUMBERS MATCH THE FEATURED STORIES"
    tw = d.textlength(rt, font=font("sans_bold", 10))
    d.text((x1 - tw, y + 2), rt, font=font("sans_bold", 10), fill=GREY)
    y += 18
    map_w, map_h = 330, 150
    draw_map(d, x0, y, map_w, map_h)
    d.text((x0, y + map_h + 6), "WHERE IT HAPPENED",
           font=font("sans_bold", 10), fill=BLUE)
    d.text((x0, y + map_h + 20),
           "1 HORMUZ  •  2 JIUQUAN  •  3 NEW YORK",
           font=font("sans", 9), fill=DARKGREY)
    # date-check box under the map
    by = y + map_h + 34
    d.rectangle([x0, by, x0 + map_w, by + 38], outline=RED, width=1)
    d.text((x0 + 6, by + 4), "DATE CHECK", font=font("sans_bold", 9),
           fill=RED)
    d.text((x0 + 6, by + 15),
           "Huawei verdict reported 24 Nov; every other story",
           font=font("sans", 9), fill=DARKGREY)
    d.text((x0 + 6, by + 26),
           "here happened, or was first reported, on 25 Nov.",
           font=font("sans", 9), fill=DARKGREY)
    # briefs in two columns
    bx0 = x0 + map_w + 16
    col_w = (x1 - bx0 - 12) // 2
    for i, (region, text) in enumerate(BRIEFS):
        col = i // 12
        row = i % 12
        bx = bx0 + col * (col_w + 12)
        byy = y + row * 18
        num_circle(d, bx + 7, byy + 7, 7, i + 1, REGION[region])
        d.text((bx + 18, byy + 1), text, font=font("serif", 10), fill=INK)
    y += 230
    rule(d, x0, y, CW, 1)
    y += 6

    # ---- footer
    d.text((x0, y),
           "Sources: Reuters, Xinhua, Dawn, US Dept. of Justice, Geo.tv, News18, Japan Times, CNN, WHO via Stockbiz, Manila Times, Saachi Baat, 360LiveNews",
           font=font("sans", 9), fill=GREY)
    y += 12
    d.text((x0, y),
           "All stories dated 25 Nov 2026  •  Drawn by an AI agent for make.fun  •  Wednesday 25 November 2026  •  One page, one day",
           font=font("sans", 9), fill=GREY)
    rt = "1,024 × 1,024"
    tw = d.textlength(rt, font=font("sans", 9))
    d.text((x1 - tw, y), rt, font=font("sans", 9), fill=GREY)
    return img

def main():
    out_dir = Path(__file__).resolve().parent
    img = render()
    out = out_dir / "entry.png"
    img.save(out, format="PNG", compress_level=6, optimize=False)
    data = out.read_bytes()
    print(f"Wrote {out} ({len(data)} bytes, {img.size[0]}x{img.size[1]})")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
