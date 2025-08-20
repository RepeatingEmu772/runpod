FROM python:3.11-slim

WORKDIR /

# Copy and install requirements
COPY builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your handler code
COPY src/handler.py .

# Start the container
CMD ["python", "-u", "/handler.py"]