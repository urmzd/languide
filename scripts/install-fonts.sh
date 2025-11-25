#!/usr/bin/env bash
set -euo pipefail

# Helper to install Japanese-friendly fonts on macOS (adapt for Linux/Windows as needed).
# Usage: ./scripts/install-fonts.sh

if [[ "$OSTYPE" == "darwin"* ]]; then
  brew list font-noto-sans-cjk || brew install --cask font-noto-sans-cjk
  brew list font-noto-serif-cjk || brew install --cask font-noto-serif-cjk
  echo "Installed Noto CJK fonts. Pandoc/xelatex can now render Japanese."
else
  echo "Please install a CJK font (e.g., Noto Sans/Serif CJK JP) via your system package manager."
fi
