import asyncio
from typing import Any, Dict, Optional
from src.integrations.base import BaseEHRConnector, PatientEHRRecord


class FHIRClient(BaseEHRConnector):
    """
    Mock Production FHIR EHR System Connector with non-blocking async execution.
    """

    def __init__(self):
        # Seeded mock EHR records
        self._records: Dict[str, PatientEHRRecord] = {
            "P-1001": PatientEHRRecord(
                patient_id="P-1001",
                mrn="987654321",
                age=54,
                gender="Male",
                diagnoses=["Type 2 Diabetes Mellitus", "Essential Hypertension"],
                medications=["Metformin 1000mg", "Lisinopril 10mg"],
                allergies=["Penicillin"],
            ),
            "P-1002": PatientEHRRecord(
                patient_id="P-1002",
                mrn="123456789",
                age=62,
                gender="Female",
                diagnoses=["Atrial Fibrillation", "Chronic Kidney Disease Stage 3"],
                medications=["Warfarin 5mg", "Metoprolol 50mg"],
                allergies=["Sulfa"],
            ),
        }

    async def get_patient_record(self, patient_id: str) -> Optional[PatientEHRRecord]:
        await asyncio.sleep(0.02)  # Non-blocking async I/O simulation
        return self._records.get(patient_id)

    async def verify_drug_interaction(self, drug_a: str, drug_b: str) -> Dict[str, Any]:
        await asyncio.sleep(0.01)
        d_a, d_b = drug_a.lower(), drug_b.lower()
        if ("warfarin" in d_a and "aspirin" in d_b) or ("aspirin" in d_a and "warfarin" in d_b):
            return {
                "has_interaction": True,
                "severity": "HIGH",
                "description": "Increased risk of severe gastrointestinal bleeding.",
            }
        return {"has_interaction": False, "severity": "NONE", "description": "No major interactions noted."}
