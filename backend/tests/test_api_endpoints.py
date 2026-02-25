import json
import os
from pathlib import Path

import joblib
from fastapi.testclient import TestClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from app.main import create_app
from app.services.feature_extraction import EngineeredFeatures
from app.services.model_registry import load_model, load_model_meta


def setup_mock_model(tmp_path):
    """Setup mock model for endpoint testing."""
    model_path = tmp_path / "model.joblib"
    meta_path = tmp_path / "meta.json"

    X = [
        "verify your account now",
        "team lunch schedule",
        "reset your password immediately",
        "project update attached",
    ]
    y = [1, 0, 1, 0]

    pipeline = Pipeline(
        [
            (
                "features",
                FeatureUnion(
                    [
                        (
                            "tfidf",
                            TfidfVectorizer(max_features=100, stop_words="english"),
                        ),
                        ("engineered", EngineeredFeatures()),
                    ]
                ),
            ),
            ("classifier", LogisticRegression(max_iter=500)),
        ]
    )
    pipeline.fit(X, y)

    joblib.dump(pipeline, model_path)
    meta_path.write_text(
        json.dumps(
            {
                "best_model": "logistic_regression",
                "trained_at": "2026-02-25T10:00:00",
                "metrics": {
                    "logistic_regression": {"accuracy": 0.95, "f1": 0.94}
                },
            }
        ),
        encoding="utf-8",
    )

    os.environ["BACKEND_MODEL_PATH"] = str(model_path)
    os.environ["BACKEND_MODEL_META_PATH"] = str(meta_path)
    load_model.cache_clear()
    load_model_meta.cache_clear()


def test_health_endpoint(tmp_path):
    """Test /api/health endpoint."""
    setup_mock_model(tmp_path)
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert data["model_name"] == "logistic_regression"


def test_predict_endpoint(tmp_path):
    """Test /api/predict endpoint."""
    setup_mock_model(tmp_path)
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


def test_predict_batch_endpoint(tmp_path):
    """Test /api/predict-batch endpoint."""
    setup_mock_model(tmp_path)
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


def test_predict_batch_empty(tmp_path):
    """Test batch endpoint with no emails."""
    setup_mock_model(tmp_path)
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/predict-batch",
        json={"emails": []},
    )
    assert response.status_code == 400


def test_predict_batch_too_many(tmp_path):
    """Test batch endpoint with too many emails."""
    setup_mock_model(tmp_path)
    app = create_app()
    client = TestClient(app)

    emails = [{"body": f"text {i}", "headers": None} for i in range(1001)]
    response = client.post(
        "/api/predict-batch",
        json={"emails": emails},
    )
    assert response.status_code == 400
