import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    \"\"\"Application configuration from environment variables.\"\"\"
    model_path: str
    model_meta_path: str
    log_level: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    \"\"\"Load and cache application settings from environment.\"\"\"
    return Settings(
        model_path=os.getenv("BACKEND_MODEL_PATH", "backend/models/phish_model.joblib"),
        model_meta_path=os.getenv(
            "BACKEND_MODEL_META_PATH", "backend/models/model_meta.json"
        ),
        log_level=os.getenv("BACKEND_LOG_LEVEL", "INFO"),
    )
