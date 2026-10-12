import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_rejects_unsupported_model():
    response = client.post("/chat", json={"question": "What is RAG?", "model": "gemini"})

    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]

def test_list_models_returns_all_models():
    response = client.get("/models")
    assert response.status_code == 200
    assert "claude" in response.json()["models"]

def test_get_model_found():
    response = client.get("/models/claude")
    assert response.status_code == 200
    assert response.json()["available"] is True

def test_get_model_not_found():
    response = client.get("/models/gemini")
    assert response.status_code == 404

def test_cost_uses_default_price():
    response = client.get("/cost", params={"tokens": 5000})
    assert response.status_code == 200
    assert response.json()["cost"] == pytest.approx(0.01)

def test_chat_returns_answer():
    response = client.post("/chat", json={"question": "What is RAG?"})
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "gpt-4o"
    assert body["tokens_used"] == 3



def test_chat_rejects_empty_question():
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422

def test_cost_requires_tokens():
    response = client.get("/cost")
    assert response.status_code == 422

def test_chat_rejects_too_many_tokens():
    response = client.post("/chat", json={"max_tokens":9000})
    assert response.status_code == 422


