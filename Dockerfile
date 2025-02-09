# Use a slim Python 3.9 image
FROM python:3.9.5-slim-buster

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 gcc g++ make && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Use Gunicorn to run the Flask app with 4 workers, binding to 0.0.0.0:5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
