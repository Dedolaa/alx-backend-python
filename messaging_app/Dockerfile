# messaging_app/Dockerfile

# Use official Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app/

# Expose port (Django default 8000)
EXPOSE 8000

# Run migrations + start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
