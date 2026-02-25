import re
from typing import Iterable

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from app.utils.keywords import SUSPICIOUS_KEYWORDS
from app.utils.text import clean_text


class EngineeredFeatures(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        self._url_re = re.compile(r"(https?://|www\.)", re.IGNORECASE)
        self._ip_url_re = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}")
        self._special_re = re.compile(r"[^A-Za-z0-9\s]")
        self._header_re = re.compile(r"(reply-to:|return-path:)", re.IGNORECASE)

    def fit(self, X: Iterable[str], y: Iterable[int] | None = None) -> "EngineeredFeatures":
        return self

    def transform(self, X: Iterable[str]) -> np.ndarray:
        rows = []
        for raw in X:
            text = clean_text(raw)
            word_count = max(1, len(text.split()))
            keyword_hits = sum(1 for k in SUSPICIOUS_KEYWORDS if k in text)
            url_count = len(self._url_re.findall(text))
            ip_url_count = len(self._ip_url_re.findall(text))
            special_count = len(self._special_re.findall(text))
            header_anomaly = 1 if self._header_re.search(text) else 0

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
