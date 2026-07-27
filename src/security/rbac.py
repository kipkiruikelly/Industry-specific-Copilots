from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class UserAuthContext(BaseModel):
    user_id: str
    role: str
    assigned_departments: List[str] = Field(default_factory=list)
    clearance_level: int = 1  # 1: Basic, 2: Sensitive, 3: Full EHR


class RBACFilterEngine:
    """
    Role-Based Access Control metadata filter builder for Vector and RAG stores.
    Ensures users only retrieve clinical documents matching their role and department permissions.
    """

    ROLE_CLEARANCE_MAP = {
        "physician": 3,
        "nurse": 2,
        "clinical_auditor": 2,
        "admin": 3,
        "patient": 1,
    }

    def build_metadata_filter(self, auth_context: UserAuthContext) -> Dict[str, Any]:
        """
        Build metadata filter query dictionary enforced at the vector retrieval layer.
        """
        user_clearance = self.ROLE_CLEARANCE_MAP.get(auth_context.role.lower(), 1)
        
        filter_dict: Dict[str, Any] = {
            "required_clearance": {"$lte": user_clearance}
        }

        # Department scoping if departments assigned
        if auth_context.assigned_departments and auth_context.role.lower() != "admin":
            filter_dict["department"] = {"$in": auth_context.assigned_departments}

        return filter_dict
