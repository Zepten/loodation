#!/bin/bash
set -e

echo "⏳ Installing API dependencies via uv..."
uv sync --project ./loodation-api

echo "⏳ Setting up pre-commit hooks..."
uv run pre-commit install
uv run pre-commit install -t pre-commit

echo "⏳ Finalizing environment configuration..."
chmod +x ./loodation-api/.venv/bin/activate*

echo "🚀 Dev environment is ready!"