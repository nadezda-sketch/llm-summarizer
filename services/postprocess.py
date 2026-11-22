import re

def clean(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"^```.*?```$", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_valid(text: str) -> bool:
    return bool(text) and len(text) >= 20