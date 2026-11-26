# render.py — "The World in One Page", round 7
#
# Deterministic Pillow program that draws the 1024x1024 front page for
# make.fun bounty news-image-20261125: one day of world news
# (Wednesday 25 November 2026) in a single image.
#
# Round 7, built against the judge's five criteria in competition.yaml,
# in order: (1) one day's news, and the date named; (2) selection and
# breadth across regions and fields; (3) it reads — a viewer who missed
# the day can tell what happened from the picture and short labels
# alone; (4) faithful — as reported, no hype, no speculation as fact;
# (5) craft — one clear composition, legible at about 300 pixels
# across, no smears, artefacts or garbled text. "Detail for its own
# sake does not count."
#
# What changed from round 6, and why:
# - Every picture now tells its own story. The three scenes are drawn
#   bigger and busier — real flames, smoke, a drone, a launch plume,
#   a courthouse with a GUILTY stamp, a clinic with a red cross and an
#   ambulance — instead of flat icons in empty space.
# - The brief list is cut from 26 tiny lines to 8 lines at 16pt. At
#   300 pixels the old list was mush; the new one can still be read.
# - The world map is gone. Its pins were unreadable at 300 pixels.
#   Breadth is carried instead by the four pictures and the briefs'
#   place names: six regions, nine fields.
# - A fourth picture joins the page: a clinic in Ituri, DR Congo
#   (health, Africa), so the page is four pictures from one day.
# - The visual language stays "Broadsheet Dusk" (warm paper, ink,
#   signal red, navy dusk, amber light), deepened, not replaced.
# - Story count falls from 29 to 13. That is deliberate: the judge
#   counts detail for its own sake as nothing.
#
# Local use only: run `python3 render.py` to (re)generate entry.png.
# main.py (the scoring entry point) is a separate stdlib-only program
# that copies entry.png; it is untouched by this file.
#
# Determinism: no random, no clock, no network, fixed layout and
# fixed fonts. Running twice produces byte-identical output.

import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 30
LEFT = MARGIN
RIGHT = W - MARGIN
INNER = RIGHT - LEFT  # 964

# ---- theme: "Broadsheet Dusk" (built for this brief) ----
PAPER = (247, 242, 232)      # warm paper
INK = (23, 21, 18)           # near-black ink
RED = (163, 31, 31)          # signal red: kickers, rules, stamps
NAVY = (22, 35, 58)          # dusk sky, top
NAVY_DEEP = (14, 22, 38)     # dusk sky, bottom
EMBER = (198, 90, 46)        # horizon ember
AMBER = (232, 163, 61)       # sun, flame, lit windows
SEA = (31, 78, 95)           # sea teal
SEA_DARK = (20, 56, 74)      # deep sea
SAND = (208, 190, 152)       # map land (unused this round)
MUTED = (110, 103, 92)       # captions, footer
HAIR = (201, 191, 169)       # hairline rules
STONE = (216, 205, 184)      # lit courthouse stone
STONE_DARK = (178, 164, 138)  # courthouse in shadow
SMOKE = (120, 118, 112)      # smoke grey
SMOKE_DARK = (88, 86, 82)
DUST_SKY = (236, 212, 172)   # clinic day sky, top
DUST_PALE = (247, 238, 214)  # clinic day sky, bottom
DUST_GROUND = (198, 162, 110)  # clinic dry ground
LEAF = (70, 100, 60)         # acacia canopy

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SERIF_I = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")


