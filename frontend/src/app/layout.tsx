import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopNav } from "@/components/layout/TopNav";

export const metadata = {
  title: "MediCopilot - Enterprise Healthcare AI Platform",
  description: "Production-grade, enterprise-ready Healthcare EHR & Clinical Synthesis Copilot",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <TopNav />
          <main className="p-8 ml-64 flex-1">{children}</main>
        </div>
      </body>
    </html>
  );
}
