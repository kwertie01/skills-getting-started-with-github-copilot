import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the activities dict before each test
    original = copy.deepcopy({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly tournaments",
            "schedule": "Tuesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["rachel@mergington.edu", "alex@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["ryan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific discoveries",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
        }
    })
    activities.clear()
    activities.update(original)
    yield

def test_get_activities():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]

def test_signup_success():
    # Arrange
    client = TestClient(app)
    email = "newstudent@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]

def test_signup_duplicate():
    # Arrange
    client = TestClient(app)
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_activity_not_found():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_success():
    # Arrange
    client = TestClient(app)
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]

def test_unregister_not_registered():
    # Arrange
    client = TestClient(app)
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"

def test_unregister_activity_not_found():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
