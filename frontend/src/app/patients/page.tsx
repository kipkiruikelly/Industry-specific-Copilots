"use client";

import { useState } from "react";
import { Users, Search, Filter, ShieldCheck, Heart, AlertTriangle } from "lucide-react";

export default function PatientsPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const patients = [
    {
      id: "P-1001",
      name: "John Doe",
      mrn: "987654321",
      age: 54,
      gender: "Male",
      diagnoses: ["Type 2 Diabetes Mellitus", "Essential Hypertension"],
      medications: ["Metformin 1000mg", "Lisinopril 10mg"],
      allergies: ["Penicillin"],
    },
    {
      id: "P-1002",
      name: "Jane Smith",
      mrn: "123456789",
      age: 62,
      gender: "Female",
      diagnoses: ["Atrial Fibrillation", "CKD Stage 3"],
      medications: ["Warfarin 5mg", "Metoprolol 50mg"],
      allergies: ["Sulfa"],
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Patient EHR Directory</h2>
          <p className="text-slate-400 text-sm">FHIR v4 Synchronized Clinical Records</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search MRN or Patient ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-sky-500 w-64"
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {patients.map((p) => (
          <div key={p.id} className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="font-bold text-white text-lg">{p.name}</h3>
                <p className="text-xs text-slate-400">ID: {p.id} • MRN: {p.mrn}</p>
              </div>
              <span className="px-3 py-1 bg-sky-500/10 text-sky-400 text-xs font-semibold rounded-full border border-sky-500/20">
                {p.age} y/o {p.gender}
              </span>
            </div>

            <div className="space-y-2">
              <p className="text-xs font-semibold text-slate-400">Diagnoses</p>
              <div className="flex flex-wrap gap-1.5">
                {p.diagnoses.map((d) => (
                  <span key={d} className="px-2.5 py-1 bg-slate-800 text-slate-200 text-xs rounded-lg border border-slate-700">
                    {d}
                  </span>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-xs font-semibold text-slate-400">Active Medications</p>
              <div className="flex flex-wrap gap-1.5">
                {p.medications.map((m) => (
                  <span key={m} className="px-2.5 py-1 bg-indigo-500/10 text-indigo-300 text-xs rounded-lg border border-indigo-500/20">
                    {m}
                  </span>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-xs font-semibold text-slate-400">Allergies</p>
              <span className="px-2.5 py-1 bg-rose-500/10 text-rose-300 text-xs rounded-lg border border-rose-500/20 font-medium">
                {p.allergies.join(", ")}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
