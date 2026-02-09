"""
Pytest configuration and fixtures for Task API tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="function")
def client():
    """
    Provide a test client for API requests.
    Resets app state before each test.
    """
    # Clear tasks before each test
    app.tasks = {}
    return TestClient(app)


@pytest.fixture
def sample_task():
    """Provide a sample task for testing."""
    return {
        "id": 1,
        "title": "Buy groceries",
        "completed": False
    }


@pytest.fixture
def sample_tasks():
    """Provide multiple sample tasks for testing."""
    return [
        {"id": 1, "title": "Buy groceries", "completed": False},
        {"id": 2, "title": "Write documentation", "completed": True},
        {"id": 3, "title": "Deploy to production", "completed": False},
    ]
