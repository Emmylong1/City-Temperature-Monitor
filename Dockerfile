# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements file and install dependencies
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY app/ /app/

# Expose port 5000 for the Flask web server
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]
