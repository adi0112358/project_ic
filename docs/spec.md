# Project IC – Specification

## Problem statement
Build an AI-assisted system that ingests a patient’s diabetes lab report and a skin image to assess:
1. Diabetes status (normal / prediabetes / diabetes)
2. Fungal infection likelihood due to diabetes (yes/no + confidence)
3. Fungal infection type (candidate classes)
4. Severity (mild / moderate / severe)

The system also provides a **chat assistant** that explains results and suggests next steps, grounded only on the user’s own data.

## User workflow
1. User uploads lab report (PDF/image) and optionally pastes text.
2. OCR + extraction parses required lab parameters.
3. User uploads a skin image.
4. System runs fusion model → returns risk/type/severity.
5. Chat assistant explains and answers questions.

## Outputs (v1)
- `diabetes_status`: `normal | prediabetes | diabetes | unknown`
- `fungal_risk`: `low | medium | high` + numeric score
- `fungal_type`: `candida | dermatophyte | aspergillus | other | unknown`
- `severity`: `mild | moderate | severe`
- `explanations`: short human-readable reasons

## Key assumptions (v1)
- No clinical prescriptions. Chat is educational and triage-focused.
- OCR and image classification are modular, replaceable components.
- Data quality checks reject implausible lab values.

## Integration points
- **OCR**: plug-in provider (Tesseract, Textract, or cloud OCR)
- **Image model**: CNN/ViT (transfer learning)
- **Fusion**: tabular + image embedding → calibrated classifier
- **Chat**: retrieval-augmented with the user’s structured data only

## Milestones
1. Baseline extraction + rule-based scoring
2. Image pipeline skeleton + placeholder inference
3. Fusion model stub + confidence calibration
4. Chat assistant with grounded summaries
5. Evaluate on labeled dataset
