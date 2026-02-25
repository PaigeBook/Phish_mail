import re


_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    lowered = text.lower().strip()
    return _WHITESPACE_RE.sub(" ", lowered)
