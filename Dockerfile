# Use a slim Python 3.9 image
FROM python:3.9.5-slim-buster

# Update and install necessary dependencies
RUN apt update -y

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install dependencies listed in the requirements.txt file
RUN apt-get update && pip install -r requirements.txt

# Use Gunicorn to run the Flask app with 4 workers and binding to 0.0.0.0:5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
