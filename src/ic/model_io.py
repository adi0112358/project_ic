from __future__ import annotations

from typing import Dict, Any, List

import joblib
import pandas as pd

from .types import LabValues
from .dataset import FEATURE_COLUMNS


def load_model(path: str) -> Dict[str, Any]:
    return joblib.load(path)


def labs_to_frame(labs: LabValues) -> pd.DataFrame:
    data = {key: getattr(labs, key) for key in FEATURE_COLUMNS}
    return pd.DataFrame([data])


def predict_with_model(model_artifact: Dict[str, Any], labs: LabValues) -> Dict[str, Any]:
    model = model_artifact["model"]
    X = labs_to_frame(labs)
    pred = model.predict(X)
    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)

    classes = model_artifact.get("classes")
    if classes is not None and len(pred) > 0:
        label = classes[int(pred[0])]
    else:
        label = pred[0]

    return {
        "prediction": label,
        "probabilities": proba.tolist() if proba is not None else None,
    }
