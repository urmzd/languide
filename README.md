# Language Communication Guides

Workspace for generating **communication-focused** language guides. Each language lives under `languages/<slug>` with numbered chapters, and PDFs are built via a Typer CLI (`guide-cli`) managed by `uv`.

## Philosophy

These guides emphasize **practical communication**—phrases and patterns for everyday interactions—rather than tourism tips. Content is organized by **scenario** (greetings, restaurants, hotels, shopping, transport, emergencies) using **tables** for phrases and **pattern templates** with customizable slots.

## Repository Layout

- `languages/<slug>/chapters/` — numbered markdown chapters:
  - `00-cover.md` — Introduction and guide structure
  - `01-core-phrases.md` — Pattern templates, greetings, emergencies, daily interactions
  - `02-language-foundations.md` — Grammar, particles, sentence patterns
  - `03-pronunciation.md` — Vowels, consonants, special sounds
  - `04-writing-systems.md` — Scripts/characters (if applicable)
  - `05-directions-navigation.md` — Asking for directions
  - `06-transportation.md` — Trains, buses, taxis
  - `07-restaurants.md` — Ordering, dietary needs, payment
  - `08-shopping.md` — Sizes, payment, returns
  - `09-hotels.md` — Check-in/out, requests, problems
  - `10-cultural-guide.md` — Regional differences, etiquette
- `languages/<slug>/spec.md` — Reference/specification for guide content
- `outputs/` — Finalized PDFs for all languages
- `apps/guide-cli/` — Typer CLI package for assembling guides
- `agents/` — Prompt/checklist docs for consistent generation

## Chapter Structure Conventions

### Communication-First Content

- Organize phrases by **scenario** (restaurant, hotel, shopping, etc.)
- Use **tables** for all phrase collections (no inline comma-separated lists)
- Include **pattern phrases** with `[brackets]` for customizable slots:

| Pattern | Japanese | Example |
|---------|----------|---------|
| [thing] please | [もの]をください | 水をください = Water please |
| Where is [place]? | [場所]はどこですか | 駅はどこですか = Where is the station? |

### Politeness Tiers

Include **casual**, **polite**, and **very polite** options where relevant:

| English | Japanese | Romaji | Politeness |
|---------|----------|--------|------------|
| Thank you | ありがとう | arigatou | Casual |
| Thank you | ありがとうございます | arigatou gozaimasu | Polite |

## Prerequisites

- Python 3.10+ with `uv` installed
- `pandoc` and LaTeX engine (`xelatex` recommended for Unicode/CJK)
- CJK-capable font for Japanese/Chinese/Korean (e.g., Noto Sans CJK)

## Quick Start

```bash
# install deps into the workspace .venv
uv sync

# build Japanese guide
uv run guide-cli japanese

# keep combined markdown or specify a font
uv run guide-cli japanese --keep-md --cjk-font "Noto Sans CJK JP"

# discover available languages
uv run guide-cli discover

# build all languages
uv run guide-cli build-all
```

## CLI Options

- `--languages-dir PATH` — Base directory for language folders (default `languages/`)
- `--output-dir/-o PATH` — Final output directory (default `outputs/`)
- `--pdf-name TEXT` — Custom PDF name (without extension)
- `--keep-md` — Retain combined markdown in `<language>/outputs/`
- `--pdf-engine TEXT` — Pandoc PDF engine (default `xelatex`)
- `--cjk-font TEXT` — Font(s) to try for CJK text (can pass multiple)

## Adding a New Language

1. Create `languages/<slug>/chapters/` with numbered chapters following the structure above
2. Use `agents/system-prompt.md` as the guide generation prompt
3. Verify against `agents/checklist.md` before finalizing
4. Run `uv run guide-cli <slug>` to produce `outputs/<slug>-guide.pdf`

## Agent Documentation

- `agents/system-prompt.md` — Prompt for generating new language guides
- `agents/checklist.md` — Quality checklist for guide content

Both emphasize:
- **Scenario-based phrases** over tourism tips
- **Tables** for all phrase collections
- **Pattern phrases** with customizable slots
- **Politeness tiers** (casual/polite/very polite)

## Notes on Fonts

- Defaults try common CJK fonts (Hiragino, Noto Sans/Serif CJK, Source Han, IPA)
- If glyphs are missing, pass `--cjk-font "Noto Sans CJK JP"`
- macOS: Run `./scripts/install-fonts.sh` to install Noto CJK fonts

## Housekeeping

- Build outputs are ignored via `.gitignore`
- Commit only source markdown/specs and code
- Workspace defined in `pyproject.toml`
