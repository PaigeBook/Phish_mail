import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def try_shap_values(model: Any, X_row: Any, feature_names: list[str]) -> list[dict]:
    """Extract SHAP values for model explainability (optional, feature-gated).
    
    Args:
        model: Trained sklearn classifier
        X_row: Feature matrix (sparse or dense)
        feature_names: List of feature names
        
    Returns:
        List of top contributing features with SHAP values, or empty list if disabled/failed
    """
    enabled = os.getenv("ENABLE_SHAP", "false").lower() in {"1", "true", "yes"}
    if not enabled:
        return []
    
    try:
        import shap  # type: ignore  # noqa: F401
    except ImportError:
        logger.debug("SHAP not installed, skipping explainability")
        return []

    try:
        explainer = shap.Explainer(model)
        shap_values = explainer(X_row)
        values = shap_values.values[0]
        top_idx = sorted(range(len(values)), key=lambda i: values[i], reverse=True)[:5]
        top = [
            {"feature": feature_names[i], "contribution": float(values[i])}
            for i in top_idx
            if values[i] > 0
        ]
        return top
    except (RuntimeError, ValueError, IndexError) as exc:
        logger.debug(f"SHAP computation failed: {exc}")
        return []
