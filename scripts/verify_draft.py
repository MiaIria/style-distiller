#!/usr/bin/env python3
"""Run basic style-distiller checks on a generated draft.

The script performs deterministic checks only: forbidden words, rough length,
and paragraph count.

Usage:
    python scripts/verify_draft.py draft.md --profile-dir ~/.claude/styles --target-words 500
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


WORD_RE = re.compile(r"[\w\u4e00-\u9fff]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def extract_terms(line: str) -> list[str]:
    cleaned = re.sub(r"[`*_#>\-\[\]（）()：:，,。；;、]", " ", line)
    terms = [term.strip() for term in cleaned.split() if term.strip()]
    stop = {"禁用", "忌讳", "不用", "反特征", "来自反样本"}
    return [term for term in terms if term not in stop]


def collect_forbidden(profile_dir: Path) -> list[str]:
    candidates = [
        profile_dir / "profile" / "vocabulary.md",
        profile_dir / "profile" / "persona.md",
        profile_dir / "profile" / "closing.md",
    ]
    forbidden: list[str] = []
    for path in candidates:
        for line in read(path).splitlines():
            if any(marker in line for marker in ("禁用", "忌讳", "不用", "反特征")):
                forbidden.extend(extract_terms(line))
    return sorted(set(term for term in forbidden if len(term) >= 2))


def visible_text(markdown: str) -> str:
    text = re.sub(r"---[\s\S]*?---", "", markdown, count=1)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"#+\s*", "", text)
    return text.strip()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--profile-dir", type=Path, default=Path.home() / ".claude" / "styles")
    parser.add_argument("--target-words", type=int, default=0)
    args = parser.parse_args()

    profile_dir = args.profile_dir.expanduser()
    draft = visible_text(read(args.draft))
    char_count = len(WORD_RE.findall(draft))
    paragraphs = [p for p in re.split(r"\n\s*\n", draft) if p.strip()]
    forbidden = collect_forbidden(profile_dir)
    hits = [term for term in forbidden if term in draft]

    print(f"draft={args.draft}")
    print(f"characters={char_count}")
    print(f"paragraphs={len(paragraphs)}")
    if args.target_words:
        lower = int(args.target_words * 0.8)
        upper = int(args.target_words * 1.2)
        print(f"target_range={lower}-{upper}")
        print(f"length_status={'ok' if lower <= char_count <= upper else 'out_of_range'}")
    print(f"forbidden_hits={len(hits)}")
    for term in hits:
        print(f"- {term}")

    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
