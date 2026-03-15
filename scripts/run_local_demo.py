from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from ic import analyze, build_chat_summary


SAMPLE_REPORT = """
Patient Age: 54 years
BMI: 29.4
HbA1c: 8.1%
FPG: 162 mg/dL
OGTT 2 hr: 210 mg/dL
CRP: 14.2 mg/L
Neutrophils: 6.1
Lymphocytes: 1.8
IL-6: 12
TNF-alpha: 9
Urine albumin: 45 mg/g
"""


def main() -> None:
    result = analyze(SAMPLE_REPORT, image_bytes=None, image_filename="tinea_sample.jpg")
    print("Analysis Result:\n", result.to_dict())
    print("\nChat Summary:\n")
    print(build_chat_summary(result))


if __name__ == "__main__":
    main()
