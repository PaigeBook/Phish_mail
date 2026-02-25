from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    body: str = Field(..., min_length=1, description="Raw email body")
    headers: Optional[str] = Field(None, description="Optional raw headers")

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Email body must not be empty")
        return value


class FeatureContribution(BaseModel):
    feature: str
    contribution: float


class Explanation(BaseModel):
    reasons: List[str]
    top_features: List[FeatureContribution]
    suspicious_terms: List[str]
    stats: dict[str, Any]


class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
    explanation: Explanation
