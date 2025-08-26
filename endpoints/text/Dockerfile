FROM python:3.11-slim

WORKDIR /app

# Copy and install requirements
COPY builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the endpoint source code
COPY src/ ./src/

# Set Python path to find modules
ENV PYTHONPATH=/app/src

# Start the container
CMD ["python", "-u", "src/main.py", "stg"]