import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

from app.utils.settings import get_settings


@lru_cache(maxsize=1)
def load_model() -> Any:
    settings = get_settings()
    model_path = Path(settings.model_path)
    if not model_path.exists():
        raise RuntimeError(
            "Model not found. Train a model using backend/scripts/train.py"
        )
    return joblib.load(model_path)


@lru_cache(maxsize=1)
def load_model_meta() -> dict[str, Any]:
    settings = get_settings()
    meta_path = Path(settings.model_meta_path)
    if not meta_path.exists():
        return {}
    return json.loads(meta_path.read_text(encoding="utf-8"))
