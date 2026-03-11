import { AnalysisResult } from "./types";

function summarize(result: AnalysisResult): string {
  return [
    `Diabetes status: ${result.diabetes_status}.`,
    `Fungal infection risk: ${result.fungal_risk} (score ${result.fungal_risk_score.toFixed(2)}).`,
    `Likely fungal type: ${result.fungal_type}.`,
    `Severity estimate: ${result.severity}.`
  ].join("\n");
}

export function buildChatResponse(message: string, analysis?: AnalysisResult | null): string {
  const msg = (message || "").toLowerCase();
  const summary = analysis ? summarize(analysis) : "No analysis data was provided.";

  if (msg.includes("dose") || msg.includes("dosage") || msg.includes("prescription") || msg.includes("drug")) {
    return [
      summary,
      "",
      "I can’t provide prescriptions or dosing. Please consult a clinician for treatment decisions.",
      "If you want, I can help you draft questions for your doctor based on your report."
    ].join("\n");
  }

  if (msg.includes("next") || msg.includes("what should") || msg.includes("what do i do")) {
    return [
      summary,
      "",
      "General next steps:",
      "1. Confirm with a clinician and consider a fungal culture if symptoms persist.",
      "2. Review glycemic control and medication adherence.",
      "3. Monitor symptoms and seek care if they worsen."
    ].join("\n");
  }

  return [
    summary,
    "",
    "I can explain how the risk score was derived or help interpret specific lab values."
  ].join("\n");
}
