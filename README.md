# Language Prompts & Guide Builder

Workspace for generating rich, standardized tourist guides. Guides live in `languages/<slug>` and are built into PDFs via a Typer CLI (`guide-cli`) managed by `uv`.

## Repository Layout
- `languages/<slug>/sections/` — markdown fragments that get concatenated.
- `languages/<slug>/outputs/` — temporary build folder (combined markdown + PDF before moving).
- `outputs/` — finalized PDFs for all languages.
- `apps/guide-cli/` — Typer-based CLI package for assembling guides.
- `agents/` — prompt/checklist docs for consistent generation.
- `scripts/install-guide-cli.sh` — helper to install the CLI as a user-level tool.

## Prerequisites
- Python 3.10+ (uv will manage envs).
- `uv` installed (`pip install uv` or official installer).
- `pandoc` and LaTeX engine (`xelatex` recommended for Unicode/CJK). macOS: `brew install pandoc mactex-no-gui` (or ensure `pdflatex/xelatex` is present).
- A CJK font (defaults attempt Hiragino/Noto/IPA). Install e.g. `Noto Sans CJK JP` if PDFs complain about missing glyphs.

## Quick Start
```bash
# install workspace deps (creates .venv and uv.lock if missing)
uv sync

# build Japanese guide (uses languages/japanese)
uv run guide-cli japanese

# keep combined markdown or choose a font if needed
uv run guide-cli japanese --keep-md --cjk-font "Noto Sans CJK JP"

# final PDF appears in outputs/japanese-guide.pdf
```

## CLI Options (summary)
- `--languages-dir PATH` — base directory for language folders (default `languages/`).
- `--output-dir/-o PATH` — final output directory (default `outputs/`).
- `--pdf-name TEXT` — custom PDF name (no extension).
- `--keep-md` — retain combined markdown in `<language>/outputs/`.
- `--pdf-engine TEXT` — Pandoc PDF engine (default `xelatex` for Unicode/CJK).
- `--cjk-font TEXT` — font(s) to try for CJK text; can be passed multiple times.

You can also install the CLI as a user-level tool:
```bash
./scripts/install-guide-cli.sh
guide-cli japanese
```

## Adding a New Language
1) Create `languages/<slug>/sections/` with numbered markdown files (e.g., `00-cover.md`, `02-vocabulary-shopping.md`, etc.).
2) Place any spec/reference in `languages/<slug>/spec.md`.
3) Run `uv run guide-cli <slug>` to produce `outputs/<slug>-guide.pdf`.

## Notes on Fonts & PDF Generation
- Defaults try common CJK fonts (Hiragino, Noto Sans/Serif CJK, Source Han, IPA). If you hit font errors, pass `--cjk-font "Noto Sans CJK JP"` and ensure it is installed.
- `xelatex` is the default engine; switch via `--pdf-engine` if your LaTeX setup differs.

## Housekeeping
- Outputs and intermediate markdown are ignored via `.gitignore`; commit only source markdown, specs, and code.
- Workspace is defined in `pyproject.toml`; keep new apps under `apps/` and new guides under `languages/`.
