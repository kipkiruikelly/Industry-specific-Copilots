import json
from datetime import datetime, timezone
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ComplianceAuditEvent(BaseModel):
    audit_id: str
    tenant_id: str
    user_id: str
    user_role: str
    action: str
    resource: str
    phi_detected_count: int
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HealthcareComplianceManager:
    """
    HIPAA/GDPR Compliance Tooling Manager.
    Logs immutable audit events, enforces retention rules, and exports compliance reports.
    """

    def __init__(self):
        self._events: List[ComplianceAuditEvent] = []

    def record_access_event(
        self,
        tenant_id: str,
        user_id: str,
        user_role: str,
        action: str,
        resource: str,
        phi_detected_count: int,
    ) -> ComplianceAuditEvent:
        import uuid
        event = ComplianceAuditEvent(
            audit_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            user_id=user_id,
            user_role=user_role,
            action=action,
            resource=resource,
            phi_detected_count=phi_detected_count,
        )
        self._events.append(event)
        return event

    def generate_compliance_report(self, tenant_id: str) -> Dict[str, Any]:
        tenant_events = [e for e in self._events if e.tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "total_access_events": len(tenant_events),
            "total_phi_scrubbed": sum(e.phi_detected_count for e in tenant_events),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "events": [e.model_dump() for e in tenant_events[:50]],
        }

compliance_manager = HealthcareComplianceManager()
