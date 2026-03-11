export type OpenRouterMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

export type OpenRouterOptions = {
  apiKey: string;
  model: string;
  baseUrl?: string;
  maxTokens?: number;
  temperature?: number;
  siteUrl?: string;
  siteName?: string;
};

export async function callOpenRouter(messages: OpenRouterMessage[], options: OpenRouterOptions): Promise<string> {
  const baseUrl = options.baseUrl || "https://openrouter.ai/api/v1";

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${options.apiKey}`
  };

  if (options.siteUrl) headers["HTTP-Referer"] = options.siteUrl;
  if (options.siteName) headers["X-Title"] = options.siteName;

  const payload = {
    model: options.model,
    messages,
    max_tokens: options.maxTokens ?? 400,
    temperature: options.temperature ?? 0.2
  };

  const res = await fetch(`${baseUrl.replace(/\/$/, "")}/chat/completions`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`OpenRouter error: ${res.status} ${text}`);
  }

  const data = await res.json();
  const content = data?.choices?.[0]?.message?.content;
  if (!content) throw new Error("OpenRouter returned empty response");

  return content;
}
