#!/usr/bin/env python3
"""Export a style-distiller profile into one Markdown file.

Usage:
    python scripts/export_profile.py --profile-dir ~/.claude/styles --output style-export.md
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


PROFILE_ORDER = [
    "persona.md",
    "hook.md",
    "rhythm.md",
    "voice.md",
    "verve.md",
    "closing.md",
    "vocabulary.md",
    "format.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-dir", type=Path, default=Path.home() / ".claude" / "styles")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    profile_dir = args.profile_dir.expanduser()
    sections = [
        "# Style Distiller Profile Export",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"Source: `{profile_dir}`",
        "",
    ]

    weights = read(profile_dir / "weights.json")
    if weights:
        sections.extend(["## weights.json", "", "```json", weights.strip(), "```", ""])

    for name in PROFILE_ORDER:
        path = profile_dir / "profile" / name
        content = read(path)
        if content:
            sections.extend([f"## profile/{name}", "", content.strip(), ""])

    history = read(profile_dir / "history.md")
    if history:
        sections.extend(["## history.md", "", history.strip(), ""])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    print(f"exported={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
