import { NextResponse } from "next/server";
import { buildChatResponse } from "@/lib/chat";
import { AnalysisResult } from "@/lib/types";
import { callOpenRouter } from "@/lib/openrouter";
import { callOpenAI } from "@/lib/openai";
import { callGemini } from "@/lib/gemini";

export async function POST(req: Request) {
  const body = await req.json();
  const message = typeof body?.message === "string" ? body.message : "";
  const analysis = (body?.analysis as AnalysisResult | undefined) ?? null;

  const provider = process.env.LLM_PROVIDER || "";

  const openAiKey = process.env.OPENAI_API_KEY || "";
  const openAiModel = process.env.OPENAI_MODEL || "gpt-4o-mini";
  const openAiBaseUrl = process.env.OPENAI_BASE_URL || "https://api.openai.com/v1";
  const openAiOrg = process.env.OPENAI_ORG || undefined;
  const openAiProject = process.env.OPENAI_PROJECT || undefined;

  const geminiKey = process.env.GEMINI_API_KEY || "";
  const geminiModel = process.env.GEMINI_MODEL || "gemini-1.5-flash";
  const geminiBaseUrl = process.env.GEMINI_BASE_URL || "https://generativelanguage.googleapis.com/v1beta";

  const openRouterKey = process.env.OPENROUTER_API_KEY || "";
  const openRouterModel = process.env.OPENROUTER_MODEL || "openrouter/free";
  const openRouterBaseUrl = process.env.OPENROUTER_BASE_URL || "https://openrouter.ai/api/v1";
  const siteUrl = process.env.OPENROUTER_SITE_URL || undefined;
  const siteName = process.env.OPENROUTER_SITE_NAME || "Project IC";

  let reply = "";
  let providerUsed = "fallback";
  let lastError = "";
  const debug = process.env.LLM_DEBUG === "1";

  const systemPrompt = [
    "You are Project IC, an educational assistant for a fungal infection classifier in type 2 diabetes.",
    "You must NOT provide prescriptions, dosing, or definitive medical diagnosis.",
    "Use only the provided analysis data and user message.",
    "If data is missing or uncertain, say so and suggest consulting a clinician.",
    "Keep responses concise and structured."
  ].join(" ");

  const context = analysis ? JSON.stringify(analysis) : "No analysis data available.";

  const useOpenAI = provider === "openai" || (!provider && openAiKey);
  const useGemini = provider === "gemini" || (!provider && !openAiKey && geminiKey);
  const useOpenRouter = provider === "openrouter" || (!provider && !openAiKey && !geminiKey && openRouterKey);

  if (useOpenAI && openAiKey) {
    try {
      reply = await callOpenAI(
        [
          { role: "system", content: systemPrompt },
          { role: "user", content: `Analysis data: ${context}` },
          { role: "user", content: message }
        ],
        {
          apiKey: openAiKey,
          model: openAiModel,
          baseUrl: openAiBaseUrl,
          organization: openAiOrg,
          project: openAiProject
        }
      );
      providerUsed = "openai";
    } catch (err) {
      reply = "";
      lastError = err instanceof Error ? err.message : "openai_error";
    }
  }

  if (!reply && useGemini && geminiKey) {
    try {
      reply = await callGemini(
        [
          { role: "system", content: systemPrompt },
          { role: "user", content: `Analysis data: ${context}` },
          { role: "user", content: message }
        ],
        { apiKey: geminiKey, model: geminiModel, baseUrl: geminiBaseUrl }
      );
      providerUsed = "gemini";
    } catch (err) {
      reply = "";
      lastError = err instanceof Error ? err.message : "gemini_error";
    }
  }

  if (!reply && useOpenRouter && openRouterKey) {
    try {
      reply = await callOpenRouter(
        [
          { role: "system", content: systemPrompt },
          { role: "system", content: `Analysis data: ${context}` },
          { role: "user", content: message }
        ],
        { apiKey: openRouterKey, model: openRouterModel, baseUrl: openRouterBaseUrl, siteUrl, siteName }
      );
      providerUsed = "openrouter";
    } catch (err) {
      reply = "";
      lastError = err instanceof Error ? err.message : "openrouter_error";
    }
  }

  if (!reply) {
    reply = buildChatResponse(message, analysis);
    providerUsed = "fallback";
  }

  const payload: Record<string, unknown> = { reply };
  if (debug) {
    payload.llm = { providerUsed, lastError };
  }

  return NextResponse.json(payload);
}
