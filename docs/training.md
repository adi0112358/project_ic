# Training Guide (v1)

## Expected data format
A CSV file with one row per patient and the columns in `docs/data_schema.md`.
Minimum required features:
- `hba1c_percent`, `fpg_mg_dl`, or `ogtt_2h_mg_dl`
- At least one label column (e.g., `fungal_infection`)

Supported label columns:
- `fungal_infection` (yes/no or 1/0)
- `fungal_type` (candida/dermatophyte/aspergillus/other)
- `severity` (mild/moderate/severe)
- `diabetes_status` (normal/prediabetes/diabetes)

## Training a baseline tabular model
```bash
python /Users/phoenix/Desktop/project_ic/scripts/train_tabular.py \
  --csv /path/to/your/labs.csv \
  --target fungal_infection \
  --out /Users/phoenix/Desktop/project_ic/artifacts/model_fungal_infection.joblib
```

## Notes
- This baseline uses logistic regression over lab values only.
- Image training is not included yet; it will be a separate pipeline.

## One-command training
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/train_all.py --rows 8000 --images 8000
```

This generates the following artifacts:
- `artifacts/model_fungal_infection.joblib`
- `artifacts/model_diabetes_status.joblib`
- `artifacts/model_severity.joblib`
- `artifacts/model_fungal_type.joblib`
- `artifacts/model_image_baseline.joblib`
