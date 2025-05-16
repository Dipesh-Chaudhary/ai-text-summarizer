"""API models used for request and response schemas."""
from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    """Request model for text summarization."""

    text: str = Field(..., min_length=10, description="The text to summarize")
    max_length: int = Field(None, description="Maximum length of the summary")
    min_length: int = Field(None, description="Minimum length of the summary")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": (
                    "FastAPI is a modern, fast (high-performance), web framework for "
                    "building APIs with Python 3.7+ based on standard Python type "
                    "hints. The key features are: Fast, Fast to code, Fewer bugs, "
                    "Intuitive, Easy, Short, Robust, Standards-based."
                ),
                "max_length": 50,
                "min_length": 10,
            }
        }
    }


class SummarizeResponse(BaseModel):
    """Response model for text summarization."""

    summary: str = Field(..., description="The generated summary")
    original_length: int = Field(..., description="Length of the original text")
    summary_length: int = Field(..., description="Length of the generated summary")
