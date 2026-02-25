# Dockerfile for Car Damage Detection Web App
#
# This Dockerfile builds a containerized Streamlit application for car damage
# detection. It includes all dependencies and pre-trained model weights.
#
# Build: docker build -t car-damage-detector:latest .
# Run:   docker run -p 8501:8501 car-damage-detector:latest
#

# Use official Python runtime as base image
# Python 3.11-slim: smaller footprint than full image, suitable for Streamlit
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables
# PYTHONUNBUFFERED=1: Print Python output immediately (don't buffer)
# STREAMLIT_SERVER_PORT=8501: Streamlit port inside container
# STREAMLIT_SERVER_HEADLESS=true: Run without browser (container has no GUI)
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true

# Copy only requirements first (for better layer caching during builds)
COPY requirements.txt .

# Install system dependencies needed for image processing
# libsm6, libxext6, libxrender-dev: OpenCV dependencies
# libgomp1: OpenMP dependency for NumPy optimization
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
# --no-cache-dir: Don't cache wheels (saves ~1GB of space)
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into container
COPY . .

# Create directory for model outputs (validation/inference results)
# These are created at runtime but pre-creating avoids permission issues
RUN mkdir -p runs/detect/{train,predict}

# Expose Streamlit port
# Container listens on 8501 but port mapping is done with docker run -p
EXPOSE 8501

# Health check ensures container is responsive
# Checks if Streamlit is responding on port 8501
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501').status" || exit 1

# Set the entrypoint command to run Streamlit app
# Uses exec form so signals (like Ctrl+C) are properly forwarded to Python process
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
