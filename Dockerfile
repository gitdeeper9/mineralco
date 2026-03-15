# MINERALCO Dockerfile
# Mineral Intelligence Network for Equation-of-state Research, Atomic Lattice COmputation
# Version: 1.0.0 | DOI: 10.5281/zenodo.19009597

FROM python:3.10-slim as builder

LABEL maintainer="Samir Baladi <gitdeeper@gmail.com>"
LABEL description="MINERALCO - Seven Parameters to Decode the Earth's Solid Interior"
LABEL version="1.0.0"
LABEL doi="10.5281/zenodo.19009597"

# ============================================
# Builder Stage: Install dependencies
# ============================================
WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    libnetcdf-dev \
    libopenblas-dev \
    libfftw3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY requirements-dev.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt && \
    pip install --user --no-cache-dir gunicorn

# ============================================
# Final Stage
# ============================================
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-103-1 \
    libnetcdf19 \
    libopenblas0 \
    libfftw3-3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Install MINERALCO
RUN pip install --no-cache-dir -e .

# Create necessary directories
RUN mkdir -p /data/{raw,processed,cache} && \
    mkdir -p /logs && \
    mkdir -p /output/{reports,figures} && \
    mkdir -p /config

# Copy default configuration
COPY config/config.yaml /config/config.yaml

# Create non-root user
RUN useradd -m -u 1000 mineralco && \
    chown -R mineralco:mineralco /app /data /logs /output /config

USER mineralco

# Expose ports
EXPOSE 5000 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set entrypoint
ENTRYPOINT ["mineralco"]

# Default command
CMD ["serve", "--host", "0.0.0.0", "--port", "5000"]
