# Base image
FROM python:3.8-slim-buster

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

# Expose port 6000
EXPOSE 6000

# Start the application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]

