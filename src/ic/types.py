from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List


@dataclass
class LabValues:
    age_years: Optional[float] = None
    bmi: Optional[float] = None
    diabetes_duration_years: Optional[float] = None

    hba1c_percent: Optional[float] = None
    fpg_mg_dl: Optional[float] = None
    ogtt_2h_mg_dl: Optional[float] = None

    neutrophils_abs: Optional[float] = None
    lymphocytes_abs: Optional[float] = None
    nlr: Optional[float] = None
    cd4_count: Optional[float] = None

    crp_mg_l: Optional[float] = None
    il6_pg_ml: Optional[float] = None
    il17_pg_ml: Optional[float] = None
    tnf_alpha_pg_ml: Optional[float] = None

    beta_hydroxybutyrate_mmol_l: Optional[float] = None
    urine_albumin_mg_g: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnalysisResult:
    diabetes_status: str
    fungal_risk: str
    fungal_risk_score: float
    fungal_type: str
    severity: str
    explanations: List[str]
    labs: LabValues

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["labs"] = self.labs.to_dict()
        return data
