from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

import joblib
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler

from ic.dataset import load_tabular_dataset


def build_model() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )


def evaluate_binary(y_true, y_pred, y_proba) -> dict:
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
    }
    try:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba))
    except Exception:
        metrics["roc_auc"] = None
    return metrics


def evaluate_multiclass(y_true, y_pred) -> dict:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--target", default="fungal_infection")
    parser.add_argument("--out", default="/Users/phoenix/Desktop/project_ic/artifacts/model_fungal_infection.joblib")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    dataset = load_tabular_dataset(args.csv, args.target)

    X = dataset.features
    y = dataset.target

    # Drop rows with missing labels
    mask = ~y.isna()
    X = X.loc[mask]
    y = y.loc[mask]

    if len(y) < 5:
        raise ValueError("Not enough labeled rows to train.")

    is_binary = args.target == "fungal_infection"

    label_encoder = None
    if not is_binary:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y if len(set(y)) > 1 else None,
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    if is_binary:
        y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        metrics = evaluate_binary(y_test, y_pred, y_proba)
    else:
        metrics = evaluate_multiclass(y_test, y_pred)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "feature_columns": dataset.feature_columns,
        "target": args.target,
        "classes": list(label_encoder.classes_) if label_encoder else None,
    }

    joblib.dump(artifact, out_path)

    metrics_path = out_path.with_suffix(".metrics.json")
    with metrics_path.open("w") as f:
        json.dump(metrics, f, indent=2)

    print("Saved model to", out_path)
    print("Metrics", metrics)


if __name__ == "__main__":
    main()
