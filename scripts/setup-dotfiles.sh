#!/bin/bash
set -e

echo "⏳ Setting up dotfiles..."
stow --restow -v -d ./.devcontainer/dotfiles -t "$HOME" bash