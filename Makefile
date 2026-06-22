.PHONY: install format lint test build check bundle-validate deploy-dev run-dev destroy-dev

install:
	uv sync --extra dev

format:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff format --check .
	uv run ruff check .

test:
	uv run pytest

build:
	uv build --wheel

check: lint test build

bundle-validate:
	databricks bundle validate --target dev

deploy-dev:
	databricks bundle deploy --target dev

run-dev:
	databricks bundle run --target dev medallion_job

destroy-dev:
	databricks bundle destroy --target dev

