# Dockerfile for Devcontainer

FROM mcr.microsoft.com/devcontainers/base:jammy

RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    git \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# TODO: node for frontend

USER vscode