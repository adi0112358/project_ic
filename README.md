# Fungal Infection Risk Classifier for Type-2 Diabetes (Project IC)

AI-assisted decision-support system for assessing fungal infection risk in people with Type-2 Diabetes using:

- Clinical lab reports (OCR + structured extraction)
- Skin lesion images
- Multimodal AI fusion
- Context-aware chat assistant

The system combines medical lab biomarkers and dermatological image signals to provide risk estimation and explanatory feedback.

⚠️ This project is for research and decision-support only. It does NOT provide medical diagnosis or treatment advice.

---

# System Overview

The pipeline integrates structured medical data and images.

Lab Report (OCR)
        │
        ▼
Feature Extraction
(HbA1c, CRP, NLR, Glucose)
        │
        ▼
Tabular Risk Model
        │
        │
Skin Image
        │
        ▼
Image Classifier
        │
        ▼
Fusion Engine
(Tabular + Image signals)
        │
        ▼
Risk / Type / Severity Prediction
        │
        ▼
Explainable Chat Assistant

---

# Core Features

## 1. Medical Report Processing

- OCR-ready report ingestion
- Structured extraction of clinical biomarkers

Supported biomarkers include:

- HbA1c
- Fasting Plasma Glucose (FPG)
- Oral Glucose Tolerance Test (OGTT)
- C-Reactive Protein (CRP)
- Neutrophil-Lymphocyte Ratio (NLR)

---

## 2. Dermatological Image Analysis

- Skin lesion ingestion
- Baseline image classifier
- Synthetic dataset generator for early experimentation

---

## 3. Multimodal Fusion Model

Combines:

- tabular medical data
- skin lesion image signals

Outputs:

- fungal infection risk score
- predicted fungal type
- severity level

---

## 4. AI Chat Assistant

Grounded in user data to explain:

- model predictions
- risk interpretation
- suggested follow-up actions

---

## 5. Web Interface

A Next.js web application provides:

- report upload
- image upload
- risk dashboard
- AI assistant interface

---

# Repository Structure

project_ic/

web/  
Next.js frontend and API routes

src/  
Python AI core  
- report parsing  
- feature extraction  
- fusion scoring

scripts/  
training utilities and demos

docs/  
documentation  
- specifications  
- training guide  
- data schema  

artifacts/  
trained models

data/  
processed datasets

---

# Quickstart

## Run the Web App

cd web  
npm install  
npm run dev

Local URL:

http://localhost:3000

---

# Python Environment Setup

python -m venv .venv  
source .venv/bin/activate  
pip install -e .

Run demo pipeline:

python scripts/run_local_demo.py

---

# Training the Tabular Model

Train a baseline classifier using lab reports.

python scripts/train_tabular.py \
--csv /path/to/labs.csv \
--target fungal_infection \
--out artifacts/model_fungal_infection.joblib

Expected schema is provided in:

docs/sample_labs.csv  
docs/training.md

---

# Image Dataset Generation

Generate synthetic training images.

.venv/bin/python scripts/generate_synthetic_images.py \
--out-root data/processed/images_synthetic \
--total 8000

Train the image baseline model:

.venv/bin/python scripts/train_image_baseline.py \
--data-root data/processed/images_synthetic \
--split train \
--out artifacts/model_image_baseline.joblib

Documentation:

docs/image_pipeline.md

---

# One-Command Training

Train all models together.

.venv/bin/python scripts/train_all.py \
--rows 8000 \
--images 8000

This trains:

- diabetes status model
- fungal infection classifier
- severity model
- fungal type model
- image classifier

---

# Fusion Inference

Run multimodal prediction.

.venv/bin/python scripts/run_fusion_inference.py \
--report /tmp/ic_sample_report.txt \
--image data/processed/images_synthetic/test/candida/candida_00001.png \
--tabular-model artifacts/model_fungal_infection.joblib \
--diabetes-model artifacts/model_diabetes_status.joblib \
--severity-model artifacts/model_severity.joblib \
--type-model artifacts/model_fungal_type.joblib \
--image-model artifacts/model_image_baseline.joblib

Outputs include:

- infection risk probability
- fungal infection type
- predicted severity level

---

# Web App Inference (Local Python)

To make the web app call the local Python models:

INFERENCE_MODE=python  
PYTHON_BIN=.venv/bin/python  

TABULAR_MODEL_PATH=artifacts/model_fungal_infection.joblib  
IMAGE_MODEL_PATH=artifacts/model_image_baseline.joblib  
DIABETES_MODEL_PATH=artifacts/model_diabetes_status.joblib  
SEVERITY_MODEL_PATH=artifacts/model_severity.joblib  
TYPE_MODEL_PATH=artifacts/model_fungal_type.joblib  

See:

web/.env.example

---

# Model API (FastAPI)

For production deployment, run a dedicated inference service.

.venv/bin/python -m uvicorn deployment.api.main:app \
--host 0.0.0.0 \
--port 8000

Then configure the web app:

INFERENCE_API_URL=http://localhost:8000

---

# LLM Chat Assistant

The assistant supports multiple providers.

## OpenAI

LLM_PROVIDER=openai  
OPENAI_API_KEY=YOUR_KEY  
OPENAI_MODEL=gpt-4o-mini  

---

## Google Gemini

LLM_PROVIDER=gemini  
GEMINI_API_KEY=YOUR_KEY  
GEMINI_MODEL=gemini-1.5-flash  

---

## OpenRouter (Free Tier)

LLM_PROVIDER=openrouter  
OPENROUTER_API_KEY=YOUR_KEY  
OPENROUTER_MODEL=openrouter/free  

This allows free hosted LLM inference with rate limits.

---

# Deployment (Vercel)

Deploy the frontend with:

Root Directory:

web/

Required environment variables:

INFERENCE_API_URL  
LLM_PROVIDER  
API_KEYS  

Typical production architecture:

Next.js Frontend (Vercel)  
        │  
        ▼  
FastAPI Model Server  
        │  
        ▼  
Python AI Models  

---

# Limitations

- Synthetic training images may not generalize to real clinical datasets.
- Predictions require validation by medical professionals.
- The system is intended for research and triage support.

See:

docs/model_card.md

---

# Ethical Considerations

This project follows responsible AI principles:

- Human-in-the-loop decision making
- Transparent model limitations
- Clinical decision-support boundaries

The system must not replace professional medical diagnosis.

---

# Documentation

docs/spec.md  
docs/data_schema.md  
docs/training.md  
docs/image_pipeline.md  

---

# Future Work

Planned improvements include:

- real dermatology datasets
- transformer-based report parsing
- CNN / Vision Transformer classifiers
- explainable AI methods (SHAP / Grad-CAM)
- federated medical model training
- clinical validation studies
