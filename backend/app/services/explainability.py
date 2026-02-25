import os
from typing import Any


def try_shap_values(model: Any, X_row, feature_names: list[str]) -> list[dict]:
    enabled = os.getenv("ENABLE_SHAP", "false").lower() in {"1", "true", "yes"}
    if not enabled:
        return []
    try:
        import shap  # type: ignore
    except Exception:  # noqa: BLE001
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
    except Exception:  # noqa: BLE001
        return []
