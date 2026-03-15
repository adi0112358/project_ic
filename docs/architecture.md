# Architecture (v1)

## High-level flow
1. Report upload → OCR → lab extraction
2. Skin image upload → image model → image embedding / class
3. Fusion model → risk/type/severity
4. Chat assistant → grounded explanations

## Services
- **Web (Vercel)**: Next.js frontend + lightweight API routes
- **Inference API (separate service)**: FastAPI service for model inference

## Module boundaries
- `web/` – UI + API stubs
- `src/ic/` – AI core logic (parsers, scorers, fusion)

## Data contracts
- `AnalysisRequest`: { report_text, report_file, image_file, metadata }
- `AnalysisResponse`: { diabetes_status, fungal_risk, fungal_type, severity, explanations }
