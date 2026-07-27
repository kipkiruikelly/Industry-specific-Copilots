"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  Bot,
  FileText,
  LayoutDashboard,
  Lock,
  Search,
  Settings,
  Users,
  ShieldCheck,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Overview Dashboard", href: "/", icon: LayoutDashboard },
  { name: "AI Clinical Copilot", href: "/copilot", icon: Bot, badge: "Live SSE" },
  { name: "Patient EHR Directory", href: "/patients", icon: Users },
  { name: "Document Semantic Search", href: "/search", icon: Search },
  { name: "Analytics & Latency", href: "/analytics", icon: Activity },
  { name: "Security & Compliance", href: "/security", icon: ShieldCheck },
  { name: "Multi-Tenant Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between h-screen fixed left-0 top-0 z-40">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-800 bg-slate-950/50">
          <div className="p-2 bg-sky-600 rounded-lg text-white">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-white text-base tracking-tight">MediCopilot</h1>
            <p className="text-xs text-slate-400">Enterprise AI Healthcare</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                  isActive
                    ? "bg-sky-600/10 text-sky-400 border border-sky-500/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                )}
              >
                <div className="flex items-center gap-3">
                  <Icon className={cn("w-4 h-4", isActive ? "text-sky-400" : "text-slate-500")} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] bg-sky-500/20 text-sky-300 font-semibold px-2 py-0.5 rounded-full border border-sky-500/30">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Compliance Footer Badge */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-950/30">
        <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
          <Lock className="w-3.5 h-3.5" />
          <span>HIPAA & PHI Protected</span>
        </div>
        <p className="text-[11px] text-slate-500 mt-1">Tenant ID: tenant-enterprise-01</p>
      </div>
    </aside>
  );
}
