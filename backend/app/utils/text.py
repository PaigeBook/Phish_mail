import re

_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Normalize and clean email text for analysis.
    
    Args:
        text: Raw email text
        
    Returns:
        Lowercased, stripped, and normalized whitespace text
    """
    lowered = text.lower().strip()
    return _WHITESPACE_RE.sub(" ", lowered)
