# Use the official Python 3.9 slim image as the base image
FROM python:3.9-slim
# Set the working directory inside the container to /app
WORKDIR /app
# Copy the requirements.txt file from the source directory to the container
COPY src/requirements.txt requirements.txt
# Install Python dependencies listed in requirements.txt without caching
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the source code from the src directory into the container
COPY src/ .
# Define the default command to run the Flask application
CMD ["python", "app.py"]
