from .cli import app, main  # re-export for entrypoint
from .discover import LanguageInfo, discover_languages, get_language_slugs, languages_to_json

__all__ = ["app", "main", "discover_languages", "get_language_slugs", "languages_to_json", "LanguageInfo"]
