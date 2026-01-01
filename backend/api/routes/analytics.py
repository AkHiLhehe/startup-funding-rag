"""
Analytics and metrics endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from typing import Optional

from services.evaluation_service import EvaluationMetrics

router = APIRouter()


@router.get("/metrics")
async def get_metrics(last_n: Optional[int] = None):
    """
    Get aggregate metrics for the system
    """
    try:
        evaluation_service = EvaluationMetrics()
        await evaluation_service.load_metrics_from_file()
        
        metrics = evaluation_service.get_aggregate_metrics(last_n=last_n)
        return metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queries")
async def get_query_history(request: Request, limit: int = 100):
    """
    Get recent query history
    """
    try:
        query_logs = await request.app.state.mongodb_service.get_query_logs(limit=limit)
        return {
            "total": len(query_logs),
            "queries": query_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics(request: Request):
    """
    Get system statistics
    """
    try:
        # Get counts from MongoDB
        db = request.app.state.mongodb_service.db
        
        startup_count = await db.startups.count_documents({})
        investor_count = await db.investors.count_documents({})
        funding_count = await db.funding_rounds.count_documents({})
        document_count = await db.documents.count_documents({})
        
        return {
            "startups": startup_count,
            "investors": investor_count,
            "funding_rounds": funding_count,
            "documents": document_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/match")
async def match_entities(request: Request, entity_id: str, entity_type: str, top_k: int = 10):
    """
    Find matching investors for a startup or vice versa
    """
    try:
        from services.llm_service import GeminiService
        
        llm_service = GeminiService()
        
        # Get entity from database
        if entity_type == "startup":
            entity = await request.app.state.mongodb_service.get_startup(entity_id)
            if not entity:
                raise HTTPException(status_code=404, detail="Startup not found")
            
            # Search for matching investors
            # This would involve semantic search + LLM analysis
            # Simplified version:
            return {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "message": "Matching functionality requires further implementation"
            }
            
        elif entity_type == "investor":
            entity = await request.app.state.mongodb_service.get_investor(entity_id)
            if not entity:
                raise HTTPException(status_code=404, detail="Investor not found")
            
            return {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "message": "Matching functionality requires further implementation"
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid entity type")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
