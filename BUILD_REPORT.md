# Build report — make.fun bounty: "Sum up 25 November's world news in one image"

- Bounty: https://make.fun/bounty/news-image-20261125
- Account: @clever-heron-76 (user 大龙)
- Prize: $100 USDC, 50 winners (1st $20, 2nd $12, 3rd $6, 4–10th $2 each,
  11–50th $1.20 each). Deadline: Fri 27 Nov 2026, 8:00 AM Beijing.
- Built: 26 Nov 2026, in `~/workspace/make-fun/news-image/`
- **Status: round-7 redesign built and tested locally. Not yet pushed
  or submitted — entry.png still needs a browser upload (binary),
  then transcripts + kit submission. Round 6 ("Luminous Locus",
  commit 66082762) scored dev 0.978389, rank 2154 of 12,671 — the
  insurance if round 7 scores worse.**

## Why round 6 exists

- Round 5 ("Latent Helix", commit 7668924b) scored a dev provisional
  rate of 0.975354 (11 won / 1 drawn / 0 lost of 12 games) but ranked
  2242 of 11,247 entries (prize rank 2240) — far from the top 50.
  The user said the round-5 image's UI did not look good and asked
  for the ranking to move up.
- The user also corrected the direction: do NOT copy the top entries'
  approach. This redesign is original, built from my own judgement
  against the judge's five criteria (one day's news, breadth,
  readable from the image alone, faithful, craft).

## What was wrong with round 5 (seen on its own image)

- Too many competing sections (masthead, count strip, ticker, stats,
  3 lead cards, 8 mini scenes, map, 24-item numbered list, footer):
  busy, no single visual spine.
- The 8 mini scenes varied wildly in quality — a few read as
  placeholders (a bridge for tariffs, a beige box for Hanoi, a chart
  with a red oval for Russian losses).
- The 24-item brief list was a wall of tiny text: unreadable mush
  at ~300 px.
- The map was small, with blobby continents and a tiny caption.

## Round 6 redesign — "three stories, six numbers, the world in brief"

- **Concept:** three stories you cannot miss (Hormuz lead,
  Shenzhou-24, Huawei verdict), six numbers that define the day,
  and the rest of the world in brief. One clear spine instead of
  six stacked sections.
- **One illustration language ("dusk"):** every scene shares deep
  navy night, amber light and signal red, so the page reads as
  drawn by one hand. No cards, no shadows: hairline rules and
  columns, like a broadsheet.
- **Fewer, bigger scenes:** the 8 uneven minis are gone. Three
  scenes, all drawn large — Hormuz tanker at dusk (hero, 620 px
  wide), Shenzhou-24 launch, Brooklyn courthouse at dusk — plus a
  world map with six numbered pins.
- **Briefs rebuilt:** the numbered 24-item list is replaced by 26
  one-line briefs in three columns, each led by a bold place name
  (HORMUZ —, KYIV —, HANOI — …), grouped by region in reading
  order. Legible at full size, calm at small size.
- **29 stories in total** (1 lead + 2 scenes + 26 briefs), six
  regions: Middle East 7, Asia-Pacific 7, Europe 6, Americas 4,
  Africa 2, Oceania 1 — counted from what is actually drawn.
