# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your ETL project files into the image
COPY . .

# Set environment variables from .env file (at runtime we'll mount this)
CMD ["python", "etl/etl_job.py"]
