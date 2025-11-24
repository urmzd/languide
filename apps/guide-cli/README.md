## guide-cli

CLI to assemble language guide sections into a single PDF.

### Usage

```bash
# install deps for this workspace
uv sync

# build a guide (uses languages/<slug> by default)
uv run guide-cli japanese

# the bare command also works if installed as a tool
guide-cli japanese

# keep the combined markdown
uv run guide-cli japanese --keep-md

# specify a font if your system lacks defaults
uv run guide-cli japanese --cjk-font "Noto Sans CJK JP"
```

### Options
- `--languages-dir`: base directory for language folders (default `languages/`).
- `--output-dir / -o`: final output directory (defaults to `outputs/` at repo root).
- `--pdf-name`: custom PDF name (without `.pdf`).
- `--keep-md`: retain the combined markdown in `<language>/outputs/`.
- `--pdf-engine`: PDF engine for pandoc (default `xelatex` for Unicode/CJK).
- `--cjk-font`: one or more fonts to try for CJK text (defaults include Hiragino/Noto/IPA).
