from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Optional, Dict, Any

import joblib

from .fusion import (
    infer_diabetes_status,
    score_fungal_risk,
    bucket_risk,
    infer_type_from_text,
    infer_severity,
    build_explanations,
)
from .report_parser import extract_labs_from_text
from .model_io import load_model, predict_with_model
from .image_features import extract_features, FeatureConfig
from .types import LabValues


@dataclass
class ModelPaths:
    tabular_risk: Optional[str] = None
    diabetes_status: Optional[str] = None
    severity: Optional[str] = None
    fungal_type: Optional[str] = None
    image_type: Optional[str] = None


def _predict_image_type(model_path: str, image_path: str) -> str:
    artifact = joblib.load(model_path)
    model = artifact["model"]
    config: FeatureConfig = artifact["feature_config"]
    feats = extract_features(image_path, config).reshape(1, -1)
    return str(model.predict(feats)[0])


def _predict_tabular_label(model_path: str, labs: LabValues) -> Dict[str, Any]:
    artifact = load_model(model_path)
    return predict_with_model(artifact, labs)


def fuse_from_text_and_image(
    report_text: str,
    image_path: Optional[str] = None,
    model_paths: Optional[ModelPaths] = None,
) -> Dict[str, Any]:
    model_paths = model_paths or ModelPaths()

    labs = extract_labs_from_text(report_text or "")

    diabetes_status = infer_diabetes_status(labs)
    if model_paths.diabetes_status:
        pred = _predict_tabular_label(model_paths.diabetes_status, labs)
        diabetes_status = str(pred.get("prediction", diabetes_status))

    risk_score = None
    if model_paths.tabular_risk:
        pred = _predict_tabular_label(model_paths.tabular_risk, labs)
        probabilities = pred.get("probabilities")
        if probabilities and len(probabilities[0]) >= 2:
            risk_score = float(probabilities[0][1])
        else:
            risk_score = 1.0 if str(pred.get("prediction")) in {"1", "yes", "true"} else 0.0

    if risk_score is None:
        risk_score = score_fungal_risk(labs, diabetes_status)

    fungal_risk = bucket_risk(risk_score)

    fungal_type = infer_type_from_text(report_text or "")

    # Prefer image-based type
    if fungal_type == "unknown" and model_paths.image_type and image_path:
        fungal_type = _predict_image_type(model_paths.image_type, image_path)

    # Fallback to tabular fungal_type model if provided
    if fungal_type == "unknown" and model_paths.fungal_type:
        pred = _predict_tabular_label(model_paths.fungal_type, labs)
        fungal_type = str(pred.get("prediction", fungal_type))

    severity = infer_severity(labs, risk_score)
    if model_paths.severity:
        pred = _predict_tabular_label(model_paths.severity, labs)
        severity = str(pred.get("prediction", severity))

    explanations = build_explanations(labs, diabetes_status, risk_score)

    return {
        "diabetes_status": diabetes_status,
        "fungal_risk": fungal_risk,
        "fungal_risk_score": risk_score,
        "fungal_type": fungal_type,
        "severity": severity,
        "explanations": explanations,
        "labs": labs.to_dict(),
    }


def fuse_from_payload(
    report_text: str,
    image_base64: Optional[str],
    image_name: Optional[str],
    model_paths: ModelPaths,
    temp_dir: str,
) -> Dict[str, Any]:
    image_path = None
    if image_base64:
        raw = base64.b64decode(image_base64)
        suffix = "png"
        if image_name and "." in image_name:
            suffix = image_name.rsplit(".", 1)[-1]
        image_path = f"{temp_dir}/ic_upload.{suffix}"
        with open(image_path, "wb") as f:
            f.write(raw)

    result = fuse_from_text_and_image(
        report_text=report_text,
        image_path=image_path,
        model_paths=model_paths,
    )

    return result
