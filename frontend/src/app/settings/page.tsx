"use client";

import { Settings, Building2, Database, Sliders } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Multi-Tenant System & Vector Settings</h2>
        <p className="text-slate-400 text-sm">Configure AI models, vector search providers, and tenant quotas</p>
      </div>

      <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl space-y-6">
        <div className="space-y-4">
          <h3 className="font-bold text-white text-base">Vector Search Provider</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-sky-600/10 border border-sky-500/30 rounded-xl text-sky-300 font-semibold text-sm flex items-center justify-between">
              <span>PostgreSQL (pgvector)</span>
              <span className="text-xs bg-sky-500/20 px-2 py-0.5 rounded">Active</span>
            </div>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-slate-400 text-sm flex items-center justify-between">
              <span>Qdrant Cloud</span>
              <span className="text-xs text-slate-500">Standby</span>
            </div>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-slate-400 text-sm flex items-center justify-between">
              <span>Pinecone</span>
              <span className="text-xs text-slate-500">Standby</span>
            </div>
          </div>
        </div>

        <div className="space-y-4 pt-4 border-t border-slate-800">
          <h3 className="font-bold text-white text-base">Tenant Organization Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-400 font-medium">Tenant Slug</label>
              <input
                type="text"
                disabled
                value="tenant-enterprise-01"
                className="w-full mt-1 px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-300"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 font-medium">Assigned Clearance Level</label>
              <input
                type="text"
                disabled
                value="Level 3 (Full EHR Access)"
                className="w-full mt-1 px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-300"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
