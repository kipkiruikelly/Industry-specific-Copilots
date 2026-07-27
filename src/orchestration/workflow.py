import asyncio
import time
from typing import Dict, List, Optional
from src.integrations.fhir_client import FHIRClient
from src.orchestration.state import AgentExecutionState, ExecutionStep
from src.rag.hybrid_retriever import HybridRetriever
from src.security.guardrails import SecurityGuardrails
from src.security.phi_redactor import PHIRedactor
from src.security.rbac import RBACFilterEngine


class ClinicalWorkflowOrchestrator:
    """
    Production-grade Clinical Agent Workflow Engine.
    Executes a deterministic state machine:
    1. Input Guardrail Validation
    2. PHI Redaction
    3. RBAC Hybrid RAG Retrieval
    4. Clinical EHR Query Synthesis
    5. Fallback Resilience & Latency Tracing
    """

    def __init__(
        self,
        retriever: HybridRetriever,
        fhir_client: FHIRClient,
        redactor: PHIRedactor,
        guardrails: SecurityGuardrails,
        rbac_engine: RBACFilterEngine,
    ):
        self.retriever = retriever
        self.fhir_client = fhir_client
        self.redactor = redactor
        self.guardrails = guardrails
        self.rbac_engine = rbac_engine

    async def execute(self, state: AgentExecutionState) -> AgentExecutionState:
        start_time = time.perf_counter()

        try:
            # Step 1: Input Guardrail Check
            state.current_step = ExecutionStep.VALIDATE
            state.execution_trace.append("Step 1: Security Guardrails Validation")
            guardrail_res = self.guardrails.validate_input(state.raw_query)
            if not guardrail_res.is_safe:
                state.current_step = ExecutionStep.FAILED
                state.error_message = f"Guardrail Violation: {guardrail_res.reason}"
                state.execution_trace.append(f"FAILED: {guardrail_res.reason}")
                return state

            # Step 2: PHI Redaction
            state.current_step = ExecutionStep.REDACT_INPUT
            state.execution_trace.append("Step 2: PHI Redaction & Tokenization")
            redaction_res = self.redactor.redact(state.raw_query)
            state.sanitized_query = redaction_res.sanitized_text
            state.redacted_tokens = redaction_res.redacted_tokens

            # Step 3: RBAC Hybrid Retrieval
            state.current_step = ExecutionStep.RETRIEVE_CONTEXT
            state.execution_trace.append("Step 3: RBAC Metadata Filtered Hybrid Retrieval")
            rbac_filter = self.rbac_engine.build_metadata_filter(state.auth_context)

            # Retrieve vector/lexical search results with fallback tolerance
            search_results = await self.retriever.search(
                query=state.sanitized_query, top_k=3, metadata_filter=rbac_filter
            )
            state.retrieved_documents = [res.document for res in search_results]

            # Step 4: EHR Record Sync if patient_id present
            ehr_summary = ""
            if state.patient_id:
                patient_record = await self.fhir_client.get_patient_record(state.patient_id)
                if patient_record:
                    ehr_summary = (
                        f"EHR Clinical Record: Age {patient_record.age}, {patient_record.gender}. "
                        f"Diagnoses: {', '.join(patient_record.diagnoses)}. "
                        f"Meds: {', '.join(patient_record.medications)}."
                    )

            # Step 5: Clinical Synthesis
            state.current_step = ExecutionStep.SYNTHESIZE
            state.execution_trace.append("Step 4: Clinical Query Synthesis")

            if not state.retrieved_documents and not ehr_summary:
                # Deterministic Fallback Response
                state.synthesis_output = (
                    "Clinical Fallback Notice: No matching clinical records or guidelines "
                    "were retrieved under your current access clearance level."
                )
            else:
                doc_texts = "\n".join([f"- {d.content}" for d in state.retrieved_documents])
                raw_synthesis = (
                    f"Synthesized Clinical Insights for Query '{state.sanitized_query}':\n"
                    f"{ehr_summary}\n"
                    f"Retrieved Clinical Evidence:\n{doc_texts}"
                )
                # Un-redact for authorized consumers
                state.synthesis_output = self.redactor.restore(raw_synthesis, state.redacted_tokens)

            state.current_step = ExecutionStep.COMPLETED
            state.execution_trace.append("Step 5: Execution Completed Successfully")

        except Exception as e:
            state.current_step = ExecutionStep.FAILED
            state.error_message = f"Orchestration Error: {str(e)}"
            state.synthesis_output = "An unexpected error occurred while processing the clinical query."
            state.execution_trace.append(f"CRITICAL FAILURE: {str(e)}")

        finally:
            state.latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return state
