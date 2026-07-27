"use client";

import { useState } from "react";
import { Search, FileText, Database, Shield, Zap } from "lucide-react";

export default function SearchPage() {
  const [query, setQuery] = useState("Metformin dosage diabetes");
  const [searched, setSearched] = useState(false);

  const results = [
    {
      id: "doc-1",
      patientId: "P-1001",
      department: "endocrinology",
      content: "Metformin initial dosage for Type 2 Diabetes is 500mg orally twice daily with meals.",
      score: 0.89,
      type: "hybrid",
    },
    {
      id: "doc-2",
      patientId: "P-1002",
      department: "cardiology",
      content: "Warfarin interaction notice: Avoid co-administration with high-dose Aspirin due to GI hemorrhage risk.",
      score: 0.72,
      type: "bm25",
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Hybrid Clinical Document Search</h2>
        <p className="text-slate-400 text-sm">Dense Cosine Vectors + Lexical BM25 with Reciprocal Rank Fusion (RRF)</p>
      </div>

      <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-2xl flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search clinical guidelines, EHR notes, or drug protocols..."
          className="flex-1 px-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-sky-500"
        />
        <button
          onClick={() => setSearched(true)}
          className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-medium rounded-xl text-sm transition flex items-center gap-2"
        >
          <Search className="w-4 h-4" />
          <span>Hybrid Search</span>
        </button>
      </div>

      <div className="space-y-4">
        {results.map((r) => (
          <div key={r.id} className="p-5 bg-slate-900/60 border border-slate-800 rounded-2xl space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-sky-400">{r.id} • Patient {r.patientId}</span>
              <span className="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-400 font-semibold rounded-full border border-emerald-500/20">
                RRF Fusion Score: {r.score}
              </span>
            </div>
            <p className="text-sm text-slate-200 leading-relaxed">{r.content}</p>
            <div className="flex items-center gap-3 text-xs text-slate-400">
              <span>Department: {r.department}</span>
              <span>•</span>
              <span className="uppercase text-indigo-400 font-semibold">{r.type} RETRIEVAL</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
