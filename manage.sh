#!/usr/bin/env bash

set -e

podman-compose exec api uv run src/loodation/cli.py "$@"