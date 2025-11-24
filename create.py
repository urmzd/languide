#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Compatibility shim that forwards to the uv-managed CLI in apps/guide-cli.
Use `uv run guide-cli ...` (defaults to languages/<slug> folders) for best results.
"""

from pathlib import Path
import sys

workspace_src = Path(__file__).resolve().parent / "apps" / "guide-cli" / "src"
if workspace_src.exists():
    sys.path.insert(0, str(workspace_src))

try:
    from guide_cli.cli import app
except Exception as exc:  # pragma: no cover - fallback for missing env
    raise SystemExit(
        "guide_cli is unavailable. Run `uv sync` to install dependencies, "
        "then use `uv run guide-cli ...`."
    ) from exc

if __name__ == "__main__":
    app()
