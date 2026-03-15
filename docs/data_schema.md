# Data Schema (v1)

## Patient metadata
- `patient_id` (string, optional)
- `age_years` (float)
- `sex` (string, optional)
- `bmi` (float, kg/m^2)
- `diabetes_duration_years` (float)

## Glycemic markers
- `hba1c_percent` (float, %)
- `fpg_mg_dl` (float, mg/dL)
- `ogtt_2h_mg_dl` (float, mg/dL)

## Immune markers
- `neutrophils_abs` (float, x10^9/L)
- `lymphocytes_abs` (float, x10^9/L)
- `nlr` (float) – derived if not provided
- `cd4_count` (float, cells/µL)

## Inflammatory markers
- `crp_mg_l` (float, mg/L)
- `il6_pg_ml` (float, pg/mL)
- `il17_pg_ml` (float, pg/mL)
- `tnf_alpha_pg_ml` (float, pg/mL)

## Metabolic stress markers
- `beta_hydroxybutyrate_mmol_l` (float, mmol/L)
- `urine_albumin_mg_g` (float, mg/g)

## Report metadata
- `report_date` (date, optional)
- `source` (string, optional)

## Image metadata
- `image_path` (string)
- `image_quality_score` (float 0–1)
- `lesion_location` (string, optional)

## Label schema (training)
- `diabetes_status` (normal/prediabetes/diabetes)
- `fungal_infection` (yes/no)
- `fungal_type` (candida/dermatophyte/aspergillus/other)
- `severity` (mild/moderate/severe)
- `ground_truth_source` (culture/clinician/self-report)
