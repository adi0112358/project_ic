import { promises as fs } from "fs";
import path from "path";
import os from "os";
import { randomUUID } from "crypto";
import { execFile } from "child_process";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

export type PythonInferenceResult = {
  result: any;
  warnings: string[];
};

function resolveRepoRoot(): string {
  return path.resolve(process.cwd(), "..");
}

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function runPythonInference(options: {
  reportText: string;
  imageBuffer?: Buffer | null;
  imageName?: string | null;
}): Promise<PythonInferenceResult> {
  const warnings: string[] = [];

  const repoRoot = resolveRepoRoot();
  const pythonBin = process.env.PYTHON_BIN || path.join(repoRoot, ".venv", "bin", "python");
  const scriptPath = path.join(repoRoot, "scripts", "run_fusion_inference.py");

  const tabularModel = process.env.TABULAR_MODEL_PATH || path.join(repoRoot, "artifacts", "model_fungal_infection.joblib");
  const imageModel = process.env.IMAGE_MODEL_PATH || path.join(repoRoot, "artifacts", "model_image_baseline.joblib");
  const diabetesModel = process.env.DIABETES_MODEL_PATH || path.join(repoRoot, "artifacts", "model_diabetes_status.joblib");
  const severityModel = process.env.SEVERITY_MODEL_PATH || path.join(repoRoot, "artifacts", "model_severity.joblib");
  const typeModel = process.env.TYPE_MODEL_PATH || path.join(repoRoot, "artifacts", "model_fungal_type.joblib");

  if (!(await fileExists(pythonBin))) {
    throw new Error(`Python binary not found at ${pythonBin}`);
  }
  if (!(await fileExists(scriptPath))) {
    throw new Error(`Inference script not found at ${scriptPath}`);
  }

  if (!(await fileExists(tabularModel))) {
    warnings.push("Tabular model artifact not found; risk score will fall back to rule-based scoring.");
  }
  if (!(await fileExists(imageModel))) {
    warnings.push("Image model artifact not found; fungal type may be unknown.");
  }
  if (!(await fileExists(diabetesModel))) {
    warnings.push("Diabetes model artifact not found; diabetes status will be rule-based.");
  }
  if (!(await fileExists(severityModel))) {
    warnings.push("Severity model artifact not found; severity will be rule-based.");
  }
  if (!(await fileExists(typeModel))) {
    warnings.push("Fungal type model artifact not found; type may rely on text or image only.");
  }

  const tmpDir = os.tmpdir();
  const runId = randomUUID();
  const reportPath = path.join(tmpDir, `ic_report_${runId}.txt`);

  await fs.writeFile(reportPath, options.reportText || "", "utf-8");

  let imagePath: string | null = null;
  if (options.imageBuffer && options.imageBuffer.length > 0) {
    const ext = options.imageName?.split(".").pop() || "png";
    imagePath = path.join(tmpDir, `ic_image_${runId}.${ext}`);
    await fs.writeFile(imagePath, options.imageBuffer);
  }

  const args: string[] = [scriptPath, "--report", reportPath];

  if (imagePath && (await fileExists(imageModel))) {
    args.push("--image", imagePath, "--image-model", imageModel);
  }

  if (await fileExists(tabularModel)) {
    args.push("--tabular-model", tabularModel);
  }

  if (await fileExists(diabetesModel)) {
    args.push("--diabetes-model", diabetesModel);
  }

  if (await fileExists(severityModel)) {
    args.push("--severity-model", severityModel);
  }

  if (await fileExists(typeModel)) {
    args.push("--type-model", typeModel);
  }

  const { stdout } = await execFileAsync(pythonBin, args, { timeout: 20_000 });

  let parsed: any = null;
  try {
    parsed = JSON.parse(stdout);
  } catch (err) {
    throw new Error("Failed to parse python inference output as JSON.");
  }

  // Best-effort cleanup
  await fs.unlink(reportPath).catch(() => undefined);
  if (imagePath) {
    await fs.unlink(imagePath).catch(() => undefined);
  }

  return { result: parsed, warnings };
}
