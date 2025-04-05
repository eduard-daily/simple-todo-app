# backend/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # Prevents python creating .pyc files
ENV PYTHONUNBUFFERED 1       # Force stdin, stdout, stderr to be totally unbuffered

# Set the working directory in the container
WORKDIR /code

# Install system dependencies if needed (e.g., for psycopg2 build)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./app /code/app

# The command to run the application will be specified in docker-compose.yml
# EXPOSE 8000 # Port exposure is handled by docker-compose
