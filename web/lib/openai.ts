export type OpenAIMessage = {
  role: "system" | "user";
  content: string;
};

export type OpenAIOptions = {
  apiKey: string;
  model: string;
  baseUrl?: string;
  maxOutputTokens?: number;
  temperature?: number;
  organization?: string;
  project?: string;
};

function extractOutputText(data: any): string {
  if (!data) return "";

  // SDK-only field; keep as a fallback if present
  if (typeof data.output_text === "string" && data.output_text.trim()) {
    return data.output_text.trim();
  }

  const output = Array.isArray(data.output) ? data.output : [];
  const chunks: string[] = [];

  for (const item of output) {
    if (item?.type === "message" && Array.isArray(item.content)) {
      for (const part of item.content) {
        if (part?.type === "output_text" && typeof part.text === "string") {
          chunks.push(part.text);
        }
      }
    }
  }

  return chunks.join("").trim();
}

export async function callOpenAI(messages: OpenAIMessage[], options: OpenAIOptions): Promise<string> {
  const baseUrl = options.baseUrl || "https://api.openai.com/v1";

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${options.apiKey}`
  };

  if (options.organization) headers["OpenAI-Organization"] = options.organization;
  if (options.project) headers["OpenAI-Project"] = options.project;

  const system = messages.find((m) => m.role === "system")?.content || "";
  const user = messages.filter((m) => m.role === "user").map((m) => m.content).join("\n\n");

  const payload = {
    model: options.model,
    instructions: system || undefined,
    input: user || "",
    max_output_tokens: options.maxOutputTokens ?? 400,
    temperature: options.temperature ?? 0.2
  };

  const res = await fetch(`${baseUrl.replace(/\/$/, "")}/responses`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`OpenAI error: ${res.status} ${text}`);
  }

  const data = await res.json();
  const content = extractOutputText(data);
  if (!content) throw new Error("OpenAI returned empty response");

  return content;
}
