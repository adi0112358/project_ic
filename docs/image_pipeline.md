# Image Pipeline (synthetic baseline)

## What this is
A baseline image classification pipeline using **synthetic images** that simulate lesion patterns for fungal types.
This is for demo purposes only and is not medically meaningful.

## Generate synthetic images
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/generate_synthetic_images.py \
  --out-root /Users/phoenix/Desktop/project_ic/data/processed/images_synthetic \
  --total 8000
```

Directory structure created:
- `data/processed/images_synthetic/train/{candida,dermatophyte,aspergillus,other}`
- `data/processed/images_synthetic/val/{...}`
- `data/processed/images_synthetic/test/{...}`

## Train a baseline image model
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/train_image_baseline.py \
  --data-root /Users/phoenix/Desktop/project_ic/data/processed/images_synthetic \
  --split train \
  --out /Users/phoenix/Desktop/project_ic/artifacts/model_image_baseline.joblib
```

## Run inference on one image
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/run_image_inference.py \
  --model /Users/phoenix/Desktop/project_ic/artifacts/model_image_baseline.joblib \
  --image /Users/phoenix/Desktop/project_ic/data/processed/images_synthetic/test/candida/candida_00001.png
```
