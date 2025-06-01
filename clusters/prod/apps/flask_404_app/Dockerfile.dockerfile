# Start from slim Python base
FROM python:3.12-slim

# Metadata
LABEL maintainer="Mangale Lopchan lopchanmangal5@gmail.com"

# Prevent interactive prompts
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Use Gunicorn as WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
