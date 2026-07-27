"use client";

import { Activity, Cpu, HardDrive, Zap, RefreshCw } from "lucide-react";

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">System Analytics & Latency Observability</h2>
        <p className="text-slate-400 text-sm">Prometheus Metrics & OpenTelemetry Distributed Tracing Overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
          <p className="text-xs text-slate-400 font-medium">P99 Latency SLA</p>
          <p className="text-3xl font-bold text-emerald-400">32.1 ms</p>
          <p className="text-xs text-slate-500">Target: &lt; 100 ms</p>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
          <p className="text-xs text-slate-400 font-medium">Redis Cache Hit Ratio</p>
          <p className="text-3xl font-bold text-sky-400">94.8 %</p>
          <p className="text-xs text-slate-500">Distributed Query Caching</p>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
          <p className="text-xs text-slate-400 font-medium">Celery Background Workers</p>
          <p className="text-3xl font-bold text-indigo-400">8 Active</p>
          <p className="text-xs text-slate-500">0 Tasks in Dead-Letter Queue</p>
        </div>
      </div>

      <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl">
        <h3 className="font-bold text-white text-base mb-3">Live Telemetry Pipeline Status</h3>
        <p className="text-sm text-slate-300">
          OpenTelemetry tracing exporter connected to OTLP Collector and Prometheus metrics endpoint at <code className="text-sky-400 bg-slate-950 px-2 py-0.5 rounded">/api/v1/metrics</code>.
        </p>
      </div>
    </div>
  );
}
