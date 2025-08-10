# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for camera and GPIO
RUN apt-get update && apt-get install -y \
    libcamera-dev \
    libcamera-apps \
    python3-libcamera \
    python3-picamera2 \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libatlas-base-dev \
    libjasper-dev \
    libqtgui4 \
    libqt4-test \
    libqtcore4 \
    libilmbase-dev \
    libopenexr-dev \
    libgstreamer1.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libwebp-dev \
    libxvidcore-dev \
    libx264-dev \
    libtiff5-dev \
    libjpeg-dev \
    libpng-dev \
    libdc1394-22-dev \
    libv4l-dev \
    v4l-utils \
    pkg-config \
    cmake \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-numpy \
    python3-scipy \
    python3-matplotlib \
    python3-pandas \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY src/ ./src/
COPY requirements.txt ./

# Create necessary directories
RUN mkdir -p /app/src/static/images
RUN mkdir -p /app/src/static/barcodes

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Setting up database..."\n\
python src/database_setup.py\n\
echo "Database setup complete!"\n\
echo "Starting main application..."\n\
python src/F123456789.py' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 5000

# Run the startup script
CMD ["/app/start.sh"]
