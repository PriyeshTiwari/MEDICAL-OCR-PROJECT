# Use an official Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies with the corrected package name for libGL
RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils libgl1

# This tells Render which port your app uses
EXPOSE 10000

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire project into the container
COPY . .

# Tell Render what command to run when the server starts
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "10000"]