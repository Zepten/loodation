FROM python:3.13-alpine

RUN apk add --no-cache build-base curl

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install the application dependencies.
WORKDIR /app

RUN mkdir -p src/loodation && touch src/loodation/__init__.py

COPY pyproject.toml uv.lock ./
COPY README.md LICENSE ./

RUN uv sync --project . --locked --no-cache

# Copy the application into the container.
COPY ./src ./src
