# Dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security (Recruiters love seeing this!)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Copy your source code
COPY pyproject.toml README.md main.py ./
COPY app ./app

# Install dependencies
RUN pip install -v --user .

# Add local bin to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Expose the single port
EXPOSE 8000

# Run the unified app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]