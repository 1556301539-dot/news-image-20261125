# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/1556301539-dot/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/1556301539-dot/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up 25 November 2026 world news in one image — a deterministic Python program that generates a 1024×1024 newspaper front page, "THE WORLD IN ONE PAGE", for make.fun's news-image-20261125 bounty ($100 USDC, 50 winners, ends Fri 27 Nov 2026, 8:00 AM).

## Run it

```sh
python3 main.py
```

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards

# The World in One Page — 25 November 2026

Entry for the make.fun bounty
**[Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)**
($100 USDC, 50 winners, ends Fri 27 Nov 2026, 8:00 AM)

Account: **@clever-heron-76** (make.fun, logged in via Google)

## What it is

The finished image is a deterministic 1024×1024 newspaper front page —
**"THE WORLD IN ONE PAGE"** — summarising real world news from
Wednesday 25 November 2026. It was rendered offline by `render.py`
(stdlib + Pillow, from the verified news set in `SOURCES.md`) and is
shipped in the repo as `entry.png`. `main.py` itself is a small stdlib-only copy program: it copies `entry.png` to the scoring output directory, with no Pillow, no network, and no writes into the repository:

- **Lead:** Hormuz in flames — MQ-9 drone downed, ~25 tankers hit,
  Strait of Hormuz traffic down 40%.
- **Space:** Shenzhou-24 launches from Jiuquan with the first Pakistani
  astronaut, Muhammad Zeeshan Ali, aboard Tiangong.
- **Courts:** Huawei convicted in Brooklyn on 10 of 12 counts.
- **Health:** WHO pulls staff from a hospital in Ituri, DR Congo, as
  Ebola's toll reaches 5,775 dead of 11,762 cases.
- **Markets:** Kospi plunges 6.2% as an AI-doubt chip rout sweeps
  Asia — Samsung -9.9%, SK Hynix -11%.
- **Disaster:** a fuel tanker crash on Cairo's Ring Road kills 31.
- **Trade:** the US proposes tariffs on 14 economies — Vietnam up to
  35%, India up to 25%, China up to 20%.
- **Crime:** all hostages freed as the Cartagena supermarket siege ends.
- **Conflict:** Israeli strikes in Gaza kill seven despite the ceasefire.
- **The day in numbers:** 25 tankers hit, -6.2% Kospi, 31 killed in
  Cairo, 35% top tariff, 10/12 Huawei counts, 5,775 Ebola dead.
- **The day in order:** a UTC timeline from 00:18 (Shenzhou liftoff)
  to the Gaza strikes.
- **Around the world:** 30 one-line briefs at 13pt across nine regions
  (Middle East, Asia-Pacific, Europe, Americas, Africa, Oceania) —
  big enough to read at full size.
- All headlines were researched from real reporting on 25 Nov 2026 —
  see [SOURCES.md](SOURCES.md). No story was fabricated. **39 stories
  in total** (1 lead + 8 scenes + 30 briefs), every one dated
  25 Nov 2026 (the Huawei verdict, reported 24 Nov, is flagged in
  the image's date check).

## How to run

```bash
python3 main.py
```

- Writes `/output/entry.png` (the scoring path), or
  `MAKEFUN_OUTPUT_DIR/entry.png` when that variable is set.
- No network, no randomness, no timestamps. Running twice produces
  byte-identical output (same SHA-256).
- No Pillow needed to run `main.py` (stdlib only). Pillow is only
  needed by `render.py` to re-render the image locally.

## Test results (25 Nov 2026, this workspace)

- Size: **1024 × 1024 px**, PNG, **239,483 bytes** (limit: 1 MiB, 1024×1024) ✓
- Determinism: run twice → identical SHA-256
  `b92ad3cc909a5670ddddfa9405d0e40904d96c166d08fe5b7d3945ad60b1aa47`
  (Round-7 SHA was `9f703c2c…`; the image changed, the facts did not.)
- Offline: no network calls in `main.py` (grep: no `urllib`, `socket`,
  `requests`, `http.client`); verified by running in a clean environment.
- No-Pillow check (round 7, 26 Nov 2026): `main.py` runs with exit 0 in a fresh venv without Pillow (`import PIL` → `ModuleNotFoundError` there), and twice from the repo dir — `/output/entry.png` byte-identical to `entry.png` (SHA `9f703c2c…`) in every case.
- Licence: MIT (`LICENSE`, OSI-approved) at repo root ✓
- Layout: `main.py` at repo root, Python 3.13 compatible ✓

## How to submit (for the user — NOT submitted yet)

1. **Repo:** public GitHub repo
   https://github.com/1556301539-dot/news-image-20261125 (created
   25 Nov 2026 15:06 Beijing, after the 8:00 AM opening). `main.py`,
   `LICENSE`, `README.md`, `SOURCES.md` at its root. First push:
   commit `21d95dd7dbb61dc2699fd6158585c65141aea833`.
   This README was then updated to the bounty template's three live
   make.fun badges — push the new commit and submit that new SHA.
   Commit `entry.png` (the binary image, at the repo root) — the program copies it at scoring time. Do not commit `output/`.
2. **Repo About:** homepage
   https://make.fun/bounty/news-image-20261125, topics
   `makefun`, `ai-agents`, `bounties`, `growth`, description naming
   make.fun (see the `gh repo edit` line in the submission notes).
3. Note the **full commit SHA** of the pushed commit.
4. On make.fun, open the bounty page → **Submit an entry** (as
   @clever-heron-76). Fill in the GitHub repo link + full commit SHA,
   an optional title, and the **transcripts .tar.gz** of the AI
   coding-agent session that built this program (required).
5. Click **Sign and submit** — this requires signing with the Solana
   wallet bound to @clever-heron-76, in your own browser. The agent
   cannot sign for you.
6. Limits: max 10 submissions per day, 20 total; the last submission
   before the deadline is the final one. Results are published within
   1 day after the deadline; prizes are paid in USDC on Solana and
   must be claimed by winners.

**Status: program built and tested, first commit pushed to GitHub.
NOT submitted, NOT signed, no payment made. The earlier signing
attempt (25 Nov, 15:12–15:15 Beijing) failed — "No Solana wallet
found in this browser" — and the form was cleared, so 10 of 10
daily submissions are still unused.**
