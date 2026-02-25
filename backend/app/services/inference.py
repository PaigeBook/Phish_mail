from typing import Any

import numpy as np

from app.services.explainability import try_shap_values
from app.services.feature_extraction import EngineeredFeatures
from app.services.model_registry import load_model, load_model_meta
from app.utils.constants import LEGIT_LABEL, PHISHING_LABEL, RISK_LOW_MAX, RISK_MED_MAX
from app.utils.keywords import find_suspicious_terms
from app.utils.text import clean_text


def _risk_level(score: float) -> str:
    """Map prediction score to risk level (Low/Medium/High)."""
    if score < RISK_LOW_MAX:
        return "Low"
    if score < RISK_MED_MAX:
        return "Medium"
    return "High"


def _combine_text(body: str, headers: str | None) -> str:
    """Combine email headers and body for analysis."""
    if headers:
        return f"{headers}\n\n{body}"
    return body


def _top_linear_features(
    model: Any, feature_names: list[str], X_row: Any
) -> list[dict]:
    """Extract top contributing features from linear model."""
    if not hasattr(model, "coef_"):
        return []
    coef = model.coef_[0]
    contrib = X_row.toarray().ravel() * coef
    top_idx = np.argsort(contrib)[-5:][::-1]
    top = []
    for idx in top_idx:
        if contrib[idx] <= 0:
            continue
        top.append({"feature": feature_names[idx], "contribution": float(contrib[idx])})
    return top


def _get_feature_names(pipeline: Any) -> list[str]:
    """Extract feature names from sklearn pipeline."""
    features = pipeline.named_steps.get("features")
    if not features:
        return []
    names = []
    for _, transformer in features.transformer_list:
        if hasattr(transformer, "get_feature_names_out"):
            names.extend(list(transformer.get_feature_names_out()))
    return names


def predict_email(body: str, headers: str | None) -> dict:
    """Predict phishing likelihood for an email with explainability.

    Args:
        body: Email body text
        headers: Optional raw email headers

    Returns:
        Dictionary with prediction, confidence, risk_level, and explanation
    """
    model = load_model()
    meta = load_model_meta()

    combined = _combine_text(body, headers)
    cleaned = clean_text(combined)

    proba = model.predict_proba([cleaned])[0]
    phishing_score = float(proba[1])
    prediction = PHISHING_LABEL if phishing_score >= 0.5 else LEGIT_LABEL

    reasons = []
    suspicious_terms = find_suspicious_terms(cleaned)
    if suspicious_terms:
        reasons.append("Suspicious keywords detected")

    if "http" in cleaned or "www" in cleaned:
        reasons.append("Contains links")

    risk = _risk_level(phishing_score)

    top_features: list[dict] = []
    classifier = model.named_steps.get("classifier")
    X_row = model.named_steps["features"].transform([cleaned])
    feature_names = meta.get("feature_names") or _get_feature_names(model)

    if hasattr(classifier, "coef_"):
        top_features = _top_linear_features(classifier, feature_names, X_row)
    else:
        top_features = try_shap_values(classifier, X_row, feature_names)

    engineered = EngineeredFeatures()
    engineered_values = engineered.transform([cleaned])[0]
    engineered_stats = dict(
        zip(engineered.get_feature_names_out(), engineered_values, strict=False)
    )

    explanation = {
        "reasons": reasons or ["Model confidence based on learned patterns"],
        "top_features": top_features,
        "suspicious_terms": suspicious_terms,
        "stats": {
            "phishing_score": phishing_score,
            "keyword_hits": len(suspicious_terms),
            "url_count": engineered_stats.get("url_count", 0),
            "ip_url_count": engineered_stats.get("ip_url_count", 0),
            "email_length": engineered_stats.get("email_length", 0),
            "special_char_count": engineered_stats.get("special_char_count", 0),
            "header_anomaly": engineered_stats.get("header_anomaly", 0),
        },
    }

    return {
        "prediction": prediction,
        "confidence": phishing_score,
        "risk_level": risk,
        "explanation": explanation,
    }
