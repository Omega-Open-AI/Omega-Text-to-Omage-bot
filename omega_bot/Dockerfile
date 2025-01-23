FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY config/ ./config/
COPY src/ ./src/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "src.main"]
