#!/usr/bin/env python3
"""Summarize a style-distiller profile directory.

Usage:
    python scripts/profile_stats.py --profile-dir ~/.claude/styles
    python scripts/profile_stats.py --style-distiller-dir ~/.claude/skills/style-distiller

Stage judgement uses total_samples = positive_samples + self_written_samples
(equal weight; self-written samples are deduped by topic — same title only
counts once, with the 终版 preferred over 初版 when both exist).
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


def _topic_key(stem: str) -> str:
    """Normalize a `result-0819_在等一个最好的状态-初版` filename to
    the topic key `0819_在等一个最好的状态`.

    Strips:
      - leading `result-`
      - trailing `-初版` or `-终版`
    """
    if stem.startswith("result-"):
        stem = stem[len("result-"):]
    for suffix in ("-初版", "-终版"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return stem


def count_self_written(style_distiller_dir: Path) -> tuple[int, dict[str, int]]:
    """Count self-written samples in style-write/results/, deduped by topic.

    Rules (per user spec):
      - 同一主题的初版+终版只算一篇
      - 优先算终版
      - 没终版算初版

    Returns (deduped_total, breakdown) where breakdown is
        {"终版": K, "初版_only": L}
    """
    results_dir = style_distiller_dir / "style-write" / "results"
    if not results_dir.exists():
        return 0, {"终版": 0, "初版_only": 0}

    # topic_key -> "终版" | "初版"
    chosen: dict[str, str] = {}
    for sub in ("初版", "终版"):
        sub_dir = results_dir / sub
        if not sub_dir.exists():
            continue
        for f in sub_dir.glob("result-*.md"):
            key = _topic_key(f.stem)
            if sub == "终版":
                # 终版 always wins (overwrite any prior 初版 entry)
                chosen[key] = "终版"
            elif key not in chosen:
                chosen[key] = "初版"

    breakdown = {"终版": 0, "初版_only": 0}
    for version in chosen.values():
        breakdown[version] += 1
    return sum(breakdown.values()), breakdown


def infer_state(positive_samples: int, self_written: int) -> str:
    """Stage judgement by total samples = positive + self-written (equal weight)."""
    total = positive_samples + self_written
    if total <= 2:
        return "cold_start"
    if total <= 9:
        return "sprout"
    if total <= 29:
        return "learning"
    return "mature"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-dir", type=Path, default=Path.home() / ".claude" / "styles")
    parser.add_argument(
        "--style-distiller-dir",
        type=Path,
        default=Path.home() / ".claude" / "skills" / "style-distiller",
        help="Style-distiller skill root, used to count self-written samples in style-write/results/.",
    )
    args = parser.parse_args()

    profile_dir = args.profile_dir.expanduser()
    style_distiller_dir = args.style_distiller_dir.expanduser()
    weights = load_weights(profile_dir)
    positive = count_files(profile_dir / "samples" / "positive")
    negative = count_files(profile_dir / "samples" / "negative")
    drafts = count_files(profile_dir / "drafts")
    backups = count_files(profile_dir / "backups", "*")
    profile_files = count_files(profile_dir / "profile")
    self_written, self_written_breakdown = count_self_written(style_distiller_dir)
    total_samples = positive + self_written
    weights_state = weights.get("current_state")
    inferred_state = infer_state(positive, self_written)
    state = weights_state or inferred_state  # weights.json wins if set

    print(f"profile_dir={profile_dir}")
    print(f"state={state}")
    print(f"state_basis={'weights_json' if weights_state else 'inferred'}")
    print(f"state_inferred={inferred_state}")
    print(f"positive_samples={positive}")
    print(f"self_written_samples={self_written}")
    print(f"self_written_breakdown={self_written_breakdown}")
    print(f"total_samples={total_samples}")
    print(f"negative_samples={negative}")
    print(f"drafts={drafts}")
    print(f"backups={backups}")
    print(f"profile_files={profile_files}")
    if weights.get("last_updated"):
        print(f"last_updated={weights['last_updated']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
