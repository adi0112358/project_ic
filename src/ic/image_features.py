from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, List

import numpy as np
from PIL import Image, ImageFilter


@dataclass
class FeatureConfig:
    image_size: Tuple[int, int] = (128, 128)
    hist_bins: int = 8


def extract_features(image_path: str, config: FeatureConfig) -> np.ndarray:
    img = Image.open(image_path).convert("RGB").resize(config.image_size)

    # Color histograms
    arr = np.asarray(img) / 255.0
    feats: List[float] = []

    for c in range(3):
        channel = arr[:, :, c].flatten()
        hist, _ = np.histogram(channel, bins=config.hist_bins, range=(0.0, 1.0), density=True)
        feats.extend(hist.tolist())
        feats.append(float(channel.mean()))
        feats.append(float(channel.std()))

    # Edge density
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES)
    edges_arr = np.asarray(edges) / 255.0
    feats.append(float(edges_arr.mean()))
    feats.append(float(edges_arr.std()))

    return np.asarray(feats, dtype=np.float32)
