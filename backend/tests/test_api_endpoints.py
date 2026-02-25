"""API endpoint integration tests."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint(mock_model_path):
    """Test /api/health endpoint."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert data["model_name"] == "logistic_regression"


def test_predict_endpoint(mock_model_path):
    """Test /api/predict endpoint."""
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/predict",
        json={"body": "verify your account now", "headers": None},
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "risk_level" in data
    assert "explanation" in data


def test_predict_batch_endpoint(mock_model_path):
    """Test /api/predict-batch endpoint."""
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/predict-batch",
        json={
            "emails": [
                {"body": "verify account", "headers": None},
                {"body": "project update", "headers": None},
            ]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["processed_count"] == 2
    assert len(data["predictions"]) == 2
    assert "batch_id" in data


def test_predict_batch_empty(mock_model_path):
    """Test batch endpoint with no emails."""
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/predict-batch",
        json={"emails": []},
    )
    assert response.status_code == 400


def test_predict_batch_too_many(mock_model_path):
    """Test batch endpoint with too many emails."""
    app = create_app()
    client = TestClient(app)

    emails = [{"body": f"text {i}", "headers": None} for i in range(1001)]
    response = client.post(
        "/api/predict-batch",
        json={"emails": emails},
    )
    assert response.status_code == 400
