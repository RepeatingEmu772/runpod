FROM python:3.11-slim

WORKDIR /app

COPY builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV PYTHONPATH=/app/src

CMD ["python", "-u", "-m", "runpod", "--handler-path", "src/handler.py"]