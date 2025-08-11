# Raspberry Pi-compatible base image (Debian Bullseye Slim, ARM 32-bit)
FROM arm32v7/debian:bullseye-slim
# Set working directory
WORKDIR /app

# Add Raspberry Pi OS repository for camera packages
RUN apt-get update && apt-get install -y wget gnupg \
 && wget -O - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add - \
 && echo "deb http://archive.raspberrypi.org/debian/ bullseye main" >> /etc/apt/sources.list \
 && apt-get update

# Install system dependencies (camera + Python + libraries)
RUN apt-get install -y \
    python3 python3-pip python3-setuptools python3-wheel \
    python3-smbus \
    libcamera0 libcamera-dev libcamera-apps python3-libcamera python3-picamera2 \
    libatlas-base-dev \
    libhdf5-dev libhdf5-serial-dev \
    libilmbase-dev libopenexr-dev \
    libgstreamer1.0-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libwebp-dev libxvidcore-dev libx264-dev \
    libtiff5-dev libjpeg-dev libpng-dev \
    libdc1394-22-dev libv4l-dev v4l-utils \
    libzbar0 libzbar-dev \
    pkg-config cmake build-essential python3-dev \
    python3-numpy python3-scipy python3-matplotlib python3-pandas python3-opencv \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# --- SPI-Py installation ---
ENV SPI_PATH=/app/src/SPI-Py
COPY src/SPI-Py/ $SPI_PATH/
WORKDIR $SPI_PATH
RUN python3 setup.py install

# Copy the rest of your source files
WORKDIR /app
COPY src/ ./src/

# Create necessary directories
RUN mkdir -p /app/src/static/images /app/src/static/barcodes

# Environment variables for Flask
ENV PYTHONPATH=/app
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Startup script (only runs main app)
RUN echo '#!/bin/bash\n\
echo "Starting main application..."\n\
python3 src/F123456789.py' > /app/start.sh \
 && chmod +x /app/start.sh

# Expose Flask port
EXPOSE 5000

# Run the startup script
CMD ["/app/start.sh"]
