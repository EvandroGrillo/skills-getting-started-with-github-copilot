import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    data = response.json()
    assert "Clube de Xadrez" in data
    assert "Aula de Programação" in data
    assert data["Clube de Xadrez"]["participants"]


def test_signup_for_activity_adds_participant(client):
    response = client.post(
        "/activities/Clube de Xadrez/signup?email=student@example.com"
    )

    assert response.status_code == 200
    assert "student@example.com" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "student@example.com" in activities["Clube de Xadrez"]["participants"]


def test_signup_for_duplicate_participant_returns_error(client):
    response = client.post(
        "/activities/Clube de Xadrez/signup?email=student@example.com"
    )

    assert response.status_code == 400
    assert "já está inscrito" in response.json()["detail"].lower()


def test_remove_participant_from_activity(client):
    response = client.delete(
        "/activities/Clube de Xadrez/participants/student@example.com"
    )

    assert response.status_code == 200
    assert "removido" in response.json()["message"].lower()

    activities = client.get("/activities").json()
    assert "student@example.com" not in activities["Clube de Xadrez"]["participants"]
