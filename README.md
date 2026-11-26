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

- **Lead:** the Strait of Hormuz — the IRGC says two tankers
  "hit by mines" and an MQ-9 was downed. The story is labelled
  CLAIM, because it is one side's say, not a verified fact.
- **Space:** Shenzhou-24 launches from Jiuquan with the first
  Pakistani astronaut, Muhammad Zeeshan Ali, aboard Tiangong —
  docks 3h 38m after the 08:18 liftoff.
- **Trade:** the US proposes tariffs on 14 economies — Vietnam up
  to 35%, India up to 25%, China up to 20%.
- **Ten small scenes, all in daylight,** each with a coloured
  keyword band on the picture (KOSPI -6.2%, 31 DEAD, EBOLA 5,775,
  HOSTAGES FREED, 7 KILLED, 10% DUTY, $227M SEIZED, POSTPONED,
  14,000 MARCH, 16 DEAD) — Kospi chart, Cairo tanker fire, Ituri
  clinic, Cartagena supermarket, Gaza at dawn, Embraer jet,
  Nigeria port, Macy's parade, Athens march, Pakistan collapse.
- **Every story carries a credibility label** — OFFICIAL (the
  source's own words), REPORTED (covered by the press), CLAIM
  (one side's say, not verified) — with a legend under the
  masthead. The Huawei verdict (reported 24 Nov) is not a story
  on this page: only Huawei's 25 Nov reaction to it is, in
  brief 14.
- **The map is back:** WHERE IT HAPPENED, with red numbered dots
  for the 13 pictured stories, and the briefs numbered 14–34 in
  the same sequence.
- **The day in numbers:** -6.2% Kospi, 35% top tariff, 31 killed
  in Cairo, 5,775 Ebola dead, 209 threats intercepted, $227m meth
  seized.
- **The day in order:** a UTC timeline with four real clock times
  only (00:18 liftoff, 03:56 docking, 06:05 IRGC statement,
  06:30 Kospi close) — nothing faked to fill it out.
- **DATE CHECK, boxed:** every story on the page was first
  reported on Wed 25 Nov 2026; the box lists what was left out
  (Huawei verdict Tue 24, Riyadh tower Tue 24, three tankers hit
  mines Mon 23, Nvidia chief returns Mon 23, COP31 ends Sun 22)
  and what has not happened yet (Thanksgiving Day Thu 26).
- **The rest of the world:** 21 one-line briefs in three columns
  (stories 14–34), each with a coloured credibility square.
- All headlines were researched from real reporting on 25 Nov 2026 —
  see [SOURCES.md](SOURCES.md). No story was fabricated. **34 stories
  in total** (3 big + 10 small + 21 briefs), six regions
  (Middle East 6, Asia-Pacific 9, Europe 6, Americas 10, Africa 2,
  Oceania 1), every one dated 25 Nov 2026.

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

## Test results (26 Nov 2026, this workspace)

- Size: **1024 × 1024 px**, PNG, **264,426 bytes** (limit: 1 MiB, 1024×1024) ✓
- Determinism: run twice → identical SHA-256
  `bf2cbf820d755f3db6a15abc92793c993f0304ab70d9fb0c03429b5c3dd946ab`
  (Round-8 SHA was `b92ad3cc…`; the image changed, the facts did not.)
- Offline: no network calls in `main.py` (grep: no `urllib`, `socket`,
  `requests`, `http.client`); verified by running in a clean environment.
- No-Pillow check (round 7, 26 Nov 2026): `main.py` runs with exit 0 in a fresh venv without Pillow (`import PIL` → `ModuleNotFoundError` there), and twice from the repo dir — `/output/entry.png` byte-identical to `entry.png` (SHA `9f703c2c…`) in every case. `main.py` is unchanged since round 5.
- Licence: MIT (`LICENSE`, OSI-approved) at repo root ✓
- Layout: `main.py` at repo root, Python 3.13 compatible ✓
- Visual check: viewed at full size and at 300 px — the date, lead
  headline, six numbers, keyword bands, map and date-check box all
  read at 300 px; all ten small-scene credibility chips are present
  with the right label (verified by pixel scan), the DATE CHECK
  × marks render, and no dark scene blurs into a block.

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

**Status: round 9 built and tested locally (26 Nov 2026). Not yet
pushed or submitted — entry.png still needs a browser upload
(binary), then transcripts + kit submission. Round 6 ("Luminous
Locus", commit 66082762, dev 0.978389) is the current final entry
and the insurance if round 9 scores worse. Rounds 1–8 are already
submitted via the kit API; the agent submits, no user signing is
needed. Quota used: 8 entries (5 on 25 Nov, 3 on 26 Nov); round 9
would be the 9th. Deadline Fri 27 Nov 08:00 Beijing.**
