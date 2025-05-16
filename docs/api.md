# API Reference

## Endpoints

## POST /api/summarize
Summarizes the provided text using AI.
### Request Body:
```json
{
  "text": "Your long text to be summarized...",
  "max_length": 150,  // Optional
  "min_length": 40    // Optional
}
```
### Response:
```json
{
  "summary": "The summarized text...",
  "original_length": 500,
  "summary_length": 100
}
```

## GET /api/health
Health check endpoint.

### Response:
```json
{
  "status": "healthy"
}
```
