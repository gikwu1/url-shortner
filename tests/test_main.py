import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_shorten_url():
    response = client.post("/shorten", json={"url": "https://www.google.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data

def test_redirect_url():
    # First shorten a URL
    shorten_response = client.post("/shorten", json={"url": "https://www.google.com"})
    short_code = shorten_response.json()["short_code"]

    # Then test the redirect
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.google.com"

def test_redirect_not_found():
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404
