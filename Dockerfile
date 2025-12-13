FROM python:3.11-slim

# Install system dependencies required by OpenCV and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements first (better Docker layer caching)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Ensure uploads directory exists
RUN mkdir -p /app/uploads

# Expose Flask port
EXPOSE 5000

# Run Flask app via Gunicorn
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-5000} app:app"]
