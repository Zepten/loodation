#!/bin/bash
set -e

# Setting up dotfiles
./scripts/setup-dotfiles.sh

# Installing API dependencies via uv
./scripts/setup-deps-api.sh

# Setting up git configuration
./scripts/setup-git-config.sh

# Setting up git hooks
./scripts/setup-git-hooks.sh

echo "🚀 Dev environment is ready!"