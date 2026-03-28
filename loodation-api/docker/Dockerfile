FROM python:3.13-alpine

RUN apk add --no-cache build-base

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install the application dependencies.
WORKDIR /app
RUN uv sync --locked --no-cache

# Copy the application into the container.
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]