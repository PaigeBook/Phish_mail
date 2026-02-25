from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response with model metadata."""
    status: Literal["ok", "degraded"]
    model_loaded: bool
    model_name: str | None
    trained_at: str | None
    accuracy: float | None
    version: str


class BatchPredictRequest(BaseModel):
    """Request model for batch email predictions."""
    emails: list[dict[str, str | None]]


class BatchPredictResponse(BaseModel):
    """Response model for batch predictions."""
    predictions: list[dict]
    batch_id: str
    processed_count: int
