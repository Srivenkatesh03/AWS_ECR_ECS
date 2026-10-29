# app/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

# set env defaults
ENV PORT=8080
ENV APP_VERSION=v1

EXPOSE 8080

# use gunicorn for production-like server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app", "--workers", "2"]
