import { NextResponse } from "next/server";
import { analyzeReport } from "@/lib/analyze";
import { runPythonInference } from "@/lib/pythonInference";
import { extractTextFromBuffer } from "@/lib/ocr";

export const runtime = "nodejs";

export async function GET() {
  return NextResponse.json({ ok: true, message: "analyze route ready" });
}

export async function POST(req: Request) {
  let form: FormData;
  try {
    form = await req.formData();
  } catch (err) {
    return NextResponse.json({ error: "Invalid form data" }, { status: 400 });
  }
  const reportText = form.get("reportText");
  const reportFile = form.get("reportFile") as File | null;
  const imageFile = form.get("imageFile") as File | null;

  let text = typeof reportText === "string" ? reportText : "";
  if (!text && reportFile) {
    try {
      const buffer = Buffer.from(await reportFile.arrayBuffer());
      const ocrText = await extractTextFromBuffer(buffer, reportFile.type || "");
      text = ocrText || "";
    } catch (err) {
      text = "";
    }
  }

  const warnings: string[] = [];
  let result: any = null;

  if (!text) {
    warnings.push("No report text found after OCR. Provide report text or a readable file.");
  }
  if (!imageFile) {
    warnings.push("No image uploaded. Image-based type inference will be limited.");
  }

  const inferenceMode = process.env.INFERENCE_MODE || "rule";
  const inferenceApi = process.env.INFERENCE_API_URL || "";

  if (inferenceApi && text) {
    try {
      const apiBase = inferenceApi.replace(/\/+$/, "");
      const imageBuffer = imageFile ? Buffer.from(await imageFile.arrayBuffer()) : null;
      const imageBase64 = imageBuffer ? imageBuffer.toString("base64") : null;

      const apiResponse = await fetch(`${apiBase}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          report_text: text,
          image_base64: imageBase64,
          image_name: imageFile?.name ?? null
        })
      });

      if (!apiResponse.ok) {
        throw new Error("Remote inference failed");
      }

      const data = await apiResponse.json();
      result = data.result ?? data;
      if (Array.isArray(data.warnings)) {
        warnings.push(...data.warnings);
      }
    } catch (err) {
      warnings.push("Remote inference failed; attempting local fallback.");
      result = null;
    }
  }

  if (!result && inferenceMode === "python" && text) {
    try {
      const imageBuffer = imageFile ? Buffer.from(await imageFile.arrayBuffer()) : null;
      const pythonResult = await runPythonInference({
        reportText: text,
        imageBuffer,
        imageName: imageFile?.name ?? null
      });
      result = pythonResult.result;
      warnings.push(...pythonResult.warnings);
    } catch (err) {
      warnings.push("Python inference failed; falling back to rule-based analysis.");
      result = analyzeReport(text, imageFile?.name ?? null);
    }
  }

  if (!result) {
    result = analyzeReport(text, imageFile?.name ?? null);
  }

  return NextResponse.json({ result, warnings });
}
