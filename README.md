# MediCopilot - Production Enterprise Healthcare Copilot

MediCopilot is a production-grade, enterprise-ready **Healthcare & EHR Synthesis AI Agent** built with Python (FastAPI/Pydantic v2), LangGraph state machine orchestration patterns, Hybrid RAG (Dense Vector + BM25 with RRF), HIPAA PHI redaction, and RBAC metadata security filters.

## System Architecture

```
[ HTTP API Request ] -> [ FastAPI Controller (/api/v1/clinical/query) ]
                              │
                              ▼
                [ Clinical Workflow Orchestrator ]
                              │
  ┌───────────────────────────┼───────────────────────────┐
  │                           │                           │
  ▼                           ▼                           ▼
[ Guardrails Engine ]  [ PHI Redactor Engine ]    [ RBAC Filter Engine ]
(Prompt Injection)    (18 HIPAA Identifiers)     (Clearance & Dept Scoping)
                              │                           │
                              └─────────────┬─────────────┘
                                            ▼
                                [ Hybrid RAG Retriever ]
                                (Dense Cosine + Lexical BM25)
                                            │
                                            ▼
                                  [ FHIR EHR Connector ]
                                            │
                                            ▼
                               [ Response Synthesis & Audit ]
```

## Setup & Running Locally

### 1. Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Running Unit Tests
```bash
PYTHONPATH=. ./venv/bin/pytest -v
```

### 3. Launching FastAPI Server
```bash
./venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
Access interactive API documentation at `http://localhost:8000/api/v1/docs`.
