# Development Guide

This document covers how to set up your development environment and contribute to the project.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/ai-text-summarizer.git
    cd ai-text-summarizer
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install pre-commit hooks:

    ```bash
    pre-commit install
    ```

5. Copy the example environment file and modify if needed:

    ```bash
    cp .env.example .env
    ```

## Development Workflow

1. Create a feature branch:

    ```bash
    git checkout -b feature/your-feature-name
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Add your meaningful commit message"
    ```

3. Run tests:

    ```bash
    pytest
    ```

4. Push your branch and create a pull request:

    ```bash
    git push origin feature/your-feature-name
    ```

## Project Structure

```
ai-text-summarizer/
├── app/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core application components
│   ├── models/        # Pydantic models
│   ├── services/      # Actual use case logic
│   ├── tests/         # Test cases
│   └── main.py        # Application entry point
├── docs/              # Documentation
├── .github/           # GitHub-specific files
├── .env               # environment variables
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt   # Python dependencies
└── README.md          # Project overview
```
