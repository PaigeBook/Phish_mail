import logging

from fastapi import APIRouter, HTTPException

from app.schemas.health import BatchPredictRequest, BatchPredictResponse, HealthResponse
from app.schemas.predict import PredictRequest, PredictResponse
from app.services.batch import batch_predict
from app.services.health import get_health
from app.services.inference import predict_email

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check with model metadata."""
    status = get_health()
    return HealthResponse(**status)


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    """Predict phishing for a single email."""
    try:
        result = predict_email(payload.body, payload.headers)
        return PredictResponse(**result)
    except RuntimeError as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unhandled prediction error")
        raise HTTPException(status_code=500, detail="Prediction error") from exc


@router.post("/predict-batch", response_model=BatchPredictResponse)
def predict_batch(payload: BatchPredictRequest) -> BatchPredictResponse:
    """Predict phishing for multiple emails."""
    if not payload.emails:
        raise HTTPException(status_code=400, detail="No emails provided")
    if len(payload.emails) > 1000:
        raise HTTPException(status_code=400, detail="Max 1000 emails per batch")

    try:
        predictions, batch_id = batch_predict(payload.emails)
        return BatchPredictResponse(
            predictions=predictions,
            batch_id=batch_id,
            processed_count=len(predictions),
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Batch prediction failed")
        raise HTTPException(status_code=500, detail="Batch prediction error") from exc
