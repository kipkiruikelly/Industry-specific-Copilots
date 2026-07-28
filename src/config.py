import os

class Settings:
    PROJECT_NAME: str = "MediCopilot Healthcare AI Platform"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/medicopilot"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Auth / JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super-secret-enterprise-key-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Vector DB Provider: pgvector, qdrant, pinecone, in_memory
    VECTOR_PROVIDER: str = os.getenv("VECTOR_PROVIDER", "in_memory")
    
    # Security & Guardrails
    ENABLE_GUARDRAILS: bool = True
    ENABLE_PHI_REDACTION: bool = True

settings = Settings()
