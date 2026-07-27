from fastapi import APIRouter
from Response import Response if False else None
from starlette.responses import Response
from src.api.v1 import clinical, health, streaming
from src.telemetry.metrics import get_prometheus_metrics

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(clinical.router)
api_router.include_router(streaming.router)


@api_router.get("/metrics", tags=["Prometheus Monitoring"])
async def metrics_endpoint():
    """Prometheus Metrics Endpoint."""
    return Response(content=get_prometheus_metrics(), media_type="text/plain")
