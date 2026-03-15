from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

import joblib
import numpy as np

from ic.image_features import extract_features, FeatureConfig


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--image", required=True)
    args = parser.parse_args()

    artifact = joblib.load(args.model)
    model = artifact["model"]
    config: FeatureConfig = artifact["feature_config"]

    feats = extract_features(args.image, config).reshape(1, -1)
    pred = model.predict(feats)[0]
    proba = model.predict_proba(feats)[0] if hasattr(model, "predict_proba") else None

    print({"prediction": pred, "probabilities": proba.tolist() if proba is not None else None})


if __name__ == "__main__":
    main()
