from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_request_id_is_returned() -> None:
    response = client.get("/health", headers={"X-Request-ID": "test-request-1"})
    assert response.headers["X-Request-ID"] == "test-request-1"


def test_readiness_reports_checks() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert set(response.json()["checks"]) == {"qdrant", "redis"}

