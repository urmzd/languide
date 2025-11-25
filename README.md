# Language Prompts & Guide Builder

Workspace for generating rich, standardized tourist guides optimized for **one-line scanning** with **tiered politeness levels** and **regional variations**. Guides live in `languages/<slug>` and are built into PDFs via a Typer CLI (`guide-cli`) managed by `uv`.

## ✨ New Features

### 📊 Tiered Politeness Structure
Every conversational phrase shows three politeness levels stacked vertically:
- **Casual (友達)** - for friends only (use with caution)
- **Polite (丁寧)** - standard polite form - **RECOMMENDED FOR TOURISTS**
- **Very Polite (とても丁寧)** - extra formal (luxury establishments, formal situations)

### 🗾 Regional Variations (Tokyo/Osaka/Kyoto)
All phrases include regional columns showing:
- Where each phrase is commonly used
- Regional dialect variations
- Cultural differences in usage
- Regional specialties and customs

### 🔍 One-Line Scannable Format
- Each phrase has its own section header for quick Ctrl+F searching
- Clear visual hierarchy with generous white space
- "TOURIST ESSENTIAL" markers on critical phrases
- Context and usage notes for every phrase

### 🎨 Automatic Font Management
The CLI now **automatically checks for and installs CJK fonts**:
- Detects if Japanese/Chinese/Korean fonts are available
- On macOS: Offers to install via Homebrew automatically
- Provides platform-specific installation instructions
- No more manual font setup required!

## Repository Layout
- `languages/<slug>/sections/` — markdown fragments that get concatenated.
- `languages/<slug>/outputs/` — temporary build folder (combined markdown + PDF before moving).
- `outputs/` — finalized PDFs for all languages.
- `apps/guide-cli/` — Typer-based CLI package for assembling guides with auto font management.
- `agents/` — prompt/checklist docs for consistent generation.
- `scripts/install-fonts.sh` — ⚠️ DEPRECATED (font installation now automatic via CLI).

## Prerequisites
- Python 3.10+ (uv will manage envs).
- `uv` installed (`pip install uv` or official installer).
- `pandoc` and LaTeX engine (`xelatex` recommended for Unicode/CJK). macOS: `brew install pandoc mactex-no-gui` (or ensure `pdflatex/xelatex` is present).
- **CJK fonts**: The CLI will automatically check and offer to install if missing!

## Quick Start
```bash
# install workspace deps into the shared .venv (uv will expose the console script)
uv sync

# build Japanese guide (uses languages/japanese)
# The CLI will automatically check for CJK fonts and offer to install if needed
uv run guide-cli japanese

# keep combined markdown or choose a font if needed
uv run guide-cli japanese --keep-md --cjk-font "Noto Sans CJK JP"

# skip automatic font checking (if you know fonts are installed)
uv run guide-cli japanese --skip-font-check

# final PDF appears in outputs/japanese-guide.pdf
```

## CLI Options (summary)
- `--languages-dir PATH` — base directory for language folders (default `languages/`).
- `--output-dir/-o PATH` — final output directory (default `outputs/`).
- `--pdf-name TEXT` — custom PDF name (without extension).
- `--keep-md` — retain combined markdown in `<language>/outputs/`.
- `--pdf-engine TEXT` — Pandoc PDF engine (default `xelatex` for Unicode/CJK).
- `--cjk-font TEXT` — font(s) to try for CJK text; can be passed multiple times.
- `--skip-font-check` — **NEW** skip automatic CJK font checking and installation.

Optional: install the CLI as a user-level tool:
```bash
uv tool install --editable apps/guide-cli
guide-cli japanese
```

## Adding a New Language
1) Create `languages/<slug>/sections/` with numbered markdown files (e.g., `00-cover.md`, `02-vocabulary-shopping.md`, etc.).
2) Place any spec/reference in `languages/<slug>/spec.md`.
3) Run `uv run guide-cli <slug>` to produce `outputs/<slug>-guide.pdf`.
4) The CLI will automatically handle font requirements for CJK languages.

## Guide Structure & Format

### Phrase Format
Each phrase follows this scannable structure:

```markdown
### "English phrase here"

| Politeness | Japanese | Romaji | Tokyo | Osaka | Kyoto | When to Use |
|------------|----------|--------|-------|-------|-------|-------------|
| Casual | カジュアル形 | casual form | ○ | ○ | △ | Friends only |
| Polite | 丁寧形 | polite form | ○ | ○ | ○ | **USE THIS** |
| Very Polite | 超丁寧形 | very polite | ○ | △ | ○ | Formal settings |

**Regional Notes**: Specific cultural or linguistic differences by region
```

### Vocabulary Format
For vocabulary items (food, clothes, etc.):
- Include regional names and variations
- Note regional specialties and price expectations
- Add cultural context where relevant

### Section Organization
1. **Emergency Quick Reference** - Critical phrases tourists need immediately
2. **Core Phrases by Context** - Restaurants, Shopping, Hotels, Transportation
3. **Grammar Building Blocks** - Pronouns, particles, sentence patterns
4. **Vocabulary Toolkits** - Categorized word lists
5. **Cultural Context** - Etiquette, regional differences, customs

## Notes on Fonts & PDF Generation
- The CLI automatically checks for CJK fonts before building
- On **macOS**: Offers to install Noto CJK fonts via Homebrew
- On **Linux**: Provides apt/dnf installation commands
- On **Windows**: Provides download links
- Defaults try common CJK fonts (Hiragino, Noto Sans/Serif CJK, Source Han, IPA)
- `xelatex` is the default engine; switch via `--pdf-engine` if your LaTeX setup differs

## Housekeeping
- Outputs and intermediate markdown are ignored via `.gitignore`; commit only source markdown, specs, and code.
- Workspace is defined in `pyproject.toml`; keep new apps under `apps/` and new guides under `languages/`.

## Recent Updates (2025-11-24)
- ✅ Restructured all Japanese sections with tiered politeness levels
- ✅ Added comprehensive regional variations (Tokyo/Osaka/Kyoto) to all phrases
- ✅ Implemented one-line scannable format for quick phrase lookup
- ✅ Added automatic CJK font detection and installation to CLI
- ✅ Deprecated manual font installation script in favor of CLI automation
