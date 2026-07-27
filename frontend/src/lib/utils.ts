import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchClinicalQuery(query: string, patientId?: string) {
  const res = await fetch(`${API_BASE_URL}/clinical/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Tenant-ID": "tenant-default",
    },
    body: JSON.stringify({
      query,
      patient_id: patientId || "P-1001",
      user_id: "dr_smith",
      user_role: "physician",
      departments: ["cardiology", "endocrinology"],
    }),
  });
  if (!res.ok) throw new Error("Failed to query clinical backend");
  return res.json();
}
