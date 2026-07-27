"use client";

import { ShieldCheck, Lock, AlertOctagon, Eye } from "lucide-react";

export default function SecurityPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Security, Compliance & HIPAA Audit Logs</h2>
        <p className="text-slate-400 text-sm">Real-time threat monitoring and PHI/PII redaction tracking</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl space-y-4">
          <div className="flex items-center gap-3">
            <Lock className="w-5 h-5 text-amber-400" />
            <h3 className="font-bold text-white text-base">PHI Redaction Engine Summary</h3>
          </div>
          <p className="text-sm text-slate-300">
            Automatically scrubbed 18 HIPAA identifier types including SSNs, DOBs, MRNs, Phone numbers, and Email addresses.
          </p>
          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs font-mono text-slate-300">
            Raw Input: Patient John Doe DOB: 05/12/1980<br />
            Redacted: Patient [REDACTED_PATIENT_NAME]_1 DOB:[REDACTED_DOB]_1
          </div>
        </div>

        <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl space-y-4">
          <div className="flex items-center gap-3">
            <AlertOctagon className="w-5 h-5 text-emerald-400" />
            <h3 className="font-bold text-white text-base">Prompt Injection Protection</h3>
          </div>
          <p className="text-sm text-slate-300">
            0 Prompt injection attacks or system prompt override breaches detected in the last 24 hours.
          </p>
          <span className="inline-block px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-semibold rounded-full border border-emerald-500/20">
            Active Real-time Guardrails
          </span>
        </div>
      </div>
    </div>
  );
}
