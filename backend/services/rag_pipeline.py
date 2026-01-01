"""
RAG Pipeline for document ingestion and retrieval
Supports both local vector DB and real-time web search via Tavily
"""
from typing import List, Dict, Any, Optional
import re
import hashlib
from datetime import datetime

from services.embedding_service import DeepSeekEmbeddingService
from services.weaviate_service import WeaviateService
from services.mongodb_service import MongoDBService
from services.llm_service import GeminiService
from services.tavily_service import TavilyService
from core.config import settings


class RAGPipeline:
    def __init__(
        self,
        embedding_service: DeepSeekEmbeddingService,
        vector_db: WeaviateService,
        mongo_db: MongoDBService,
        llm_service: GeminiService,
        tavily_service: Optional[TavilyService] = None
    ):
        self.embedding_service = embedding_service
        self.vector_db = vector_db
        self.mongo_db = mongo_db
        self.llm_service = llm_service
        self.tavily_service = tavily_service or TavilyService()
    
    async def ingest_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        document_type: str = "article"
    ) -> Dict[str, Any]:
        """
        Ingest a document: chunk, embed, and store
        """
        try:
            # Generate source ID
            source_id = self._generate_source_id(content, metadata)
            
            # Check if document already exists
            existing_doc = await self.mongo_db.get_document(source_id)
            if existing_doc:
                return {
                    "status": "skipped",
                    "message": "Document already exists",
                    "document_id": source_id
                }
            
            # Chunk the document
            chunks = self._chunk_document(content)
            
            # Generate embeddings
            embeddings = await self.embedding_service.batch_generate_embeddings(chunks)
            
            # Determine collection based on document type
            collection_name = self._get_collection_name(metadata)
            
            # Prepare documents for vector DB
            documents = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                doc = {
                    "content": chunk,
                    "source_id": source_id,
                    "source_type": document_type,
                    "source_title": metadata.get("title", "Unknown"),
                    "source_url": metadata.get("url", ""),
                    "chunk_index": idx,
                    "published_date": metadata.get("published_date")
                }
                
                # Add entity-specific IDs
                if "startup_id" in metadata:
                    doc["startup_id"] = metadata["startup_id"]
                if "investor_id" in metadata:
                    doc["investor_id"] = metadata["investor_id"]
                if "round_id" in metadata:
                    doc["round_id"] = metadata["round_id"]
                
                documents.append(doc)
            
            # Store in vector database
            await self.vector_db.add_documents(collection_name, documents, embeddings)
            
            # Store metadata in MongoDB
            doc_metadata = {
                "source_id": source_id,
                "source_type": document_type,
                "title": metadata.get("title", "Unknown"),
                "url": metadata.get("url", ""),
                "published_date": metadata.get("published_date"),
                "num_chunks": len(chunks),
                "metadata": metadata
            }
            await self.mongo_db.create_document(doc_metadata)
            
            return {
                "status": "success",
                "message": "Document ingested successfully",
                "document_id": source_id,
                "chunks_created": len(chunks)
            }
            
        except Exception as e:
            print(f"❌ Error ingesting document: {e}")
            raise
    
    async def retrieve_and_generate(
        self,
        query: str,
        query_type: str = "general",
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        use_web_search: bool = True,  # New parameter for real-time search
        web_search_only: bool = False,  # New parameter to use ONLY web search
        response_language: Optional[str] = None  # Language for response
    ) -> Dict[str, Any]:
        """
        RAG: Retrieve relevant chunks and generate response
        Supports hybrid local + web search or web-only search
        
        Args:
            query: User query
            query_type: Type of query (startup_search, investor_search, etc.)
            top_k: Number of results to retrieve
            filters: Optional filters for local search
            use_web_search: Whether to include real-time web search
            web_search_only: If True, only search web (no local DB)
        """
        start_time = datetime.utcnow()
        
        try:
            local_results = []
            web_results = []
            
            # Local vector DB search (unless web_search_only)
            if not web_search_only:
                # Generate query embedding
                query_embedding = await self.embedding_service.generate_embedding(query)
                
                # Determine which collections to search
                collections = self._get_search_collections(query_type)
                
                # Retrieve from all relevant collections
                all_results = []
                for collection in collections:
                    results = await self.vector_db.hybrid_search(
                        collection_name=collection,
                        query_text=query,
                        query_vector=query_embedding,
                        limit=top_k,
                        alpha=0.7
                    )
                    all_results.extend(results)
                
                # Sort and filter local results
                all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
                local_results = [
                    r for r in all_results[:top_k]
                    if r.get('score', 0) >= settings.SIMILARITY_THRESHOLD
                ]
                print(f"📚 Local DB: Retrieved {len(local_results)} chunks")
            
            # Web search (if enabled)
            if use_web_search and self.tavily_service.enabled:
                print(f"🌐 Performing real-time web search...")
                
                # Determine search strategy based on query type
                if "investor" in query_type.lower() or any(kw in query.lower() for kw in ["vc", "investor", "fund", "venture capital"]):
                    tavily_results = await self.tavily_service.search_investor_info(query, max_results=5)
                else:
                    tavily_results = await self.tavily_service.search_startup_news(query, max_results=5)
                
                # Convert to RAG chunks
                web_chunks = self.tavily_service.format_as_rag_chunks(tavily_results)
                
                # Format web chunks to match local format
                for chunk in web_chunks:
                    web_results.append({
                        'properties': chunk,
                        'score': chunk.get('score', 0.8)  # Tavily results are pre-scored
                    })
                
                print(f"🌐 Web search: Retrieved {len(web_results)} chunks")
            
            # Combine results
            combined_results = local_results + web_results
            
            # Sort by score and take top_k
            combined_results.sort(key=lambda x: x.get('score', 0), reverse=True)
            filtered_results = combined_results[:top_k]
            
            print(f"📊 Total: {len(filtered_results)} chunks (Local: {len(local_results)}, Web: {len(web_results)})")
            
            if not filtered_results:
                return {
                    "query": query,
                    "answer": "I couldn't find sufficient relevant information to answer your query. Please try rephrasing or providing more context.",
                    "citations": [],
                    "retrieved_chunks": 0,
                    "processing_time": (datetime.utcnow() - start_time).total_seconds(),
                    "confidence_score": 0.0,
                    "sources": {
                        "local": 0,
                        "web": 0
                    }
                }
            
            # Generate response with citations
            try:
                generation_result = await self.llm_service.generate_with_citations(
                    query=query,
                    retrieved_chunks=filtered_results,
                    query_type=query_type,
                    response_language=response_language
                )
            except Exception as e:
                print(f"⚠️  LLM generation failed: {e}")
                # Fallback: return retrieved chunks as answer
                chunks_text = "\n\n".join([
                    f"[{i+1}] {chunk['properties'].get('source_title', 'Unknown')}: {chunk['properties'].get('content', '')[:200]}..."
                    for i, chunk in enumerate(filtered_results[:5])
                ])
                generation_result = {
                    "answer": f"Based on the retrieved documents:\n\n{chunks_text}",
                    "citations": [
                        {
                            "source_id": chunk['properties'].get('source_id', 'unknown'),
                            "source_type": chunk['properties'].get('source_type', 'document'),
                            "source_title": chunk['properties'].get('source_title', 'Unknown'),
                            "source_url": chunk['properties'].get('source_url', ''),
                            "excerpt": chunk['properties'].get('content', '')[:300],
                            "confidence_score": chunk.get('score', 0.5)
                        }
                        for chunk in filtered_results[:5]
                    ]
                }
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Calculate confidence score
            confidence = self._calculate_confidence(filtered_results, generation_result)
            
            return {
                "query": query,
                "answer": generation_result["answer"],
                "citations": generation_result["citations"],
                "retrieved_chunks": len(filtered_results),
                "processing_time": processing_time,
                "confidence_score": confidence,
                "sources": {
                    "local": len(local_results),
                    "web": len(web_results)
                },
                "metadata": {
                    "query_type": query_type,
                    "search_mode": "web_only" if web_search_only else ("hybrid" if use_web_search else "local"),
                    "collections_searched": [] if web_search_only else self._get_search_collections(query_type)
                }
            }
            
        except Exception as e:
            print(f"❌ Error in RAG pipeline: {e}")
            raise
    
    def _chunk_document(self, content: str) -> List[str]:
        """
        Chunk document with overlap for better context preservation
        """
        # Clean content
        content = re.sub(r'\s+', ' ', content).strip()
        
        chunks = []
        start = 0
        content_length = len(content)
        
        while start < content_length:
            end = start + settings.CHUNK_SIZE
            
            # Try to break at sentence boundary
            if end < content_length:
                # Look for sentence endings
                sentence_end = content.rfind('. ', start, end)
                if sentence_end != -1 and sentence_end > start + settings.CHUNK_SIZE // 2:
                    end = sentence_end + 1
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start with overlap
            start = end - settings.CHUNK_OVERLAP
        
        return chunks
    
    def _generate_source_id(self, content: str, metadata: Dict[str, Any]) -> str:
        """Generate unique source ID"""
        # Use URL if available, otherwise hash content
        if metadata.get('url'):
            return hashlib.md5(metadata['url'].encode()).hexdigest()
        else:
            content_hash = hashlib.md5(content[:1000].encode()).hexdigest()
            return f"doc_{content_hash}"
    
    def _get_collection_name(self, metadata: Dict[str, Any]) -> str:
        """Determine which collection to store in"""
        if "startup_id" in metadata:
            return "StartupDocument"
        elif "investor_id" in metadata:
            return "InvestorDocument"
        elif "round_id" in metadata:
            return "FundingDocument"
        else:
            return "StartupDocument"  # Default
    
    def _get_search_collections(self, query_type: str) -> List[str]:
        """Determine which collections to search based on query type"""
        if query_type == "investor_search":
            return ["InvestorDocument", "FundingDocument"]
        elif query_type == "startup_search":
            return ["StartupDocument", "FundingDocument"]
        elif query_type == "funding_analysis":
            return ["FundingDocument", "StartupDocument", "InvestorDocument"]
        else:
            return ["StartupDocument", "InvestorDocument", "FundingDocument"]
    
    def _calculate_confidence(
        self,
        results: List[Dict[str, Any]],
        generation_result: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for the response"""
        if not results:
            return 0.0
        
        # Average similarity of top results
        avg_similarity = sum(
            1 - r.get('distance', 1) for r in results[:5]
        ) / min(5, len(results))
        
        # Number of citations used
        citation_score = min(len(generation_result["citations"]) / 5, 1.0)
        
        # Combine scores
        confidence = (avg_similarity * 0.7) + (citation_score * 0.3)
        
        return round(confidence, 2)
