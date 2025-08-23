# Multi-stage build for different endpoints
ARG ENDPOINT=text

# Base stage with common dependencies
FROM python:3.11-slim as base

WORKDIR /app

# Copy and install requirements
COPY builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Text endpoint stage
FROM base as text-endpoint

# Copy the text endpoint source code
COPY endpoints/text/src/ ./src/

# Set Python path to find modules
ENV PYTHONPATH=/app/src

# Start the container
CMD ["python", "-u", "src/main.py", "stg"]

# Image endpoint stage
FROM base as image-endpoint

# Copy the image endpoint source code
COPY endpoints/image/src/ ./src/

# Set Python path to find modules
ENV PYTHONPATH=/app/src

# Start the container
CMD ["python", "-u", "src/main.py", "stg"]

# Final stage - select the endpoint
FROM ${ENDPOINT}-endpoint as final