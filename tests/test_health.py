"""
Health check and readiness tests for Task API.
Verifies liveness and readiness probes.
"""

import pytest


def test_health_endpoint_exists(client):
    """Test health endpoint is accessible."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_status_is_healthy(client):
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"


def test_health_endpoint_content_type(client):
    """Test health endpoint returns JSON."""
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"


def test_root_endpoint_health(client):
    """Test root endpoint is accessible for basic healthcheck."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
