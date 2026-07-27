from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from src.rag.store import ClinicalDocument
from src.security.rbac import UserAuthContext


class ExecutionStep(str, Enum):
    VALIDATE = "validate"
    REDACT_INPUT = "redact_input"
    RETRIEVE_CONTEXT = "retrieve_context"
    SYNTHESIZE = "synthesize"
    AUDIT = "audit"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentExecutionState(BaseModel):
    session_id: str
    patient_id: Optional[str] = None
    auth_context: UserAuthContext
    raw_query: str
    sanitized_query: str = ""
    current_step: ExecutionStep = ExecutionStep.VALIDATE
    retrieved_documents: List[ClinicalDocument] = Field(default_factory=list)
    redacted_tokens: Dict[str, str] = Field(default_factory=dict)
    synthesis_output: str = ""
    error_message: Optional[str] = None
    execution_trace: List[str] = Field(default_factory=list)
    latency_ms: float = 0.0
