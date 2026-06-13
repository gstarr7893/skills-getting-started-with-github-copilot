"""Backend API tests for the activities endpoints."""


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()

    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert activities["Chess Club"]["max_participants"] == 12


def test_get_activities_includes_participants(client):
    response = client.get("/activities")
    activities = response.json()

    for activity_data in activities.values():
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)
        assert "schedule" in activity_data
        assert "description" in activity_data
        assert "max_participants" in activity_data


def test_signup_new_participant(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_participant_fails(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    response = client.post("/activities/Nonexistent Club/signup?email=test@example.com")

    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_existing_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_fails(client):
    response = client.delete("/activities/Chess Club/unregister?email=notregistered@example.com")

    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_nonexistent_activity_fails(client):
    response = client.delete("/activities/Nonexistent Club/unregister?email=test@example.com")

    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
