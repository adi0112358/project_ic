from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from ic.image_dataset import load_image_samples
from ic.image_features import FeatureConfig, extract_features


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--split", default="train")
    parser.add_argument("--out", required=True)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    split_root = Path(args.data_root) / args.split
    samples = load_image_samples(str(split_root))

    if not samples:
        raise ValueError(f"No samples found in {split_root}")

    config = FeatureConfig()

    X: List[np.ndarray] = []
    y: List[str] = []

    for sample in samples:
        feats = extract_features(sample.path, config)
        X.append(feats)
        y.append(sample.label)

    X_arr = np.stack(X, axis=0)

    X_train, X_test, y_train, y_test = train_test_split(
        X_arr,
        y,
        test_size=0.2,
        random_state=args.random_state,
        stratify=y,
    )

    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": clf,
        "labels": sorted(set(y)),
        "feature_config": config,
    }

    joblib.dump(artifact, out_path)

    metrics_path = out_path.with_suffix(".metrics.json")
    with metrics_path.open("w") as f:
        json.dump(metrics, f, indent=2)

    print("Saved model to", out_path)
    print("Metrics", metrics)


if __name__ == "__main__":
    main()
