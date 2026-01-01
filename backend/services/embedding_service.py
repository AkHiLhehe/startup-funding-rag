"""
Embedding service using Voyage AI with hash-based fallback
Voyage AI voyage-large-2-instruct is optimized for RAG tasks
"""
import httpx
from typing import List
import asyncio
import numpy as np
import hashlib
import voyageai

from core.config import settings


class DeepSeekEmbeddingService:
    def __init__(self):
        self.voyage_api_key = settings.VOYAGE_API_KEY
        self.dimension = 1024  # Voyage AI dimension
        self.model = "voyage-large-2-instruct"  # Best for RAG
        
        # Initialize Voyage AI client
        try:
            self.voyage_client = voyageai.Client(api_key=self.voyage_api_key)
            print("✅ Voyage AI embeddings initialized (1024 dimensions)")
            self.use_api = True
        except Exception as e:
            print(f"⚠️  Voyage AI initialization failed: {e}")
            print("⚠️  Falling back to hash-based embeddings...")
            self.voyage_client = None
            self.use_api = False
        
        print("✅ Embedding service ready")
        
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Voyage AI or hash-based fallback
        All embeddings are exactly 1024 dimensions
        """
        if self.use_api and self.voyage_client:
            try:
                return await self._generate_with_voyage(texts)
            except Exception as e:
                print(f"⚠️  Voyage AI failed ({e}), falling back to hash-based...")
                return [self._hash_to_embedding(text) for text in texts]
        else:
            return [self._hash_to_embedding(text) for text in texts]
    
    async def _generate_with_voyage(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Voyage AI API"""
        try:
            # Voyage AI client is synchronous, run in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.voyage_client.embed(
                    texts,
                    model=self.model,
                    input_type="document"  # Use "document" for ingestion
                )
            )
            return result.embeddings
        except Exception as e:
            raise Exception(f"Voyage AI API error: {str(e)}")
    
    def _hash_to_embedding(self, text: str) -> List[float]:
        """Generate deterministic hash-based embedding"""
        # Use SHA-256 hash as seed for reproducible random vector
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()
        
        # Convert hash to integer seed
        seed = int.from_bytes(hash_bytes[:4], byteorder='big')
        
        # Generate deterministic random vector
        rng = np.random.RandomState(seed)
        embedding = rng.randn(self.dimension)
        
        # Normalize to unit length
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding.tolist()
    
    def _normalize_dimension(self, embedding: List[float]) -> List[float]:
        """Normalize embedding to exactly 1024 dimensions"""
        current_dim = len(embedding)
        
        if current_dim == self.dimension:
            return embedding
        elif current_dim > self.dimension:
            # Truncate
            return embedding[:self.dimension]
        else:
            # Pad with zeros
            return embedding + [0.0] * (self.dimension - current_dim)
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embeddings = await self.generate_embeddings([text])
        return embeddings[0]
    
    async def batch_generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> List[List[float]]:
        """Generate embeddings in batches for efficiency"""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = await self.generate_embeddings(batch)
            all_embeddings.extend(embeddings)
            
            # Small delay to avoid rate limiting
            if i + batch_size < len(texts):
                await asyncio.sleep(0.1)
        
        return all_embeddings
