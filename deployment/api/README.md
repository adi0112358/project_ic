# Project IC Inference API

## Run locally
```bash
cd /Users/phoenix/Desktop/project_ic
.venv/bin/python -m pip install -e .
.venv/bin/python -m uvicorn deployment.api.main:app --host 0.0.0.0 --port 8000
```

## Environment variables
Set model artifact paths:
- `TABULAR_MODEL_PATH` (fungal_infection model)
- `IMAGE_MODEL_PATH` (image type model)
- `DIABETES_MODEL_PATH`
- `SEVERITY_MODEL_PATH`
- `TYPE_MODEL_PATH`

Example:
```bash
export TABULAR_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_fungal_infection.joblib
export IMAGE_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_image_baseline.joblib
export DIABETES_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_diabetes_status.joblib
export SEVERITY_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_severity.joblib
export TYPE_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_fungal_type.joblib
```

## API
- `GET /health`
- `POST /analyze`

Payload:
```json
{
  "report_text": "HbA1c 8.2% ...",
  "image_base64": "<base64>",
  "image_name": "image.png"
}
```
