from __future__ import annotations

from typing import Optional

from .types import AnalysisResult
from .report_parser import extract_labs_from_text
from .image_classifier import classify_image
from .fusion import (
    infer_diabetes_status,
    score_fungal_risk,
    bucket_risk,
    infer_type_from_text,
    infer_severity,
    build_explanations,
)


def analyze(report_text: str, image_bytes: Optional[bytes] = None, image_filename: Optional[str] = None) -> AnalysisResult:
    labs = extract_labs_from_text(report_text or "")
    diabetes_status = infer_diabetes_status(labs)

    risk_score = score_fungal_risk(labs, diabetes_status)
    risk_bucket = bucket_risk(risk_score)

    type_from_text = infer_type_from_text(report_text or "")
    image_info = classify_image(image_bytes, image_filename)
    type_from_image = image_info.get("image_type_hint", "unknown")
    fungal_type = type_from_text if type_from_text != "unknown" else type_from_image

    severity = infer_severity(labs, risk_score)
    explanations = build_explanations(labs, diabetes_status, risk_score)

    return AnalysisResult(
        diabetes_status=diabetes_status,
        fungal_risk=risk_bucket,
        fungal_risk_score=risk_score,
        fungal_type=fungal_type,
        severity=severity,
        explanations=explanations,
        labs=labs,
    )
