# render.py — "The World in One Page", round 6
#
# Deterministic Pillow program that draws the 1024x1024 front page for
# make.fun bounty news-image-20261125: one day of world news
# (Wednesday 25 November 2026) in a single image.
#
# Original design, round 6. Concept: three stories you cannot miss, six
# numbers that define the day, and the rest of the world in brief.
# One shared illustration language ("dusk": deep navy night, amber
# light, signal red) across every scene, so the page reads as drawn
# by one hand. No cards, no shadows: hairline rules and columns,
# like a broadsheet. Every fact comes from SOURCES.md; nothing new
# was invented for this round.
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

# ---- custom theme: "Broadsheet Dusk" (built for this brief) ----
PAPER = (247, 242, 232)      # warm paper
INK = (23, 21, 18)           # near-black ink
RED = (163, 31, 31)          # signal red: kickers, rules, map pins
NAVY = (22, 35, 58)          # dusk sky, top
NAVY_DEEP = (14, 22, 38)     # dusk sky, bottom
EMBER = (198, 90, 46)        # horizon ember
AMBER = (232, 163, 61)       # sun, flame, lit windows
SEA = (31, 78, 95)           # sea teal
SEA_DARK = (20, 56, 74)      # deep sea
SAND = (208, 190, 152)       # map land
SAND_LINE = (170, 152, 110)  # map outline
MUTED = (110, 103, 92)       # captions, footer
HAIR = (201, 191, 169)       # hairline rules
STONE = (216, 205, 184)      # lit courthouse stone
STONE_DARK = (178, 164, 138) # courthouse in shadow
SMOKE = (120, 118, 112)      # smoke grey
SMOKE_DARK = (88, 86, 82)

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


def ls(text, f, spacing=2):
    """Width of text drawn with letter-spacing."""
    return sum(f.getlength(ch) + spacing for ch in text) - spacing


