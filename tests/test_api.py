"""Tests for NAGRO 4.1 API endpoints."""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    def test_health(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert data["model"] == "NAGRO 4.1"


class TestInfoEndpoint:
    def test_info(self, client):
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "NAGRO 4.1"
        assert "capabilities" in data


class TestChatEndpoint:
    def test_chat(self, client):
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hello", "stream": False},
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "conversation_id" in data


class TestRootEndpoint:
    def test_root_serves_html(self, client):
        response = client.get("/")
        assert response.status_code == 200
