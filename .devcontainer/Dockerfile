# Dockerfile for Devcontainer

FROM mcr.microsoft.com/devcontainers/base:jammy

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iputils-ping \
    git \
    build-essential \
    libpq-dev \
    postgresql-client \
    stow \
    && rm -rf /var/lib/apt/lists/*

USER vscode

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# TODO: node for frontend