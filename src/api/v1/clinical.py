import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas import ClinicalQueryRequest, ClinicalQueryResponse
from src.integrations.fhir_client import FHIRClient
from src.orchestration.state import AgentExecutionState
from src.orchestration.workflow import ClinicalWorkflowOrchestrator
from src.rag.hybrid_retriever import HybridRetriever, MockEmbeddingGenerator
from src.rag.store import ClinicalDocument, InMemoryVectorStore
from src.security.guardrails import SecurityGuardrails
from src.security.phi_redactor import PHIRedactor
from src.security.rbac import RBACFilterEngine, UserAuthContext
from src.telemetry.audit import HIPAAAuditLogger

router = APIRouter(prefix="/clinical", tags=["Clinical Query & EHR Synthesis"])

# Initialize Global Shared Components
vector_store = InMemoryVectorStore()
retriever = HybridRetriever(vector_store=vector_store)
fhir_client = FHIRClient()
redactor = PHIRedactor()
guardrails = SecurityGuardrails()
rbac_engine = RBACFilterEngine()
audit_logger = HIPAAAuditLogger()

orchestrator = ClinicalWorkflowOrchestrator(
    retriever=retriever,
    fhir_client=fhir_client,
    redactor=redactor,
    guardrails=guardrails,
    rbac_engine=rbac_engine,
)

# Seed Sample Vector Documents
async def seed_documents():
    if not vector_store._docs:
        embedder = MockEmbeddingGenerator()
        doc1 = ClinicalDocument(
            id="doc-1",
            patient_id="P-1001",
            content="Metformin initial dosage for Type 2 Diabetes is 500mg orally twice daily with meals.",
            required_clearance=2,
            department="endocrinology",
            vector=embedder.embed_text("Metformin initial dosage for Type 2 Diabetes is 500mg orally twice daily with meals."),
        )
        doc2 = ClinicalDocument(
            id="doc-2",
            patient_id="P-1002",
            content="Warfarin interaction notice: Avoid co-administration with high-dose Aspirin due to GI hemorrhage risk.",
            required_clearance=2,
            department="cardiology",
            vector=embedder.embed_text("Warfarin interaction notice: Avoid co-administration with high-dose Aspirin due to GI hemorrhage risk."),
        )
        await vector_store.add_documents([doc1, doc2])


@router.post("/query", response_model=ClinicalQueryResponse)
async def process_clinical_query(req: ClinicalQueryRequest):
    """
    Process clinical EHR synthesis request through state machine orchestration,
    PHI redaction, and RBAC filtered hybrid RAG.
    """
    await seed_documents()

    session_id = str(uuid.uuid4())
    auth_ctx = UserAuthContext(
        user_id=req.user_id,
        role=req.user_role,
        assigned_departments=req.departments,
    )

    initial_state = AgentExecutionState(
        session_id=session_id,
        patient_id=req.patient_id,
        auth_context=auth_ctx,
        raw_query=req.query,
    )

    final_state = await orchestrator.execute(initial_state)

    audit_logger.log_event(
        event_type="CLINICAL_QUERY_PROCESSED",
        details={
            "session_id": session_id,
            "user_id": req.user_id,
            "role": req.user_role,
            "patient_id": req.patient_id,
            "latency_ms": final_state.latency_ms,
            "status": final_state.current_step.value,
        },
    )

    return ClinicalQueryResponse(
        session_id=final_state.session_id,
        status=final_state.current_step.value,
        synthesis=final_state.synthesis_output,
        execution_trace=final_state.execution_trace,
        detected_phi_tokens_count=len(final_state.redacted_tokens),
        latency_ms=final_state.latency_ms,
        error_message=final_state.error_message,
    )
