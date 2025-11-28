# guide-cli

CLI to assemble language communication guide chapters into a single PDF.

## Overview

The CLI discovers and combines numbered markdown chapters from `languages/<slug>/chapters/`, then uses pandoc/XeLaTeX to render a PDF.

## Expected Chapter Structure

Chapters are numbered files in `languages/<slug>/chapters/`:

```
00-cover.md              # Introduction, guide structure
01-core-phrases.md       # Pattern templates, greetings, emergencies
02-language-foundations.md
03-pronunciation.md
04-writing-systems.md
05-directions-navigation.md
06-transportation.md
07-restaurants.md
08-shopping.md
09-hotels.md
10-cultural-guide.md
```

Files are sorted numerically by prefix (00-, 01-, etc.) and combined in order.

## Usage

```bash
# install deps for this workspace
uv sync

# build a guide (uses languages/<slug> by default)
uv run guide-cli japanese

# keep the combined markdown
uv run guide-cli japanese --keep-md

# specify a font if your system lacks defaults
uv run guide-cli japanese --cjk-font "Noto Sans CJK JP"

# discover available languages
uv run guide-cli discover

# build all languages
uv run guide-cli build-all --continue-on-error
```

## Commands

### `guide-cli <slug>`
Build a single language guide.

### `guide-cli discover`
List all available languages in the languages directory.

Options:
- `--json` / `-j` — Output JSON format
- `--compact` / `-c` — Compact JSON for CI/CD
- `--slugs-only` / `-s` — Output only language slugs

### `guide-cli build-all`
Build PDF guides for all discovered languages.

Options:
- `--pattern` / `-p` — Filter languages by pattern
- `--continue-on-error` — Continue building if one language fails
- `--manifest` / `-m` — Path to write build manifest JSON

## Options

- `--languages-dir` — Base directory for language folders (default `languages/`)
- `--output-dir` / `-o` — Final output directory (default `outputs/`)
- `--pdf-name` — Custom PDF name (without `.pdf`)
- `--keep-md` — Retain the combined markdown in `<language>/outputs/`
- `--pdf-engine` — PDF engine for pandoc (default `xelatex` for Unicode/CJK)
- `--cjk-font` — One or more fonts to try for CJK text
- `--skip-font-check` — Skip automatic CJK font checking

## Adding New Chapters

1. Create a new markdown file with appropriate numeric prefix
2. The CLI automatically discovers all `*.md` files in `chapters/`
3. Files are sorted by numeric prefix, then alphabetically
4. Run `guide-cli <slug>` to build the updated PDF
