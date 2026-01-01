"""
Health check endpoint
"""
from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "weaviate": "connected" if hasattr(request.app.state, 'weaviate_service') else "disconnected",
            "mongodb": "connected" if hasattr(request.app.state, 'mongodb_service') else "disconnected"
        }
    }


@router.get("/info")
async def system_info():
    """System information endpoint"""
    from core.config import settings
    
    return {
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "features": {
            "rag_pipeline": True,
            "citation_tracking": settings.ENABLE_CITATION_VERIFICATION,
            "evaluation_metrics": settings.ENABLE_METRICS
        },
        "models": {
            "llm": settings.GEMINI_MODEL,
            "embeddings": settings.DEEPSEEK_EMBEDDING_MODEL
        }
    }
