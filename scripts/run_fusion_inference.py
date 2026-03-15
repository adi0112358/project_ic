from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from ic.fusion_inference import fuse_from_text_and_image, ModelPaths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--image", required=False)
    parser.add_argument("--tabular-model", required=False)
    parser.add_argument("--image-model", required=False)
    parser.add_argument("--diabetes-model", required=False)
    parser.add_argument("--severity-model", required=False)
    parser.add_argument("--type-model", required=False)
    args = parser.parse_args()

    with open(args.report, "r", encoding="utf-8") as f:
        text = f.read()

    model_paths = ModelPaths(
        tabular_risk=args.tabular_model,
        image_type=args.image_model,
        diabetes_status=args.diabetes_model,
        severity=args.severity_model,
        fungal_type=args.type_model,
    )

    output = fuse_from_text_and_image(
        report_text=text,
        image_path=args.image,
        model_paths=model_paths,
    )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
