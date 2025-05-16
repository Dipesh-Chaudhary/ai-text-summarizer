from transformers import pipeline
from typing import Optional
from app.core.config import settings
from app.core.logging import logger
import time


class TextSummarizer:
    """Service for text summarization using transformers."""
    
    def __init__(self):
        logger.info(f"Loading summarization model: {settings.MODEL_NAME}")
        start_time = time.time()
        self.summarizer = pipeline("summarization", model=settings.MODEL_NAME)
        logger.info(f"Model loaded in {time.time() - start_time:.2f} seconds")
    
    def summarize(
        self, 
        text: str, 
        max_length: Optional[int] = None, 
        min_length: Optional[int] = None
    ) -> str:
        """Summarize the given text."""
        logger.debug(f"Summarizing text of length: {len(text)}")
        
        # Use default values from settings if not provided
        max_length = max_length or settings.MAX_LENGTH
        min_length = min_length or settings.MIN_LENGTH
        
        # Check if text is too short for min_length
        if len(text.split()) < min_length:
            logger.warning(f"Text too short for min_length={min_length}, adjusting min_length")
            min_length = max(1, len(text.split()) - 1)
        
        result = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        
        logger.debug("Summarization completed")
        return result[0]['summary_text']


# Create a singleton instance
summarizer = None


def get_summarizer():
    """Return singleton instance of the summarizer."""
    global summarizer
    if summarizer is None:
        summarizer = TextSummarizer()
    return summarizer
