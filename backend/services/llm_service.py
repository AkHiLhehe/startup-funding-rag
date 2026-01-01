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
        # Use gemini-2.5-flash which is available in the API
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        print("✅ Gemini LLM initialized (models/gemini-2.5-flash)")
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
        query_type: str = "general",
        response_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate response with strict citation tracking
        Supports multilingual responses (auto-detect or specified)
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
        
        # Detect language if not specified
        if not response_language:
            response_language = self._detect_language(query)
        
        # Language-specific instruction
        language_instruction = ""
        if response_language and response_language != "en":
            language_map = {
                "hi": "Hindi (हिंदी)",
                "ta": "Tamil (தமிழ்)",
                "te": "Telugu (తెలుగు)",
                "bn": "Bengali (বাংলা)",
                "mr": "Marathi (मराठी)",
                "gu": "Gujarati (ગુજરાતી)",
                "kn": "Kannada (ಕನ್ನಡ)",
                "ml": "Malayalam (മലയാളം)",
                "pa": "Punjabi (ਪੰਜਾਬੀ)",
                "ur": "Urdu (اردو)"
            }
            lang_name = language_map.get(response_language, response_language)
            language_instruction = f"\n\nIMPORTANT: Respond in {lang_name}. Translate your entire response to {lang_name} while maintaining citations."
        
        # Instruction for citation
        system_instruction = f"""You are an expert investment analyst. Your task is to provide accurate, 
        well-researched answers based ONLY on the provided context. 

        CRITICAL RULES:
        1. You MUST cite sources using the format [1], [2], etc. for every factual claim
        2. Only use information from the provided context
        3. If the context doesn't contain enough information, explicitly state what's missing
        4. Be precise with numbers, dates, and names
        5. Include multiple citations when information comes from multiple sources{language_instruction}
        
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
    
    def _detect_language(self, text: str) -> str:
        """Detect language of the query (simple heuristic-based detection)"""
        # Hindi Unicode range
        if any('\u0900' <= char <= '\u097F' for char in text):
            return "hi"
        # Tamil
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):
            return "ta"
        # Telugu
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):
            return "te"
        # Bengali
        elif any('\u0980' <= char <= '\u09FF' for char in text):
            return "bn"
        # Marathi (uses Devanagari like Hindi)
        # Gujarati
        elif any('\u0A80' <= char <= '\u0AFF' for char in text):
            return "gu"
        # Kannada
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):
            return "kn"
        # Malayalam
        elif any('\u0D00' <= char <= '\u0D7F' for char in text):
            return "ml"
        # Punjabi
        elif any('\u0A00' <= char <= '\u0A7F' for char in text):
            return "pa"
        # Urdu (Arabic script)
        elif any('\u0600' <= char <= '\u06FF' for char in text):
            return "ur"
        else:
            return "en"
    
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
