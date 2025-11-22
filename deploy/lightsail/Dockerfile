FROM python:3.11-slim as builder

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install dependencies early for caching
COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r <(pip install -q poetry && poetry export --without-hashes)

# Copy application
COPY . /app

# Final runtime image
FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app

ENV ENVIRONMENT=production
ENV PORT=8080
EXPOSE 8080

CMD ["python", "main.py"]