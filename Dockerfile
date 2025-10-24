# Use official Python image
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies (optional but useful)
RUN apt-get update && apt-get install -y build-essential

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]