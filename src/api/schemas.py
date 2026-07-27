from typing import List, Optional
from pydantic import BaseModel, Field


class ClinicalQueryRequest(BaseModel):
    query: str = Field(..., example="What is the recommended dosage of Metformin for Patient John Doe DOB 05/12/1980?")
    patient_id: Optional[str] = Field(None, example="P-1001")
    user_id: str = Field(..., example="doc_smith_42")
    user_role: str = Field("physician", example="physician")
    departments: List[str] = Field(default_factory=lambda: ["cardiology"], example=["cardiology", "endocrinology"])


class ClinicalQueryResponse(BaseModel):
    session_id: str
    status: str
    synthesis: str
    execution_trace: List[str]
    detected_phi_tokens_count: int
    latency_ms: float
    error_message: Optional[str] = None
