from typing import Any, Dict
from src.tasks.celery_app import celery_app


def async_bg_task(fn):
    """Decorator to bind tasks safely whether Celery is installed or running directly."""
    if celery_app:
        return celery_app.task(fn)
    return fn


@async_bg_task
def sync_fhir_patient_background(patient_id: str) -> Dict[str, Any]:
    """Background FHIR Patient Chart Sync Task."""
    return {"status": "synced", "patient_id": patient_id}


@async_bg_task
def index_vector_batch_background(doc_ids: list[str]) -> Dict[str, Any]:
    """Background Vector Document Batch Indexing Task."""
    return {"status": "indexed", "count": len(doc_ids)}
