# Use Python 3.11 as the base image
FROM python:3.11

# Set environnement variables for python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set environnement to fetch data
ENV SATELLITE_FEED_URL "https://data.ivanstanojevic.me/api/tle/?search=yam-"
ENV PYTHONPATH /code/

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /code/

# Expose port 8000 for external access
EXPOSE 8000

# Migration
RUN python manage.py migrate

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]