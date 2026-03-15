import pdfParse from "pdf-parse";
import Tesseract from "tesseract.js";

export async function extractTextFromBuffer(buffer: Buffer, mime?: string): Promise<string> {
  const lowerMime = (mime || "").toLowerCase();

  // Text-based PDF
  if (lowerMime.includes("pdf")) {
    try {
      const data = await pdfParse(buffer);
      return data.text?.trim() || "";
    } catch (err) {
      console.error("pdf-parse failed", err);
    }
  }

  // Image OCR via Tesseract
  try {
    const result = await Tesseract.recognize(buffer, "eng", { logger: () => {} });
    return result.data?.text?.trim() || "";
  } catch (err) {
    console.error("tesseract failed", err);
    return "";
  }
}
