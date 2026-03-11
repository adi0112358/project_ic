import { AnalysisResult, LabValues } from "./types";
import { extractLabsFromText } from "./reportParser";

function inferDiabetesStatus(labs: LabValues): AnalysisResult["diabetes_status"] {
  const hba1c = labs.hba1c_percent ?? undefined;
  const fpg = labs.fpg_mg_dl ?? undefined;
  const ogtt = labs.ogtt_2h_mg_dl ?? undefined;

  if ((hba1c !== undefined && hba1c >= 6.5) || (fpg !== undefined && fpg >= 126) || (ogtt !== undefined && ogtt >= 200)) {
    return "diabetes";
  }
  if ((hba1c !== undefined && hba1c >= 5.7 && hba1c < 6.5) || (fpg !== undefined && fpg >= 100 && fpg < 126) || (ogtt !== undefined && ogtt >= 140 && ogtt < 200)) {
    return "prediabetes";
  }
  if (hba1c !== undefined || fpg !== undefined || ogtt !== undefined) {
    return "normal";
  }
  return "unknown";
}

function scoreMarker(value: number | null | undefined, threshold: number, weight: number): number {
  if (value === null || value === undefined) return 0;
  return value >= threshold ? weight : 0;
}

function scoreFungalRisk(labs: LabValues, status: AnalysisResult["diabetes_status"]): number {
  let score = 0;
  if (status === "diabetes") score += 0.35;
  if (status === "prediabetes") score += 0.15;

  if (labs.hba1c_percent !== undefined && labs.hba1c_percent !== null) {
    if (labs.hba1c_percent >= 8.0) score += 0.2;
    else if (labs.hba1c_percent >= 7.0) score += 0.1;
  }

  score += scoreMarker(labs.crp_mg_l, 10.0, 0.1);
  score += scoreMarker(labs.nlr, 3.0, 0.1);
  score += scoreMarker(labs.il6_pg_ml, 7.0, 0.05);
  score += scoreMarker(labs.tnf_alpha_pg_ml, 8.0, 0.05);
  score += scoreMarker(labs.beta_hydroxybutyrate_mmol_l, 1.0, 0.05);
  score += scoreMarker(labs.urine_albumin_mg_g, 30.0, 0.05);

  return Math.min(score, 1.0);
}

function bucketRisk(score: number): AnalysisResult["fungal_risk"] {
  if (score < 0.35) return "low";
  if (score < 0.65) return "medium";
  return "high";
}

function inferTypeFromText(text: string): AnalysisResult["fungal_type"] {
  const t = (text || "").toLowerCase();
  if (t.includes("candida") || t.includes("thrush") || t.includes("candidiasis")) return "candida";
  if (t.includes("tinea") || t.includes("ringworm") || t.includes("dermatophyte")) return "dermatophyte";
  if (t.includes("aspergillus")) return "aspergillus";
  if (t.includes("mucor") || t.includes("zygomycosis")) return "other";
  return "unknown";
}

function inferTypeFromImageName(imageName?: string | null): AnalysisResult["fungal_type"] {
  if (!imageName) return "unknown";
  const t = imageName.toLowerCase();
  if (t.includes("candida") || t.includes("thrush")) return "candida";
  if (t.includes("tinea") || t.includes("ringworm") || t.includes("dermatophyte")) return "dermatophyte";
  if (t.includes("aspergillus")) return "aspergillus";
  return "unknown";
}

function inferSeverity(labs: LabValues, riskScore: number): AnalysisResult["severity"] {
  if ((labs.crp_mg_l ?? 0) >= 20 || (labs.il6_pg_ml ?? 0) >= 20 || riskScore >= 0.7) return "severe";
  if (riskScore >= 0.45) return "moderate";
  return "mild";
}

function buildExplanations(labs: LabValues, status: AnalysisResult["diabetes_status"], riskScore: number): string[] {
  const reasons: string[] = [];
  if (status !== "unknown") reasons.push(`Diabetes status inferred as ${status} based on glycemic markers.`);
  if (labs.hba1c_percent !== undefined && labs.hba1c_percent !== null) reasons.push(`HbA1c recorded at ${labs.hba1c_percent.toFixed(2)}%.`);
  if (labs.fpg_mg_dl !== undefined && labs.fpg_mg_dl !== null) reasons.push(`Fasting glucose recorded at ${Math.round(labs.fpg_mg_dl)} mg/dL.`);
  if (labs.crp_mg_l !== undefined && labs.crp_mg_l !== null) reasons.push(`CRP recorded at ${labs.crp_mg_l.toFixed(1)} mg/L.`);
  if (labs.nlr !== undefined && labs.nlr !== null) reasons.push(`NLR recorded at ${labs.nlr.toFixed(2)}.`);
  reasons.push(`Overall fungal risk score: ${riskScore.toFixed(2)}.`);
  return reasons;
}

export function analyzeReport(reportText: string, imageName?: string | null): AnalysisResult {
  const labs = extractLabsFromText(reportText || "");
  const diabetes_status = inferDiabetesStatus(labs);
  const fungal_risk_score = scoreFungalRisk(labs, diabetes_status);
  const fungal_risk = bucketRisk(fungal_risk_score);

  const typeFromText = inferTypeFromText(reportText || "");
  const typeFromImage = inferTypeFromImageName(imageName);
  const fungal_type = typeFromText !== "unknown" ? typeFromText : typeFromImage;

  const severity = inferSeverity(labs, fungal_risk_score);
  const explanations = buildExplanations(labs, diabetes_status, fungal_risk_score);

  return {
    diabetes_status,
    fungal_risk,
    fungal_risk_score,
    fungal_type,
    severity,
    explanations,
    labs
  };
}
