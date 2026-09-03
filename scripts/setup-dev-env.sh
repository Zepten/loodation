#!/bin/bash
set -e

# Setting up environment file (.env)
if [ ! -f .env ]; then
    echo "📄 .env not found, creating from .env.example..."
    cp .env.example .env
else
    echo "📄 .env already exists, skipping..."
fi

# Setting up dotfiles
./scripts/setup-dotfiles.sh

# Installing API dependencies via uv
./scripts/setup-deps-api.sh

# Setting up git configuration
./scripts/setup-git-config.sh

# Setting up git hooks
./scripts/setup-git-hooks.sh

# Run database migrations
./scripts/setup-alembic-upgrade.sh

echo "🚀 Dev environment is ready!"