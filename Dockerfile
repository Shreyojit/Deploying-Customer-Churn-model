# Use the official Python 3.9 image (Ubuntu-based)
FROM python:3.9

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Run the application directly with Python
CMD ["python", "app.py"]
