from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel


class PatientEHRRecord(BaseModel):
    patient_id: str
    mrn: str
    age: int
    gender: str
    diagnoses: list[str]
    medications: list[str]
    allergies: list[str]


class BaseEHRConnector(ABC):
    """
    Abstract Integration Connector for External EHR / FHIR systems.
    Isolated via Clean Interfaces/Abstract Classes.
    """

    @abstractmethod
    async def get_patient_record(self, patient_id: str) -> Optional[PatientEHRRecord]:
        """Fetch patient clinical chart by ID."""
        pass

    @abstractmethod
    async def verify_drug_interaction(self, drug_a: str, drug_b: str) -> Dict[str, Any]:
        """Check potential contraindications or drug interactions."""
        pass
