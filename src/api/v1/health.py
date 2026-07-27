from fastapi import APIRouter
from src.config import settings

router = APIRouter(prefix="/health", tags=["Health & Readiness"])


@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
