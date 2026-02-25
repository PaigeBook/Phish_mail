import logging

from fastapi import APIRouter, HTTPException

from app.schemas.predict import PredictRequest, PredictResponse
from app.services.inference import predict_email

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    try:
        result = predict_email(payload.body, payload.headers)
        return PredictResponse(**result)
    except RuntimeError as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unhandled prediction error")
        raise HTTPException(status_code=500, detail="Prediction error") from exc
