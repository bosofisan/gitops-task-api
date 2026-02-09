"""
API endpoint tests for Task API.
Tests full CRUD operations and error handling.
"""

import pytest
from fastapi import HTTPException


def test_root_endpoint(client):
    """Test root endpoint returns status and version."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task API is running"
    assert data["version"] == "1.0.0"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


class TestTaskCreation:
    """Tests for task creation."""

    def test_create_task(self, client, sample_task):
        """Test creating a task."""
        response = client.post("/tasks", json=sample_task)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task["id"]
        assert data["title"] == sample_task["title"]
        assert data["completed"] == sample_task["completed"]

    def test_create_task_with_default_completed(self, client):
        """Test creating a task defaults completed to False."""
        task = {"id": 1, "title": "Test task"}
        response = client.post("/tasks", json=task)
        assert response.status_code == 200
        assert response.json()["completed"] is False

    def test_create_duplicate_task(self, client, sample_task):
        """Test creating a task with duplicate ID raises 409."""
        # Create first task
        response1 = client.post("/tasks", json=sample_task)
        assert response1.status_code == 200

        # Try to create duplicate
        response2 = client.post("/tasks", json=sample_task)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"]


class TestTaskRetrieval:
    """Tests for retrieving tasks."""

    def test_get_all_tasks(self, client, sample_tasks):
        """Test retrieving all tasks."""
        # Create multiple tasks
        for task in sample_tasks:
            client.post("/tasks", json=task)

        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(sample_tasks)

    def test_get_all_tasks_empty(self, client):
        """Test retrieving tasks when none exist."""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == {}

    def test_get_single_task(self, client, sample_task):
        """Test retrieving a single task by ID."""
        # Create task
        client.post("/tasks", json=sample_task)

        # Retrieve it
        response = client.get(f"/tasks/{sample_task['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == sample_task["id"]

    def test_get_nonexistent_task(self, client):
        """Test retrieving non-existent task returns 404."""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestTaskUpdate:
    """Tests for updating tasks."""

    def test_update_task(self, client, sample_task):
        """Test updating an existing task."""
        # Create task
        client.post("/tasks", json=sample_task)

        # Update it
        updated_task = {
            "id": sample_task["id"],
            "title": "Updated title",
            "completed": True
        }
        response = client.put(f"/tasks/{sample_task['id']}", json=updated_task)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["completed"] is True

    def test_update_nonexistent_task(self, client, sample_task):
        """Test updating non-existent task returns 404."""
        response = client.put(f"/tasks/{sample_task['id']}", json=sample_task)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestTaskDeletion:
    """Tests for deleting tasks."""

    def test_delete_task(self, client, sample_task):
        """Test deleting an existing task."""
        # Create task
        client.post("/tasks", json=sample_task)

        # Delete it
        response = client.delete(f"/tasks/{sample_task['id']}")
        assert response.status_code == 200
        assert response.json()["message"] == "Task deleted"

        # Verify it's gone
        get_response = client.get(f"/tasks/{sample_task['id']}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_task(self, client):
        """Test deleting non-existent task returns 404."""
        response = client.delete("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestTaskIntegration:
    """Integration tests for task workflow."""

    def test_complete_task_workflow(self, client):
        """Test complete create -> read -> update -> delete workflow."""
        # Create
        task = {"id": 1, "title": "Integration test", "completed": False}
        create_response = client.post("/tasks", json=task)
        assert create_response.status_code == 200

        # Read all
        all_response = client.get("/tasks")
        assert len(all_response.json()) == 1

        # Read single
        single_response = client.get("/tasks/1")
        assert single_response.status_code == 200

        # Update
        updated = {"id": 1, "title": "Updated", "completed": True}
        update_response = client.put("/tasks/1", json=updated)
        assert update_response.json()["completed"] is True

        # Delete
        delete_response = client.delete("/tasks/1")
        assert delete_response.status_code == 200

        # Verify deleted
        final_response = client.get("/tasks")
        assert len(final_response.json()) == 0
