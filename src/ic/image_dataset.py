from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class ImageSample:
    path: str
    label: str


def load_image_samples(root: str) -> List[ImageSample]:
    root_path = Path(root)
    samples: List[ImageSample] = []

    for label_dir in sorted(root_path.iterdir()):
        if not label_dir.is_dir():
            continue
        label = label_dir.name
        for img_path in label_dir.glob("*.png"):
            samples.append(ImageSample(path=str(img_path), label=label))

    return samples
