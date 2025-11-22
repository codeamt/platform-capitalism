# Multi-stage build for production
ARG PYTHON_VERSION=3.11-slim

# Builder stage
FROM python:${PYTHON_VERSION} as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:${PYTHON_VERSION}

WORKDIR /app

# Copy virtual env
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY . .

# Setup persistent volume
RUN mkdir -p /data && chown nobody:nogroup /data
VOLUME /data

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f <http://localhost:8000/api/health> || exit 1

# Run with production server
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", \\
#    "--bind", "0.0.0.0:8000", \\
#    "--workers", "4", \\
#    "--threads", "2", \\
#    "--access-logfile", "-", \\
#    "app.serve:app"]