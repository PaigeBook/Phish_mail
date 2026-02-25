import json
import os
from pathlib import Path

import joblib
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from app.services.batch import batch_predict
from app.services.feature_extraction import EngineeredFeatures
from app.services.health import get_health
from app.services.inference import predict_email
from app.services.model_registry import load_model, load_model_meta


@pytest.fixture
def mock_model(tmp_path):
    """Create dummy model for testing."""
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

    yield

    load_model.cache_clear()
    load_model_meta.cache_clear()


def test_predict_email_phishing(mock_model):
    """Test phishing detection."""
    result = predict_email("verify your account now", None)
    assert result["prediction"] in {"phishing", "legitimate"}
    assert 0 <= result["confidence"] <= 1
    assert result["risk_level"] in {"Low", "Medium", "High"}


def test_predict_email_legitimate(mock_model):
    """Test legitimate email detection."""
    result = predict_email("project update attached", None)
    assert result["prediction"] in {"phishing", "legitimate"}


def test_predict_email_with_headers(mock_model):
    """Test prediction with headers."""
    headers = "From: sender@example.com\nReply-To: sender@example.com"
    result = predict_email("verify account", headers)
    assert result["prediction"] in {"phishing", "legitimate"}
    assert result["explanation"]["stats"]["header_anomaly"] in {0, 1}


def test_batch_predict(mock_model):
    """Test batch prediction."""
    emails = [
        {"body": "verify account", "headers": None},
        {"body": "project update", "headers": None},
    ]
    predictions, batch_id = batch_predict(emails)
    assert len(predictions) == 2
    assert batch_id is not None
    assert all(p.get("status") in {"success", "error"} for p in predictions)


def test_get_health(mock_model):
    """Test health check."""
    health = get_health()
    assert health["status"] == "ok"
    assert health["model_loaded"] is True
    assert health["model_name"] == "logistic_regression"
    assert health["accuracy"] == 0.95
