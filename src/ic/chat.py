from __future__ import annotations

from .types import AnalysisResult


def build_chat_summary(result: AnalysisResult) -> str:
    lines = []
    lines.append(f"Diabetes status: {result.diabetes_status}.")
    lines.append(f"Fungal infection risk: {result.fungal_risk} (score {result.fungal_risk_score:.2f}).")
    lines.append(f"Likely fungal type: {result.fungal_type}.")
    lines.append(f"Severity estimate: {result.severity}.")

    if result.explanations:
        lines.append("Key signals:")
        lines.extend([f"- {reason}" for reason in result.explanations])

    lines.append("\nThis is not medical advice. Please consult a clinician for diagnosis and treatment.")
    return "\n".join(lines)
