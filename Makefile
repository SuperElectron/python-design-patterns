.PHONY: install lint format typecheck test check clean

install:            ## Sync dev environment
	uv sync --group dev

lint:               ## Ruff lint + format check
	uv run ruff check .
	uv run ruff format --check .

format:             ## Auto-fix lint and formatting
	uv run ruff check --fix .
	uv run ruff format .

typecheck:          ## mypy --strict
	uv run mypy

test:               ## Run test suite with coverage
	uv run pytest

check: lint typecheck test   ## Everything CI runs

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist build
