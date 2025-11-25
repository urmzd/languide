#!/usr/bin/env python3
"""
Helper script for discovering languages in GitHub Actions workflows.

This script provides a standalone way to discover languages without
requiring the full guide-cli installation. It outputs JSON that can
be consumed by GitHub Actions matrix strategies.

Usage:
    python scripts/discover-languages.py [--languages-dir LANGUAGES_DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def discover_languages(languages_dir: Path) -> list[dict]:
    """Discover all languages with chapters/ subdirectories."""
    languages = []

    if not languages_dir.is_dir():
        return languages

    for item in sorted(languages_dir.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue

        chapters_dir = item / "chapters"
        if not chapters_dir.is_dir():
            continue

        chapter_files = list(chapters_dir.glob("*.md"))
        if not chapter_files:
            continue

        languages.append({
            "slug": item.name,
            "chapters": len(chapter_files),
        })

    return languages


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover languages for GitHub Actions workflows"
    )
    parser.add_argument(
        "--languages-dir",
        type=Path,
        default=Path("languages"),
        help="Directory containing language folders (default: languages)",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "matrix", "slugs"],
        default="matrix",
        help="Output format: json (pretty), matrix (compact for GH Actions), slugs (one per line)",
    )

    args = parser.parse_args()
    languages = discover_languages(args.languages_dir.resolve())

    if not languages:
        print("[]" if args.output_format != "slugs" else "", end="")
        return 0

    if args.output_format == "json":
        print(json.dumps(languages, indent=2))
    elif args.output_format == "matrix":
        # Output format suitable for GitHub Actions matrix
        print(json.dumps(languages, separators=(",", ":")))
    else:  # slugs
        for lang in languages:
            print(lang["slug"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
