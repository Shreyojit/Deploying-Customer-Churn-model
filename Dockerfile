# Use the official Python 3.9 image (Ubuntu-based)
FROM python:3.9.5-slim-buster

# Install system dependencies
RUN apt update -y

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Upgrade pip and install Python dependencies
RUN app-get update && pip install -r requirements.txt

# Run the application directly with Python
CMD ["python", "app.py"]
