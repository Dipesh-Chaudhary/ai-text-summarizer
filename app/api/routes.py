from fastapi import APIRouter, Depends, HTTPException
from app.models.api import SummarizeRequest, SummarizeResponse
from app.services.summarizer import get_summarizer, TextSummarizer
from app.core.logging import logger

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(
    request: SummarizeRequest,
    summarizer: TextSummarizer = Depends(get_summarizer)
):
    """Summarize the provided text."""
    try:
        summary = summarizer.summarize(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        return SummarizeResponse(
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary)
        )
    
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
