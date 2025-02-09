# Use the official Ubuntu 20.04 image
FROM ubuntu:20.04

# Install Python and system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3.9 \
    python3-pip \
    python3-setuptools \
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

# Set Python 3.9 as the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r requirements.txt

# Run the application directly with Python
CMD ["python", "app.py"]
