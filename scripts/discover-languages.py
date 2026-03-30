#!/usr/bin/env python3
"""
Helper script for discovering languages in GitHub Actions workflows.

Delegates to guide_cli.discover so that discovery logic has a single
authoritative implementation. Requires the guide-cli package to be
installed (e.g. ``uv sync``).

Usage:
    python scripts/discover-languages.py [--languages-dir LANGUAGES_DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from guide_cli.discover import discover_languages, get_language_slugs, languages_to_json


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
        print(languages_to_json(languages))
    elif args.output_format == "matrix":
        print(languages_to_json(languages, compact=True))
    else:  # slugs
        for slug in get_language_slugs(languages):
            print(slug)

    return 0


if __name__ == "__main__":
    sys.exit(main())
