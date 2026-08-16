from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_successfully_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200, response.text
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]

    client.delete(f"/activities/{activity_name}/participants/{email}")


def test_duplicate_signup_returns_400():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400, response.text
    assert "already signed up" in response.json()["detail"]


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200, response.text
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants/not-here@mergington.edu")

    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Participant not found"
