"""Pytest configuration and shared fixtures for backend tests."""

import json
import os

import joblib
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from app.services.feature_extraction import EngineeredFeatures
from app.services.model_registry import load_model, load_model_meta


@pytest.fixture
def mock_model_path(tmp_path):
    """Create and setup a mock model for testing."""
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
                "metrics": {"logistic_regression": {"accuracy": 0.95, "f1": 0.94}},
            }
        ),
        encoding="utf-8",
    )

    # Store environment variables
    old_model_path = os.environ.get("BACKEND_MODEL_PATH")
    old_model_meta_path = os.environ.get("BACKEND_MODEL_META_PATH")

    # Set new paths
    os.environ["BACKEND_MODEL_PATH"] = str(model_path)
    os.environ["BACKEND_MODEL_META_PATH"] = str(meta_path)

    # Clear caches
    load_model.cache_clear()
    load_model_meta.cache_clear()

    yield model_path, meta_path

    # Restore environment
    if old_model_path is not None:
        os.environ["BACKEND_MODEL_PATH"] = old_model_path
    else:
        os.environ.pop("BACKEND_MODEL_PATH", None)

    if old_model_meta_path is not None:
        os.environ["BACKEND_MODEL_META_PATH"] = old_model_meta_path
    else:
        os.environ.pop("BACKEND_MODEL_META_PATH", None)

    # Clear caches again
    load_model.cache_clear()
    load_model_meta.cache_clear()
