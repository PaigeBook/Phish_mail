SUSPICIOUS_KEYWORDS = [
    "urgent",
    "immediately",
    "verify",
    "password",
    "account",
    "suspend",
    "click",
    "login",
    "confirm",
    "security",
    "update",
    "invoice",
    "payment",
    "wire",
    "bank",
    "gift card",
    "reset",
    "limited time",
    "action required",
    "credentials",
    "unauthorized",
    "compromised"
]


def find_suspicious_terms(text: str) -> list[str]:
    lowered = text.lower()
    hits = [term for term in SUSPICIOUS_KEYWORDS if term in lowered]
    return sorted(set(hits))
