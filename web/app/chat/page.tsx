"use client";

import { useEffect, useState } from "react";
import type { AnalysisResult } from "@/lib/types";

export default function ChatPage() {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [message, setMessage] = useState("");
  const [log, setLog] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("ic_analysis");
    if (stored) {
      try {
        setAnalysis(JSON.parse(stored) as AnalysisResult);
      } catch {
        setAnalysis(null);
      }
    }
  }, []);

  const sendMessage = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!message.trim()) return;
    setLoading(true);

    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, analysis })
    });

    const data = await response.json();
    setLog((prev) => [...prev, `You: ${message}`, `Assistant: ${data.reply}`]);
    setMessage("");
    setLoading(false);
  };

  return (
    <section>
      <h1 className="brand" style={{ fontSize: 28, marginBottom: 6 }}>Chat assistant</h1>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>
        The assistant answers based on your latest analysis. Upload a report and image first.
      </p>

      <div className="chat">
        <div className="chat-log">
          {log.length === 0 ? "No messages yet." : log.join("\n\n")}
        </div>
        <form className="form" onSubmit={sendMessage}>
          <div>
            <label className="label">Your question</label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask about your risk, severity, or how the score was computed."
            />
          </div>
          <button className="button" type="submit" disabled={loading}>
            {loading ? "Thinking..." : "Send"}
          </button>
        </form>
      </div>
    </section>
  );
}
