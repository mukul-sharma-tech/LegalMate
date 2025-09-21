# Use a lightweight Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (needed for FAISS, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask default port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
