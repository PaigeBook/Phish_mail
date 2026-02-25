import logging
from typing import Any

from app.services.model_registry import load_model, load_model_meta

logger = logging.getLogger(__name__)


def get_health() -> dict[str, Any]:
    """Get comprehensive health status including model metadata.
    
    Returns:
        Dictionary with status, model metadata, and version info.
        Returns 'degraded' status if model cannot be loaded.
    """
    try:
        model = load_model()
        meta = load_model_meta()
        model_loaded = True
        model_name = meta.get("best_model")
        trained_at = meta.get("trained_at")
        accuracy = meta.get("metrics", {}).get(model_name, {}).get("accuracy")
    except RuntimeError as exc:
        logger.warning(f"Model not available: {exc}")
        model_loaded = False
        model_name = None
        trained_at = None
        accuracy = None

    return {
        "status": "ok" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "model_name": model_name,
        "trained_at": trained_at,
        "accuracy": accuracy,
        "version": "0.1.0",
    }