def draw_spaced(d, xy, text, f, fill, spacing=2):
    """Draw text with letter-spacing (for kickers and labels)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + spacing
    return x


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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
        print(f"OVERFLOW {where}: {w:.0f}px > {max_w}px :: {text}", file=sys.stderr)
    return w


# ---------------------------------------------------------------- scenes
# Every scene is painted from fixed PIL primitives into its own small
# image (so nothing spills outside its box). No randomness, no time.
# Shared language: deep navy dusk, amber light, signal red.

def paint_hormuz(w, h):
    """Strait of Hormuz at dusk: a burning tanker under an ember sky."""
    img = Image.new("RGB", (w, h), NAVY)
    vgrad(img, (0, 0, w, h), NAVY, (140, 80, 60))
    d = ImageDraw.Draw(img)
    # stars in the upper sky
    for fx, fy, r in [(0.06, 0.10, 1), (0.16, 0.06, 2), (0.30, 0.14, 1),
                      (0.45, 0.08, 1), (0.58, 0.12, 2), (0.88, 0.08, 1),
                      (0.94, 0.20, 1), (0.38, 0.22, 1)]:
        d.ellipse([fx * w - r, fy * h - r, fx * w + r, fy * h + r],
                  fill=(255, 255, 255))
    sea_y = int(h * 0.55)
    # low sun, half sunk on the horizon, with a pale halo
    sx, sr = int(w * 0.70), 18
    d.ellipse([sx - sr - 10, sea_y - sr - 10, sx + sr + 10, sea_y + sr + 10],
              fill=(214, 130, 70))
    d.ellipse([sx - sr, sea_y - sr, sx + sr, sea_y + sr], fill=AMBER)
    # sea: dark teal, sun reflection under the sun, pale wave lines
    d.rectangle([0, sea_y, w, h], fill=SEA_DARK)
    for i in range(5):
        yy = sea_y + 10 + i * 14
        half = 46 - i * 6
        d.line([(sx - half, yy), (sx + half, yy)], fill=(200, 140, 70),
               width=3)
    for i in range(6):
        yy = sea_y + 8 + i * 12
        x0 = 10 + (i % 3) * 22
        d.line([(x0, yy), (w - 10 - (i % 2) * 30, yy)],
               fill=(58, 102, 128), width=2)
    # distant second ship, small and dark
    dx, dy = int(w * 0.84), sea_y - 6
    d.polygon([(dx, dy), (dx + 52, dy), (dx + 46, dy + 10), (dx + 4, dy + 10)],
              fill=(10, 12, 16))
    d.rectangle([dx + 10, dy - 10, dx + 26, dy], fill=(10, 12, 16))
    # the tanker: long black hull, slanted bow right, bridge tower at
    # the stern (left), red containers amidships
    hx, hy = int(w * 0.06), sea_y + 6
    hw, hh = int(w * 0.72), int(h * 0.17)
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 16, hy + hh),
               (hx + 10, hy + hh)], fill=(12, 12, 14))
    d.rectangle([hx + 6, hy + hh - 5, hx + hw - 16, hy + hh],
                fill=(140, 30, 26))
    d.rectangle([hx + 10, hy - 34, hx + 34, hy], fill=(220, 200, 160))
    d.rectangle([hx + 14, hy - 28, hx + 30, hy - 20], fill=(40, 60, 90))
    d.rectangle([hx + 14, hy - 18, hx + 30, hy - 10], fill=(40, 60, 90))
    for i, cx in enumerate(range(hx + 44, hx + hw - 60, 42)):
        col = (178, 60, 40) if i % 2 == 0 else (140, 44, 30)
        d.rectangle([cx, hy - 20, cx + 36, hy - 4], fill=col)
    # flame amidships and a smoke column drifting right
    fx = hx + int(hw * 0.55)
    d.polygon([(fx, hy - 34), (fx + 12, hy - 60), (fx + 24, hy - 34)],
              fill=(240, 140, 30))
    d.polygon([(fx + 6, hy - 28), (fx + 12, hy - 48), (fx + 18, hy - 28)],
              fill=(250, 210, 60))
    for cx, cy, r, col in [(fx + 30, hy - 44, 7, SMOKE),
                           (fx + 44, hy - 58, 9, SMOKE_DARK),
                           (fx + 60, hy - 70, 8, SMOKE),
                           (fx + 76, hy - 80, 6, SMOKE_DARK)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # naval mines in the foreground water
    for mx, my in [(0.16, 0.88), (0.44, 0.92), (0.70, 0.89)]:
        cx, cy = int(mx * w), int(my * h)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(10, 14, 18))
        d.line([(cx - 9, cy), (cx + 9, cy)], fill=(10, 14, 18), width=2)
        d.line([(cx, cy - 9), (cx, cy + 9)], fill=(10, 14, 18), width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(90, 100, 120))
    return img


def paint_launch(w, h):
    """Shenzhou-24 night launch: rocket, stars, Earth curve, station."""
    img = Image.new("RGB", (w, h), NAVY_DEEP)
    d = ImageDraw.Draw(img)
    for fx, fy, r in [(0.08, 0.14, 1), (0.20, 0.08, 2), (0.38, 0.18, 1),
                      (0.55, 0.10, 1), (0.72, 0.20, 2), (0.88, 0.12, 1),
                      (0.14, 0.38, 1), (0.62, 0.34, 1), (0.94, 0.40, 2),
                      (0.48, 0.05, 1)]:
        d.ellipse([fx * w - r, fy * h - r, fx * w + r, fy * h + r],
                  fill=(255, 255, 255))
    # Earth curve along the bottom
    d.ellipse([-int(w * 0.30), int(h * 0.78), int(w * 1.10), int(h * 1.60)],
              fill=(40, 90, 160))
    d.arc([-int(w * 0.30), int(h * 0.78), int(w * 1.10), int(h * 1.60)],
          180, 360, fill=(120, 180, 230), width=3)
    # rocket, left of centre, climbing
    rx, ry = int(w * 0.28), int(h * 0.10)
    rw, rh = 18, 56
    d.polygon([(rx, ry), (rx + rw // 2, ry - 15), (rx + rw, ry)],
              fill=RED)
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=(235, 235, 230))
    d.ellipse([rx + 5, ry + 12, rx + 13, ry + 20], fill=(120, 180, 230))
    d.polygon([(rx, ry + rh), (rx - 7, ry + rh + 11), (rx, ry + rh)],
              fill=RED)
    d.polygon([(rx + rw, ry + rh), (rx + rw + 7, ry + rh + 11),
               (rx + rw, ry + rh)], fill=RED)
    d.polygon([(rx + 2, ry + rh + 13), (rx + 9, ry + rh + 28),
               (rx + 16, ry + rh + 13)], fill=(250, 180, 40))
    d.polygon([(rx + 6, ry + rh + 13), (rx + 9, ry + rh + 22),
               (rx + 12, ry + rh + 13)], fill=(250, 230, 120))
    for cx, cy, r in [(rx - 2, ry + rh + 26, 5), (rx + 20, ry + rh + 28, 6),
                      (rx + 9, ry + rh + 34, 5)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # Tiangong station, top right
    sx, sy = int(w * 0.64), int(h * 0.12)
    d.rectangle([sx - 26, sy + 2, sx, sy + 9], fill=(60, 90, 160))
    d.rectangle([sx, sy, sx + 32, sy + 11], fill=(200, 200, 195))
    d.rectangle([sx + 32, sy + 2, sx + 58, sy + 9], fill=(60, 90, 160))
    d.rectangle([sx + 12, sy + 11, sx + 20, sy + 18], fill=(180, 180, 175))
    return img


def paint_court(w, h):
    """Brooklyn courthouse at dusk: lit columns against a night sky."""
    img = Image.new("RGB", (w, h), NAVY)
    vgrad(img, (0, 0, w, h), NAVY, NAVY_DEEP)
    d = ImageDraw.Draw(img)
    for fx, fy, r in [(0.08, 0.12, 1), (0.22, 0.07, 1), (0.85, 0.10, 2),
                      (0.94, 0.22, 1), (0.60, 0.06, 1)]:
        d.ellipse([fx * w - r, fy * h - r, fx * w + r, fy * h + r],
                  fill=(255, 255, 255))
    # moon
    d.ellipse([int(w * 0.80) - 9, 8, int(w * 0.80) + 9, 26], fill=AMBER)
    # pediment and entablature
    d.polygon([(8, 30), (w // 2, 10), (w - 8, 30)], fill=STONE_DARK)
    d.ellipse([w // 2 - 7, 14, w // 2 + 7, 28], fill=(120, 100, 70))
    d.rectangle([8, 30, w - 8, 38], fill=STONE)
    # four lit columns
    for i in range(4):
        cx = 22 + i * int((w - 44) / 3)
        d.rectangle([cx - 6, 38, cx + 6, h - 24], fill=STONE)
        d.rectangle([cx - 9, 34, cx + 9, 38], fill=STONE_DARK)
        d.rectangle([cx - 9, h - 28, cx + 9, h - 24], fill=STONE_DARK)
    # warm windows between the columns, dark door in the middle
    for i in range(3):
        cx = 22 + (i + 0.5) * int((w - 44) / 3)
        d.rectangle([cx - 8, 48, cx + 8, 66], fill=AMBER)
    d.rectangle([w // 2 - 11, h - 44, w // 2 + 11, h - 24],
                fill=(60, 50, 40))
    # steps
    for i in range(3):
        yy = h - 20 + i * 5
        d.rectangle([6, yy, w - 6, yy + 3], fill=STONE_DARK)
    return img


# Simplified continents as (lon, lat) outlines; equirectangular.
LAND_POLYS = [
    [(-168, 66), (-145, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-84, 30), (-90, 21), (-97, 16), (-94, 17), (-87, 13),
     (-83, 9), (-79, 9), (-86, 12), (-92, 15), (-97, 16), (-105, 20),
     (-110, 24), (-114, 28), (-120, 34), (-125, 40), (-124, 48),
     (-130, 55), (-145, 60), (-158, 58), (-165, 60)],
    [(-79, 9), (-72, 12), (-62, 11), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-68, -52),
     (-70, -55), (-73, -45), (-73, -30), (-70, -18), (-77, -12),
     (-80, -5), (-81, 0), (-80, 5)],
    [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (10, 37), (20, 32),
     (32, 31), (35, 28), (38, 22), (43, 12), (51, 11), (48, 2),
     (40, -10), (35, -20), (32, -29), (26, -34), (19, -35), (15, -27),
     (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (3, 53),
     (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (32, 70), (40, 68), (44, 66), (40, 60), (35, 55), (30, 50),
     (28, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 42), (0, 40),
     (-2, 37), (-6, 36)],
    [(32, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 67), (178, 65), (170, 60), (162, 56),
     (156, 51), (150, 59), (142, 55), (140, 45), (135, 43), (130, 40),
     (127, 35), (122, 38), (120, 32), (115, 25), (110, 20), (108, 12),
     (105, 9), (100, 7), (98, 12), (95, 16), (92, 21), (88, 22),
     (85, 19), (80, 13), (77, 8), (75, 15), (72, 20), (68, 23),
     (66, 25), (61, 25), (57, 26), (55, 26), (52, 28), (50, 29),
     (48, 30), (44, 29), (40, 32), (38, 36), (35, 36), (33, 41),
     (30, 46), (28, 48), (30, 55), (32, 62)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]
# (lon, lat, number): 1 Hormuz, 2 Jiuquan, 3 Brooklyn, 4 Ituri,
# 5 Hanoi, 6 Gaza.
MAP_PINS = [(57, 26.5, "1"), (100.3, 39.8, "2"), (-74, 40.7, "3"),
            (29.5, 1.5, "4"), (105.8, 21, "5"), (34.5, 31.5, "6")]


def paint_world(w, h):
    """Simplified world map, cropped to lat 75..-60, with six pins."""
    img = Image.new("RGB", (w, h), (222, 232, 238))
    d = ImageDraw.Draw(img)
    for gx in range(0, w, 39):
        d.line([(gx, 0), (gx, h)], fill=(210, 222, 230), width=1)
    for gy in range(0, h, 32):
        d.line([(0, gy), (w, gy)], fill=(210, 222, 230), width=1)

    def px(lon):
        return (lon + 180.0) / 360.0 * w

    def py(lat):
        return (75.0 - lat) / 135.0 * h

    for poly in LAND_POLYS:
        d.polygon([(px(lon), py(lat)) for lon, lat in poly],
                  fill=SAND, outline=SAND_LINE)
    nf = font(SANS_B, 10)
    for lon, lat, num in MAP_PINS:
        cx, cy = px(lon), py(lat)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        bb = d.textbbox((0, 0), num, font=nf)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), num, font=nf,
               fill=(255, 255, 255))
    return img


# ---------------------------------------------------------------- content
# All facts below are the verified 25 Nov 2026 set (SOURCES.md).
# Deliberately NOT used: anything absent from SOURCES.md.

LEAD_KICKER = "LEAD · STRAIT OF HORMUZ"
LEAD_HEAD = "25 tankers hit, Hormuz traffic down 40%"
LEAD_BODY = ("Iran says it downed a US MQ-9 drone over the strait as "
             "around 25 tankers were hit and shipping fell 40%. Tehran "
             "said three tankers struck naval mines and caught fire. "
             "Saudi defences intercepted 209 Houthi threats, after a "
             "strike injured 11 in Riyadh.")

SCENE2_KICKER = "SPACE · ASIA"
SCENE2_HEAD = "First Pakistani in orbit as Shenzhou-24 docks"
SCENE2_BODY = ("Launched 08:18 from Jiuquan with Tang Hongbo, Wu Yi and "
               "Muhammad Zeeshan Ali — first Pakistani in orbit. "
               "Docked 3h 38m after liftoff.")

SCENE3_KICKER = "COURTS · US-CHINA"
SCENE3_HEAD = "Huawei guilty on 10 of 12 counts"
SCENE3_BODY = ("A Brooklyn jury convicted Huawei of bank fraud, wire "
               "fraud, sanctions and trade-secret counts. Acquitted of "
               "racketeering; sentencing 14 Sep 2027.")

NUMBERS = [
    ("25", "tankers reported hit in the Strait of Hormuz"),
    ("40%", "fall in shipping traffic through Hormuz"),
    ("209", "Houthi aerial threats intercepted since Sept."),
    ("08:18", "Shenzhou-24 liftoff, Beijing time, Jiuquan"),
    ("10/12", "counts Huawei was convicted on in Brooklyn"),
    ("≈500,000", "Russian losses in Ukraine, per leaked files"),
]

# 26 one-line briefs: (place, fact). Regions flow Middle East,
# Asia-Pacific, Europe, Americas, Africa, Oceania across 3 columns.
# With the lead and the two scenes that is 29 stories in total.
BRIEFS = [
    ("HORMUZ", "Iran claims it downed a US MQ-9 drone"),
    ("SAUDI DEFENCES", "Intercepted 209 aerial threats"),
    ("RIYADH", "Tower attack injured 11 people"),
    ("HODEIDAH", "Coalition targeted the port"),
    ("JEDDAH", "Houthis threatened the city"),
    ("GAZA", "Strikes kill seven despite ceasefire"),
    ("STRAIT", "Three tankers hit mines, caught fire"),
    ("WASHINGTON", "New tariffs on India, China + 14"),
    ("SHANGHAI", "Party chief Chen Jining investigated"),
    ("CANBERRA", "Australia signs Solomons pact"),
    ("HANOI", "Hot-pot gas blast kills 7, injures 9"),
    ("OTTAWA", "India–Canada talks 'very close'"),
    ("NEW DELHI", "Modi and Merz hold a call"),
    ("LONDON", "UK warns firms over Russian sabotage"),
    ("KYIV", "Libya ship strike was self-defence"),
    ("KYIV", "Ukraine seeks €115bn aid for 2027"),
    ("PYONGYANG", "Swiss office ordered shut"),
    ("UKRAINE", "Leaked files: losses near 500,000"),
    ("LISBON", "Lego picks Portugal for 8th factory"),
    ("LANGLEY", "CIA, ODNI hit by cyberattack"),
    ("COLOMBIA", "Gunmen take 25 hostage in market"),
    ("US STATES", "Sue Musk firms over Grok images"),
    ("VATICAN", "Pope applies for mail ballot"),
    ("ITURI", "WHO evacuates hospital staff"),
    ("DR CONGO", "Ebola: 5,775 dead of 11,762 cases"),
    ("US", "Criticises Australia's social media law"),
]

STANDFIRST = ("Hormuz in flames, a first Pakistani in orbit, Huawei "
              "convicted — one day, in one page.")
COUNT_LINE = "29 STORIES · ALL FROM WEDNESDAY 25 NOVEMBER 2026 · 6 REGIONS"
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
    d.text((LEFT, y), STANDFIRST, font=font(SERIF_I, 17), fill=INK)
    y = 118
    rule(d, LEFT, RIGHT, y, fill=INK, width=3)
    rule(d, LEFT, RIGHT, y + 5, fill=INK, width=1)
    y = 130
    draw_spaced(d, (LEFT, y), COUNT_LINE, font(SANS_B, 12), INK, spacing=1)
    return 154


def section_lead(img, d, y):
    """Hero: big Hormuz scene left, lead story right."""
    hero = paint_hormuz(620, 250)
    img.paste(hero, (LEFT, y))
    tx = LEFT + 620 + 18
    tw = RIGHT - tx
    yy = y + 2
    draw_spaced(d, (tx, yy), LEAD_KICKER, font(SANS_B, 12), RED, spacing=2)
    yy += 20
    for line in wrap(d, LEAD_HEAD, font(SERIF_B, 29), tw):
        d.text((tx, yy), line, font=font(SERIF_B, 29), fill=INK)
        yy += 35
    yy += 6
    for line in wrap(d, LEAD_BODY, font(SANS, 13), tw):
        d.text((tx, yy), line, font=font(SANS, 13), fill=INK)
        yy += 17
    return y + 250


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
    """Two scenes plus the world map, one shared dusk language."""
    col_w = 312
    gx = 18
    x1 = LEFT
    x2 = LEFT + col_w + gx
    x3 = LEFT + 2 * (col_w + gx)
    # scene 1: Shenzhou-24
    img.paste(paint_launch(col_w, 96), (x1, y))
    yy = y + 96 + 8
    draw_spaced(d, (x1, yy), SCENE2_KICKER, font(SANS_B, 11), RED,
                spacing=2)
    yy += 17
    for line in wrap(d, SCENE2_HEAD, font(SERIF_B, 18), col_w):
        d.text((x1, yy), line, font=font(SERIF_B, 18), fill=INK)
        yy += 22
    yy += 2
    for line in wrap(d, SCENE2_BODY, font(SANS, 12), col_w)[:3]:
        d.text((x1, yy), line, font=font(SANS, 12), fill=INK)
        yy += 15
    # scene 2: Huawei courthouse
    img.paste(paint_court(col_w, 96), (x2, y))
    yy = y + 96 + 8
    draw_spaced(d, (x2, yy), SCENE3_KICKER, font(SANS_B, 11), RED,
                spacing=2)
    yy += 17
    for line in wrap(d, SCENE3_HEAD, font(SERIF_B, 18), col_w):
        d.text((x2, yy), line, font=font(SERIF_B, 18), fill=INK)
        yy += 22
    yy += 2
    for line in wrap(d, SCENE3_BODY, font(SANS, 12), col_w)[:3]:
        d.text((x2, yy), line, font=font(SANS, 12), fill=INK)
        yy += 15
    # cell 3: world map with numbered pins
    img.paste(paint_world(col_w, 130), (x3, y))
    yy = y + 130 + 8
    draw_spaced(d, (x3, yy), "WHERE IT HAPPENED", font(SANS_B, 11), RED,
                spacing=2)
    yy += 17
    f_cap = font(SANS, 10)
    d.text((x3, yy), "1 Hormuz · 2 Jiuquan · 3 Brooklyn", font=f_cap,
           fill=MUTED)
    yy += 13
    d.text((x3, yy), "4 Ituri · 5 Hanoi · 6 Gaza", font=f_cap, fill=MUTED)
    return y + 204


def section_briefs(d, y):
    """The rest of the world: 26 one-line briefs in three columns."""
    hf = font(SERIF_B, 20)
    d.text((LEFT, y), "THE WORLD IN BRIEF", font=hf, fill=INK)
    rt = "EVERY STORY DATED 25 NOV 2026"
    rf = font(SANS_B, 10)
    d.text((RIGHT - d.textlength(rt, font=rf), y + 5), rt, font=rf,
           fill=MUTED)
    y += 28
    rule(d, LEFT, RIGHT, y, fill=RED, width=2)
    y += 12
    col_w = (INNER - 2 * 18) // 3
    fb = font(SANS_B, 12)
    fr = font(SANS, 12)
    per_col = [9, 9, 8]
    idx = 0
    for col in range(3):
        bx = LEFT + col * (col_w + 18)
        for row in range(per_col[col]):
            place, fact = BRIEFS[idx]
            idx += 1
            yy = y + row * 19
            lead = place + " — "
            check_fit(d, lead + fact, fr, col_w, "brief " + place)
            d.text((bx, yy), lead, font=fb, fill=INK)
            d.text((bx + d.textlength(lead, font=fb), yy), fact,
                   font=fr, fill=INK)
    return y + 9 * 19


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
    y = section_lead(img, d, y)
    y += 10
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 10
    y = section_numbers(d, y)
    y += 10
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 10
    y = section_scenes(img, d, y)
    y += 10
    rule(d, LEFT, RIGHT, y, fill=HAIR, width=1)
    y += 10
    y = section_briefs(d, y)
    y += 10
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
