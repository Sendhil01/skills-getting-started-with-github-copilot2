import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory activities before each test
    for activity in activities.values():
        if "Chess Club" in activity["description"]:
            activity["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        elif "Programming" in activity["description"]:
            activity["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        elif "Gym" in activity["description"]:
            activity["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
        else:
            activity["participants"] = []


def test_get_activities():
    # Arrange
    # (fixture resets state)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_for_activity():
    # Arrange
    email = "newstudent@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant():
    # Arrange
    email = "daniel@mergington.edu"
    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_participant():
    # Arrange
    email = "ghost@mergington.edu"
    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    # Act
    response = client.post("/activities/Nonexistent/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    # Act
    response = client.delete("/activities/Nonexistent/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
