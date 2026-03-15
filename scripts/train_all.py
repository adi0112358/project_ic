from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data" / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=8000)
    parser.add_argument("--images", type=int, default=8000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--tabular-only", action="store_true")
    parser.add_argument("--image-only", action="store_true")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = DATA_DIR / f"synthetic_labs_{args.rows}.csv"
    image_root = DATA_DIR / "images_synthetic"

    if not args.image_only:
        if args.force or not csv_path.exists():
            run([
                sys.executable,
                str(SCRIPTS / "generate_synthetic_dataset.py"),
                "--rows",
                str(args.rows),
                "--out",
                str(csv_path),
                "--seed",
                str(args.seed),
            ])

        run([
            sys.executable,
            str(SCRIPTS / "train_tabular.py"),
            "--csv",
            str(csv_path),
            "--target",
            "fungal_infection",
            "--out",
            str(ARTIFACTS_DIR / "model_fungal_infection.joblib"),
        ])

        run([
            sys.executable,
            str(SCRIPTS / "train_tabular.py"),
            "--csv",
            str(csv_path),
            "--target",
            "diabetes_status",
            "--out",
            str(ARTIFACTS_DIR / "model_diabetes_status.joblib"),
        ])

        run([
            sys.executable,
            str(SCRIPTS / "train_tabular.py"),
            "--csv",
            str(csv_path),
            "--target",
            "severity",
            "--out",
            str(ARTIFACTS_DIR / "model_severity.joblib"),
        ])

        run([
            sys.executable,
            str(SCRIPTS / "train_tabular.py"),
            "--csv",
            str(csv_path),
            "--target",
            "fungal_type",
            "--out",
            str(ARTIFACTS_DIR / "model_fungal_type.joblib"),
        ])

    if not args.tabular_only:
        if args.force or not (image_root / "train").exists():
            run([
                sys.executable,
                str(SCRIPTS / "generate_synthetic_images.py"),
                "--out-root",
                str(image_root),
                "--total",
                str(args.images),
                "--size",
                "128",
                "--seed",
                str(args.seed),
            ])

        run([
            sys.executable,
            str(SCRIPTS / "train_image_baseline.py"),
            "--data-root",
            str(image_root),
            "--split",
            "train",
            "--out",
            str(ARTIFACTS_DIR / "model_image_baseline.joblib"),
        ])


if __name__ == "__main__":
    main()
