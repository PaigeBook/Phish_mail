from typing import Any

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    """Request model for single email prediction."""

    body: str = Field(..., min_length=1, description="Raw email body")
    headers: str | None = Field(None, description="Optional raw email headers")

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, value: str) -> str:
        """Ensure email body is not blank after stripping whitespace."""
        if not value.strip():
            raise ValueError("Email body must not be empty")
        return value


class FeatureContribution(BaseModel):
    """Model feature contribution for explainability."""

    feature: str
    contribution: float


class Explanation(BaseModel):
    """Prediction explanation with reasons, features, and detected terms."""

    reasons: list[str]
    top_features: list[FeatureContribution]
    suspicious_terms: list[str]
    stats: dict[str, Any]


class PredictResponse(BaseModel):
    """Response model for email prediction."""

    prediction: str
    confidence: float
    risk_level: str
    explanation: Explanation
