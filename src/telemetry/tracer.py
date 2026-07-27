from typing import Optional
from src.config import settings

# OpenTelemetry Distributed Tracing Setup
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    provider = TracerProvider(resource=Resource.create({"service.name": settings.PROJECT_NAME}))
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("medicopilot.tracer")
except ImportError:
    tracer = None


def get_tracer():
    """Return OpenTelemetry Tracer instance."""
    return tracer
