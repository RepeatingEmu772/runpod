# Multi-stage build for different endpoints
ARG ENDPOINT=text

# Text endpoint stage
FROM python:3.11-slim as text-endpoint

WORKDIR /app

# Copy and install requirements for text endpoint
COPY endpoints/text/builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the text endpoint source code
COPY endpoints/text/src/ ./src/

# Set Python path to find modules
ENV PYTHONPATH=/app/src

# Start the container
CMD ["python", "-u", "src/main.py", "stg"]

# Image endpoint stage
FROM python:3.11-slim as image-endpoint

WORKDIR /app

# Copy and install requirements for image endpoint
COPY endpoints/image/src/builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the image endpoint source code
COPY endpoints/image/src/ ./src/

# Set Python path to find modules
ENV PYTHONPATH=/app/src

# Start the container
CMD ["python", "-u", "src/main.py", "stg"]

# Final stage - select the endpoint
FROM ${ENDPOINT}-endpoint as final