FROM python:3.13-alpine

ARG UID=1000
ARG GID=1000

RUN apk add --no-cache build-base curl

RUN addgroup -g ${GID} app \
    && adduser -D -u ${UID} -G app app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_PYTHON=/usr/local/bin/python
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install the application dependencies.
WORKDIR /app

RUN mkdir -p src/loodation /opt/venv \
    && touch src/loodation/__init__.py

COPY pyproject.toml uv.lock ./
COPY README.md LICENSE ./

RUN uv sync --project . --locked --no-cache --all-groups \
    && chown -R app:app /app /opt/venv

# Copy the application into the container.
COPY --chown=app:app ./src ./src

USER app