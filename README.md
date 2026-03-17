# Languide

Practical, communication-focused language guides for travelers — built from markdown, rendered to PDF.

> Every release automatically produces downloadable PDF guides. Check the [Releases](https://github.com/urmzd/languide/releases) page for the latest.

## Philosophy

These guides emphasize **practical communication** — phrases and patterns for everyday interactions — rather than tourism tips. Content is organized by scenario (restaurants, hotels, shopping, transport, emergencies) using tables for phrases and pattern templates with customizable slots.

## Quick Start

```bash
uv sync                       # install dependencies
uv run guide-cli japanese      # build a single guide
uv run guide-cli build-all     # build all guides
uv run guide-cli discover      # list available languages
```

### Prerequisites

- Python 3.10+ with [uv](https://docs.astral.sh/uv/)
- [Pandoc](https://pandoc.org/) and a LaTeX engine (`xelatex` recommended)
- CJK font for Japanese/Chinese/Korean (e.g., Noto Sans CJK)

## Adding a New Language

The easiest way is with [Claude Code](https://github.com/anthropics/claude-code):

```bash
claude "/create-language french"
```

This generates all 11 chapters following the system prompt, validates against the quality checklist, and reports phrase counts.

To add one manually:

1. Create `languages/<slug>/chapters/` with numbered chapters following the structure below
2. Use `agents/system-prompt.md` as the generation prompt
3. Verify against `agents/checklist.md`
4. Run `uv run guide-cli <slug>` to produce `outputs/<slug>-guide.pdf`

## Repository Layout

```
languages/<slug>/chapters/   Numbered markdown chapters (00-cover.md … 10-cultural-guide.md)
languages/<slug>/spec.md     Content specification for that language
agents/                      System prompt and quality checklist
skills/                      Claude Code skills for automating guide creation
apps/guide-cli/              Typer CLI for assembling chapters into PDFs
outputs/                     Built PDFs (gitignored)
```

## Chapter Structure

Each guide contains 11 chapters:

| Chapter | File | Content |
|---------|------|---------|
| Cover | `00-cover.md` | Introduction, usage notes, guide overview |
| Core Phrases | `01-core-phrases.md` | Pattern templates, greetings, emergencies, daily interactions |
| Language Foundations | `02-language-foundations.md` | Grammar, particles, sentence patterns |
| Pronunciation | `03-pronunciation.md` | Vowels, consonants, special sounds |
| Writing Systems | `04-writing-systems.md` | Scripts and characters, survival reading |
| Directions & Navigation | `05-directions-navigation.md` | Asking directions, landmarks |
| Transportation | `06-transportation.md` | Trains, buses, taxis, airports |
| Restaurants | `07-restaurants.md` | Ordering, dietary needs, payment |
| Shopping | `08-shopping.md` | Sizes, trying on, payment, returns |
| Hotels | `09-hotels.md` | Check-in/out, requests, problems |
| Cultural Guide | `10-cultural-guide.md` | Regional differences, etiquette |

### Conventions

- **Tables** for all phrase collections — 4-column format: `English | Target Language | Transliteration | Notes`
- **Pattern phrases** with `[brackets]` for customizable slots
- **Politeness tiers**: Casual / Polite / Very Polite
- **50+ phrases** per scenario chapter, **30+** for directions and emergencies
- **No tourism tips** — focus on how to communicate, not what to see

### Example: Pattern Phrases

| Pattern | Japanese | Example |
|---------|----------|---------|
| [thing] please | [もの]をください | 水をください = Water please |
| Where is [place]? | [場所]はどこですか | 駅はどこですか = Where is the station? |

### Example: Politeness Tiers

| English | Japanese | Romaji | Politeness |
|---------|----------|--------|------------|
| Thank you | ありがとう | arigatou | Casual |
| Thank you | ありがとうございます | arigatou gozaimasu | Polite |

## CLI Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--languages-dir PATH` | Base directory for language folders | `languages/` |
| `--output-dir`, `-o PATH` | Final output directory | `outputs/` |
| `--pdf-name TEXT` | Custom PDF name (without extension) | `<slug>-guide` |
| `--keep-md` | Retain combined markdown | off |
| `--pdf-engine TEXT` | Pandoc PDF engine | `xelatex` |
| `--cjk-font TEXT` | CJK font(s) to try (repeatable) | auto-detect |
| `--skip-font-check` | Skip CJK font detection | off |

## Agents & Skills

| Resource | Purpose |
|----------|---------|
| `agents/system-prompt.md` | Prompt for generating new language guides |
| `agents/checklist.md` | Quality checklist for guide content |
| `skills/create-language.md` | Claude Code skill that automates guide creation |
| `AGENTS.md` | Agent conventions and project context |

## Fonts

The CLI auto-detects CJK fonts and offers to install them on macOS. If glyphs are missing:

```bash
# macOS
brew install --cask font-noto-sans-cjk font-noto-serif-cjk

# or specify directly
uv run guide-cli japanese --cjk-font "Noto Sans CJK JP"
```

## License

[Apache 2.0](LICENSE)
