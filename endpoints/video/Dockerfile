FROM python:3.11-slim

WORKDIR /app

COPY ./builder/requirements.txt /app/builder/requirements.txt
RUN pip install --no-cache-dir -r /app/builder/requirements.txt

COPY ./src /app/src

CMD ["python", "src/main.py", "prod"]
