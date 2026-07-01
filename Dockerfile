# ==========================================
# STAGE 1: The Builder (The Factory)
# ==========================================
FROM python:3.13-slim AS builder

WORKDIR /app

# 1. Install heavy system build tools (gcc, g++, etc.)
# These are needed to compile some Python packages, but we WON'T keep them.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Create a virtual environment
# This makes it incredibly easy to copy all dependencies to the next stage in one move.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. Copy only requirement files first (to cache this layer if dependencies don't change)
COPY pyproject.toml ./

# 4. Install the massive PyTorch CPU-only wheel FIRST
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 5. Install the rest of your app dependencies
RUN pip install --no-cache-dir .

# ==========================================
# STAGE 2: The Runtime (The Showroom)
# ==========================================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# --- THE FIX IS HERE ---
# Added libgl1 and libglib2.0-0 for OpenCV (cv2) support
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    pandoc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Create the secure non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 3. THE MAGIC TRICK: Copy the fully built virtual environment from Stage 1
COPY --from=builder /opt/venv /opt/venv

# 4. Pre-download NLTK data for unstructured
RUN python -m nltk.downloader punkt averaged_perceptron_tagger

# 5. Copy your actual application code
COPY app ./app
COPY main.py ./


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]