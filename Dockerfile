# Use the official Python slim image for smaller image size
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file for caching dependencies
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Create the instance folder for SQLite if needed
RUN mkdir -p /app/instance

# Expose the Flask port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Start the Flask application
CMD ["python", "run.py"]
