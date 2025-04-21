import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rank_endpoint_success():
    payload = {
        "resume_text": "Experienced backend engineer with microservices and Docker knowledge.",
        "job_description": "We are looking for someone who has worked with backend APIs, Docker, and PostgreSQL.",
        "photo_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBD..."  # use real or dummy base64 string
    }

    response = client.post("/rank/rank", json=payload)
    assert response.status_code == 200, f"Unexpected response: {response.text}"
    data = response.json()
    assert "score" in data
    assert isinstance(data["score"], (int, float))
