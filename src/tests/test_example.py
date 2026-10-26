from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_accueil():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "L'API fonctionne"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
