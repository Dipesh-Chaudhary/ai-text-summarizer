# AI Text Summarizer

A microservice for summarizing text using AI technology, built with FastAPI and following the 12-Factor App methodology.

## Features

- Text summarization using pre-trained AI models
---
- RESTful API with FastAPI
---
- Containerized with Docker
---
- Configurable via environment variables

- Comprehensive testing and CI/CD pipeline

## Quick Start

The easiest way to run the application is using Docker:

```bash
# Clone the repository
git clone https://github.com/Dipesh-Chaudhary/ai-text-summarizer.git
cd ai-text-summarizer

# Copy the example environment file and modify if needed
cp .env.example .env

# Start the application with Docker Compose
docker-compose up -d
```


## Once running, you can access:

- API Documentation: http://localhost:8000/docs
- Alternative API Documentation: http://localhost:8000/redoc


## Example API Usage
```python
import requests

response = requests.post(
    "http://localhost:8000/api/summarize",
    json={
        "text": "Your long text to be summarized goes here...",
        "max_length": 150,
        "min_length": 40
    }
)

print(response.json())
```
