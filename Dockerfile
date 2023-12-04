# Use the slim version of Python 3.9 as the base image
FROM python:3.9-slim

WORKDIR /app

CMD ["python", "-i"]
