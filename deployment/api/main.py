from __future__ import annotations

import os
import tempfile
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ic.fusion_inference import ModelPaths, fuse_from_payload

app = FastAPI(title="Project IC Inference API", version="0.1.0")


class AnalyzeRequest(BaseModel):
    report_text: str
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class AnalyzeResponse(BaseModel):
    result: dict
    warnings: List[str]


def _path_if_exists(path: Optional[str]) -> Optional[str]:
    if path and os.path.exists(path):
        return path
    return None


def _load_model_paths() -> tuple[ModelPaths, List[str]]:
    warnings: List[str] = []

    tabular = _path_if_exists(os.getenv("TABULAR_MODEL_PATH"))
    image = _path_if_exists(os.getenv("IMAGE_MODEL_PATH"))
    diabetes = _path_if_exists(os.getenv("DIABETES_MODEL_PATH"))
    severity = _path_if_exists(os.getenv("SEVERITY_MODEL_PATH"))
    fungal_type = _path_if_exists(os.getenv("TYPE_MODEL_PATH"))

    if not tabular:
        warnings.append("Tabular model not found; risk score will be rule-based.")
    if not image:
        warnings.append("Image model not found; fungal type may be unknown.")
    if not diabetes:
        warnings.append("Diabetes model not found; diabetes status will be rule-based.")
    if not severity:
        warnings.append("Severity model not found; severity will be rule-based.")
    if not fungal_type:
        warnings.append("Fungal type model not found; type may rely on text or image only.")

    return (
        ModelPaths(
            tabular_risk=tabular,
            image_type=image,
            diabetes_status=diabetes,
            severity=severity,
            fungal_type=fungal_type,
        ),
        warnings,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    if not payload.report_text:
        raise HTTPException(status_code=400, detail="report_text is required")

    model_paths, warnings = _load_model_paths()

    with tempfile.TemporaryDirectory() as tmp:
        result = fuse_from_payload(
            report_text=payload.report_text,
            image_base64=payload.image_base64,
            image_name=payload.image_name,
            model_paths=model_paths,
            temp_dir=tmp,
        )

    return AnalyzeResponse(result=result, warnings=warnings)
