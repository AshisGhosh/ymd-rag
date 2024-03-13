# Use an official lightweight Python image.
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy only the pyproject.toml and poetry.lock* to install dependencies
COPY backend/pyproject.toml backend/poetry.lock* /app/

# Install dependencies
RUN poetry install --no-dev
RUN apt-get update && apt-get install -y pandoc \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra 

# The source code will be mounted via Docker Compose, so no need to COPY
# COPY backend /app

# The command to run the app will be specified in docker-compose.yml