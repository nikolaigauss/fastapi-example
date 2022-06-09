# Using Python image to ensure smallest footprint
FROM python:3.9

# Establishing application working directory
WORKDIR /code

#  Unstalling packages with pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./code /code/app

# CMD option is irrelevant as we're using Docker Compose