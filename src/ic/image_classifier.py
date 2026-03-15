from __future__ import annotations

from typing import Optional, Dict, Any


def _hint_from_filename(filename: Optional[str]) -> str:
    if not filename:
        return "unknown"
    t = filename.lower()
    if "candida" in t or "thrush" in t:
        return "candida"
    if "tinea" in t or "ringworm" in t or "dermatophyte" in t:
        return "dermatophyte"
    if "aspergillus" in t:
        return "aspergillus"
    return "unknown"


def assess_image_quality(image_bytes: Optional[bytes]) -> float:
    if not image_bytes:
        return 0.0
    size_kb = len(image_bytes) / 1024.0
    if size_kb < 50:
        return 0.3
    if size_kb < 200:
        return 0.6
    return 0.8


def classify_image(image_bytes: Optional[bytes], filename: Optional[str] = None) -> Dict[str, Any]:
    # Placeholder: swap with a real CNN/ViT model
    return {
        "image_quality_score": assess_image_quality(image_bytes),
        "image_type_hint": _hint_from_filename(filename),
    }
