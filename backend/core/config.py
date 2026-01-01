"""
Configuration management for the application
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Startup Investment Intelligence"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Gemini API Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))
    GEMINI_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "8192"))
    
    # DeepSeek Embeddings Settings
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_EMBEDDING_MODEL: str = os.getenv("DEEPSEEK_EMBEDDING_MODEL", "deepseek-chat")
    
    # Voyage AI Embeddings Settings
    VOYAGE_API_KEY: str = os.getenv("VOYAGE_API_KEY", "")
    
    # Tavily Search Settings
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1024"))
    
    # Weaviate Settings
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY: str = os.getenv("WEAVIATE_API_KEY", "")
    WEAVIATE_USE_EMBEDDED: bool = os.getenv("WEAVIATE_USE_EMBEDDED", "False") == "True"
    
    # MongoDB Settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "startup_intelligence")
    
    # RAG Settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "10"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # Citation Settings
    ENABLE_CITATION_VERIFICATION: bool = True
    MIN_CITATION_CONFIDENCE: float = 0.8
    MAX_CITATIONS_PER_RESPONSE: int = 10
    
    # Evaluation Metrics Settings
    ENABLE_METRICS: bool = True
    METRICS_LOG_PATH: str = os.getenv("METRICS_LOG_PATH", "./logs/metrics.json")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
