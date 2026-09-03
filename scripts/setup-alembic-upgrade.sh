#!/bin/bash
set -e

cd "$(dirname "$0")/../loodation-api"

echo "🗄️ Running Alembic migrations..."

uv run --env-file ../.env alembic upgrade head

echo "✅ Migrations completed! Upgraded to head (latest)."