import logging
import uuid
from typing import Any

from app.services.inference import predict_email

logger = logging.getLogger(__name__)


def batch_predict(emails: list[dict]) -> tuple[list[dict], str]:
    """Process multiple emails with graceful error handling per email.
    
    Args:
        emails: List of dicts with 'body' and optional 'headers' keys
        
    Returns:
        Tuple of (predictions list, batch_id str)
    """
    batch_id = str(uuid.uuid4())
    predictions = []

    for email in emails:
        try:
            result = predict_email(email.get("body", ""), email.get("headers"))
            predictions.append(
                {
                    "body_preview": email.get("body", "")[:50],
                    **result,
                    "status": "success",
                }
            )
        except RuntimeError as exc:
            logger.exception("Model error during batch prediction")
            predictions.append(
                {
                    "body_preview": email.get("body", "")[:50],
                    "status": "error",
                    "error": str(exc),
                }
            )
        except ValueError as exc:
            logger.exception("Invalid input during batch prediction")
            predictions.append(
                {
                    "body_preview": email.get("body", "")[:50],
                    "status": "error",
                    "error": str(exc),
                }
            )
        except Exception as exc:
            logger.exception("Unexpected error during batch prediction")
            predictions.append(
                {
                    "body_preview": email.get("body", "")[:50],
                    "status": "error",
                    "error": "Prediction failed",
                }
            )

    return predictions, batch_id