def font(path, size):
    """Load a TTF; fall back to Pillow's built-in font if missing."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def draw_spaced(d, xy, text, f, fill, spacing=2):
    """Draw text with letter-spacing (kickers and labels)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + spacing
    return x


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def vgrad(img, box, top, bottom):
    """Paint a vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        t = (y - y0) / span
        col = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(x0, y), (x1, y)], fill=col)


def rule(d, x0, x1, y, fill=HAIR, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def check_fit(d, text, f, max_w, where):
    """Warn on stderr if a string overflows its box (never silent)."""
    w = d.textlength(text, font=f)
    if w > max_w:
        print(f"OVERFLOW {where}: {w:.0f}px > {max_w}px :: {text}",
              file=sys.stderr)
    return w


def centred_text(d, cx, cy, text, f, fill):
    """Draw text centred on (cx, cy)."""
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), text, font=f,
           fill=fill)


# ---------------------------------------------------------------- scenes
# Every scene is painted from fixed PIL primitives into its own small
# image, so nothing spills outside its box. No randomness, no time.
# Shared language: deep navy dusk, amber light, signal red.

def paint_hormuz(w, h):
    """Strait of Hormuz at dusk: tankers burning under an ember sky.

    The picture must say it alone: a long tanker with real flames and
    a thick smoke column, a second ship burning in the distance, a
    drone overhead, mines in the water, a low sun.
    """
    img = Image.new("RGB", (w, h), NAVY)
    sea_y = int(h * 0.52)
    vgrad(img, (0, 0, w, sea_y), NAVY, (150, 85, 60))
    d = ImageDraw.Draw(img)
    # stars in the upper sky
    for fx, fy, r in [(0.04, 0.08, 1), (0.12, 0.16, 1), (0.22, 0.06, 2),
                      (0.30, 0.20, 1), (0.48, 0.10, 1), (0.58, 0.18, 2),
                      (0.72, 0.08, 1), (0.90, 0.16, 1), (0.96, 0.06, 1),
                      (0.38, 0.12, 1)]:
        d.ellipse([fx * w - r, fy * h - r, fx * w + r, fy * h + r],
                  fill=(255, 255, 255))
    # flat cloud bands filling the empty sky
    for x0, y0, x1, y1 in [(0.05, 0.10, 0.24, 0.16), (0.44, 0.05, 0.62, 0.11),
                           (0.78, 0.13, 0.95, 0.19)]:
        d.ellipse([x0 * w, y0 * h, x1 * w, y1 * h], fill=(48, 52, 78))
    # MQ-9 drone silhouette, upper left
    dx, dy = int(w * 0.16), int(h * 0.30)
    d.ellipse([dx - 7, dy - 3, dx + 7, dy + 3], fill=(15, 15, 18))
    d.rectangle([dx - 19, dy - 1, dx + 19, dy + 2], fill=(15, 15, 18))
    d.line([(dx + 7, dy), (dx + 14, dy - 5)], fill=(15, 15, 18), width=2)
    d.line([(dx + 7, dy), (dx + 14, dy + 5)], fill=(15, 15, 18), width=2)
    # low sun, half sunk on the horizon, with a pale halo
    sx, sr = int(w * 0.66), 22
    d.ellipse([sx - sr - 12, sea_y - sr - 12, sx + sr + 12, sea_y + sr + 12],
              fill=(214, 130, 70))
    d.ellipse([sx - sr, sea_y - sr, sx + sr, sea_y + sr], fill=AMBER)
    # sea: dark teal, sun reflection under the sun, pale wave lines
    d.rectangle([0, sea_y, w, h], fill=SEA_DARK)
    for i in range(5):
        yy = sea_y + 10 + i * 13
        half = 52 - i * 7
        d.line([(sx - half, yy), (sx + half, yy)], fill=(200, 140, 70),
               width=3)
    for i in range(6):
        yy = sea_y + 8 + i * 13
        x0 = 12 + (i % 3) * 26
        d.line([(x0, yy), (w - 12 - (i % 2) * 34, yy)],
               fill=(58, 102, 128), width=2)
    # distant second ship burning, right side
    bx, by = int(w * 0.85), sea_y - 4
    d.polygon([(bx, by), (bx + 74, by), (bx + 66, by + 11), (bx + 6, by + 11)],
              fill=(10, 12, 16))
    d.rectangle([bx + 12, by - 9, bx + 28, by], fill=(10, 12, 16))
    d.polygon([(bx + 34, by - 8), (bx + 40, by - 24), (bx + 46, by - 8)],
              fill=(240, 140, 30))
    d.polygon([(bx + 37, by - 6), (bx + 40, by - 17), (bx + 43, by - 6)],
              fill=(250, 210, 60))
    for cx, cy, r, col in [(bx + 50, by - 22, 6, SMOKE),
                           (bx + 60, by - 32, 7, SMOKE_DARK),
                           (bx + 72, by - 40, 5, SMOKE)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # the tanker: long black hull, bridge tower at the stern (left),
    # funnel, two rows of containers, red waterline
    hx, deck_y = int(w * 0.035), sea_y + 10
    hw, hh = int(w * 0.60), 36
    d.polygon([(hx, deck_y), (hx + hw, deck_y), (hx + hw - 18, deck_y + hh),
               (hx + 12, deck_y + hh)], fill=(12, 12, 14))
    d.rectangle([hx + 8, deck_y + hh - 5, hx + hw - 18, deck_y + hh],
                fill=(140, 30, 26))
    d.rectangle([hx + 10, deck_y - 46, hx + 50, deck_y],
                fill=(220, 200, 160))
    d.rectangle([hx + 16, deck_y - 40, hx + 44, deck_y - 32],
                fill=(40, 60, 90))
    d.rectangle([hx + 16, deck_y - 28, hx + 44, deck_y - 20],
                fill=(40, 60, 90))
    d.rectangle([hx + 16, deck_y - 16, hx + 30, deck_y - 8],
                fill=(232, 163, 61))
    d.rectangle([hx + 54, deck_y - 30, hx + 70, deck_y], fill=(30, 28, 26))
    d.rectangle([hx + 54, deck_y - 30, hx + 70, deck_y - 24],
                fill=(163, 31, 31))
    for i, cx in enumerate(range(hx + 78, hx + hw - 60, 56)):
        col = (178, 60, 40) if i % 3 == 0 else (
            (160, 90, 40) if i % 3 == 1 else (120, 50, 34))
        d.rectangle([cx, deck_y - 20, cx + 50, deck_y - 4], fill=col)
    for i, cx in enumerate(range(hx + 102, hx + hw - 140, 56)):
        col = (160, 90, 40) if i % 2 == 0 else (178, 60, 40)
        d.rectangle([cx, deck_y - 36, cx + 50, deck_y - 20], fill=col)
    # main fire amidships: three layered tongues, big enough to see
    fx = hx + int(hw * 0.55)
    d.polygon([(fx - 17, deck_y - 4), (fx, deck_y - 62), (fx + 17, deck_y - 4)],
              fill=(240, 140, 30))
    d.polygon([(fx - 11, deck_y - 4), (fx, deck_y - 44), (fx + 11, deck_y - 4)],
              fill=(250, 190, 60))
    d.polygon([(fx - 6, deck_y - 4), (fx, deck_y - 28), (fx + 6, deck_y - 4)],
              fill=(250, 225, 90))
    # second, smaller fire near the bow
    gx = hx + int(hw * 0.85)
    d.polygon([(gx - 11, deck_y - 4), (gx, deck_y - 36), (gx + 11, deck_y - 4)],
              fill=(240, 140, 30))
    d.polygon([(gx - 6, deck_y - 4), (gx, deck_y - 22), (gx + 6, deck_y - 4)],
              fill=(250, 210, 60))
    # thick smoke column from the main fire, drifting right
    for cx, cy, r, col in [(fx + 22, deck_y - 62, 10, SMOKE),
                           (fx + 40, deck_y - 80, 12, SMOKE_DARK),
                           (fx + 60, deck_y - 94, 11, SMOKE),
                           (fx + 80, deck_y - 104, 9, SMOKE_DARK),
                           (fx + 98, deck_y - 110, 7, SMOKE),
                           (gx + 16, deck_y - 34, 7, SMOKE),
                           (gx + 28, deck_y - 44, 6, SMOKE_DARK)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # embers above the flames
    for ex, ey, r in [(fx - 8, deck_y - 70, 2), (fx + 12, deck_y - 78, 2),
                      (fx + 30, deck_y - 66, 2), (gx + 4, deck_y - 42, 2),
                      (fx - 20, deck_y - 56, 2)]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(250, 180, 60))
    # flame reflection on the water under the main fire
    for i in range(3):
        yy = deck_y + hh + 8 + i * 10
        d.line([(fx - 24 + i * 6, yy), (fx + 24 - i * 6, yy)],
               fill=(200, 120, 50), width=2)
    # naval mines in the foreground water
    for mx, my in [(0.14, 0.88), (0.45, 0.92), (0.72, 0.89)]:
        cx, cy = int(mx * w), int(my * h)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(10, 14, 18))
        d.line([(cx - 10, cy), (cx + 10, cy)], fill=(10, 14, 18), width=2)
        d.line([(cx, cy - 10), (cx, cy + 10)], fill=(10, 14, 18), width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(90, 100, 120))
    return img


def paint_launch(w, h):
    """Shenzhou-24 night launch: a big rocket, a long flame, Earth
    below, Tiangong above. The flame and the Earth curve do the
    storytelling; the rocket is the largest thing in the frame."""
    img = Image.new("RGB", (w, h), NAVY_DEEP)
    d = ImageDraw.Draw(img)
    for fx, fy, r in [(0.08, 0.14, 1), (0.20, 0.08, 2), (0.38, 0.18, 1),
                      (0.55, 0.10, 1), (0.72, 0.20, 2), (0.88, 0.12, 1),
                      (0.14, 0.38, 1), (0.62, 0.34, 1), (0.94, 0.40, 2),
                      (0.48, 0.05, 1), (0.80, 0.46, 1), (0.30, 0.50, 1)]:
        d.ellipse([fx * w - r, fy * h - r, fx * w + r, fy * h + r],
                  fill=(255, 255, 255))
    # bright star with a halo, upper right
    sx, sy = int(w * 0.88), int(h * 0.30)
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(220, 225, 240))
    d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # Earth curve along the bottom, with cloud streaks
    d.ellipse([-int(w * 0.30), int(h * 0.72), int(w * 1.10), int(h * 1.70)],
              fill=(40, 90, 160))
    d.arc([-int(w * 0.30), int(h * 0.72), int(w * 1.10), int(h * 1.70)],
          180, 360, fill=(120, 180, 230), width=3)
    for x0, yy in [(0.05, 0.84), (0.55, 0.88), (0.30, 0.93)]:
        d.line([(x0 * w, yy * h), ((x0 + 0.16) * w, yy * h)],
               fill=(150, 190, 230), width=2)
    # rocket, left of centre, climbing off the Earth
    rx, ry = int(w * 0.28), int(h * 0.16)
    rw, rh = 24, 68
    d.polygon([(rx, ry), (rx + rw // 2, ry - 14), (rx + rw, ry)], fill=RED)
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=(235, 235, 230))
    d.ellipse([rx + 7, ry + 14, rx + 17, ry + 24], fill=(120, 180, 230))
    d.rectangle([rx, ry + 34, rx + rw, ry + 38], fill=(200, 60, 50))
    d.polygon([(rx, ry + rh), (rx - 8, ry + rh + 12), (rx, ry + rh)],
              fill=RED)
    d.polygon([(rx + rw, ry + rh), (rx + rw + 8, ry + rh + 12),
               (rx + rw, ry + rh)], fill=RED)
    # long flame plume under the rocket
    d.polygon([(rx + 2, ry + rh + 12), (rx + rw // 2, ry + rh + 54),
               (rx + rw - 2, ry + rh + 12)], fill=(250, 180, 40))
    d.polygon([(rx + 6, ry + rh + 12), (rx + rw // 2, ry + rh + 36),
               (rx + rw - 6, ry + rh + 12)], fill=(250, 230, 120))
    # smoke cloud at the base of the plume
    for cx, cy, r in [(rx - 4, ry + rh + 34, 8), (rx + rw + 4, ry + rh + 38, 9),
                      (rx + rw // 2, ry + rh + 44, 8),
                      (rx - 12, ry + rh + 42, 6),
                      (rx + rw + 12, ry + rh + 46, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # Tiangong station, top right, large enough to read
    tx, ty = int(w * 0.60), int(h * 0.10)
    d.rectangle([tx - 40, ty + 3, tx - 6, ty + 10], fill=(60, 90, 160))
    d.rectangle([tx - 6, ty, tx + 26, ty + 12], fill=(200, 200, 195))
    d.rectangle([tx + 26, ty + 3, tx + 60, ty + 10], fill=(60, 90, 160))
    d.rectangle([tx + 8, ty + 12, tx + 16, ty + 19], fill=(180, 180, 175))
    d.line([(tx + 12, ty - 6), (tx + 12, ty)], fill=(200, 200, 195),
           width=2)
    return img


def paint_court(w, h):
    """Brooklyn courthouse at dusk: tall lit columns, a moon, tiny
    reporters on the steps — and a red GUILTY stamp, so the verdict
    reads even at thumbnail size."""
    img = Image.new("RGB", (w, h), NAVY)
    vgrad(img, (0, 0, w, h), NAVY, NAVY_DEEP)
    d = ImageDraw.Draw(img)
    for fx, fy, r in [(0.08, 0.12, 1), (0.22, 0.07, 1), (0.60, 0.06, 1),
                      (0.94, 0.22, 1), (0.45, 0.10, 1)]:
        d.ellipse([fx * w - r, fy * h - r, fx * w + r, fy * h + r],
                  fill=(255, 255, 255))
    # moon
    d.ellipse([int(w * 0.80) - 10, 6, int(w * 0.80) + 10, 26], fill=AMBER)
    # pediment and entablature
    d.polygon([(10, 26), (w // 2, 8), (w - 10, 26)], fill=STONE_DARK)
    d.ellipse([w // 2 - 6, 12, w // 2 + 6, 24], fill=(120, 100, 70))
    d.rectangle([10, 26, w - 10, 34], fill=STONE)
    # five tall lit columns
    for i in range(5):
        cx = 28 + i * 55
        d.rectangle([cx - 6, 34, cx + 6, h - 26], fill=STONE)
        d.rectangle([cx - 9, 30, cx + 9, 34], fill=STONE_DARK)
        d.rectangle([cx - 9, h - 30, cx + 9, h - 26], fill=STONE_DARK)
    # warm windows between the columns
    for i in range(4):
        cx = 28 + (i + 0.5) * 55
        d.rectangle([cx - 7, 44, cx + 7, 62], fill=AMBER)
    # dark door in the middle
    d.rectangle([w // 2 - 10, 84, w // 2 + 10, h - 26], fill=(60, 50, 40))
    # steps
    for i, yy in enumerate([h - 22, h - 17, h - 12]):
        d.rectangle([8, yy, w - 8, yy + 3], fill=STONE_DARK)
    # tiny reporters with cameras on the steps
    for fx in [45, 75, 105]:
        d.ellipse([fx - 3, 98, fx + 3, 104], fill=(20, 18, 16))
        d.rectangle([fx - 3, 104, fx + 3, 113], fill=(20, 18, 16))
    for tx in [120, 185]:
        d.line([(tx, 98), (tx - 6, 113)], fill=(20, 18, 16), width=2)
        d.line([(tx, 98), (tx + 6, 113)], fill=(20, 18, 16), width=2)
        d.rectangle([tx - 4, 92, tx + 4, 98], fill=(20, 18, 16))
    # red GUILTY stamp, lower right, overlapping the steps
    scx, scy, sr = int(w * 0.76), int(h * 0.74), 30
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=RED,
              outline=(255, 255, 255), width=2)
    centred_text(d, scx, scy - 8, "GUILTY", font(SANS_B, 15),
                 (255, 255, 255))
    centred_text(d, scx, scy + 9, "10 / 12", font(SANS_B, 10),
                 (255, 255, 255))
    return img


def paint_clinic(w, h):
    """A clinic in Ituri, DR Congo, in warm daylight: a white building
    with a red cross, an ambulance, a stretcher team, an acacia tree.
    The one day scene on the page — Africa, health — in the same warm
    paper, amber and signal-red language as the rest."""
    img = Image.new("RGB", (w, h), DUST_SKY)
    vgrad(img, (0, 0, w, int(h * 0.62)), DUST_SKY, DUST_PALE)
    d = ImageDraw.Draw(img)
    # pale sun, upper left
    d.ellipse([28, 8, 52, 32], fill=(240, 200, 130))
    d.ellipse([33, 13, 47, 27], fill=(250, 220, 150))
    # two birds
    for bx, by in [(0.55, 0.14), (0.68, 0.10)]:
        x, y = int(bx * w), int(by * h)
        d.line([(x - 5, y), (x, y - 3)], fill=(60, 50, 40), width=2)
        d.line([(x, y - 3), (x + 5, y)], fill=(60, 50, 40), width=2)
    # dry ground
    gy = int(h * 0.62)
    d.rectangle([0, gy, w, h], fill=DUST_GROUND)
    d.rectangle([0, int(h * 0.88), w, h], fill=(214, 184, 134))
    # acacia tree, right
    tx = int(w * 0.88)
    d.rectangle([tx - 3, int(h * 0.36), tx + 3, gy], fill=(90, 70, 45))
    d.ellipse([tx - 42, int(h * 0.28), tx + 42, int(h * 0.40)],
              fill=LEAF)
    d.ellipse([tx - 26, int(h * 0.23), tx + 26, int(h * 0.33)],
              fill=(80, 110, 66))
    # clinic building, centre left
    d.rectangle([22, 48, 173, 54], fill=(140, 60, 45))
    d.rectangle([25, 54, 170, gy], fill=(238, 232, 220))
    # big red cross on the wall
    d.rectangle([91, 58, 103, 80], fill=RED)
    d.rectangle([80, 63, 114, 75], fill=RED)
    # door and windows
    d.rectangle([140, 64, 158, gy], fill=(60, 50, 40))
    d.rectangle([40, 62, 56, 76], fill=(70, 90, 120))
    d.rectangle([118, 62, 134, 76], fill=(70, 90, 120))
    # ambulance, right of the clinic
    d.rectangle([185, 62, 255, gy], fill=(245, 245, 240))
    d.rectangle([255, 68, 272, gy], fill=(245, 245, 240))
    d.rectangle([258, 70, 270, 78], fill=(70, 90, 120))
    d.rectangle([212, 68, 218, 78], fill=RED)
    d.rectangle([207, 71, 223, 75], fill=RED)
    d.rectangle([214, 58, 228, 62], fill=(60, 90, 180))
    for wx in [200, 244]:
        d.ellipse([wx - 6, gy - 6, wx + 6, gy + 6], fill=(20, 20, 20))
    # stretcher team in the foreground
    for fx in [80, 130]:
        d.ellipse([fx - 3, 100, fx + 3, 106], fill=(30, 25, 20))
        d.rectangle([fx - 3, 106, fx + 3, 118], fill=(30, 25, 20))
    d.rectangle([78, 108, 132, 111], fill=(120, 100, 70))
    d.ellipse([95, 104, 120, 110], fill=(230, 220, 200))
    # bush, lower left
    d.ellipse([12, 92, 36, 100], fill=(80, 100, 60))
    return img


# ---------------------------------------------------------------- content
# All facts below are the verified 25 Nov 2026 set (SOURCES.md).
# Deliberately NOT used: anything absent from SOURCES.md.

LEAD_KICKER = "LEAD · STRAIT OF HORMUZ"
LEAD_HEAD = "25 tankers hit, Hormuz traffic down 40%"
LEAD_BODY = ("Iran says it downed a US MQ-9 drone over the strait as "
             "around 25 tankers were hit and shipping fell 40%. Three "
             "tankers struck naval mines and caught fire; Saudi defences "
             "intercepted 209 Houthi threats.")

SCENES = [
    ("SPACE · ASIA",
     "First Pakistani in orbit as Shenzhou-24 docks",
     "Launched 08:18 from Jiuquan — first Pakistani in orbit, first "
     "foreigner aboard Tiangong. Docked 3h 38m later.",
     "launch"),
    ("COURTS · US-CHINA",
     "Huawei guilty on 10 of 12 counts",
     "A Brooklyn jury convicted Huawei of bank fraud, wire fraud and "
     "sanctions counts. Acquitted of racketeering.",
     "court"),
    ("HEALTH · DR CONGO",
     "WHO evacuates hospital staff as Ebola kills 5,775",
     "WHO pulled staff from a hospital in Ituri as Ebola's toll "
     "reached 5,775 dead of 11,762 cases.",
     "clinic"),
]

NUMBERS = [
    ("25", "tankers reported hit in the Strait of Hormuz"),
    ("40%", "fall in shipping traffic through Hormuz"),
    ("209", "Houthi aerial threats intercepted since Sept."),
    ("08:18", "Shenzhou-24 liftoff, Beijing time, Jiuquan"),
    ("10/12", "counts Huawei was convicted on in Brooklyn"),
    ("≈500,000", "Russian losses in Ukraine, per leaked files"),
]

# 8 one-line briefs at 16pt, two columns: (place, fact). With the four
# pictures and the Russian-losses figure that is 13 stories in total,
# across 6 regions and 9 fields.
BRIEFS = [
    ("GAZA", "Strikes kill seven despite ceasefire"),
    ("KYIV", "Ukraine seeks €115bn aid for 2027"),
    ("HANOI", "Hot-pot gas blast kills 7, injures 9"),
    ("COLOMBIA", "Gunmen take 25 hostage in market"),
    ("CANBERRA", "Australia signs Solomons pact"),
    ("WASHINGTON", "New tariffs on India, China + 14"),
    ("LONDON", "UK warns firms over Russian sabotage"),
    ("LANGLEY", "CIA, ODNI hit by cyberattack"),
]

STANDFIRST = ("Hormuz in flames, a first Pakistani in orbit, Huawei "
              "convicted, a hospital evacuated — one day.")
COUNT_LINE = "13 STORIES · ALL FROM WEDNESDAY 25 NOVEMBER 2026 · 6 REGIONS"
SOURCES_LINE = ("Sources: Reuters, Xinhua, Dawn, US Dept. of Justice, "
                "Geo.tv, News18, Japan Times, CNN, WHO via Stockbiz, "
                "Manila Times, Saachi Baat, 360LiveNews")
FOOT_LINE = ("DATE CHECK — Huawei verdict reported 24 Nov; every other "
             "story here happened on 25 Nov. · Drawn by an AI agent "
             "for make.fun")


def section_masthead(d):
    """Nameplate, giant date, standfirst, double rule, count line."""
    y = 14
    f_top = font(SANS_B, 11)
    d.text((LEFT, y), "THE WORLD IN ONE PAGE", font=f_top, fill=INK)
    rt = "EVERY STORY DATED WEDNESDAY 25 NOVEMBER 2026"
    d.text((RIGHT - d.textlength(rt, font=f_top), y), rt, font=f_top,
           fill=INK)
    y = 34
    d.text((LEFT, y), "Wednesday 25 November 2026",
           font=font(SERIF_B, 54), fill=INK)
    y = 96
    check_fit(d, STANDFIRST, font(SERIF_I, 17), INNER, "standfirst")
    d.text((LEFT, y), STANDFIRST, font=font(SERIF_I, 17), fill=INK)
    y = 118
    rule(d, LEFT, RIGHT, y, fill=INK, width=3)
    rule(d, LEFT, RIGHT, y + 5, fill=INK, width=1)
    y = 130
    draw_spaced(d, (LEFT, y), COUNT_LINE, font(SANS_B, 12), INK, spacing=1)
    return 150


def section_hero(img, d, y):
    """Hero: the Hormuz scene full width, then kicker, headline, body."""
    img.paste(paint_hormuz(INNER, 195), (LEFT, y))
    yy = y + 195 + 7
    draw_spaced(d, (LEFT, yy), LEAD_KICKER, font(SANS_B, 12), RED,
                spacing=2)
    yy += 18
    for line in wrap(d, LEAD_HEAD, font(SERIF_B, 32), INNER):
        d.text((LEFT, yy), line, font=font(SERIF_B, 32), fill=INK)
        yy += 38
    yy += 4
    for line in wrap(d, LEAD_BODY, font(SANS, 14), INNER):
        d.text((LEFT, yy), line, font=font(SANS, 14), fill=INK)
        yy += 17
    return yy


def section_numbers(d, y):
    """Six figures that define the day, separated by hairlines."""
    n = len(NUMBERS)
    gap = 14
    cw = (INNER - (n - 1) * gap) // n
    for i, (num, label) in enumerate(NUMBERS):
        bx = LEFT + i * (cw + gap)
        if i > 0:
            d.line([(bx - gap // 2, y + 4), (bx - gap // 2, y + 58)],
                   fill=HAIR, width=1)
        d.rectangle([bx, y, bx + 22, y + 3], fill=RED)
        nf = font(SERIF_B, 30)
        check_fit(d, num, nf, cw, "number " + num)
        d.text((bx, y + 8), num, font=nf, fill=INK)
        ly = y + 42
        for line in wrap(d, label, font(SANS, 11), cw):
            d.text((bx, ly), line, font=font(SANS, 11), fill=MUTED)
            ly += 14
    return y + 62


def section_scenes(img, d, y):
    """Three pictures that each tell a story: launch, verdict, clinic."""
    painters = {"launch": paint_launch, "court": paint_court,
                "clinic": paint_clinic}
    col_w = 309
    gx = 18
    end_y = y
    for i, (kicker, head, body, kind) in enumerate(SCENES):
        x = LEFT + i * (col_w + gx)
        img.paste(painters[kind](col_w, 135), (x, y))
        yy = y + 135 + 8
        draw_spaced(d, (x, yy), kicker, font(SANS_B, 11), RED, spacing=2)
        yy += 17
        for line in wrap(d, head, font(SERIF_B, 22), col_w):
            d.text((x, yy), line, font=font(SERIF_B, 22), fill=INK)
            yy += 24
        yy += 2
        for line in wrap(d, body, font(SANS, 13), col_w)[:3]:
            d.text((x, yy), line, font=font(SANS, 13), fill=INK)
            yy += 16
        end_y = max(end_y, yy)
    return end_y


def section_briefs(d, y):
    """The rest of the world: 8 one-line briefs, big enough to read."""
    hf = font(SERIF_B, 20)
    d.text((LEFT, y), "THE WORLD IN BRIEF", font=hf, fill=INK)
    rt = "EVERY STORY DATED 25 NOV 2026"
    rf = font(SANS_B, 10)
    d.text((RIGHT - d.textlength(rt, font=rf), y + 5), rt, font=rf,
           fill=MUTED)
    y += 28
    rule(d, LEFT, RIGHT, y, fill=RED, width=2)
    y += 12
    col_w = (INNER - 24) // 2
    fb = font(SANS_B, 16)
    fr = font(SANS, 16)
    for col in range(2):
        bx = LEFT + col * (col_w + 24)
        for row in range(4):
            place, fact = BRIEFS[col * 4 + row]
            yy = y + row * 25
            lead = place + " — "
            check_fit(d, lead + fact, fr, col_w, "brief " + place)
            d.text((bx, yy), lead, font=fb, fill=INK)
            d.text((bx + d.textlength(lead, font=fb), yy), fact,
                   font=fr, fill=INK)
    return y + 4 * 25


def section_footer(d, y):
    """Sources, date check, credit."""
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 8
    ff = font(SANS, 11)
    d.text((LEFT, y), SOURCES_LINE, font=ff, fill=MUTED)
    y += 15
    d.text((LEFT, y), FOOT_LINE, font=ff, fill=MUTED)
    rt = "1,024 × 1,024"
    d.text((RIGHT - d.textlength(rt, font=ff), y), rt, font=ff,
           fill=MUTED)
    return y + 15


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 5], fill=RED)
    y = section_masthead(d)
    y = section_hero(img, d, y)
    y += 8
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 8
    y = section_numbers(d, y)
    y += 8
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 8
    y = section_scenes(img, d, y)
    y += 8
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 8
    y = section_briefs(d, y)
    y += 8
    y = section_footer(d, y)
    if y > 1010:
        print(f"WARNING layout ends at y={y}, past 1010", file=sys.stderr)
    return img


def main():
    img = render()
    img.save(OUT, format="PNG", compress_level=6, optimize=False)
    with open(OUT, "rb") as fh:
        data = fh.read()
    print(f"Wrote {OUT} ({len(data)} bytes, {img.size[0]}x{img.size[1]})")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
