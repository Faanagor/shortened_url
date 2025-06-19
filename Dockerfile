# Use Python 3.10 slim image as the base
# The slim version is a lightweight image that only contains essential packages
FROM python:3.10-slim

# Set working directory in the container
# This is where our code will live inside the container
WORKDIR /app

# Install uv first - it's much faster than pip
RUN pip install --no-cache-dir uv

# Copy only the requirements file first
# This is a best practice to leverage Docker cache layers
COPY requirements.txt .

# Install dependencies using uv in system mode
# uv pip install is significantly faster than regular pip
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application code
# This includes all files in the current directory
COPY . .

# Expose port 8000 for the FastAPI application
# This is a documentation feature that tells Docker which port the container will listen on
EXPOSE 8000

# Command to run the application using uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
# --reload is removed in production for better performance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
