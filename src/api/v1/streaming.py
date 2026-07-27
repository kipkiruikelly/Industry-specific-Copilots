import asyncio
import json
import uuid
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import StreamingResponse
from src.api.schemas import ClinicalQueryRequest
from src.orchestration.state import AgentExecutionState
from src.orchestration.workflow import ClinicalWorkflowOrchestrator
from src.security.oauth import get_current_user_auth
from src.security.rbac import UserAuthContext

router = APIRouter(prefix="/clinical", tags=["Real-time Streaming EHR Synthesis"])


async def event_generator(
    raw_query: str,
    patient_id: Optional[str],
    auth_ctx: UserAuthContext,
    orchestrator: ClinicalWorkflowOrchestrator,
) -> AsyncGenerator[str, None]:
    """
    Server-Sent Events (SSE) Real-Time Token & Execution State Streamer.
    Outputs state updates, retrieved evidence, token chunks, and completion events.
    """
    session_id = str(uuid.uuid4())
    state = AgentExecutionState(
        session_id=session_id,
        patient_id=patient_id,
        auth_context=auth_ctx,
        raw_query=raw_query,
    )

    # Event 1: Init Stream
    yield f"data: {json.dumps({'event': 'init', 'session_id': session_id, 'step': 'VALIDATE'})}\n\n"
    await asyncio.sleep(0.01)

    # Execute State Machine Workflow
    final_state = await orchestrator.execute(state)

    # Event 2: Execution Step Trace
    for trace in final_state.execution_trace:
        yield f"data: {json.dumps({'event': 'trace', 'trace': trace})}\n\n"
        await asyncio.sleep(0.01)

    # Event 3: Token Streaming Simulation
    text = final_state.synthesis_output
    words = text.split()
    for i in range(0, len(words), 3):
        chunk = " ".join(words[i : i + 3]) + " "
        yield f"data: {json.dumps({'event': 'token_chunk', 'text': chunk})}\n\n"
        await asyncio.sleep(0.02)

    # Event 4: Complete Event
    yield f"data: {json.dumps({'event': 'complete', 'status': final_state.current_step.value, 'latency_ms': final_state.latency_ms})}\n\n"


@router.get("/stream")
async def stream_clinical_query(
    query: str = Query(..., description="Clinical Query Text"),
    patient_id: Optional[str] = Query(None, description="Optional Patient ID"),
    auth_ctx: UserAuthContext = Depends(get_current_user_auth),
):
    """
    Server-Sent Events (SSE) Endpoint for Streaming AI Synthesis.
    """
    from src.api.v1.clinical import orchestrator

    return StreamingResponse(
        event_generator(
            raw_query=query,
            patient_id=patient_id,
            auth_ctx=auth_ctx,
            orchestrator=orchestrator,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
