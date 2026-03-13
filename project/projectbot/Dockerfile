# =============================================================================
# PRODUCTION DOCKERFILE FOR TELEGRAM BOT
# =============================================================================
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd --gid 1000 botuser && \
    useradd --uid 1000 --gid botuser --shell /bin/false --create-home botuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=botuser:botuser . .

# Create data directory and set permissions
RUN mkdir -p /app/data && chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Run the bot
CMD ["python", "main.py"]
