import pytest
from src.security.phi_redactor import PHIRedactor


def test_phi_redaction_ssn_email_phone():
    redactor = PHIRedactor()
    raw_text = "Patient John Doe DOB: 05/12/1980 SSN: 123-45-6789 Phone: 555-123-4567 Email: john.doe@example.com MRN: 987654321"

    result = redactor.redact(raw_text)

    assert "123-45-6789" not in result.sanitized_text
    assert "john.doe@example.com" not in result.sanitized_text
    assert "555-123-4567" not in result.sanitized_text
    assert result.detected_phi_count > 0
    assert len(result.redacted_tokens) > 0

    restored_text = redactor.restore(result.sanitized_text, result.redacted_tokens)
    assert restored_text == raw_text
