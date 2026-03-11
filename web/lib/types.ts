export type LabValues = {
  age_years?: number | null;
  bmi?: number | null;
  diabetes_duration_years?: number | null;
  hba1c_percent?: number | null;
  fpg_mg_dl?: number | null;
  ogtt_2h_mg_dl?: number | null;
  neutrophils_abs?: number | null;
  lymphocytes_abs?: number | null;
  nlr?: number | null;
  cd4_count?: number | null;
  crp_mg_l?: number | null;
  il6_pg_ml?: number | null;
  il17_pg_ml?: number | null;
  tnf_alpha_pg_ml?: number | null;
  beta_hydroxybutyrate_mmol_l?: number | null;
  urine_albumin_mg_g?: number | null;
};

export type AnalysisResult = {
  diabetes_status: "normal" | "prediabetes" | "diabetes" | "unknown";
  fungal_risk: "low" | "medium" | "high";
  fungal_risk_score: number;
  fungal_type: "candida" | "dermatophyte" | "aspergillus" | "other" | "unknown";
  severity: "mild" | "moderate" | "severe";
  explanations: string[];
  labs: LabValues;
};
