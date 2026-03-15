from __future__ import annotations

from typing import List, Optional

from .types import LabValues


def infer_diabetes_status(labs: LabValues) -> str:
    hba1c = labs.hba1c_percent
    fpg = labs.fpg_mg_dl
    ogtt = labs.ogtt_2h_mg_dl

    if (hba1c is not None and hba1c >= 6.5) or (fpg is not None and fpg >= 126) or (ogtt is not None and ogtt >= 200):
        return "diabetes"
    if (hba1c is not None and 5.7 <= hba1c < 6.5) or (fpg is not None and 100 <= fpg < 126) or (ogtt is not None and 140 <= ogtt < 200):
        return "prediabetes"
    if hba1c is not None or fpg is not None or ogtt is not None:
        return "normal"
    return "unknown"


def _score_marker(value: Optional[float], threshold: float, weight: float) -> float:
    if value is None:
        return 0.0
    return weight if value >= threshold else 0.0


def score_fungal_risk(labs: LabValues, diabetes_status: str) -> float:
    score = 0.0

    if diabetes_status == "diabetes":
        score += 0.35
    elif diabetes_status == "prediabetes":
        score += 0.15

    if labs.hba1c_percent is not None:
        if labs.hba1c_percent >= 8.0:
            score += 0.2
        elif labs.hba1c_percent >= 7.0:
            score += 0.1

    score += _score_marker(labs.crp_mg_l, 10.0, 0.1)
    score += _score_marker(labs.nlr, 3.0, 0.1)
    score += _score_marker(labs.il6_pg_ml, 7.0, 0.05)
    score += _score_marker(labs.tnf_alpha_pg_ml, 8.0, 0.05)
    score += _score_marker(labs.beta_hydroxybutyrate_mmol_l, 1.0, 0.05)
    score += _score_marker(labs.urine_albumin_mg_g, 30.0, 0.05)

    return min(score, 1.0)


def bucket_risk(score: float) -> str:
    if score < 0.35:
        return "low"
    if score < 0.65:
        return "medium"
    return "high"


def infer_type_from_text(text: str) -> str:
    if not text:
        return "unknown"

    t = text.lower()
    if any(k in t for k in ["candida", "thrush", "candidiasis"]):
        return "candida"
    if any(k in t for k in ["tinea", "ringworm", "dermatophyte"]):
        return "dermatophyte"
    if "aspergillus" in t:
        return "aspergillus"
    if any(k in t for k in ["mucor", "zygomycosis"]):
        return "other"
    return "unknown"


def infer_type_from_image_hint(image_name: Optional[str]) -> str:
    if not image_name:
        return "unknown"
    t = image_name.lower()
    if "candida" in t or "thrush" in t:
        return "candida"
    if "tinea" in t or "ringworm" in t or "dermatophyte" in t:
        return "dermatophyte"
    if "aspergillus" in t:
        return "aspergillus"
    return "unknown"


def infer_severity(labs: LabValues, risk_score: float) -> str:
    if (labs.crp_mg_l is not None and labs.crp_mg_l >= 20) or (labs.il6_pg_ml is not None and labs.il6_pg_ml >= 20) or risk_score >= 0.7:
        return "severe"
    if risk_score >= 0.45:
        return "moderate"
    return "mild"


def build_explanations(labs: LabValues, diabetes_status: str, risk_score: float) -> List[str]:
    reasons: List[str] = []
    if diabetes_status != "unknown":
        reasons.append(f"Diabetes status inferred as {diabetes_status} based on glycemic markers.")
    if labs.hba1c_percent is not None:
        reasons.append(f"HbA1c recorded at {labs.hba1c_percent:.2f}%.")
    if labs.fpg_mg_dl is not None:
        reasons.append(f"Fasting glucose recorded at {labs.fpg_mg_dl:.0f} mg/dL.")
    if labs.crp_mg_l is not None:
        reasons.append(f"CRP recorded at {labs.crp_mg_l:.1f} mg/L.")
    if labs.nlr is not None:
        reasons.append(f"NLR recorded at {labs.nlr:.2f}.")
    reasons.append(f"Overall fungal risk score: {risk_score:.2f}.")
    return reasons
