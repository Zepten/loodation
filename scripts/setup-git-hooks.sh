#!/bin/bash
set -e

echo "⏳ Setting up git hooks..."
uv run --project ./loodation-api pre-commit install
uv run --project ./loodation-api pre-commit install -t pre-push