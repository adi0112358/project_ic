from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw


def clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(val, hi))


def draw_candida(draw: ImageDraw.ImageDraw, w: int, h: int) -> None:
    for _ in range(random.randint(12, 30)):
        r = random.randint(3, 10)
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(245, 240, 240), outline=(230, 210, 210))


def draw_dermatophyte(draw: ImageDraw.ImageDraw, w: int, h: int) -> None:
    cx, cy = w // 2, h // 2
    r_outer = random.randint(25, 45)
    r_inner = r_outer - random.randint(6, 12)
    draw.ellipse((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer), outline=(165, 35, 45), width=5)
    draw.ellipse((cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner), outline=(215, 140, 140), width=3)


def draw_aspergillus(draw: ImageDraw.ImageDraw, w: int, h: int) -> None:
    for _ in range(random.randint(6, 14)):
        r = random.randint(8, 18)
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(60, 120, 80), outline=(35, 80, 50))


def draw_other(draw: ImageDraw.ImageDraw, w: int, h: int) -> None:
    for _ in range(random.randint(8, 18)):
        r = random.randint(5, 14)
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        draw.rectangle((x - r, y - r, x + r, y + r), fill=(120, 70, 140), outline=(90, 40, 110))


def generate_image(label: str, size: int) -> Image.Image:
    base = (220, 170, 160) if label in {"candida", "dermatophyte"} else (205, 165, 150)
    img = Image.new("RGB", (size, size), base)
    draw = ImageDraw.Draw(img)

    if label == "candida":
        draw_candida(draw, size, size)
    elif label == "dermatophyte":
        draw_dermatophyte(draw, size, size)
    elif label == "aspergillus":
        draw_aspergillus(draw, size, size)
    else:
        draw_other(draw, size, size)

    return img


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", required=True)
    parser.add_argument("--total", type=int, default=8000)
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    labels = ["candida", "dermatophyte", "aspergillus", "other"]
    per_class = math.ceil(args.total / len(labels))

    split_counts = {
        "train": int(per_class * 0.7),
        "val": int(per_class * 0.15),
        "test": per_class - int(per_class * 0.7) - int(per_class * 0.15),
    }

    root = Path(args.out_root)

    for split, count in split_counts.items():
        for label in labels:
            out_dir = root / split / label
            out_dir.mkdir(parents=True, exist_ok=True)
            for i in range(count):
                img = generate_image(label, args.size)
                img.save(out_dir / f"{label}_{i:05d}.png")


if __name__ == "__main__":
    main()
