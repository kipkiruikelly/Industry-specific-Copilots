import pytest
from src.integrations.fhir_client import FHIRClient
from src.orchestration.state import AgentExecutionState, ExecutionStep
from src.orchestration.workflow import ClinicalWorkflowOrchestrator
from src.rag.hybrid_retriever import HybridRetriever
from src.rag.store import ClinicalDocument, InMemoryVectorStore
from src.security.guardrails import SecurityGuardrails
from src.security.phi_redactor import PHIRedactor
from src.security.rbac import RBACFilterEngine, UserAuthContext
from src.telemetry.compliance import compliance_manager


@pytest.mark.asyncio
async def test_full_end_to_end_clinical_pipeline():
    # 1. Setup Component Architecture
    store = InMemoryVectorStore()
    retriever = HybridRetriever(vector_store=store)
    fhir_client = FHIRClient()
    redactor = PHIRedactor()
    guardrails = SecurityGuardrails()
    rbac_engine = RBACFilterEngine()

    orchestrator = ClinicalWorkflowOrchestrator(
        retriever=retriever,
        fhir_client=fhir_client,
        redactor=redactor,
        guardrails=guardrails,
        rbac_engine=rbac_engine,
    )

    # 2. Seed Clinical Document
    doc = ClinicalDocument(
        id="doc-e2e-1",
        patient_id="P-1001",
        content="Patient John Doe DOB: 05/12/1980 taking Metformin 1000mg.",
        required_clearance=1,
        department="cardiology",
    )
    await store.add_documents([doc])

    # 3. Simulate Authenticated Multi-tenant Request
    auth_ctx = UserAuthContext(
        user_id="doc_smith_e2e",
        role="physician",
        assigned_departments=["cardiology"],
    )

    raw_query = "What is the medication plan for Patient John Doe DOB 05/12/1980?"
    state = AgentExecutionState(
        session_id="e2e-session-123",
        patient_id="P-1001",
        auth_context=auth_ctx,
        raw_query=raw_query,
    )

    # 4. Execute Orchestrated Pipeline
    final_state = await orchestrator.execute(state)

    # 5. Assert End-to-End Success
    assert final_state.current_step == ExecutionStep.COMPLETED
    assert "Metformin 1000mg" in final_state.synthesis_output
    assert final_state.latency_ms > 0

    # 6. Compliance Event Logging
    compliance_event = compliance_manager.record_access_event(
        tenant_id="tenant-e2e",
        user_id=auth_ctx.user_id,
        user_role=auth_ctx.role,
        action="EHR_QUERY_SYNTHESIS",
        resource="P-1001",
        phi_detected_count=len(final_state.redacted_tokens),
    )
    assert compliance_event.phi_detected_count > 0
