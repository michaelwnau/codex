# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.8.2

# Install system dependencies
RUN apt-get update \

    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Optional install six if dependencies require it
# RUN pip install six

# Run Poetry debug to verify environment setup (this step is optional and can be removed once the build issues are resolved)
RUN poetry debug info

# Install project dependencies including dev dependencies for running Ruff
RUN poetry config virtualenvs.create false \

    && poetry install --no-interaction --no-ansi

# Run Ruff to check for linting errors
RUN poetry run ruff check

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "streamlit_app.py"]
