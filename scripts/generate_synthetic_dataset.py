from __future__ import annotations

import argparse
import csv
import math
import random
from typing import Optional


def clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(val, hi))


def maybe_missing(val: Optional[float], prob: float) -> Optional[float]:
    if val is None:
        return None
    return None if random.random() < prob else val


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def fmt(val: Optional[float]) -> str:
    if val is None:
        return ""
    return f"{val:.3f}" if abs(val) < 100 else f"{val:.2f}"


def generate_row(idx: int) -> dict:
    status = random.choices(
        ["normal", "prediabetes", "diabetes"],
        weights=[0.25, 0.25, 0.50],
        k=1,
    )[0]

    age_mean = 45 if status == "normal" else 52 if status == "prediabetes" else 58
    age = clamp(random.gauss(age_mean, 12), 18, 85)

    bmi_mean = 25 if status == "normal" else 27 if status == "prediabetes" else 30
    bmi = clamp(random.gauss(bmi_mean, 4.5), 18, 45)

    if status == "normal":
        duration = 0.0
        hba1c = clamp(random.gauss(5.3, 0.3), 4.5, 5.6)
        fpg = clamp(random.gauss(90, 8), 70, 99)
        ogtt = clamp(random.gauss(125, 10), 90, 139)
    elif status == "prediabetes":
        duration = clamp(random.gauss(2.0, 1.5), 0, 8)
        hba1c = clamp(random.gauss(6.0, 0.2), 5.7, 6.4)
        fpg = clamp(random.gauss(110, 8), 100, 125)
        ogtt = clamp(random.gauss(165, 15), 140, 199)
    else:
        duration = clamp(random.gauss(7.0, 4.0), 0, 25)
        hba1c = clamp(random.gauss(8.5, 1.4), 6.5, 13.5)
        fpg = clamp(random.gauss(170, 35), 126, 320)
        ogtt = clamp(random.gauss(240, 40), 200, 380)

    neutrophils = clamp(random.gauss(4.8, 1.3), 1.8, 11.5)
    lymphocytes = clamp(random.gauss(2.1, 0.6), 0.6, 4.8)
    nlr = neutrophils / lymphocytes if lymphocytes > 0 else None

    # Base infection risk from glycemic control + duration + immune ratio
    risk = sigmoid(
        -2.0
        + (0.8 if status == "prediabetes" else 0.0)
        + (1.5 if status == "diabetes" else 0.0)
        + 0.18 * max(hba1c - 6.0, 0.0)
        + 0.06 * duration
        + 0.15 * max(nlr - 2.0, 0.0)
    )

    fungal_infection = 1 if random.random() < risk else 0

    # Inflammatory markers
    if fungal_infection:
        crp = clamp(random.lognormvariate(2.2, 0.45), 4.0, 80.0)
        il6 = clamp(random.lognormvariate(2.1, 0.4), 3.0, 80.0)
        il17 = clamp(random.lognormvariate(1.8, 0.4), 2.0, 60.0)
        tnf = clamp(random.lognormvariate(2.0, 0.4), 3.0, 70.0)
    else:
        crp = clamp(random.lognormvariate(1.0, 0.35), 0.2, 12.0)
        il6 = clamp(random.lognormvariate(0.9, 0.35), 0.5, 12.0)
        il17 = clamp(random.lognormvariate(0.8, 0.35), 0.3, 10.0)
        tnf = clamp(random.lognormvariate(0.9, 0.35), 0.4, 12.0)

    # Metabolic stress markers
    beta_hb = clamp(
        random.gauss(0.5 + 0.08 * max(hba1c - 6.0, 0.0) + (0.3 if fungal_infection else 0.0), 0.25),
        0.1,
        4.0,
    )

    urine_albumin = clamp(
        random.gauss(15 + 4.0 * duration + 5.0 * max(hba1c - 6.0, 0.0), 18),
        2.0,
        600.0,
    )

    # CD4 count
    cd4 = clamp(random.gauss(650 - (80 if fungal_infection else 0), 140), 200, 1200)

    # Fungal type and severity
    if fungal_infection:
        fungal_type = random.choices(
            ["candida", "dermatophyte", "aspergillus", "other"],
            weights=[0.5, 0.3, 0.12, 0.08],
            k=1,
        )[0]
        severity_score = 0
        if crp >= 20:
            severity_score += 1
        if il6 >= 20:
            severity_score += 1
        if hba1c >= 8.5:
            severity_score += 1
        if beta_hb >= 1.5:
            severity_score += 1
        if severity_score >= 3:
            severity = "severe"
        elif severity_score == 2:
            severity = "moderate"
        else:
            severity = "mild"
    else:
        fungal_type = "unknown"
        severity = "mild"

    # Missingness for advanced markers
    ogtt = maybe_missing(ogtt, 0.08)
    cd4 = maybe_missing(cd4, 0.15)
    il6 = maybe_missing(il6, 0.12)
    il17 = maybe_missing(il17, 0.12)
    tnf = maybe_missing(tnf, 0.12)

    return {
        "patient_id": f"P{idx:05d}",
        "age_years": fmt(age),
        "bmi": fmt(bmi),
        "diabetes_duration_years": fmt(duration),
        "hba1c_percent": fmt(hba1c),
        "fpg_mg_dl": fmt(fpg),
        "ogtt_2h_mg_dl": fmt(ogtt),
        "neutrophils_abs": fmt(neutrophils),
        "lymphocytes_abs": fmt(lymphocytes),
        "nlr": fmt(nlr),
        "cd4_count": fmt(cd4),
        "crp_mg_l": fmt(crp),
        "il6_pg_ml": fmt(il6),
        "il17_pg_ml": fmt(il17),
        "tnf_alpha_pg_ml": fmt(tnf),
        "beta_hydroxybutyrate_mmol_l": fmt(beta_hb),
        "urine_albumin_mg_g": fmt(urine_albumin),
        "fungal_infection": str(fungal_infection),
        "fungal_type": fungal_type,
        "severity": severity,
        "diabetes_status": status,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=8000)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    fieldnames = [
        "patient_id",
        "age_years",
        "bmi",
        "diabetes_duration_years",
        "hba1c_percent",
        "fpg_mg_dl",
        "ogtt_2h_mg_dl",
        "neutrophils_abs",
        "lymphocytes_abs",
        "nlr",
        "cd4_count",
        "crp_mg_l",
        "il6_pg_ml",
        "il17_pg_ml",
        "tnf_alpha_pg_ml",
        "beta_hydroxybutyrate_mmol_l",
        "urine_albumin_mg_g",
        "fungal_infection",
        "fungal_type",
        "severity",
        "diabetes_status",
    ]

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, args.rows + 1):
            writer.writerow(generate_row(i))


if __name__ == "__main__":
    main()
