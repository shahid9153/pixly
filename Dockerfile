# Frontend overlay, screenshots, and game detection won't work in container.
FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./


RUN uv sync --frozen --no-dev

COPY backend/ ./backend/
COPY PROMPTS.txt ./
COPY games_info/ ./games_info/


RUN mkdir -p vector_db
EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/games/list')"

CMD ["uv", "run", "uvicorn", "backend.backend:app", "--host", "0.0.0.0", "--port", "8000"]

