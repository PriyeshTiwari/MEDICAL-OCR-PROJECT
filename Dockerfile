# Use an official Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (Tesseract and Poppler)
# This RUN command works because we have full control in a Dockerfile
RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire project into the container
COPY . .

# Tell Render what command to run when the server starts
# Note: Render provides the $PORT variable, so we use that.
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "10000"]