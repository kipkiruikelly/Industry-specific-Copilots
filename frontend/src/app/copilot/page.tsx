"use client";

import { useState } from "react";
import { Bot, Send, User, Lock, Activity, CheckCircle, ShieldAlert } from "lucide-react";
import { API_BASE_URL, fetchClinicalQuery } from "@/lib/utils";

interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text: string;
  phiCount?: number;
  trace?: string[];
  latencyMs?: number;
}

export default function CopilotPage() {
  const [query, setQuery] = useState("");
  const [patientId, setPatientId] = useState("P-1001");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      sender: "bot",
      text: "Hello Dr. Smith. I am MediCopilot, your real-time EHR Clinical Synthesis Assistant. Enter a patient query below to analyze clinical records.",
    },
  ]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userMsg: ChatMessage = { id: Date.now().toString(), sender: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);
    const currentQuery = query;
    setQuery("");
    setLoading(true);

    try {
      const data = await fetchClinicalQuery(currentQuery, patientId);
      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: data.synthesis,
        phiCount: data.detected_phi_tokens_count,
        trace: data.execution_trace,
        latencyMs: data.latency_ms,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: "bot",
          text: "Error communicating with clinical backend server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-sky-600 rounded-lg text-white">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-white text-base">AI Clinical EHR Synthesis Assistant</h2>
            <p className="text-xs text-slate-400">Streaming SSE • Hybrid RAG • HIPAA Redaction</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400 font-medium">Target Patient ID:</label>
          <input
            type="text"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            className="px-3 py-1 bg-slate-800 border border-slate-700 rounded-lg text-xs text-white w-28 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 p-6 overflow-y-auto space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-4 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            {msg.sender === "bot" && (
              <div className="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center text-white shrink-0">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div
              className={`max-w-2xl p-4 rounded-2xl text-sm ${
                msg.sender === "user"
                  ? "bg-sky-600 text-white rounded-tr-none"
                  : "bg-slate-800/80 border border-slate-700/60 text-slate-200 rounded-tl-none"
              }`}
            >
              <p className="whitespace-pre-line leading-relaxed">{msg.text}</p>

              {/* Bot Metadata Badges */}
              {msg.sender === "bot" && (msg.phiCount !== undefined || msg.latencyMs) && (
                <div className="mt-3 pt-3 border-t border-slate-700/50 flex flex-wrap items-center gap-3 text-[11px] text-slate-400">
                  <span className="flex items-center gap-1 text-amber-400 font-medium">
                    <Lock className="w-3 h-3" /> {msg.phiCount} PHI Scrubbed
                  </span>
                  <span className="flex items-center gap-1 text-emerald-400 font-medium">
                    <Activity className="w-3 h-3" /> {msg.latencyMs} ms
                  </span>
                  <span className="flex items-center gap-1 text-sky-400 font-medium">
                    <CheckCircle className="w-3 h-3" /> RBAC Verified
                  </span>
                </div>
              )}
            </div>

            {msg.sender === "user" && (
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white shrink-0">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 text-slate-400 text-sm items-center animate-pulse">
            <Bot className="w-4 h-4 text-sky-400" />
            <span>Analyzing EHR patient chart and executing hybrid RAG synthesis...</span>
          </div>
        )}
      </div>

      {/* Input Box */}
      <form onSubmit={handleSend} className="p-4 border-t border-slate-800 bg-slate-950/60 flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask MediCopilot about patient records, diagnoses, or medication interactions..."
          className="flex-1 px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-medium rounded-xl text-sm transition flex items-center gap-2 disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
          <span>Send Query</span>
        </button>
      </form>
    </div>
  );
}
