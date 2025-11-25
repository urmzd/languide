# Language Prompts & Guide Builder

Workspace for generating standardized tourist guides. Each language lives under `languages/<slug>` with numbered chapters, and PDFs are built via a Typer CLI (`guide-cli`) managed by `uv`.

## Repository Layout
- `languages/<slug>/chapters/` — book-style chapters (00-cover, 01-foundations, 02-pronunciation, 03-writing-systems, 04-directions/navigation, 05-transport, 06-restaurants, 07-shopping, 08-hotels, 09-cultural).
- `languages/<slug>/outputs/` — temporary build folder (combined markdown + PDF before moving).
- `outputs/` — finalized PDFs for all languages.
- `apps/guide-cli/` — Typer CLI package for assembling guides.
- `agents/` — prompt/checklist docs for consistent generation.
- `scripts/install-fonts.sh` — helper to install CJK fonts (macOS).

## Prerequisites
- Python 3.10+ with `uv` installed.
- `pandoc` and LaTeX engine (`xelatex` recommended for Unicode/CJK). macOS: `brew install pandoc mactex-no-gui`.
- A Japanese-capable font (e.g., Noto Sans/Serif CJK JP). Use `./scripts/install-fonts.sh` on macOS if needed.

## Quick Start
```bash
# install deps into the workspace .venv
uv sync

# build Japanese guide (uses languages/japanese)
uv run guide-cli japanese

# keep combined markdown or specify a font if necessary
uv run guide-cli japanese --keep-md --cjk-font "Noto Sans CJK JP"

# optional: install as a user-level tool
uv tool install --editable apps/guide-cli
guide-cli japanese
```

## CLI Options (summary)
- `--languages-dir PATH` — base directory for language folders (default `languages/`).
- `--output-dir/-o PATH` — final output directory (default `outputs/`).
- `--pdf-name TEXT` — custom PDF name (no extension).
- `--keep-md` — retain combined markdown in `<language>/outputs/`.
- `--pdf-engine TEXT` — Pandoc PDF engine (default `xelatex` for Unicode/CJK).
- `--cjk-font TEXT` — font(s) to try for CJK text; can be passed multiple times.

## Adding a New Language
1) Create `languages/<slug>/chapters/` with numbered chapters following the pattern above.
2) Add any specs/reference in `languages/<slug>/spec.md`.
3) Run `uv run guide-cli <slug>` to produce `outputs/<slug>-guide.pdf`.

## Notes on Fonts
- Defaults try common CJK fonts (Hiragino, Noto Sans/Serif CJK, Source Han, IPA). If glyphs are missing, pass `--cjk-font "Noto Sans CJK JP"` and ensure it is installed.
- macOS helper: `./scripts/install-fonts.sh`.

## Housekeeping
- Build outputs are ignored via `.gitignore`; commit only source markdown/specs and code.
- Workspace is defined in `pyproject.toml`; keep new apps under `apps/` and guides under `languages/`.
