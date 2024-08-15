from fastapi.testclient import TestClient
from app.presentation.application import get_app

client = TestClient(get_app())


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
