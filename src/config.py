from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediCopilot - Enterprise Healthcare EHR AI Platform"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Debug
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Security & Guardrails
    ENABLE_PHI_REDACTION: bool = True
    ENABLE_GUARDRAILS: bool = True
    ALLOWED_ROLES: List[str] = ["physician", "nurse", "clinical_auditor", "admin", "tenant_admin"]
    SECRET_KEY: str = "super-secret-key-change-in-production-12345"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # OAuth2 / OIDC Settings
    OIDC_ISSUER: Optional[str] = None
    OIDC_CLIENT_ID: Optional[str] = None
    OIDC_JWKS_URI: Optional[str] = None
    
    # Database Settings (PostgreSQL + pgvector)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/medicopilot"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # Redis Cache & Broker Settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # Celery Background Processing
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Vector DB Abstraction Settings
    VECTOR_DB_PROVIDER: str = "pgvector"  # Options: "pgvector", "qdrant", "pinecone", "in_memory"
    VECTOR_DIMENSION: int = 1536
    RRF_K_PARAM: int = 60
    DEFAULT_TOP_K: int = 5
    
    # OpenTelemetry & Prometheus
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    ENABLE_PROMETHEUS: bool = True
    
    # Vault / Cloud Secret Manager
    VAULT_ADDR: Optional[str] = None
    VAULT_TOKEN: Optional[str] = None
    
    # Model Timeout Settings
    LLM_TIMEOUT_SECONDS: float = 15.0
    LLM_MAX_RETRIES: int = 3
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
