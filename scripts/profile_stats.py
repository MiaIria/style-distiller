#!/usr/bin/env python3
"""Summarize a style-distiller profile directory.

Usage:
    python scripts/profile_stats.py --profile-dir ~/.claude/styles
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def count_files(path: Path, pattern: str = "*.md") -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.glob(pattern) if item.is_file())


def load_weights(profile_dir: Path) -> dict:
    weights_path = profile_dir / "weights.json"
    if not weights_path.exists():
        return {}
    return json.loads(weights_path.read_text(encoding="utf-8-sig"))


def infer_state(positive_samples: int) -> str:
    if positive_samples <= 2:
        return "cold_start"
    if positive_samples <= 9:
        return "sprout"
    if positive_samples <= 29:
        return "learning"
    return "mature"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-dir", type=Path, default=Path.home() / ".claude" / "styles")
    args = parser.parse_args()

    profile_dir = args.profile_dir.expanduser()
    weights = load_weights(profile_dir)
    positive = count_files(profile_dir / "samples" / "positive")
    negative = count_files(profile_dir / "samples" / "negative")
    drafts = count_files(profile_dir / "drafts")
    backups = count_files(profile_dir / "backups", "*")
    profile_files = count_files(profile_dir / "profile")
    state = weights.get("current_state") or infer_state(positive)

    print(f"profile_dir={profile_dir}")
    print(f"state={state}")
    print(f"positive_samples={positive}")
    print(f"negative_samples={negative}")
    print(f"drafts={drafts}")
    print(f"backups={backups}")
    print(f"profile_files={profile_files}")
    if weights.get("last_updated"):
        print(f"last_updated={weights['last_updated']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
