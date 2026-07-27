"use client";

import { Activity, Bot, ShieldCheck, Users, Zap, FileText, ArrowUpRight, Lock } from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="p-6 bg-gradient-to-r from-sky-900/40 via-slate-900 to-indigo-900/30 rounded-2xl border border-sky-500/20 flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold px-2.5 py-1 bg-sky-500/20 text-sky-300 rounded-full border border-sky-500/30">
            Enterprise MediCopilot v2.0
          </span>
          <h2 className="text-2xl font-bold text-white mt-2">Clinical EHR Synthesis Dashboard</h2>
          <p className="text-slate-400 text-sm mt-1">
            Real-time hybrid RAG, HIPAA PHI redaction, and FHIR patient record integration active.
          </p>
        </div>
        <Link
          href="/copilot"
          className="px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-medium rounded-xl text-sm transition flex items-center gap-2 shadow-lg shadow-sky-600/20"
        >
          <Bot className="w-4 h-4" />
          <span>Launch AI Copilot</span>
        </Link>
      </div>

      {/* Metrics Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Daily EHR Queries</span>
            <Zap className="w-4 h-4 text-sky-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-3">1,482</p>
          <p className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <ArrowUpRight className="w-3 h-3" /> +14.2% from yesterday
          </p>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Avg Retrieval Latency</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-3">28.4 ms</p>
          <p className="text-xs text-slate-400 mt-1">Hybrid Vector + BM25 RRF</p>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>PHI Tokens Redacted</span>
            <Lock className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-3">8,920</p>
          <p className="text-xs text-emerald-400 mt-1">100% HIPAA Compliant</p>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Active Patients Managed</span>
            <Users className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-3">452</p>
          <p className="text-xs text-slate-400 mt-1">FHIR v4 Synchronized</p>
        </div>
      </div>

      {/* Recent Activity Table */}
      <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl">
        <h3 className="text-lg font-bold text-white mb-4">Recent Clinical Query Logs</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="text-xs text-slate-400 bg-slate-800/50 uppercase border-b border-slate-800">
              <tr>
                <th className="px-4 py-3">Patient ID</th>
                <th className="px-4 py-3">Query Summary</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">PHI Scrubbed</th>
                <th className="px-4 py-3">Latency</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              <tr>
                <td className="px-4 py-3 font-medium text-white">P-1001</td>
                <td className="px-4 py-3">Metformin dosage for Type 2 Diabetes</td>
                <td className="px-4 py-3">Physician</td>
                <td className="px-4 py-3 text-amber-400 font-semibold">2 tokens</td>
                <td className="px-4 py-3">24.2 ms</td>
                <td className="px-4 py-3"><span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">COMPLETED</span></td>
              </tr>
              <tr>
                <td className="px-4 py-3 font-medium text-white">P-1002</td>
                <td className="px-4 py-3">Warfarin & Aspirin drug interaction check</td>
                <td className="px-4 py-3">Physician</td>
                <td className="px-4 py-3 text-amber-400 font-semibold">1 token</td>
                <td className="px-4 py-3">31.0 ms</td>
                <td className="px-4 py-3"><span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">COMPLETED</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
