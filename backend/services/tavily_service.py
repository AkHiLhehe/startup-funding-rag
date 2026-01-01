"""
Tavily Search Service for real-time web search
Integrates web search results into RAG pipeline
"""
from typing import List, Dict, Any, Optional
import httpx
from datetime import datetime
import os

from core.config import settings


class TavilyService:
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.api_url = "https://api.tavily.com/search"
        self.timeout = 30.0
        
        if not self.api_key:
            print("⚠️  No Tavily API key found")
            self.enabled = False
        else:
            print("✅ Tavily search service initialized")
            self.enabled = True
    
    async def search(
        self,
        query: str,
        search_depth: str = "advanced",  # "basic" or "advanced"
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search the web using Tavily API
        
        Args:
            query: Search query
            search_depth: "basic" (faster) or "advanced" (more comprehensive)
            max_results: Maximum number of results (default 5)
            include_domains: Optional list of domains to include
            exclude_domains: Optional list of domains to exclude
            
        Returns:
            Dictionary with search results and metadata
        """
        if not self.enabled:
            return {
                "results": [],
                "error": "Tavily API key not configured"
            }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": search_depth,
                    "max_results": max_results,
                    "include_answer": True,  # Get AI-generated answer
                    "include_raw_content": True,  # Get full content
                    "include_images": False
                }
                
                if include_domains:
                    payload["include_domains"] = include_domains
                if exclude_domains:
                    payload["exclude_domains"] = exclude_domains
                
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                data = response.json()
                return self._format_results(data)
                
        except httpx.TimeoutException:
            return {
                "results": [],
                "error": "Tavily search timed out"
            }
        except Exception as e:
            print(f"❌ Tavily search error: {str(e)}")
            return {
                "results": [],
                "error": str(e)
            }
    
    async def search_startup_news(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search for startup-related news from trusted sources
        
        Args:
            query: Search query about startups
            max_results: Maximum number of results
            
        Returns:
            Formatted search results
        """
        # Target startup/tech news sources
        include_domains = [
            "techcrunch.com",
            "crunchbase.com",
            "theinformation.com",
            "venturebeat.com",
            "reuters.com",
            "bloomberg.com",
            "wsj.com",
            "forbes.com",
            "news.ycombinator.com"
        ]
        
        return await self.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_domains=include_domains
        )
    
    async def search_investor_info(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search for investor/VC information
        
        Args:
            query: Search query about investors
            max_results: Maximum number of results
            
        Returns:
            Formatted search results
        """
        include_domains = [
            "crunchbase.com",
            "pitchbook.com",
            "bloomberg.com",
            "reuters.com",
            "wsj.com",
            "techcrunch.com"
        ]
        
        return await self.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_domains=include_domains
        )
    
    def _format_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format Tavily API response into consistent structure
        
        Args:
            data: Raw Tavily API response
            
        Returns:
            Formatted results with chunks and metadata
        """
        formatted_results = []
        
        for result in data.get("results", []):
            formatted_results.append({
                "content": result.get("content", ""),
                "raw_content": result.get("raw_content", ""),
                "url": result.get("url", ""),
                "title": result.get("title", ""),
                "score": result.get("score", 0.0),
                "published_date": result.get("published_date"),
                "source_type": "web_search",
                "source_id": f"tavily_{result.get('url', '')}"
            })
        
        return {
            "results": formatted_results,
            "answer": data.get("answer", ""),  # Tavily's AI-generated answer
            "query": data.get("query", ""),
            "response_time": data.get("response_time", 0),
            "total_results": len(formatted_results)
        }
    
    def format_as_rag_chunks(self, search_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Convert Tavily results into RAG-compatible chunks
        
        Args:
            search_results: Formatted Tavily search results
            
        Returns:
            List of chunks compatible with RAG pipeline
        """
        chunks = []
        
        for idx, result in enumerate(search_results.get("results", [])):
            # Use raw_content if available, otherwise use content
            content = result.get("raw_content") or result.get("content", "")
            
            # Chunk if content is too long (split at 1000 chars)
            if len(content) > 1000:
                # Split into chunks
                for chunk_idx, i in enumerate(range(0, len(content), 1000)):
                    chunk = {
                        "content": content[i:i+1000],
                        "source_id": result.get("source_id", f"tavily_{idx}"),
                        "source_type": "web_search",
                        "source_title": result.get("title", ""),
                        "source_url": result.get("url", ""),
                        "chunk_index": chunk_idx,
                        "score": result.get("score", 0.0),
                        "published_date": result.get("published_date"),
                        "metadata": {
                            "search_engine": "tavily",
                            "real_time": True
                        }
                    }
                    chunks.append(chunk)
            else:
                chunk = {
                    "content": content,
                    "source_id": result.get("source_id", f"tavily_{idx}"),
                    "source_type": "web_search",
                    "source_title": result.get("title", ""),
                    "source_url": result.get("url", ""),
                    "chunk_index": 0,
                    "score": result.get("score", 0.0),
                    "published_date": result.get("published_date"),
                    "metadata": {
                        "search_engine": "tavily",
                        "real_time": True
                    }
                }
                chunks.append(chunk)
        
        return chunks
