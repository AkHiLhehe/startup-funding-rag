"""
FastAPI backend for Startup Investment Intelligence RAG System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import search, ingest, analytics, health
from core.config import settings
from services.weaviate_service import WeaviateService
from services.mongodb_service import MongoDBService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup and cleanup on shutdown"""
    # Startup
    print("🚀 Initializing Startup Investment Intelligence System...")
    
    # Initialize Weaviate
    app.state.weaviate_service = WeaviateService()
    await app.state.weaviate_service.initialize()
    
    # Initialize MongoDB
    app.state.mongodb_service = MongoDBService()
    await app.state.mongodb_service.connect()
    
    print("✅ All services initialized successfully")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down services...")
    await app.state.weaviate_service.close()
    await app.state.mongodb_service.disconnect()
    print("✅ Shutdown complete")


app = FastAPI(
    title="Startup Investment Intelligence API",
    description="Production-grade RAG system for startup and investor intelligence",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    return {
        "message": "Startup Investment Intelligence API",
        "version": "1.0.0",
        "status": "operational"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
