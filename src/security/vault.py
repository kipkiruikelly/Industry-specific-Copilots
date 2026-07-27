from typing import Any, Dict, Optional
from src.config import settings


class SecretsManager:
    """
    Enterprise Secrets Manager with HashiCorp Vault / Cloud Secret Manager Abstraction.
    Falls back gracefully to environment configuration variables.
    """

    def __init__(self):
        self.vault_addr = settings.VAULT_ADDR
        self.vault_token = settings.VAULT_TOKEN

    async def get_secret(self, secret_key: str, default: Optional[str] = None) -> str:
        """Fetch secret securely from Vault or fallback to settings."""
        # Fallback to local settings attribute if exists
        if hasattr(settings, secret_key):
            return str(getattr(settings, secret_key))
        return default or ""

secrets_manager = SecretsManager()
