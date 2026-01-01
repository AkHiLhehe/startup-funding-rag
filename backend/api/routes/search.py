"""
Search and query endpoints
Supports local DB search, real-time web search, and hybrid mode
"""
from fastapi import APIRouter, HTTPException, Request
from datetime import datetime

from models.schemas import SearchRequest, SearchResponse
from services.rag_pipeline import RAGPipeline
from services.embedding_service import DeepSeekEmbeddingService
from services.llm_service import GeminiService
from services.tavily_service import TavilyService
from services.evaluation_service import EvaluationMetrics

router = APIRouter()


@router.post("/", response_model=SearchResponse)
async def search(request: Request, search_request: SearchRequest):
    """
    Main search endpoint for RAG queries
    Supports local DB, real-time web search, or hybrid mode
    """
    try:
        # Initialize services
        embedding_service = DeepSeekEmbeddingService()
        llm_service = GeminiService()
        tavily_service = TavilyService()
        evaluation_service = EvaluationMetrics()
        
        rag_pipeline = RAGPipeline(
            embedding_service=embedding_service,
            vector_db=request.app.state.weaviate_service,
            mongo_db=request.app.state.mongodb_service,
            llm_service=llm_service,
            tavily_service=tavily_service
        )
        
        # Execute RAG pipeline with web search support
        result = await rag_pipeline.retrieve_and_generate(
            query=search_request.query,
            query_type=search_request.query_type.value,
            top_k=search_request.top_k or 10,
            filters=search_request.filters,
            use_web_search=search_request.use_web_search if hasattr(search_request, 'use_web_search') else True,
            web_search_only=search_request.web_search_only if hasattr(search_request, 'web_search_only') else False
        )
        
        # Evaluate and log metrics
        if search_request.include_citations:
            retrieval_metrics = await evaluation_service.evaluate_retrieval(
                query=search_request.query,
                retrieved_chunks=[]  # Would need to pass actual chunks
            )
            
            citation_metrics = await evaluation_service.evaluate_citations(
                response=result['answer'],
                citations=result['citations'],
                retrieved_chunks=[]
            )
            
            await evaluation_service.log_query_metrics(
                query=search_request.query,
                response_data=result,
                additional_metrics={
                    **retrieval_metrics,
                    **citation_metrics
                }
            )
        
        # Log to MongoDB
        await request.app.state.mongodb_service.log_query({
            "query": search_request.query,
            "query_type": search_request.query_type.value,
            "response": result,
            "timestamp": datetime.utcnow()
        })
        
        return SearchResponse(**result)
        
    except Exception as e:
        import traceback
        print(f"❌ Search error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/investor/{investor_name}")
async def search_investor(request: Request, investor_name: str, web_search: bool = True):
    """
    Search for information about a specific investor
    Includes real-time web search by default
    """
    try:
        embedding_service = DeepSeekEmbeddingService()
        llm_service = GeminiService()
        tavily_service = TavilyService()
        
        rag_pipeline = RAGPipeline(
            embedding_service=embedding_service,
            vector_db=request.app.state.weaviate_service,
            mongo_db=request.app.state.mongodb_service,
            llm_service=llm_service,
            tavily_service=tavily_service
        )
        
        query = f"Tell me about {investor_name}, their investment thesis, portfolio companies, and investment focus areas."
        
        result = await rag_pipeline.retrieve_and_generate(
            query=query,
            query_type="investor_search",
            top_k=15,
            use_web_search=web_search
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/startup/{startup_name}")
async def search_startup(request: Request, startup_name: str, web_search: bool = True):
    """
    Search for information about a specific startup
    Includes real-time web search by default
    """
    try:
        embedding_service = DeepSeekEmbeddingService()
        llm_service = GeminiService()
        tavily_service = TavilyService()
        
        rag_pipeline = RAGPipeline(
            embedding_service=embedding_service,
            vector_db=request.app.state.weaviate_service,
            mongo_db=request.app.state.mongodb_service,
            llm_service=llm_service,
            tavily_service=tavily_service
        )
        
        query = f"Tell me about {startup_name}, their business model, funding history, and key metrics."
        
        result = await rag_pipeline.retrieve_and_generate(
            query=query,
            query_type="startup_search",
            top_k=15,
            use_web_search=web_search
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
