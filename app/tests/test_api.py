from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test that the health check endpoint returns successfully."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.parametrize(
    "text,expected_status",
    [
        ("This is a test text that should be long enough for summarization.", 200),
        ("Too short", 422),  # Should fail validation
    ],
)
def test_summarize_validation(text, expected_status):
    """Test input validation for the summarize endpoint."""
    response = client.post(
        "/api/summarize",
        json={"text": text},
    )
    assert response.status_code == expected_status
