#!/usr/bin/env python3
"""Retrieve likely relevant positive samples for a writing task.

Scores sample files by keyword overlap, dimension match, and recency based on
frontmatter.

Usage:
    python scripts/retrieve_samples.py --profile-dir ~/.claude/styles --topic "35岁后的变化" --dimension voice
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9_\u4e00-\u9fff]+")


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in WORD_RE.findall(text) if len(token.strip()) > 1}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, parts[2]


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value[:10], fmt).date()
        except ValueError:
            pass
    return None


def time_score(fed_at: date | None) -> float:
    if fed_at is None:
        return 0.5
    months_old = max((date.today() - fed_at).days / 30, 0)
    return math.pow(0.95, months_old)


def dimension_score(meta: dict[str, str], dimensions: set[str]) -> float:
    if not dimensions:
        return 0.5
    sample_dimensions = set(tokenize(meta.get("dimensions", "")))
    if not sample_dimensions:
        return 0.0
    return len(sample_dimensions & dimensions) / len(dimensions)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-dir", type=Path, default=Path.home() / ".claude" / "styles")
    parser.add_argument("--topic", required=True, help="Writing topic or keywords")
    parser.add_argument("--dimension", action="append", default=[], help="Preferred dimension, can repeat")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    samples_dir = args.profile_dir.expanduser() / "samples" / "positive"
    topic_tokens = tokenize(args.topic)
    requested_dimensions = {d.lower() for d in args.dimension}
    scored: list[tuple[float, Path, float, float, float]] = []

    for sample in samples_dir.glob("*.md"):
        text = sample.read_text(encoding="utf-8-sig")
        meta, body = parse_frontmatter(text)
        sample_tokens = tokenize(sample.stem + " " + meta.get("remark", "") + " " + body[:2000])
        topic = len(topic_tokens & sample_tokens) / max(len(topic_tokens), 1)
        dim = dimension_score(meta, requested_dimensions)
        fresh = time_score(parse_date(meta.get("fed_at")))
        final = topic * 0.5 + dim * 0.3 + fresh * 0.2
        scored.append((final, sample, topic, dim, fresh))

    scored.sort(reverse=True, key=lambda item: item[0])

    for final, sample, topic, dim, fresh in scored[: args.limit]:
        print(f"{final:.3f}\ttopic={topic:.2f}\tdimension={dim:.2f}\ttime={fresh:.2f}\t{sample.name}")

    if not scored:
        print("No positive samples found.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
