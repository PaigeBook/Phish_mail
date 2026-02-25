import json
import os
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline

from app.services.feature_extraction import EngineeredFeatures
from app.utils.text import clean_text

TEXT_COLUMNS = ["text", "body", "email", "content", "message"]
LABEL_COLUMNS = ["label", "is_phishing", "target", "class", "category"]


def _resolve_columns(df: pd.DataFrame) -> tuple[str, str]:\n    \"\"\"Detect text and label columns from DataFrame.\n    \n    Searches for common column name variations to identify text inputs and labels.\n    \"\"\""}}]
    text_col = next((c for c in TEXT_COLUMNS if c in df.columns), None)
    label_col = next((c for c in LABEL_COLUMNS if c in df.columns), None)
    if not text_col or not label_col:
        raise ValueError("Dataset must contain text and label columns")
    return text_col, label_col


def _normalize_labels(values: pd.Series) -> np.ndarray:
    def to_int(val):
        if isinstance(val, (int, float)):
            return int(val)
        lowered = str(val).strip().lower()
        if lowered in {"phishing", "spam", "malicious"}:
            return 1
        return 0

    return values.apply(to_int).to_numpy()


def _build_pipeline(model) -> Pipeline:
    features = FeatureUnion(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    stop_words="english",
                ),
            ),
            ("engineered", EngineeredFeatures()),
        ]
    )
    return Pipeline([("features", features), ("classifier", model)])


def _get_feature_names(pipeline: Pipeline) -> list[str]:
    names = []
    for _, transformer in pipeline.named_steps["features"].transformer_list:
        if hasattr(transformer, "get_feature_names_out"):
            names.extend(list(transformer.get_feature_names_out()))
    return names


def _evaluate(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:\n    \"\"\"Compute comprehensive evaluation metrics for model performance.\"\"\""}}]
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred)),
        "recall": float(recall_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }


def main() -> None:
    dataset_path = os.getenv("BACKEND_DATASET_PATH", "backend/data/phishing.csv")
    model_path = Path(
        os.getenv("BACKEND_MODEL_PATH", "backend/models/phish_model.joblib")
    )
    meta_path = Path(
        os.getenv("BACKEND_MODEL_META_PATH", "backend/models/model_meta.json")
    )

    df = pd.read_csv(dataset_path)
    text_col, label_col = _resolve_columns(df)

    X = df[text_col].fillna("").apply(clean_text)
    y = _normalize_labels(df[label_col])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": LogisticRegression(
            max_iter=1000, class_weight="balanced"
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            n_jobs=-1,
            class_weight="balanced",
            random_state=42,
        ),
    }

    metrics = {}
    best_name = None
    best_f1 = -1.0
    best_pipeline = None

    for name, model in models.items():
        pipeline = _build_pipeline(model)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        metrics[name] = _evaluate(y_test, y_pred, y_proba)
        if metrics[name]["f1"] > best_f1:
            best_f1 = metrics[name]["f1"]
            best_name = name
            best_pipeline = pipeline

    if not best_pipeline:
        raise RuntimeError("No model trained")

    model_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_pipeline, model_path)

    meta = {
        "best_model": best_name,
        "trained_at": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "feature_names": _get_feature_names(best_pipeline),
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("Training complete. Best model:", best_name)


if __name__ == "__main__":
    main()
