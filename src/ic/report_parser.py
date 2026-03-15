from __future__ import annotations

import re
from typing import Optional, Dict, List

from .types import LabValues


_NUM_RE = r"([0-9]+(?:\.[0-9]+)?)"


def _find_first(patterns: List[str], text: str) -> Optional[float]:
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                continue
    return None


def extract_labs_from_text(text: str) -> LabValues:
    if not text:
        return LabValues()

    cleaned = text.replace(",", " ")

    values = LabValues(
        age_years=_find_first([
            rf"age[^0-9]{{0,10}}{_NUM_RE}",
            rf"{_NUM_RE}\s*years"
        ], cleaned),
        bmi=_find_first([
            rf"bmi[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        diabetes_duration_years=_find_first([
            rf"duration[^0-9]{{0,10}}{_NUM_RE}\s*(years|yrs)",
        ], cleaned),
        hba1c_percent=_find_first([
            rf"hba1c[^0-9]{{0,10}}{_NUM_RE}\s*%?",
            rf"a1c[^0-9]{{0,10}}{_NUM_RE}\s*%?",
        ], cleaned),
        fpg_mg_dl=_find_first([
            rf"(fpg|fasting plasma glucose|fasting glucose)[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        ogtt_2h_mg_dl=_find_first([
            rf"(ogtt|oral glucose)[^0-9]{{0,10}}{_NUM_RE}",
            rf"2\s*hr[^0-9]{{0,10}}{_NUM_RE}"
        ], cleaned),
        crp_mg_l=_find_first([
            rf"crp[^0-9]{{0,10}}{_NUM_RE}",
            rf"c\s*-?\s*reactive protein[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        neutrophils_abs=_find_first([
            rf"neutrophil[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        lymphocytes_abs=_find_first([
            rf"lymphocyte[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        nlr=_find_first([
            rf"nlr[^0-9]{{0,10}}{_NUM_RE}",
            rf"neutrophil[^\n]{{0,20}}lymphocyte[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        cd4_count=_find_first([
            rf"cd4[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        il6_pg_ml=_find_first([
            rf"il\s*-?\s*6[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        il17_pg_ml=_find_first([
            rf"il\s*-?\s*17[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        tnf_alpha_pg_ml=_find_first([
            rf"tnf\s*-?\s*alpha[^0-9]{{0,10}}{_NUM_RE}",
            rf"tnf\s*-?\s*a[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        beta_hydroxybutyrate_mmol_l=_find_first([
            rf"beta\s*-?\s*hydroxybutyrate[^0-9]{{0,10}}{_NUM_RE}",
            rf"b\s*-?\s*hba?[^0-9]{{0,10}}{_NUM_RE}",
        ], cleaned),
        urine_albumin_mg_g=_find_first([
            rf"urine albumin[^0-9]{{0,10}}{_NUM_RE}",
            rf"albumin[^0-9]{{0,10}}{_NUM_RE}\s*(mg/g|mg\s*/\s*g)",
        ], cleaned),
    )

    if values.nlr is None and values.neutrophils_abs and values.lymphocytes_abs:
        try:
            values.nlr = round(values.neutrophils_abs / values.lymphocytes_abs, 3)
        except ZeroDivisionError:
            pass

    return values
