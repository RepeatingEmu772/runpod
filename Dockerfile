FROM python:3.11-slim

WORKDIR /app

# Copy pyproject.toml
COPY pyproject.toml .

# Copy source code
COPY src/ ./src/

# Install the package
RUN pip install --no-cache-dir -e .

# Start the container
CMD ["python", "-u", "-m", "runpod_mistral", "stg"]