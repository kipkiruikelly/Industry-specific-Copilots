"use client";

import { Bell, Shield, User, Building2 } from "lucide-react";

export function TopNav() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur px-8 flex items-center justify-between sticky top-0 z-30 ml-64">
      {/* Search / Context Status */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
          <Building2 className="w-3.5 h-3.5 text-sky-400" />
          <span>Organization: St. Jude Medical System</span>
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>FastAPI Engine: Active</span>
        </div>
      </div>

      {/* User Actions */}
      <div className="flex items-center gap-4">
        <button className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition">
          <Bell className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-sky-600 flex items-center justify-center font-bold text-xs text-white">
            DS
          </div>
          <div className="text-left hidden sm:block">
            <p className="text-xs font-semibold text-white">Dr. Sarah Smith, MD</p>
            <p className="text-[11px] text-slate-400">Chief of Cardiology</p>
          </div>
        </div>
      </div>
    </header>
  );
}
