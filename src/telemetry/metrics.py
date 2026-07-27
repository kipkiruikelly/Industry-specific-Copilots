from typing import Dict
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Prometheus Monitoring Metrics
HTTP_REQUESTS_TOTAL = Counter(
    "medicopilot_http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "medicopilot_http_request_duration_seconds",
    "HTTP Request Latency Seconds",
    ["endpoint"],
)

CLINICAL_QUERIES_TOTAL = Counter(
    "medicopilot_clinical_queries_total",
    "Total Clinical EHR Queries Synthesized",
    ["status", "threat_category"],
)

RETRIEVAL_LATENCY_SECONDS = Histogram(
    "medicopilot_retrieval_latency_seconds",
    "Hybrid RAG Retrieval Latency Seconds",
)


def get_prometheus_metrics() -> bytes:
    """Export Prometheus Metrics Output."""
    return generate_latest()
