"""Discovery module for finding languages in the repository."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class LanguageInfo:
    """Information about a discovered language."""

    slug: str
    path: str
    chapters_path: str
    chapter_count: int
    has_spec: bool


def discover_languages(
    languages_dir: Path,
    pattern: str | None = None,
) -> list[LanguageInfo]:
    """
    Discover all languages in the languages directory.

    A valid language directory must contain a 'chapters/' subdirectory
    with at least one markdown file.

    Args:
        languages_dir: Directory containing language folders
        pattern: Optional pattern to filter language names (case-insensitive substring match)

    Returns:
        List of LanguageInfo objects for discovered languages
    """
    languages: list[LanguageInfo] = []

    if not languages_dir.is_dir():
        return languages

    for item in sorted(languages_dir.iterdir()):
        if not item.is_dir():
            continue

        # Skip hidden directories
        if item.name.startswith("."):
            continue

        chapters_dir = item / "chapters"
        if not chapters_dir.is_dir():
            continue

        # Count markdown files in chapters
        chapter_files = list(chapters_dir.glob("*.md"))
        if not chapter_files:
            continue

        # Apply pattern filter if provided
        if pattern and pattern.lower() not in item.name.lower():
            continue

        languages.append(
            LanguageInfo(
                slug=item.name,
                path=str(item.resolve()),
                chapters_path=str(chapters_dir.resolve()),
                chapter_count=len(chapter_files),
                has_spec=(item / "spec.md").exists(),
            )
        )

    return languages


def languages_to_json(languages: list[LanguageInfo], compact: bool = False) -> str:
    """
    Convert discovered languages to JSON format.

    Args:
        languages: List of LanguageInfo objects
        compact: If True, output compact JSON for CI/CD usage

    Returns:
        JSON string representation
    """
    data = [asdict(lang) for lang in languages]
    if compact:
        return json.dumps(data, separators=(",", ":"))
    return json.dumps(data, indent=2)


def get_language_slugs(languages: list[LanguageInfo]) -> list[str]:
    """Extract just the slugs from discovered languages."""
    return [lang.slug for lang in languages]
