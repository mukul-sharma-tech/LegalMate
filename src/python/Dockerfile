# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file first and install them
# This leverages Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Gunicorn will listen on the port provided by Render's $PORT environment variable
# We use gunicorn as the production-ready web server instead of Flask's built-in server
#
# --- MODIFIED ---
# We use the "shell" form of CMD (just a string) so that the $PORT
# environment variable is correctly expanded by the shell.
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT app:app
