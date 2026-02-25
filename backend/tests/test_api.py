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


def _train_dummy_model(model_path: Path, meta_path: Path) -> None:
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
        json.dumps({"feature_names": []}, indent=2), encoding="utf-8"
    )


def test_predict_endpoint(tmp_path):
    model_path = tmp_path / "model.joblib"
    meta_path = tmp_path / "meta.json"
    _train_dummy_model(model_path, meta_path)

    os.environ["BACKEND_MODEL_PATH"] = str(model_path)
    os.environ["BACKEND_MODEL_META_PATH"] = str(meta_path)
    load_model.cache_clear()
    load_model_meta.cache_clear()

    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/predict", json={"body": "verify your account", "headers": None}
    )

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "risk_level" in data
