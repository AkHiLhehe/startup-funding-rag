# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .rag_pipeline import analyst_app

app = FastAPI(title="AI Investment Analyst")

class QueryRequest(BaseModel):
    query: str
    language: str

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        # Executes the LangGraph workflow
        result = analyst_app.invoke({
            "query": request.query, 
            "indic_language": request.language
        })
        return {
            "answer": result["answer"],
            "sources": result.get("sources", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))