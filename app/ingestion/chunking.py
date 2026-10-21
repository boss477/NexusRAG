import re


def chunk_text(text: str, *, max_chars: int = 1200, overlap: int = 120) -> list[str]:
    """Split text on paragraph/sentence boundaries with a bounded character overlap."""
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap must be non-negative and smaller than max_chars")

    units = _units(text)
    chunks: list[str] = []
    current = ""
    for unit in units:
        if not current:
            current = unit
            continue
        candidate = f"{current} {unit}"
        if len(candidate) <= max_chars:
            current = candidate
            continue
        chunks.append(current.strip())
        prefix = current[-overlap:].strip() if overlap else ""
        current = f"{prefix} {unit}".strip()
        if len(current) > max_chars:
            chunks.extend(_hard_split(current, max_chars))
            current = ""
    if current.strip():
        chunks.append(current.strip())
    return chunks


def _units(text: str) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n+", text) if part.strip()]
    units: list[str] = []
    for paragraph in paragraphs or [text.strip()]:
        units.extend(part.strip() for part in re.split(r"(?<=[.!?])\s+", paragraph) if part.strip())
    return units


def _hard_split(text: str, max_chars: int) -> list[str]:
    return [text[start : start + max_chars].strip() for start in range(0, len(text), max_chars) if text[start : start + max_chars].strip()]

