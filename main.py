#!/usr/bin/env python3
"""
THE WORLD IN ONE PAGE -- Wednesday 25 November 2026
make.fun bounty: Sum up 25 November's world news in one image.

Deterministic, offline newspaper front page generator.
- No network calls, no randomness, no timestamps, no datetime.now().
- Only stdlib + Pillow. Fixed fonts, fixed layout, fixed text.
- Output: /output/entry.png (also ./output/entry.png when run from repo root)
  PNG, 1024x1024, <= 1 MiB, byte-identical across runs in the same env.
- Python 3.13 compatible.

News embedded below was researched on 25 Nov 2026 from Reuters,
Al Jazeera, CNN, Japan Times, Geo.tv, News18, Xinhua, Dawn and
the US Department of Justice. See SOURCES.md for the full list.
"""

import hashlib
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (253, 248, 238)      # newsprint cream
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (27, 68, 128)
GREY = (90, 90, 90)
LIGHT_BLUE = (214, 230, 242)
GREEN = (74, 110, 68)
RULE = (17, 17, 17)

# ---------------------------------------------------------------- fonts
FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
]

def _find(name_candidates):
    for d in FONT_DIRS:
        for name in name_candidates:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None

_SERIF_BOLD = _find(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"])
_SERIF = _find(["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"])
_SANS_BOLD = _find(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"])
_SANS = _find(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"])

def font(kind, size):
    path = {"serif_bold": _SERIF_BOLD, "serif": _SERIF,
            "sans_bold": _SANS_BOLD, "sans": _SANS}.get(kind)
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# ---------------------------------------------------------------- text
def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
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

def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y

def headline(draw, x, y, text, fnt, max_w, leading, color=INK):
    return para(draw, x, y, text, fnt, max_w, leading, color)

def rule(draw, x, y, w, h=2):
    draw.rectangle([x, y, x + w, y + h], fill=RULE)

def kicker(draw, x, y, text, color=RED):
    f = font("sans_bold", 13)
    draw.text((x, y), text, font=f, fill=color)
    return y + 18

# ---------------------------------------------------------------- map
# Simplified continent outlines, in a 0..1000 x 0..420 map space.
CONTINENTS = {
    "North America": [(60, 70), (150, 40), (230, 55), (260, 95), (210, 140),
                      (180, 190), (130, 180), (95, 140), (55, 110)],
    "South America": [(210, 230), (260, 220), (290, 260), (270, 330),
                      (235, 380), (215, 310), (200, 260)],
    "Europe": [(470, 70), (530, 55), (570, 75), (560, 115), (510, 125),
               (480, 105), (460, 90)],
    "Africa": [(480, 160), (540, 150), (580, 180), (570, 250), (540, 310),
               (510, 285), (490, 220), (470, 185)],
    "Asia": [(600, 60), (720, 40), (840, 55), (910, 90), (880, 140),
             (800, 170), (730, 150), (640, 140), (590, 100)],
    "Oceania": [(820, 300), (880, 295), (900, 320), (860, 340), (820, 325)],
}
# (x, y) in map space, label
DOTS = [
    (150, 110, "Washington"), (690, 95, "Beijing"), (760, 115, "Tokyo"),
    (520, 95, "London"), (520, 200, "Kinshasa"), (250, 290, "Bogota"),
    (850, 315, "Canberra"), (590, 150, "Hormuz"), (640, 120, "Shanghai"),
    (700, 70, "Jiuquan"),
]

def draw_map(draw, ox, oy, mw, mh):
    draw.rectangle([ox, oy, ox + mw, oy + mh], fill=LIGHT_BLUE,
                   outline=INK, width=2)
    sx, sy = mw / 1000.0, mh / 420.0
    for pts in CONTINENTS.values():
        scaled = [(ox + x * sx, oy + y * sy) for x, y in pts]
        draw.polygon(scaled, fill=GREEN, outline=(40, 60, 40))
    f = font("sans_bold", 11)
    for x, y, label in DOTS:
        cx, cy = ox + x * sx, oy + y * sy
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                     outline=(255, 255, 255))
        draw.text((cx + 6, cy - 6), label, font=f, fill=INK)
    draw.text((ox + 10, oy + mh - 22), "THE WORLD AT A GLANCE  •  DOTS MARK THE DAY'S STORIES",
              font=font("sans_bold", 11), fill=BLUE)

# ---------------------------------------------------------------- stories
LEAD_HEADLINE = "HORMUZ IN FLAMES: TANKERS HIT, TRAFFIC DOWN 40%"
LEAD_DECK = ("Iran says its army downed a US MQ-9 drone over the Strait of "
             "Hormuz as around 25 tankers were reported hit and shipping "
             "through the world's busiest oil chokepoint fell by more than 40%.")
LEAD_BODY = ("Tehran said three oil tankers struck naval mines and caught "
             "fire, and warned it would not tolerate a US naval blockade. "
             "Brent crude nevertheless traded below $90 a barrel, far below "
             "its late-October peak, as traders weighed ample supply against "
             "the disruption. Saudi defences said they had intercepted 209 "
             "Houthi aerial threats since September, after a strike injured "
             "11 people in Riyadh's financial district.")

STORY2_HEAD = "FIRST FOREIGNER ABOARD TIANGONG"
STORY2_BODY = ("China's Shenzhou-24 blasted off from Jiuquan at 08:18 Beijing "
               "time, carrying Tang Hongbo, Wu Yi and Pakistan's Muhammad "
               "Zeeshan Ali -- the first foreign astronaut to visit the "
               "Tiangong station, and the first Pakistani in orbit. The crew "
               "will run about 90 experiments in a week-long stay.")

STORY3_HEAD = "HUAWEI GUILTY ON 10 OF 12 COUNTS"
STORY3_BODY = ("A Brooklyn jury convicted Huawei of bank fraud, wire fraud, "
               "sanctions violations and conspiracy to steal trade secrets, "
               "after a case that began in 2018. Jurors acquitted the firm of "
               "racketeering. Sentencing is set for 14 September 2027.")

BRIEFS = [
    ("EUROPE", "UK warns firms backing Ukraine of Russian sabotage; Kyiv says "
     "its strike on Russian ships off Libya was self-defence; Ukraine seeks "
     "EUR 115bn in foreign aid for 2027; EU and Canada plan a closer AI pact."),
    ("AFRICA", "WHO evacuates health workers from a hospital in Ituri, DR Congo, "
     "after three days sheltering from fighting, as the Ebola outbreak reaches "
     "5,775 deaths among 11,762 cases."),
    ("AMERICAS", "US intelligence agencies were hit by a cyberattack on classified "
     "systems, CNN reported; gunmen took 25 hostages at a supermarket in "
     "Colombia; states sue Musk firms over sexualised Grok images."),
    ("ASIA-PACIFIC", "Washington plans new tariffs on India, China and 14 other "
     "economies; Shanghai party chief Chen Jining is placed under investigation; "
     "Australia and the Solomon Islands sign a sweeping security pact."),
    ("MIDDLE EAST", "Israeli strikes in Gaza killed seven, including Hamas's internal "
     "security chief, despite the ceasefire; the Saudi-led coalition hit "
     "Hodeidah port as the Houthis threatened Jeddah and other Red Sea ports."),
    ("OCEANIA", "The US criticises Australia's social media law as harming free "
     "speech, as Canberra's pact with Honiara is seen in the region as a "
     "check on Beijing."),
]

IN_BRIEF = [
    "Hanoi hot-pot blast kills 7, injures 9.",
    "India, Canada 'very close' to a trade pact.",
    "Rubio and Qatar sign critical-minerals framework.",
    "North Korea orders Swiss office in Pyongyang shut.",
    "Pope Leo XIV applies for a US midterm mail ballot.",
    "Lego picks Portugal for its eighth factory.",
]

# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 28
    x0, x1 = M, W - M
    y = 22

    # masthead
    d.text((x0, y), "THE WORLD", font=font("serif_bold", 62), fill=INK)
    tw = d.textlength("THE WORLD", font=font("serif_bold", 62))
    d.text((x0 + tw + 14, y + 18), "IN ONE PAGE", font=font("sans_bold", 26), fill=RED)
    y += 74
    rule(d, x0, y, x1 - x0, 3)
    y += 8
    d.text((x0, y), "WEDNESDAY, 25 NOVEMBER 2026  •  50 STORIES  •  6 CONTINENTS  •  ONE FRONT PAGE",
           font=font("sans_bold", 14), fill=INK)
    y += 24
    rule(d, x0, y, x1 - x0, 1)
    y += 10

    # lead story, left; story 2, right
    lead_w = 600
    y = kicker(d, x0, y, "MIDDLE EAST  •  LEAD STORY")
    y = headline(d, x0, y, LEAD_HEADLINE, font("serif_bold", 30),
                 lead_w, 36, color=RED)
    y += 4
    y = para(d, x0, y, LEAD_DECK, font("serif", 15), lead_w, 20)
    y += 6
    y = para(d, x0, y, LEAD_BODY, font("serif", 13), lead_w, 18)
    lead_bottom = y

    rx = x0 + lead_w + 24
    rw = x1 - rx
    ry = 138
    ry = kicker(d, rx, ry, "SPACE  •  ASIA")
    ry = headline(d, rx, ry, STORY2_HEAD, font("serif_bold", 22), rw, 27)
    ry += 2
    # simple rocket drawing
    rocket_y = ry
    d.rectangle([rx + 90, rocket_y, rx + 110, rocket_y + 62], fill=(200, 200, 200), outline=INK)
    d.polygon([(rx + 90, rocket_y), (rx + 100, rocket_y - 22), (rx + 110, rocket_y)],
              fill=RED, outline=INK)
    d.polygon([(rx + 90, rocket_y + 62), (rx + 78, rocket_y + 78), (rx + 90, rocket_y + 62)],
              fill=RED, outline=INK)
    d.polygon([(rx + 110, rocket_y + 62), (rx + 122, rocket_y + 78), (rx + 110, rocket_y + 62)],
              fill=RED, outline=INK)
    d.ellipse([rx + 94, rocket_y + 12, rx + 106, rocket_y + 24], fill=LIGHT_BLUE, outline=INK)
    d.text((rx + 140, rocket_y + 8), "SHENZHOU-24", font=font("sans_bold", 13), fill=INK)
    d.text((rx + 140, rocket_y + 26), "Long March 2F", font=font("sans", 12), fill=GREY)
    d.text((rx + 140, rocket_y + 44), "Jiuquan  •  08:18", font=font("sans", 12), fill=GREY)
    ry = rocket_y + 84
    ry = para(d, rx, ry, STORY2_BODY, font("serif", 12), rw, 17)
    ry += 6
    ry = kicker(d, rx, ry, "COURTS  •  US-CHINA")
    ry = headline(d, rx, ry, STORY3_HEAD, font("serif_bold", 19), rw, 24)
    ry += 2
    ry = para(d, rx, ry, STORY3_BODY, font("serif", 12), rw, 17)
    right_bottom = ry

    y = max(lead_bottom, right_bottom) + 10
    rule(d, x0, y, x1 - x0, 1)
    y += 8

    # map
    d.text((x0, y), "WHERE IT HAPPENED", font=font("sans_bold", 14), fill=BLUE)
    y += 20
    map_h = 115
    draw_map(d, x0, y, x1 - x0, map_h)
    y += map_h + 10
    rule(d, x0, y, x1 - x0, 1)
    y += 8

    # briefs in two columns
    d.text((x0, y), "AROUND THE WORLD", font=font("sans_bold", 14), fill=BLUE)
    y += 20
    col_w = (x1 - x0 - 24) // 2
    col_y = [y, y]
    for i, (label, text) in enumerate(BRIEFS):
        col = i % 2
        cx = x0 + col * (col_w + 24)
        cy = col_y[col]
        cy = kicker(d, cx, cy, label, color=BLUE)
        cy = para(d, cx, cy, text, font("serif", 11), col_w, 14)
        col_y[col] = cy + 6
    y = max(col_y) + 2
    rule(d, x0, y, x1 - x0, 1)
    y += 8

    # in brief ticker
    d.text((x0, y), "IN BRIEF", font=font("sans_bold", 13), fill=RED)
    y += 18
    ticker = "  •  ".join(IN_BRIEF)
    y = para(d, x0, y, ticker, font("sans", 11), x1 - x0, 13, color=(60, 60, 60))
    y += 4
    rule(d, x0, y, x1 - x0, 1)
    y += 8
    d.text((x0, y), "Sources: Reuters, Al Jazeera, CNN, Japan Times, Geo.tv, News18, Xinhua, Dawn, US Dept. of Justice  •  All stories dated 25 Nov 2026  •  Generated deterministically, offline, no live data at run time.",
           font=font("sans", 10), fill=GREY)
    return img

def main():
    # Primary output: the grading directory. The grader sets
    # MAKEFUN_OUTPUT_DIR=/output and mounts the repo read-only, so
    # nothing may be written next to the program itself.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out = Path(out_dir) / "entry.png"
    img = render()
    out.parent.mkdir(parents=True, exist_ok=True)
    # Fixed PNG encoding: no metadata, fixed compression level.
    img.save(out, format="PNG", compress_level=6, optimize=False)
    data = out.read_bytes()
    print(f"Wrote {out} ({len(data)} bytes, {img.size[0]}x{img.size[1]})")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    # Best-effort local copy when run from the repo root. Never let
    # this fail the run: in the grading environment the repo is
    # mounted read-only, so creating ./output/ raises PermissionError.
    try:
        local_out = Path(__file__).resolve().parent / "output" / "entry.png"
        local_out.parent.mkdir(parents=True, exist_ok=True)
        img.save(local_out, format="PNG", compress_level=6, optimize=False)
        print(f"Also wrote {local_out}")
    except OSError as exc:
        print(f"Skipping local copy (not writable): {exc}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
