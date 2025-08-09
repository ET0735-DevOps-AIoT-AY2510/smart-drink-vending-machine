# Use a Python base image
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pyzbar (zbar library)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    gcc \
    g++ \
    python3-dev \
    libcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
# This includes src/, templates/, static/, and vending_machine.db
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=src/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask application
# Note: F123456789.py is the main entry point for the vending machine logic,
# which starts the Flask app in a separate thread.
# So, we'll run F123456789.py directly.
CMD ["python", "src/F123456789.py"]