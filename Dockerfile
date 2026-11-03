FROM python:3.13-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml .python-version ./

# Install dependencies globally in the container
RUN uv pip install --system .

# Copy application code
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# The entry point is handled by docker-compose
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
