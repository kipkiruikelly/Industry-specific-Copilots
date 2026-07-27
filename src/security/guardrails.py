import re
from typing import Tuple
from pydantic import BaseModel


class GuardrailCheckResult(BaseModel):
    is_safe: bool
    reason: str = ""
    threat_category: str = "none"


class SecurityGuardrails:
    """
    Real-time safety and prompt injection guardrails engine.
    Detects malicious system prompt jailbreaks, unauthorized system instruction overrides,
    and out-of-scope domain commands.
    """

    PROMPT_INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
        re.compile(r"disregard\s+(system\s+)?prompts", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+(a|an)\s+unrestricted", re.IGNORECASE),
        re.compile(r"dump\s+all\s+(patient|user|database)\s+records", re.IGNORECASE),
        re.compile(r"<script.*?>", re.IGNORECASE),
        re.compile(r"DROP\s+TABLE|DELETE\s+FROM", re.IGNORECASE),
    ]

    def validate_input(self, prompt: str) -> GuardrailCheckResult:
        """
        Validate incoming user query against safety rules and prompt injection vectors.
        """
        if not prompt or not prompt.strip():
            return GuardrailCheckResult(is_safe=False, reason="Empty prompt provided", threat_category="validation_error")

        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if pattern.search(prompt):
                return GuardrailCheckResult(
                    is_safe=False,
                    reason="Potential prompt injection or security policy violation detected",
                    threat_category="prompt_injection",
                )

        return GuardrailCheckResult(is_safe=True, reason="Passes security checks", threat_category="none")
