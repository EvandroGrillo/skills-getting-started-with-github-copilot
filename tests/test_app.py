from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_data():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["participants"]


def test_signup_for_activity_adds_participant():
    response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )

    assert response.status_code == 200
    assert "student@example.com" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "student@example.com" in activities["Chess Club"]["participants"]


def test_signup_for_duplicate_participant_returns_error():
    response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_remove_participant_from_activity():
    response = client.delete(
        "/activities/Chess Club/participants/student@example.com"
    )

    assert response.status_code == 200
    assert "removed" in response.json()["message"].lower()

    activities = client.get("/activities").json()
    assert "student@example.com" not in activities["Chess Club"]["participants"]
