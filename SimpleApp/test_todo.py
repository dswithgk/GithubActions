from app import app

def test_create_task():
    from fastapi.testclient import TestClient 
    client = TestClient(app)

    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks():
    from fastapi.testclient import TestClient
    client = TestClient(app)

    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_task():
    from fastapi.testclient import TestClient
    client = TestClient(app)

    # Create a task first
    response = client.post("/tasks/", json={
        "title": "Initial Task",
        "description": "To be updated",
        "completed": False
    })
    task_id = response.json()["id"]

    # Update the task
    update_response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description",
        "completed": True
    })
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Task"

def test_delete_task():
    from fastapi.testclient import TestClient
    client = TestClient(app)

    # Create a task first
    response = client.post("/tasks/", json={
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "completed": False
    })
    task_id = response.json()["id"]

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted"