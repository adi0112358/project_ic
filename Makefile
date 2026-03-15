VENV := .venv
PY := $(VENV)/bin/python

.PHONY: venv install data images train-tabular train-image train-all infer

venv:
	python3 -m venv $(VENV)

install: venv
	$(PY) -m pip install -e .

data:
	$(PY) scripts/generate_synthetic_dataset.py --rows 8000 --out data/processed/synthetic_labs_8000.csv --seed 42

images:
	$(PY) scripts/generate_synthetic_images.py --out-root data/processed/images_synthetic --total 8000 --size 128 --seed 42

train-tabular: data
	$(PY) scripts/train_tabular.py --csv data/processed/synthetic_labs_8000.csv --target fungal_infection --out artifacts/model_fungal_infection.joblib
	$(PY) scripts/train_tabular.py --csv data/processed/synthetic_labs_8000.csv --target diabetes_status --out artifacts/model_diabetes_status.joblib
	$(PY) scripts/train_tabular.py --csv data/processed/synthetic_labs_8000.csv --target severity --out artifacts/model_severity.joblib
	$(PY) scripts/train_tabular.py --csv data/processed/synthetic_labs_8000.csv --target fungal_type --out artifacts/model_fungal_type.joblib

train-image: images
	$(PY) scripts/train_image_baseline.py --data-root data/processed/images_synthetic --split train --out artifacts/model_image_baseline.joblib

train-all: train-tabular train-image

infer:
	$(PY) scripts/run_fusion_inference.py --report /tmp/ic_sample_report.txt --tabular-model artifacts/model_fungal_infection.joblib
