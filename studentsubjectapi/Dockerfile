# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional for production)
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "studentsubjectapi.wsgi:application", "--bind", "0.0.0.0:8000"]
