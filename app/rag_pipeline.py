# app/rag_pipeline.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import google.generativeai as genai
from .db_connectors import db

class GraphState(TypedDict):
    query: str
    indic_language: str
    retrieved_docs: List[dict]
    answer: str
    sources: List[str]

genai.configure(api_key="YOUR_GEMINI_KEY")
model = genai.GenerativeModel('gemini-1.5-pro')

def retrieve_node(state: GraphState):
    # Hybrid Search: Vector (DeepSeek) + Keyword
    collection = db.weaviate.collections.get("InvestmentData")
    # In production, use deepseek_client.embeddings.create(...) here
    results = collection.query.hybrid(query=state["query"], limit=3)
    
    docs = [{"content": r.properties['content'], "source": r.properties['source']} for r in results.objects]
    return {"retrieved_docs": docs, "sources": [d['source'] for d in docs]}

def reason_node(state: GraphState):
    context = "\n\n".join([f"Source: {d['source']}\n{d['content']}" for d in state["retrieved_docs"]])
    prompt = f"""
    Act as a Senior VC Analyst. Answer in {state['indic_language']}.
    Use ONLY the context. Cite sources as [Source Name].
    Context: {context}
    Question: {state['query']}
    """
    response = model.generate_content(prompt)
    return {"answer": response.text}

workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("reason", reason_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "reason")
workflow.add_edge("reason", END)
analyst_app = workflow.compile()