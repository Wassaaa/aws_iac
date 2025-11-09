# Multi-stage build: First stage builds C++ binary
FROM python:3.13-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy probit source and build
COPY probit /build/probit
RUN cd /build/probit && \
    cmake -B build -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build

# Second stage: Runtime image
FROM python:3.13-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy compiled binary from builder
COPY --from=builder /build/probit/build/probit_api /app/probit_api

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY hello.py index.html ./

# Expose port and run
EXPOSE 8080
CMD ["python", "hello.py"]
