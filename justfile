default: check

# Install dependencies
install:
    uv sync --group dev

# Run tests
test:
    uv run pytest

# Run linter
lint:
    uv run ruff check .

# Format code
fmt:
    uv run ruff format .

# Check formatting without modifying
check-fmt:
    uv run ruff format --check .

# Quality gate: format + lint + test
check: check-fmt lint test

# Full CI gate
ci: check-fmt lint test
