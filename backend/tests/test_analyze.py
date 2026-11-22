from fastapi.testclient import TestClient
from app.main import app

def test_requires_key(monkeypatch):
    monkeypatch.setenv("PROMPTGUARD_API_KEY", "test-key")
    response = TestClient(app).post("/api/v1/analyze", json={"prompt": "hello"})
    assert response.status_code == 401

def test_empty_prompt_rejected(monkeypatch):
    monkeypatch.setenv("PROMPTGUARD_API_KEY", "test-key")
    response = TestClient(app).post("/api/v1/analyze", json={"prompt": ""}, headers={"X-API-Key": "test-key"})
    assert response.status_code == 422