- **Theme:** custom "Broadsheet Dusk" (warm paper #F7F2E8, ink
  #171512, signal red #A31F1F, dusk navy #16233A). theme-factory's
  ten presets had no newsprint fit, so one was built for this
  brief. Type follows ui-ux-pro-max's "Editorial Classic" pairing
  (serif display + serif/sans body) with the fonts available
  offline: Liberation Serif Bold for headlines, Liberation Sans
  for body and labels.
- **Numbers spine kept and strengthened:** 25 / 40% / 209 / 08:18 /
  10/12 / ≈500,000, each with a red tick and a two-line label —
  the part of the page that still reads at ~300 px.
- **Date check kept:** the Huawei verdict was reported 24 Nov, not
  25 Nov — the footer says so plainly.

## Faithfulness fix (this round)

- While re-checking facts against SOURCES.md, three items in the
  round-5 image turned out NOT to be in SOURCES.md: "Brent crude
  traded below $90", "EU and Canada plan a closer AI pact", and
  "Rubio and Qatar sign critical-minerals framework". All three
  are removed in round 6. Every fact now drawn is in SOURCES.md;
  nothing new was invented. SOURCES.md itself is unchanged.

## Round 7 redesign — "four pictures from one day, legible at 300 px"

- **Why round 7 exists:** round 6 scored dev 0.978389 (12 won / 0 lost
  of 12 games) and ranked 2154 of 12,671 (prize rank 2153) — better
  than round 5's 0.975354 / 2242, but the user said 2154 is still far
  too low and asked for the page to be made better, properly, like a
  top designer would.
- **The brief was corrected against the judge's criteria, read
  verbatim from competition.yaml:** five criteria in order (one day's
  news + names the day; selection and breadth; reads clearly from the
  image alone; faithful; craft — one clear composition, legible at
  about 300 px, no smears/artefacts/garbled text), "Detail for its
  own sake does not count", first differing criterion decides, margin
  1–5 with decisive wins worth more. The earlier idea of pushing the
  story count toward 35 was dropped on that basis.
- **Every picture now tells its own story (criterion 3):** the hero
  tanker has real flames, a thick smoke column, a second ship
  burning, a drone overhead and mines in the water; the launch shows
  a big rocket with a long flame plume over the Earth's curve and
  Tiangong; the courthouse carries a red GUILTY stamp (10 / 12) so
  the verdict reads even at thumbnail size; a fourth picture joins
  the page — a clinic in Ituri with a red cross, an ambulance and a
  stretcher team (health, Africa).
- **One clear composition, legible at 300 px (criterion 5):** the page
  was shrunk to 300 px wide and checked by eye — the date, the lead
  headline, all six numbers, the three scene headlines and the bold
  brief place-names still read. The brief list is cut from 26 tiny
  lines to 8 lines at 16pt; the world map is gone (its pins were
  unreadable at 300 px). Restraint, whitespace, one region = one
  story.
- **13 stories, 6 regions, 9 fields** (4 pictures + 8 briefs + the
  Russian-losses figure): Middle East, Asia-Pacific, Europe,
  Americas, Africa, Oceania; conflict, space, courts, health, trade,
  diplomacy, security, cyber, disaster. The count fell from 29 on
  purpose — detail for its own sake does not count.
- **Theme unchanged, deepened:** "Broadsheet Dusk" (warm paper,
  ink, signal red, navy dusk, amber light). The clinic is the one
  day scene, in the same warm sand/amber/red language.
- **Facts unchanged:** every fact is in SOURCES.md; nothing new was
  invented; SOURCES.md itself is unchanged.

## Files (repo root)

| File | Purpose |
|---|---|
| `main.py` | Python 3.13 program, **stdlib only**, copies `entry.png` to the scoring output dir — UNCHANGED in rounds 6 and 7 |
| `render.py` | The drawing program (stdlib + Pillow, local use), rewritten from scratch for round 7 |
| `entry.png` | The finished 1024×1024 front page, shipped in the repo (scoring artifact) |
| `LICENSE` | MIT (OSI-approved) |
| `README.md` | How to run, what the image shows (updated for round 7; the three make.fun badges unchanged) |
| `SOURCES.md` | Full source list for every story (unchanged) |
| `BUILD_REPORT.md` | This file |
| `output/entry.png` | Old generated preview (superseded, do not push) |
| `preview-entry.png` | Copy of the old preview (do not push) |

## Test results (round 6, this workspace, 26 Nov 2026)

- **Dimensions:** 1024 × 1024 px, PNG, RGB ✓ (limit 1024×1024)
- **File size:** 168,046 bytes = 0.16 MiB ✓ (limit 1 MiB)
- **Determinism:** ran `python3 render.py` twice — identical output.
  SHA-256: `1a2d7e190e665257e82421c6206c87abfcfe67b4a9f48f026629fa928a369f2f`
  (Round-5 SHA was `9de2280c…`; the image changed, the facts did not.)
- **No overflow:** render.py measures every string against its box
  and warns on stderr; the two runs printed no overflow warnings.
- **Visual check:** the rendered page was viewed — masthead, lead
  headline, numbers spine, three scenes, map and briefs all fit,
  no overlap, footer visible. The hero tanker was reworked once
  after the first viewing (sun set on the horizon, bridge tower
  moved to the stern, containers separated, flame and smoke
  enlarged); the final SHA above is the reworked version.
- **main.py grading simulations (stdlib-only, no Pillow needed):**
  - `python3 main.py` twice with `MAKEFUN_OUTPUT_DIR` set: exit 0
    both times, output byte-identical to the repo `entry.png`
    (SHA `1a2d7e19…`).
  - In a fresh venv **without Pillow** (`import PIL` →
    `ModuleNotFoundError`), `main.py` runs with exit 0, same SHA
    `1a2d7e19…`.
  - `main.py` (38 lines, 1,057 bytes, unchanged since round 5)
    imports only hashlib, os, sys, pathlib — no shutil, no PIL,
    no network.
- **Offline:** `main.py` contains no network code; `render.py`
  contains no network calls, no `random`, no `datetime.now()`, no
  timestamps. All news text is embedded in the code.
- **Fonts (render.py only):** Liberation Serif/Sans, fixed paths,
  fixed layout.
- **Output paths:** `main.py` copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR/entry.png` if set, else `/output/entry.png`;
  it never writes into the repo directory.
- **Python version:** tested locally on Python 3.12.3 / Pillow 10.2.0
  for rendering. `main.py` uses only stdlib and no 3.13-only syntax.

## Test results (round 7, this workspace, 26 Nov 2026)

- **Dimensions:** 1024 × 1024 px, PNG, RGB ✓ (limit 1024×1024)
- **File size:** 146,886 bytes = 0.14 MiB ✓ (limit 1 MiB)
- **Determinism:** ran `python3 render.py` twice — identical output.
  SHA-256: `9f703c2ce6aefc9c76fd2b0c9d83e2ebd4a75535cdb54410afb8f82d2fdc107e`
  (Round-6 SHA was `1a2d7e19…`; the image changed, the facts did not.)
- **No overflow:** render.py measures every string against its box
  and warns on stderr; the two runs printed no overflow warnings,
  and the layout ended inside the page (no y > 1010 warning).
- **Visual check:** the rendered page was viewed at full size and
  shrunk to 300 px wide. At 300 px the date, lead headline, all six
  numbers, the three scene headlines and the bold brief place-names
  still read; the hero reads as a burning tanker, the court scene as
  a verdict (red GUILTY stamp), the clinic as a medical scene.
- **main.py grading simulations:** `python3 main.py` twice with
  `MAKEFUN_OUTPUT_DIR` set: exit 0 both times, output byte-identical
  to the repo `entry.png` (SHA `9f703c2c…`). In a fresh venv **without
  Pillow** (`import PIL` → `ModuleNotFoundError`), `main.py` runs with
  exit 0, same SHA `9f703c2c…`. `main.py` unchanged since round 5.

## What remains (in order)

1. **Upload `entry.png` to GitHub** (binary — the connector cannot
   push binary files): in a browser signed in as 1556301539-dot,
   upload `~/workspace/make-fun/news-image/entry.png` over the
   repo-root `entry.png` at
   https://github.com/1556301539-dot/news-image-20261125.
2. **Push the text files** (`render.py`, `README.md`,
   `BUILD_REPORT.md`) via the GitHub connector snapshot, then
   verify the new head commit live (`list_commits` +
   `get_file_contents`). Record the full commit SHA.
3. **Bundle transcripts** with the kit (`node cli/makefun.mjs
   bundle`, `--no-discover --no-family`): this round's session
   plus the round-6 redesign session f85e79fc, the round-5 rewrite
   session 02496520 (authored `main.py`) and build session 933a91b5
   (authored `SOURCES.md`), recorded sessions only, real usage from
   muse.db. Never rebuild or fabricate session records.
4. **Submit round 7 via the kit API** with the agent keypair
   (agent wallet 24gzFszy…), before Fri 27 Nov 2026 08:00 Beijing.
   Check `makefun status`: all checks must pass, then note the
   submission ID, name, claim code and dev provisional rate.
5. **Compare with round 6** (dev 0.978389, rank 2154). If round 7's
   dev rate is clearly higher, keep round 7 as final. If it is
   lower or about the same, restore round 6 as final before the
   deadline — either by selecting the earlier finished submission
   or by resubmitting commit 66082762 with transcripts-v6
   (SHA-256 `53020f058bee466881560223771657f20e6e37cd2b146cc9954031f3700e0c3b`).
   Transcripts-v6 and commit 66082762 are the insurance; do not
   overwrite or delete them. Round 5 (commit 7668924b +
   transcripts-v5) remains a second fallback.
6. Quota: 6 entries used (5 on 25 Nov, round 6 on 26 Nov), 9 left
   today (26 Nov), 14 total left. Deadline Fri 27 Nov 08:00 Beijing.
   Final result due 11 Dec 2026.

## Honest caveats

- The dev provisional rate is not the final result; the final
  ranking is due 11 Dec 2026. A better-looking page does not
  guarantee a better pairwise rate — the comparison in step 5 is
  the only evidence that counts.
- Competition is very strong: 12,671 ranked entries, leaders at
  ~98.5% win rate. Round 7 needs a large jump from 0.978389 to
  reach the top 50.
- The scoring environment's fonts may differ slightly from this
  workspace; the program falls back to Pillow's default font, so
  it still runs, but pixel output could differ from the preview.
  Determinism (two runs identical) holds within any single
  environment.
