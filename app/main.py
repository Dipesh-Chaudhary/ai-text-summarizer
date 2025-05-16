"""This is the main application file for the FastAPI app.

It initializes the app, sets up middleware.
And includes routers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logging import logger
from app.services.summarizer import get_summarizer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifespan events."""
    # Startup events
    logger.info("Application starting up...")

    # Pre-load the summarizer model
    get_summarizer()

    logger.info("Application startup complete")

    yield

    # Shutdown events
    logger.info("Application shutting down...")


# Initialize the application
app = FastAPI(
    title="AI Text Summarizer",
    description="A microservice for summarizing text using AI",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
