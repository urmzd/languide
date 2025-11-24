#!/usr/bin/env bash
set -euo pipefail

# Install the guide-cli as a user-level tool via uv (editable from the workspace).
# Usage: ./scripts/install-guide-cli.sh

cd "$(dirname "$0")/.."
uv tool install --editable apps/guide-cli
echo "guide-cli installed. Run: guide-cli guide <language-slug>"
