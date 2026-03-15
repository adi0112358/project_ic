from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from ic.model_io import load_model, predict_with_model
from ic.report_parser import extract_labs_from_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    with open(args.report, "r", encoding="utf-8") as f:
        text = f.read()

    labs = extract_labs_from_text(text)
    artifact = load_model(args.model)
    result = predict_with_model(artifact, labs)

    print(result)


if __name__ == "__main__":
    main()
