# Use Raspberry Pi Python 3 base image (ARM 32-bit)
FROM arm32v7/python:3

# Set working directory
WORKDIR /app

# Add Raspberry Pi OS repository for camera packages
RUN apt-get update && apt-get install -y wget gnupg \
 && wget -O - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add - \
 && echo "deb http://archive.raspberrypi.org/debian/ bullseye main" >> /etc/apt/sources.list \
 && apt-get update

# Install system dependencies (camera + libraries)
RUN apt-get install -y \
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
    pkg-config cmake build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (including rpi.gpio in requirements.txt)
RUN pip3 install --no-cache-dir -r requirements.txt

# --- SPI-Py installation ---
ENV SPI_PATH=/app/src/SPI-Py

# Copy SPI-Py source into container
COPY src/SPI-Py/ $SPI_PATH/

# Install SPI-Py C extension
WORKDIR $SPI_PATH
RUN python3 setup.py install

# Copy rest of application source files
WORKDIR /app
COPY src/ ./src/

# Create directories for static content
RUN mkdir -p /app/src/static/images /app/src/static/barcodes

# Fix PYTHONPATH: append to existing paths instead of overwriting
ENV PYTHONPATH=/app:$PYTHONPATH

# Set Flask environment variables (optional)
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Setting up database..."\n\
python3 src/database_setup.py\n\
echo "Database setup complete!"\n\
echo "Starting main application..."\n\
python3 src/F123456789.py' > /app/start.sh \
 && chmod +x /app/start.sh

# Expose Flask port
EXPOSE 5000

# Run startup script by default
CMD ["/app/start.sh"]
