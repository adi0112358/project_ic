# Fungal Infection Classifier for Type 2 Diabetes (Project IC)

This project builds an AI-assisted workflow for assessing fungal infection risk in people with type 2 diabetes, using lab reports (OCR + extraction), skin images, and a chat assistant grounded in the user’s own data. It is designed as decision-support for clinicians and patients, not medical advice.

## What’s in the box
- **Report ingestion**: OCR-ready pipeline + structured lab extraction (HbA1c, FPG/OGTT, CRP, NLR, etc.)
- **Image analysis**: skin image ingestion with placeholder classifier hooks
- **Fusion scoring**: combines tabular features + image signals into risk/type/severity
- **Chat assistant**: explains results, flags risk, and suggests next steps
- **Web app**: Next.js app intended for Vercel deployment

## Repo layout
- `web/` Next.js frontend + API routes
- `src/` Python AI core (report parsing, scoring, fusion logic)
- `docs/` specifications and data schema
- `scripts/` local demos and utilities

## Quickstart (web)
```bash
cd web
npm install
npm run dev
```

## Quickstart (python demo)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python scripts/run_local_demo.py
```

## Training a baseline model
```bash
python /Users/phoenix/Desktop/project_ic/scripts/train_tabular.py \
  --csv /path/to/your/labs.csv \
  --target fungal_infection \
  --out /Users/phoenix/Desktop/project_ic/artifacts/model_fungal_infection.joblib
```

See `docs/training.md` and `docs/sample_labs.csv` for expected columns.

## Image baseline (synthetic)
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/generate_synthetic_images.py \
  --out-root /Users/phoenix/Desktop/project_ic/data/processed/images_synthetic \
  --total 8000

.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/train_image_baseline.py \
  --data-root /Users/phoenix/Desktop/project_ic/data/processed/images_synthetic \
  --split train \
  --out /Users/phoenix/Desktop/project_ic/artifacts/model_image_baseline.joblib
```

See `docs/image_pipeline.md` for details.

## One-command training (tabular + image)
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/train_all.py --rows 8000 --images 8000
```

## Fusion inference (tabular + image)
```bash
.venv/bin/python /Users/phoenix/Desktop/project_ic/scripts/run_fusion_inference.py \
  --report /tmp/ic_sample_report.txt \
  --image /Users/phoenix/Desktop/project_ic/data/processed/images_synthetic/test/candida/candida_00001.png \
  --tabular-model /Users/phoenix/Desktop/project_ic/artifacts/model_fungal_infection.joblib \
  --diabetes-model /Users/phoenix/Desktop/project_ic/artifacts/model_diabetes_status.joblib \
  --severity-model /Users/phoenix/Desktop/project_ic/artifacts/model_severity.joblib \
  --type-model /Users/phoenix/Desktop/project_ic/artifacts/model_fungal_type.joblib \
  --image-model /Users/phoenix/Desktop/project_ic/artifacts/model_image_baseline.joblib
```

## Deployment notes (Vercel)
- Set Vercel **Root Directory** to `web/`.
- For production inference, connect `web/` API routes to a dedicated model API (FastAPI or similar).

## Web app inference (local)
To make the web app use the trained Python models locally, set:
```bash
INFERENCE_MODE=python
PYTHON_BIN=/Users/phoenix/Desktop/project_ic/.venv/bin/python
TABULAR_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_fungal_infection.joblib
IMAGE_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_image_baseline.joblib
DIABETES_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_diabetes_status.joblib
SEVERITY_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_severity.joblib
TYPE_MODEL_PATH=/Users/phoenix/Desktop/project_ic/artifacts/model_fungal_type.joblib
```
See `web/.env.example`.

## Inference API (for Vercel)
Run the FastAPI service and point `INFERENCE_API_URL` to it:
```bash
.venv/bin/python -m uvicorn deployment.api.main:app --host 0.0.0.0 --port 8000
```
Then set in `web/.env.local`:
```
INFERENCE_API_URL=http://localhost:8000
```

## LLM chat (free tier hosted)
This project can use a hosted LLM for chat. For OpenAI, set:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=YOUR_KEY
OPENAI_MODEL=gpt-4o-mini
```

The OpenAI API uses Bearer token auth and the Responses endpoint at `https://api.openai.com/v1/responses`. citeturn2view0turn4view0

For Gemini, set:
```
LLM_PROVIDER=gemini
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-1.5-flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```
Gemini uses the `generateContent` endpoint on the Generative Language API. citeturn0search0turn0search2turn0search3

Alternatively, use the **OpenRouter** free tier for chat. Create an API key and set:
```
OPENROUTER_API_KEY=YOUR_KEY
OPENROUTER_MODEL=openrouter/free
```
This keeps the UI free and uses OpenRouter’s hosted models with rate limits. citeturn6search0turn0search5

## Safety and scope
This project **does not provide medical advice**. Predictions are for research/triage only and must be validated by a qualified clinician.

See `docs/model_card.md` for limitations and ethical notes.

## Next steps
See `docs/spec.md` and `docs/data_schema.md` for the current design and integration points.
