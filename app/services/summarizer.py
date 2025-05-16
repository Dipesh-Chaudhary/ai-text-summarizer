"""Text summarization service using Hugging Face transformers."""
import time
from typing import List, Optional

from transformers import AutoTokenizer, pipeline

from app.core.config import settings
from app.core.logging import logger


class TextSummarizer:
    """Service for text summarization using transformers."""

    def __init__(self):
        """Initialize the TextSummarizer with a model and tokenizer."""
        logger.info(f"Loading summarization model: {settings.MODEL_NAME}")
        start_time = time.time()

        # Force CPU usage for resource-constrained environments
        self.summarizer = pipeline(
            "summarization", model=settings.MODEL_NAME, device=-1
        )

        # Get the tokenizer for the model to properly handle text length
        self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)

        logger.info("Model loaded in %.2f seconds", time.time() - start_time)

    def _chunk_text(self, text: str, max_chunk_size: int = 1024) -> List[str]:
        """Split text into chunks that the model can process."""
        # Simple chunking by sentences
        sentences = text.split(". ")
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            # Add period back except for the last sentence if it doesn't have one
            if not sentence.strip().endswith(".") and sentence.strip():
                sentence = sentence + "."
            # Handle multiple spaces after period during split
            sentence = sentence.strip()

            if not sentence:  # Skip empty sentences
                continue

            # Get token count for this sentence
            token_count = len(self.tokenizer.encode(sentence))

            if current_length + token_count <= max_chunk_size:
                current_chunk.append(sentence)
                current_length += token_count
            else:
                # Only add if current_chunk is not empty
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = token_count

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def summarize(
        self,
        text: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
    ) -> str:
        """Summarize the given text."""
        logger.debug(f"Summarizing text of length: {len(text)}")

        # Use default values from settings if not provided
        max_length = max_length or settings.MAX_LENGTH
        min_length = min_length or settings.MIN_LENGTH

        # Check if text is too short for min_length
        # Use token length instead of word count for better estimation
        text_tokens = self.tokenizer.encode(text)
        if len(text_tokens) < min_length:
            logger.warning(
                (
                    "Text token length (%d) too short for min_length=%d, "
                    "adjusting min_length"
                ),
                len(text_tokens),
                min_length,
            )
            min_length = max(1, len(text_tokens) - 1)  # Adjusted based on token length

        try:
            # Use token length for checks instead of word count
            if len(text_tokens) < 250:  # Use a token count threshold
                result = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True,
                )
                summary = result[0]["summary_text"].strip()
            else:
                # For longer texts, chunk and summarize each part
                chunks = self._chunk_text(text)
                logger.debug(f"Text split into {len(chunks)} chunks")

                if not chunks:  # Handle empty text case (more Pythonic)
                    return ""
                elif len(chunks) == 1:
                    result = self.summarizer(
                        chunks[0],
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False,
                        truncation=True,
                    )
                    summary = result[0]["summary_text"].strip()
                else:
                    # First summarize each chunk
                    intermediate_summaries = []
                    # Adjust intermediate lengths to be potentially smaller
                    intermediate_max_length = max(50, max_length // 2)
                    intermediate_min_length = min(20, min_length)

                    for i, chunk in enumerate(chunks):
                        logger.debug(f"Summarizing chunk {i + 1}/{len(chunks)}")
                        result = self.summarizer(
                            chunk,
                            max_length=intermediate_max_length,
                            min_length=intermediate_min_length,
                            do_sample=False,
                            truncation=True,
                        )
                        intermediate_summaries.append(result[0]["summary_text"].strip())

                    # Then summarize the combined intermediate summaries
                    combined_text = " ".join(intermediate_summaries)

                    # Check if combined text is too short after intermediate summaries
                    combined_tokens = self.tokenizer.encode(combined_text)
                    final_min_length = min_length
                    if len(combined_tokens) < final_min_length:
                        logger.warning(
                            "Combined intermediate text token length (%d) "
                            "too short for final min_length=%d, "
                            "adjusting final min_length",
                            len(combined_tokens),
                            final_min_length,
                        )
                        final_min_length = max(1, len(combined_tokens) - 1)

                    result = self.summarizer(
                        combined_text,
                        max_length=max_length,
                        min_length=final_min_length,
                        do_sample=False,
                        truncation=True,
                    )
                    summary = result[0]["summary_text"].strip()

            # Ensure summary ends with proper punctuation if it doesn't already
            if summary and not any(summary.endswith(p) for p in [".", "!", "?"]):
                # Add a period if the original text ended with one
                # or if it's just a generic summary end
                if text.rstrip().endswith(".") or True:  # Default to adding period
                    summary += "."

            logger.debug("Summarization completed")
            return summary

        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            # Fallback to a simple extraction-based summary
            # Split and clean sentences
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            if len(sentences) > 3:
                fallback_summary = ". ".join(sentences[:3]) + "."
            elif sentences:  # If there are sentences, join them
                fallback_summary = ". ".join(sentences)
                if not fallback_summary.endswith("."):
                    fallback_summary += "."
            else:  # If text was empty or only whitespace
                fallback_summary = ""

            logger.warning("Using fallback summary due to error")
            return fallback_summary


# Create a singleton instance
summarizer = None


def get_summarizer():
    """Return singleton instance of the summarizer."""
    global summarizer
    if summarizer is None:
        summarizer = TextSummarizer()
    return summarizer
