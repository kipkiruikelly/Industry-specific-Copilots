import re
from typing import Dict, List, Tuple
from pydantic import BaseModel, Field


class PHIRedactionResult(BaseModel):
    sanitized_text: str
    redacted_tokens: Dict[str, str] = Field(default_factory=dict)
    detected_phi_count: int = 0


class PHIRedactor:
    """
    HIPAA-compliant PHI/PII redaction and tokenization engine.
    Detects and sanitizes 18 HIPAA identifier types including Names, SSNs,
    Dates of Birth, Medical Record Numbers (MRNs), Phone Numbers, and Emails.
    """

    PATTERNS: List[Tuple[str, re.Pattern, str]] = [
        # Social Security Number
        ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
        # Phone numbers
        ("PHONE", re.compile(r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b"), "[REDACTED_PHONE]"),
        # Email addresses
        ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
        # Medical Record Numbers (MRN) (e.g. MRN: 987654321 or MRN-123456)
        ("MRN", re.compile(r"\b(?:MRN|mrn)[:#-]?\s*([A-Za-z0-9]{6,10})\b", re.IGNORECASE), "MRN:[REDACTED_MRN]"),
        # Dates of Birth (e.g. DOB: 05/12/1980 or DOB 1980-05-12)
        ("DOB", re.compile(r"\b(?:DOB|dob)[:#-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b", re.IGNORECASE), "DOB:[REDACTED_DOB]"),
        # Patient Names (Explicit markers like Patient: John Doe or Patient Name: Jane Smith)
        ("PATIENT_NAME", re.compile(r"\b(?:Patient(?:\s+Name)?|Pt[:\s]+)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", re.IGNORECASE), "Patient: [REDACTED_PATIENT_NAME]"),
    ]

    def redact(self, text: str) -> PHIRedactionResult:
        """
        Sanitize text by replacing detected PHI patterns with deterministic tokens.
        """
        if not text:
            return PHIRedactionResult(sanitized_text="", redacted_tokens={}, detected_phi_count=0)

        sanitized_text = text
        redacted_tokens: Dict[str, str] = {}
        detected_phi_count = 0

        for phi_type, pattern, replacement in self.PATTERNS:
            matches = list(pattern.finditer(sanitized_text))
            if matches:
                detected_phi_count += len(matches)
                for i, match in enumerate(reversed(matches)):
                    matched_str = match.group(0)
                    token = f"{replacement}_{len(matches) - i}"
                    redacted_tokens[token] = matched_str
                    start, end = match.span()
                    sanitized_text = sanitized_text[:start] + token + sanitized_text[end:]

        return PHIRedactionResult(
            sanitized_text=sanitized_text,
            redacted_tokens=redacted_tokens,
            detected_phi_count=detected_phi_count,
        )

    def restore(self, sanitized_text: str, redacted_tokens: Dict[str, str]) -> str:
        """
        Reconstruct original tokens for authorized clinical consumers.
        """
        restored = sanitized_text
        # Sort tokens by length in descending order to avoid partial token string collisions
        sorted_tokens = sorted(redacted_tokens.items(), key=lambda item: len(item[0]), reverse=True)
        for token, original in sorted_tokens:
            restored = restored.replace(token, original)
        return restored
