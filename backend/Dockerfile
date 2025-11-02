# Multi-stage Docker build for H.O.M.E. Platform backend
# Optimized for GCP Cloud Run

FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY ./app ./app

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Cloud Run expects port 8080
ENV PORT=8080

# Run the application
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
