export type GeminiMessage = {
  role: "system" | "user";
  content: string;
};

export type GeminiOptions = {
  apiKey: string;
  model: string;
  baseUrl?: string;
  temperature?: number;
  maxOutputTokens?: number;
};

function buildPrompt(messages: GeminiMessage[]): string {
  const system = messages.find((m) => m.role === "system")?.content || "";
  const user = messages.filter((m) => m.role === "user").map((m) => m.content).join("\n\n");
  return system ? `${system}\n\n${user}` : user;
}

export async function callGemini(messages: GeminiMessage[], options: GeminiOptions): Promise<string> {
  const baseUrl = options.baseUrl || "https://generativelanguage.googleapis.com/v1beta";
  const prompt = buildPrompt(messages);

  const payload = {
    contents: [
      {
        role: "user",
        parts: [{ text: prompt }]
      }
    ],
    generationConfig: {
      temperature: options.temperature ?? 0.2,
      maxOutputTokens: options.maxOutputTokens ?? 400
    }
  };

  const res = await fetch(`${baseUrl.replace(/\/$/, "")}/models/${options.model}:generateContent`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-goog-api-key": options.apiKey
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Gemini error: ${res.status} ${text}`);
  }

  const data = await res.json();
  const textOut = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!textOut) throw new Error("Gemini returned empty response");

  return String(textOut).trim();
}
