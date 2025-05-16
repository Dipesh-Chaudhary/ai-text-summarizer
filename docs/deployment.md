# Deployment Guide
This document covers how to deploy the AI Text Summarizer microservice.

## Docker Deployment
The simplest way to deploy the application is using Docker:

1. Build the Docker image:
```bash
docker build -t ai-text-summarizer .
```

2. Run the Docker container:
```bash
docker run -d -p 8000:8000 --env-file .env ai-text-summarizer
```

### Environment Variables
The application can be configured using environment variables:

| Variable     | Description                | Default               |
|--------------|----------------------------|------------------------|
| API_HOST     | Host to bind the API server | 0.0.0.0               |
| API_PORT     | Port for the API server     | 8000                  |
| DEBUG        | Enable debug mode           | False                 |
| MODEL_NAME   | Hugging Face model name     | sshleifer/distilbart-cnn-12-6|
| MAX_LENGTH   | Max summary length          | 150                   |
| MIN_LENGTH   | Min summary length          | 40                    |
| LOG_LEVEL    | Logging level               | INFO                  |



## Cloud Deployment

Each platform has their own specific deployment steps, but all support Docker containers.
