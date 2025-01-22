# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY omega_bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY omega_bot /app/omega_bot/

# Create necessary directories
RUN mkdir -p /app/models /app/output /app/logs /app/cache

# Set up environment variables
ENV BOT_TOKEN="" \
    MODEL_DIRECTORY="/app/models" \
    OUTPUT_DIRECTORY="/app/output" \
    LOG_DIRECTORY="/app/logs" \
    CACHE_DIRECTORY="/app/cache"

# Run the bot
CMD ["python", "-m", "omega_bot"]
