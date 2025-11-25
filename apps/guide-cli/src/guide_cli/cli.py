from __future__ import annotations

import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import typer

from .discover import discover_languages, get_language_slugs, languages_to_json

app = typer.Typer(help="Generate standardized tourist guide PDFs from a language folder.")

# Languages that require CJK font support
CJK_LANGUAGES = frozenset({"japanese", "chinese", "korean"})


def _check_cjk_fonts_available() -> bool:
    """Check if any CJK fonts are available on the system."""
    # Try to list fonts using fc-list (Linux/macOS) or system_profiler (macOS)
    if platform.system() == "Darwin":
        # macOS: Check for common Japanese fonts
        result = subprocess.run(
            ["system_profiler", "SPFontsDataType"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        fonts_text = result.stdout.lower()
        return any(
            font_name in fonts_text
            for font_name in ["hiragino", "noto sans cjk", "noto serif cjk", "source han", "ipa"]
        )
    elif shutil.which("fc-list"):
        # Linux: Use fontconfig
        result = subprocess.run(["fc-list", ":lang=ja"], capture_output=True, text=True, timeout=10)
        return bool(result.stdout.strip())
    return False  # Unknown system, assume fonts might not be available


def _install_cjk_fonts_macos() -> bool:
    """Attempt to install CJK fonts on macOS using Homebrew. Returns True if successful."""
    if shutil.which("brew") is None:
        typer.echo("⚠️  Homebrew not found. Please install Homebrew first:", err=True)
        typer.echo("   Visit: https://brew.sh", err=True)
        return False

    typer.echo("📦 Installing Noto CJK fonts via Homebrew...")

    # Install font-noto-sans-cjk
    result1 = subprocess.run(
        ["brew", "install", "--cask", "font-noto-sans-cjk"],
        capture_output=True,
        text=True,
    )

    # Install font-noto-serif-cjk
    result2 = subprocess.run(
        ["brew", "install", "--cask", "font-noto-serif-cjk"],
        capture_output=True,
        text=True,
    )

    if result1.returncode == 0 or result2.returncode == 0:
        typer.echo("✅ CJK fonts installed successfully!")
        return True
    else:
        typer.echo("⚠️  Font installation failed. Please install manually:", err=True)
        typer.echo("   brew install --cask font-noto-sans-cjk font-noto-serif-cjk", err=True)
        return False


def _ensure_cjk_fonts(auto_install: bool = True) -> None:
    """Ensure CJK fonts are available, installing them if necessary and permitted."""
    typer.echo("🔍 Checking for CJK fonts...")

    if _check_cjk_fonts_available():
        typer.echo("✅ CJK fonts detected")
        return

    typer.echo("⚠️  No CJK fonts detected on your system")

    if not auto_install:
        _print_manual_font_instructions()
        raise typer.Exit(code=1)

    # Auto-install on macOS
    if platform.system() == "Darwin":
        if typer.confirm("Would you like to install CJK fonts automatically via Homebrew?", default=True):
            if _install_cjk_fonts_macos():
                return
        else:
            _print_manual_font_instructions()
            raise typer.Exit(code=1)
    else:
        _print_manual_font_instructions()
        raise typer.Exit(code=1)


def _print_manual_font_instructions() -> None:
    """Print instructions for manually installing CJK fonts."""
    system = platform.system()
    typer.echo("\n📖 Manual Installation Instructions:", err=True)

    if system == "Darwin":
        typer.echo("   macOS:", err=True)
        typer.echo("   brew install --cask font-noto-sans-cjk font-noto-serif-cjk", err=True)
    elif system == "Linux":
        typer.echo("   Linux (Debian/Ubuntu):", err=True)
        typer.echo("   sudo apt-get install fonts-noto-cjk", err=True)
        typer.echo("\n   Linux (Fedora/RHEL):", err=True)
        typer.echo("   sudo dnf install google-noto-sans-cjk-fonts", err=True)
    elif system == "Windows":
        typer.echo("   Windows:", err=True)
        typer.echo("   Download from: https://www.google.com/get/noto/#sans-jpan", err=True)
        typer.echo("   Install the .ttf files by double-clicking them", err=True)
    else:
        typer.echo("   Please install a Japanese/CJK font compatible with XeLaTeX", err=True)
        typer.echo("   Recommended: Noto Sans CJK JP or Noto Serif CJK JP", err=True)

    typer.echo("\n   After installation, run this command again.\n", err=True)


def _section_sort_key(path: Path) -> tuple[int, str]:
    """Sort numerically when files start with 00-, 01-, etc., then by name."""
    stem = path.stem
    prefix = stem.split("-", 1)[0]
    try:
        return int(prefix), stem
    except ValueError:
        return 10_000, stem


def _collect_sections(sections_dir: Path | None, chapters_dir: Path | None = None) -> list[Path]:
    """
    Collect markdown files from chapters/ (preferred) and sections/ (fallback).

    Files are sorted by their numeric prefix (00-, 01-, etc.) and combined in order.
    """
    files: list[Path] = []

    if chapters_dir and chapters_dir.is_dir():
        files.extend(sorted(chapters_dir.glob("*.md"), key=_section_sort_key))

    if sections_dir and sections_dir.is_dir():
        files.extend(sorted(sections_dir.glob("*.md"), key=_section_sort_key))

    if not files:
        raise typer.BadParameter(
            f"No markdown files found. Looked in chapters={chapters_dir} and sections={sections_dir}"
        )

    return files


def _combine_sections(section_files: Iterable[Path], combined_path: Path) -> Path:
    combined_path.parent.mkdir(parents=True, exist_ok=True)
    parts = [path.read_text(encoding="utf-8") for path in section_files]
    combined_path.write_text("\n\n".join(parts), encoding="utf-8")
    return combined_path


def _render_pdf(
    md_path: Path, pdf_path: Path, title: str, pdf_engine: str, cjk_fonts: list[str] | None
) -> Path:
    if shutil.which("pandoc") is None:
        raise RuntimeError(
            "pandoc is required to build PDFs. Install it (e.g. `brew install pandoc`) "
            "and ensure LaTeX tooling like TeX Live is available."
        )

    candidates: list[str | None] = cjk_fonts or [
        "Hiragino Sans W3",  # macOS default Japanese font
        "Hiragino Mincho ProN",
        "Noto Sans CJK JP",
        "Noto Serif CJK JP",
        "Source Han Sans",
        "IPAMincho",
        "IPAGothic",
        None,  # final fallback
    ]

    errors: list[str] = []
    for font in candidates:
        cmd = [
            "pandoc",
            str(md_path),
            "-o",
            str(pdf_path),
            "--from=markdown",
            "--pdf-engine",
            pdf_engine,
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "-V",
            f"title={title}",
            "-V",
            "geometry:margin=1in",
            "-V",
            "colorlinks=true",
        ]
        if font:
            cmd.extend(["-V", f"mainfont={font}", "-V", f"CJKmainfont={font}"])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return pdf_path

        errors.append(
            f"font={font or 'default'} code={result.returncode} "
            f"stdout={result.stdout.strip() or 'n/a'} stderr={result.stderr.strip() or 'n/a'}"
        )

    raise RuntimeError(
        "pandoc failed while creating the PDF after trying fonts: "
        f"{', '.join(str(f or 'default') for f in candidates)}. "
        "Consider installing a CJK font (e.g., Noto Sans CJK JP) or set --cjk-font. "
        f"Details:\n" + "\n".join(errors)
    )


def _resolve_folder(slug_or_path: Path, languages_dir: Path) -> Path:
    """Resolve a language folder, preferring an explicit path, otherwise languages/<slug>."""
    if slug_or_path.is_dir():
        return slug_or_path.resolve()
    candidate = (languages_dir / slug_or_path).resolve()
    if candidate.is_dir():
        return candidate
    raise typer.BadParameter(f"Could not find language folder at {slug_or_path} or {candidate}")


@app.command()
def guide(
    language: Path = typer.Argument(
        ...,
        help="Language slug or path (defaults to languages/<slug> if not a directory).",
        show_default=False,
    ),
    languages_dir: Path = typer.Option(
        Path("languages"), "--languages-dir", help="Directory containing language guides."
    ),
    output_dir: Path = typer.Option(Path("outputs"), "--output-dir", "-o", help="Final outputs directory."),
    pdf_name: str | None = typer.Option(None, help="Custom PDF name (without extension)."),
    keep_combined_markdown: bool = typer.Option(
        False, "--keep-md", help="Keep the combined markdown used to render the PDF."
    ),
    pdf_engine: str = typer.Option(
        "xelatex", "--pdf-engine", help="Pandoc PDF engine (use xelatex/lualatex for Unicode)."
    ),
    cjk_font: list[str] = typer.Option(
        None,
        "--cjk-font",
        help="Font(s) to try for CJK text (can be passed multiple times). Defaults include Hiragino/Noto/IPA.",
    ),
    skip_font_check: bool = typer.Option(
        False,
        "--skip-font-check",
        help="Skip automatic CJK font checking and installation.",
    ),
) -> None:
    """
    Build a PDF for a language guide by combining all markdown sections,
    rendering them to a PDF in <language>/outputs, then moving the PDF
    into the root-level outputs directory.

    The CLI automatically checks for CJK fonts and offers to install them
    on macOS if missing. Use --skip-font-check to bypass this check.

    Returns:
        Path to the generated PDF file.
    """
    # Check for CJK fonts if building a language that needs them
    if not skip_font_check and language.name in CJK_LANGUAGES:
        try:
            _ensure_cjk_fonts(auto_install=True)
        except typer.Exit:
            raise

    languages_dir = languages_dir.resolve()
    folder = _resolve_folder(language, languages_dir)
    language = folder.name
    sections_dir = folder / "sections"
    chapters_dir = folder / "chapters"
    language_output_dir = folder / "outputs"

    try:
        section_files = _collect_sections(sections_dir, chapters_dir)
    except typer.BadParameter as exc:
        typer.echo(f"[error] {exc}", err=True)
        raise typer.Exit(code=1)

    pdf_basename = f"{language}-guide" if pdf_name is None else pdf_name
    combined_md = language_output_dir / f"{pdf_basename}.md"
    pdf_path = language_output_dir / f"{pdf_basename}.pdf"

    using_chapters = chapters_dir.exists() and any(chapters_dir in f.parents for f in section_files)
    if using_chapters:
        typer.echo(f"Combining {len(section_files)} chapter files from {chapters_dir}...")
    else:
        typer.echo(f"Combining {len(section_files)} section files from {sections_dir}...")
    _combine_sections(section_files, combined_md)

    try:
        typer.echo("Rendering PDF with pandoc...")
        _render_pdf(
            combined_md,
            pdf_path,
            title=f"{language.title()} Tourist Guide",
            pdf_engine=pdf_engine,
            cjk_fonts=cjk_font or None,
        )
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    final_pdf = output_dir / pdf_path.name
    if final_pdf.exists():
        final_pdf.unlink()
    shutil.move(str(pdf_path), final_pdf)

    if keep_combined_markdown:
        typer.echo(f"Combined markdown retained at {combined_md}")
    else:
        combined_md.unlink(missing_ok=True)

    typer.echo(f"Guide ready: {final_pdf}")
    return final_pdf


@app.command()
def discover(
    languages_dir: Path = typer.Option(
        Path("languages"), "--languages-dir", help="Directory containing language guides."
    ),
    pattern: str | None = typer.Option(
        None, "--pattern", "-p", help="Filter languages by pattern (case-insensitive substring match)."
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Output in JSON format for CI/CD integration."
    ),
    compact: bool = typer.Option(
        False, "--compact", "-c", help="Output compact JSON (for GitHub Actions)."
    ),
    slugs_only: bool = typer.Option(
        False, "--slugs-only", "-s", help="Output only language slugs, one per line."
    ),
) -> None:
    """
    Discover all available languages in the languages directory.

    Languages are directories containing a 'chapters/' subdirectory with markdown files.
    """
    languages_dir = languages_dir.resolve()
    languages = discover_languages(languages_dir, pattern)

    if not languages:
        typer.echo("No languages found.", err=True)
        raise typer.Exit(code=1)

    if slugs_only:
        for slug in get_language_slugs(languages):
            typer.echo(slug)
    elif json_output or compact:
        typer.echo(languages_to_json(languages, compact=compact))
    else:
        typer.echo(f"Found {len(languages)} language(s):\n")
        for lang in languages:
            typer.echo(f"  • {lang.slug}")
            typer.echo(f"    Path: {lang.path}")
            typer.echo(f"    Chapters: {lang.chapter_count}")
            typer.echo(f"    Has spec: {'Yes' if lang.has_spec else 'No'}")
            typer.echo()


@app.command("build-all")
def build_all(
    languages_dir: Path = typer.Option(
        Path("languages"), "--languages-dir", help="Directory containing language guides."
    ),
    output_dir: Path = typer.Option(
        Path("outputs"), "--output-dir", "-o", help="Final outputs directory."
    ),
    pattern: str | None = typer.Option(
        None, "--pattern", "-p", help="Filter languages by pattern."
    ),
    skip_font_check: bool = typer.Option(
        False, "--skip-font-check", help="Skip automatic CJK font checking."
    ),
    pdf_engine: str = typer.Option(
        "xelatex", "--pdf-engine", help="Pandoc PDF engine."
    ),
    manifest_file: Path | None = typer.Option(
        None, "--manifest", "-m", help="Path to write build manifest JSON."
    ),
    continue_on_error: bool = typer.Option(
        False, "--continue-on-error", help="Continue building other languages if one fails."
    ),
) -> None:
    """
    Build PDF guides for all discovered languages.

    Generates a manifest file tracking build status for each language.
    """
    languages_dir = languages_dir.resolve()
    output_dir = output_dir.resolve()
    languages = discover_languages(languages_dir, pattern)

    if not languages:
        typer.echo("No languages found to build.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Building {len(languages)} language(s)...\n")

    manifest = {
        "build_time": datetime.now(timezone.utc).isoformat(),
        "languages_dir": str(languages_dir),
        "output_dir": str(output_dir),
        "builds": [],
    }

    success_count = 0
    failure_count = 0

    for lang in languages:
        typer.echo(f"[{lang.slug}] Building...")
        build_entry = {
            "slug": lang.slug,
            "chapters": lang.chapter_count,
            "status": "pending",
            "output_file": None,
            "error": None,
        }

        try:
            # Build the guide using the existing guide command logic
            pdf_path = _build_single_language(
                language_slug=lang.slug,
                languages_dir=languages_dir,
                output_dir=output_dir,
                skip_font_check=skip_font_check,
                pdf_engine=pdf_engine,
            )
            build_entry["status"] = "success"
            build_entry["output_file"] = str(pdf_path)
            success_count += 1
            typer.echo(f"[{lang.slug}] ✓ Built: {pdf_path}")
        except Exception as e:
            build_entry["status"] = "failed"
            build_entry["error"] = str(e)
            failure_count += 1
            typer.echo(f"[{lang.slug}] ✗ Failed: {e}", err=True)
            if not continue_on_error:
                manifest["builds"].append(build_entry)
                _write_manifest(manifest, manifest_file, output_dir)
                raise typer.Exit(code=1)

        manifest["builds"].append(build_entry)

    # Write manifest
    _write_manifest(manifest, manifest_file, output_dir)

    # Summary
    typer.echo(f"\nBuild complete: {success_count} succeeded, {failure_count} failed")

    if failure_count > 0:
        raise typer.Exit(code=1)


def _build_single_language(
    language_slug: str,
    languages_dir: Path,
    output_dir: Path,
    skip_font_check: bool,
    pdf_engine: str,
) -> Path:
    """Build a single language guide and return the output path."""
    folder = languages_dir / language_slug
    if not folder.is_dir():
        raise ValueError(f"Language folder not found: {folder}")

    sections_dir = folder / "sections"
    chapters_dir = folder / "chapters"
    language_output_dir = folder / "outputs"

    # Check for CJK fonts if needed
    if not skip_font_check and language_slug in CJK_LANGUAGES:
        _ensure_cjk_fonts(auto_install=False)

    section_files = _collect_sections(sections_dir, chapters_dir)

    pdf_basename = f"{language_slug}-guide"
    combined_md = language_output_dir / f"{pdf_basename}.md"
    pdf_path = language_output_dir / f"{pdf_basename}.pdf"

    _combine_sections(section_files, combined_md)

    _render_pdf(
        combined_md,
        pdf_path,
        title=f"{language_slug.title()} Tourist Guide",
        pdf_engine=pdf_engine,
        cjk_fonts=None,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    final_pdf = output_dir / pdf_path.name
    if final_pdf.exists():
        final_pdf.unlink()
    shutil.move(str(pdf_path), final_pdf)

    # Clean up combined markdown
    combined_md.unlink(missing_ok=True)

    return final_pdf


def _write_manifest(manifest: dict, manifest_file: Path | None, output_dir: Path) -> None:
    """Write build manifest to file."""
    if manifest_file is None:
        manifest_file = output_dir / "build-manifest.json"

    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    app()
