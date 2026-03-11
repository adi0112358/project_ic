"use client";

import { useState } from "react";
import type { AnalysisResult } from "@/lib/types";
import Link from "next/link";
import { jsPDF } from "jspdf";

export default function UploadPage() {
  const [reportText, setReportText] = useState("");
  const [reportFile, setReportFile] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [warnings, setWarnings] = useState<string[]>([]);

  const downloadJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "project_ic_result.json";
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadPDF = () => {
    if (!result) return;
    const doc = new jsPDF();
    const lines: string[] = [
      "Project IC - Analysis Report",
      "",
      `Diabetes status: ${result.diabetes_status}`,
      `Fungal risk: ${result.fungal_risk} (score ${result.fungal_risk_score.toFixed(2)})`,
      `Fungal type: ${result.fungal_type}`,
      `Severity: ${result.severity}`,
      "",
      "Key signals:"
    ];

    result.explanations.forEach((ex) => lines.push(`- ${ex}`));

    const text = doc.splitTextToSize(lines.join("\n"), 180);
    doc.text(text, 15, 20);
    doc.save("project_ic_report.pdf");
  };

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setWarnings([]);

    const form = new FormData();
    if (reportText) form.append("reportText", reportText);
    if (reportFile) form.append("reportFile", reportFile);
    if (imageFile) form.append("imageFile", imageFile);

    const response = await fetch("/api/analyze", {
      method: "POST",
      body: form
    });

    const data = await response.json();
    setResult(data.result ?? null);
    setWarnings(data.warnings ?? []);
    if (data.result) {
      localStorage.setItem("ic_analysis", JSON.stringify(data.result));
    }
    setLoading(false);
  };

  return (
    <section>
      <h1 className="brand" style={{ fontSize: 28, marginBottom: 6 }}>Upload report + image</h1>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        Provide report text or a text-based report file. PDF/image OCR will be plugged in later.
      </p>

      <form className="form" onSubmit={onSubmit}>
        <div>
          <label className="label">Report text (paste)</label>
          <textarea
            value={reportText}
            onChange={(e) => setReportText(e.target.value)}
            placeholder="Example: HbA1c 7.8%, FPG 140 mg/dL, CRP 12 mg/L..."
          />
        </div>

        <div>
          <label className="label">Report file (txt or readable PDF)</label>
          <input type="file" accept=".txt,.pdf" onChange={(e) => setReportFile(e.target.files?.[0] ?? null)} />
        </div>

        <div>
          <label className="label">Skin image</label>
          <input type="file" accept="image/*" onChange={(e) => setImageFile(e.target.files?.[0] ?? null)} />
        </div>

        <button className="button" type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Run analysis"}
        </button>
      </form>

      {warnings.length > 0 && (
        <div className="result">
          <strong>Warnings</strong>
          <ul>
            {warnings.map((w) => (
              <li key={w}>{w}</li>
            ))}
          </ul>
        </div>
      )}

      {result && (
        <div className="result">
          <strong>Result</strong>
          <p>Diabetes status: {result.diabetes_status}</p>
          <p>Fungal risk: {result.fungal_risk} (score {result.fungal_risk_score.toFixed(2)})</p>
          <p>Fungal type: {result.fungal_type}</p>
          <p>Severity: {result.severity}</p>
          <div style={{ marginTop: 12 }}>
            <strong>Explanations</strong>
            <ul>
              {result.explanations.map((ex) => (
                <li key={ex}>{ex}</li>
              ))}
            </ul>
          </div>
          <div style={{ marginTop: 12 }}>
            <Link className="button secondary" href="/chat">Open chat</Link>
            <button className="button secondary" type="button" onClick={downloadJSON} style={{ marginLeft: 8 }}>
              Download JSON
            </button>
            <button className="button secondary" type="button" onClick={downloadPDF} style={{ marginLeft: 8 }}>
              Download PDF
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
