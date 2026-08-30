#!/bin/bash
set -e

echo "⏳ Installing API dependencies via uv..."
uv sync --project ./loodation-api