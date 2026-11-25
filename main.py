#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE -- Wednesday 25 November 2026.

make.fun bounty: sum up 25 November's world news in one image.

The finished front page ships in this repository as entry.png. This
program only copies it to the scoring output directory. It uses the
Python standard library only, so it runs in the grading sandbox with
no third-party packages installed.
"""

import hashlib
import os
import sys
from pathlib import Path


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target = output_dir / "entry.png"

    try:
        image = source.read_bytes()
    except FileNotFoundError:
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    target.write_bytes(image)

    print(f"Wrote {target} ({len(image)} bytes)")
    print(f"SHA-256: {hashlib.sha256(image).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
