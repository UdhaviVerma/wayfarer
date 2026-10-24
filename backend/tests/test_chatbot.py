from fastapi.testclient import TestClient

from app.main import app


def test_chatbot_query():
    client = TestClient(app)
    response = client.post("/api/v1/chatbot/query", json={"message": "Should I move to Germany or UAE?"})
    assert response.status_code == 200
    assert "Germany" in response.json()["response"]
