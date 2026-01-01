"""
Document ingestion endpoints
"""
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from typing import List
import PyPDF2
import io

from models.schemas import IngestDocumentRequest, IngestDocumentResponse
from services.rag_pipeline import RAGPipeline
from services.embedding_service import DeepSeekEmbeddingService
from services.llm_service import GeminiService

router = APIRouter()


@router.post("/document", response_model=IngestDocumentResponse)
async def ingest_document(request: Request, ingest_request: IngestDocumentRequest):
    """
    Ingest a document into the RAG system
    """
    try:
        embedding_service = DeepSeekEmbeddingService()
        llm_service = GeminiService()
        
        rag_pipeline = RAGPipeline(
            embedding_service=embedding_service,
            vector_db=request.app.state.weaviate_service,
            mongo_db=request.app.state.mongodb_service,
            llm_service=llm_service
        )
        
        result = await rag_pipeline.ingest_document(
            content=ingest_request.content,
            metadata=ingest_request.metadata,
            document_type=ingest_request.document_type
        )
        
        return IngestDocumentResponse(**result)
        
    except Exception as e:
        print(f"❌ Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pdf")
async def ingest_pdf(request: Request, file: UploadFile = File(...), metadata: dict = {}):
    """
    Ingest a PDF document
    """
    try:
        # Read PDF
        contents = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
        
        # Extract text
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
        
        # Prepare metadata
        doc_metadata = {
            "title": metadata.get("title", file.filename),
            "source_type": "pdf",
            "filename": file.filename,
            **metadata
        }
        
        # Ingest
        embedding_service = DeepSeekEmbeddingService()
        llm_service = GeminiService()
        
        rag_pipeline = RAGPipeline(
            embedding_service=embedding_service,
            vector_db=request.app.state.weaviate_service,
            mongo_db=request.app.state.mongodb_service,
            llm_service=llm_service
        )
        
        result = await rag_pipeline.ingest_document(
            content=text_content,
            metadata=doc_metadata,
            document_type="pdf"
        )
        
        return result
        
    except Exception as e:
        print(f"❌ PDF ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def ingest_batch(request: Request, documents: List[IngestDocumentRequest]):
    """
    Ingest multiple documents in batch
    """
    try:
        embedding_service = DeepSeekEmbeddingService()
        llm_service = GeminiService()
        
        rag_pipeline = RAGPipeline(
            embedding_service=embedding_service,
            vector_db=request.app.state.weaviate_service,
            mongo_db=request.app.state.mongodb_service,
            llm_service=llm_service
        )
        
        results = []
        for doc in documents:
            try:
                result = await rag_pipeline.ingest_document(
                    content=doc.content,
                    metadata=doc.metadata,
                    document_type=doc.document_type
                )
                results.append({
                    "status": "success",
                    "document_id": result["document_id"],
                    "chunks": result["chunks_created"]
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "total": len(documents),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"]),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
