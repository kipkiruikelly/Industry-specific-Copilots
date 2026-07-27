import pytest
from src.integrations.fhir_client import FHIRClient
from src.orchestration.state import AgentExecutionState, ExecutionStep
from src.orchestration.workflow import ClinicalWorkflowOrchestrator
from src.rag.hybrid_retriever import HybridRetriever
from src.rag.store import InMemoryVectorStore
from src.security.guardrails import SecurityGuardrails
from src.security.phi_redactor import PHIRedactor
from src.security.rbac import RBACFilterEngine, UserAuthContext


@pytest.mark.asyncio
async def test_workflow_orchestration_happy_path_and_fallback():
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

    auth_ctx = UserAuthContext(
        user_id="doc_101",
        role="physician",
        assigned_departments=["cardiology"],
    )

    state = AgentExecutionState(
        session_id="test-session-1",
        patient_id="P-1001",
        auth_context=auth_ctx,
        raw_query="What medications is Patient John Doe taking?",
    )

    final_state = await orchestrator.execute(state)

    assert final_state.current_step == ExecutionStep.COMPLETED
    assert "Metformin 1000mg" in final_state.synthesis_output
    assert final_state.latency_ms > 0
    assert len(final_state.execution_trace) > 0
