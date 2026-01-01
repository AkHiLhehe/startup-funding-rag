"""
Google Gemini LLM service
"""
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from core.config import settings


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    async def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        system_instruction: Optional[str] = None
    ) -> str:
        """Generate a response using Gemini"""
        try:
            # Construct the full prompt
            full_prompt = ""
            
            if system_instruction:
                full_prompt += f"System: {system_instruction}\n\n"
            
            if context:
                full_prompt += f"Context:\n{context}\n\n"
            
            full_prompt += f"Query: {prompt}\n\nResponse:"
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                self._generate_sync,
                full_prompt
            )
            
            return response.text
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            raise
    
    def _generate_sync(self, prompt: str):
        """Synchronous generation for executor"""
        return self.model.generate_content(
            prompt,
            generation_config={
                "temperature": settings.GEMINI_TEMPERATURE,
                "max_output_tokens": settings.GEMINI_MAX_TOKENS,
            }
        )
    
    async def generate_with_citations(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        query_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Generate response with strict citation tracking
        """
        # Build context with source markers
        context_parts = []
        source_map = {}
        
        for idx, chunk in enumerate(retrieved_chunks):
            source_id = f"[{idx + 1}]"
            source_map[source_id] = chunk
            
            context_parts.append(
                f"{source_id} {chunk['properties'].get('content', '')}"
            )
        
        context = "\n\n".join(context_parts)
        
        # Instruction for citation
        system_instruction = """You are an expert investment analyst. Your task is to provide accurate, 
        well-researched answers based ONLY on the provided context. 

        CRITICAL RULES:
        1. You MUST cite sources using the format [1], [2], etc. for every factual claim
        2. Only use information from the provided context
        3. If the context doesn't contain enough information, explicitly state what's missing
        4. Be precise with numbers, dates, and names
        5. Include multiple citations when information comes from multiple sources
        
        Format your response with inline citations like this:
        "Company X raised $50M in Series B [1]. The round was led by Sequoia Capital [2][3]."
        """
        
        prompt = f"""Based on the provided sources, answer this {query_type} query:

{query}

Provide a comprehensive answer with inline citations."""
        
        response_text = await self.generate_response(
            prompt=prompt,
            context=context,
            system_instruction=system_instruction
        )
        
        # Extract citations from response
        citations = self._extract_citations(response_text, source_map)
        
        return {
            "answer": response_text,
            "citations": citations,
            "source_map": source_map
        }
    
    def _extract_citations(
        self,
        response: str,
        source_map: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract and validate citations from the response"""
        import re
        
        citations = []
        citation_pattern = r'\[(\d+)\]'
        cited_indices = set(re.findall(citation_pattern, response))
        
        for idx in cited_indices:
            source_id = f"[{idx}]"
            if source_id in source_map:
                chunk = source_map[source_id]
                props = chunk['properties']
                
                citations.append({
                    "source_id": props.get('source_id', 'unknown'),
                    "source_type": props.get('source_type', 'unknown'),
                    "source_title": props.get('source_title', 'Unknown Source'),
                    "source_url": props.get('source_url'),
                    "excerpt": props.get('content', '')[:200] + "...",
                    "confidence_score": 1.0 - chunk.get('distance', 0.5),
                    "published_date": props.get('published_date')
                })
        
        return citations
    
    async def analyze_match(
        self,
        entity1: Dict[str, Any],
        entity2: Dict[str, Any],
        entity_type: str
    ) -> Dict[str, Any]:
        """
        Use Gemini to analyze compatibility between startup and investor
        """
        if entity_type == "startup":
            prompt = f"""Analyze the fit between this startup and investor:

Startup: {entity1.get('name')}
- Industry: {entity1.get('industry')}
- Stage: {entity1.get('stage')}
- Description: {entity1.get('description')}

Investor: {entity2.get('name')}
- Type: {entity2.get('type')}
- Focus Industries: {entity2.get('industries')}
- Investment Stages: {entity2.get('stages')}
- Thesis: {entity2.get('investment_thesis')}

Provide:
1. Match score (0-100)
2. Key alignment points
3. Potential concerns
4. Recommendation
"""
        else:
            prompt = f"""Analyze the fit between this investor and startup:

Investor: {entity1.get('name')}
- Type: {entity1.get('type')}
- Focus: {entity1.get('industries')}
- Stages: {entity1.get('stages')}

Startup: {entity2.get('name')}
- Industry: {entity2.get('industry')}
- Stage: {entity2.get('stage')}
- Description: {entity2.get('description')}

Provide:
1. Match score (0-100)
2. Key reasons for this match
3. Investment potential
4. Next steps
"""
        
        response = await self.generate_response(prompt)
        
        return {
            "analysis": response,
            "entities": [entity1, entity2]
        }
