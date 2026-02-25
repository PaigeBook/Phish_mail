import re
from collections.abc import Iterable

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from app.utils.keywords import SUSPICIOUS_KEYWORDS
from app.utils.text import clean_text

# Compile regex patterns at module level for efficiency
_URL_RE = re.compile(r"(https?://|www\.)", re.IGNORECASE)
_IP_URL_RE = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}")
_SPECIAL_RE = re.compile(r"[^A-Za-z0-9\s]")
_HEADER_RE = re.compile(r"(reply-to:|return-path:)", re.IGNORECASE)


class EngineeredFeatures(BaseEstimator, TransformerMixin):
    """Extract engineered features from email text for phishing detection.

    Computes 6 features per email:
    - keyword_freq: Ratio of suspicious keywords to words
    - url_count: Number of URLs found
    - ip_url_count: Number of IP-based URLs
    - email_length: Character count
    - special_char_count: Non-alphanumeric character count
    - header_anomaly: Binary indicator for suspicious email patterns
    """

    def __init__(self) -> None:
        """Initialize transformer with pre-compiled regex patterns."""

    def fit(
        self, X: Iterable[str], y: Iterable[int] | None = None
    ) -> "EngineeredFeatures":
        return self

    def transform(self, X: Iterable[str]) -> np.ndarray:
        """Transform raw email text into engineered feature vectors.

        Args:
            X: Iterable of raw email text strings

        Returns:
            NumPy array of shape (n_samples, 6) with computed features
        """
        rows = []
        for raw in X:
            text = clean_text(raw)
            word_count = max(1, len(text.split()))
            keyword_hits = sum(1 for k in SUSPICIOUS_KEYWORDS if k in text)
            url_count = len(_URL_RE.findall(text))
            ip_url_count = len(_IP_URL_RE.findall(text))
            special_count = len(_SPECIAL_RE.findall(text))
            header_anomaly = 1 if _HEADER_RE.search(text) else 0

            rows.append(
                [
                    keyword_hits / word_count,
                    url_count,
                    ip_url_count,
                    len(text),
                    special_count,
                    header_anomaly,
                ]
            )
        return np.asarray(rows, dtype=float)

    def get_feature_names_out(self) -> list[str]:
        return [
            "keyword_freq",
            "url_count",
            "ip_url_count",
            "email_length",
            "special_char_count",
            "header_anomaly",
        ]
