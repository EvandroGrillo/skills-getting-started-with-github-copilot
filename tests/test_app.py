from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_remove_participant_from_activity():
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "removed" in response.json()["message"].lower()

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
