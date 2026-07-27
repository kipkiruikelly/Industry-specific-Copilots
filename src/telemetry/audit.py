import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict


class HIPAAAuditLogger:
    """
    HIPAA Audit Logger recording structured query contexts, authorization roles,
    execution latencies, and redacted PHI markers.
    """

    def __init__(self):
        self.logger = logging.getLogger("HIPAAAuditLogger")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)

    def log_event(self, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
        }
        self.logger.info(json.dumps(audit_entry))
        return audit_entry
