FROM python:3.9-slim  # or any other specific version

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-i"]
docker build -t safe-python-env .
