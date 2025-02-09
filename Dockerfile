# Use a slim Python 3.9 image
FROM python:3.9.5-slim-buster

# Install system dependencies (including libgomp1 to fix the shared library error)
RUN apt-get update -y && \
    apt-get install -y libgomp1

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application directly with Python
CMD ["python", "app.py"]