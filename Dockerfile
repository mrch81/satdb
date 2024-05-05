# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set environnement variables for python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set environnement to fetch data
ENV SATELLITE_FEED_URL "https://tle.ivanstanojevic.me/api/tle/"

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Expose port 8000 for external access
EXPOSE 8000

# Make migration
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]