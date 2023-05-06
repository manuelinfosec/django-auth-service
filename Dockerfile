# Official Python for minimal image size and attack surface
FROM python-3.9:slim

# Buffer optimizations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up working directory
WORKDIR /production

# Install system dependencies
RUN apt update && \
    apt install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY src/requirements.txt /production/

# Copy entire project to container
COPY src/ /production/

# Create low priviledged user to run the application (for security)
RUN adduser --disabled-password --gecos '' app_user

# Use the created user
USER app_user

# Start Gunicorn with Unix socket binding
CMD ["gunicorn", "--bind=unix:/production/authservice.sock", "auth_service.wsgi:application"]
