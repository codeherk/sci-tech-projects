# Base image
FROM python:3.8-slim-buster

RUN apt update && apt upgrade -y

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock to container
COPY Pipfile* ./

# Install packages from Pipfile.lock
RUN pipenv install --deploy

# Copy the application files
COPY app.py ./

# Start the application
CMD ["pipenv", "run", "python", "app.py"]