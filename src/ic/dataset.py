from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd


FEATURE_COLUMNS: List[str] = [
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
]


@dataclass
class TabularDataset:
    features: pd.DataFrame
    target: pd.Series
    feature_columns: List[str]


def _ensure_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def _derive_nlr(df: pd.DataFrame) -> pd.DataFrame:
    if "nlr" not in df.columns:
        df["nlr"] = pd.NA
    if "neutrophils_abs" in df.columns and "lymphocytes_abs" in df.columns:
        missing = df["nlr"].isna()
        denom = df.loc[missing, "lymphocytes_abs"].replace({0: pd.NA})
        df.loc[missing, "nlr"] = df.loc[missing, "neutrophils_abs"] / denom
    return df


def _normalize_binary(series: pd.Series) -> pd.Series:
    def conv(val):
        if pd.isna(val):
            return pd.NA
        if isinstance(val, (int, float)):
            return 1 if float(val) > 0 else 0
        s = str(val).strip().lower()
        if s in {"1", "yes", "y", "true", "pos", "positive"}:
            return 1
        if s in {"0", "no", "n", "false", "neg", "negative"}:
            return 0
        try:
            f = float(s)
            return 1 if f > 0 else 0
        except ValueError:
            return pd.NA

    return series.map(conv)


def load_tabular_dataset(csv_path: str, target: str) -> TabularDataset:
    df = pd.read_csv(csv_path)
    df = _ensure_columns(df, FEATURE_COLUMNS)
    df = _derive_nlr(df)

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset.")

    X = df[FEATURE_COLUMNS].copy()
    y = df[target].copy()

    if target == "fungal_infection":
        y = _normalize_binary(y)

    return TabularDataset(features=X, target=y, feature_columns=FEATURE_COLUMNS)
