"""
Evaluation metrics system for RAG pipeline
"""
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from pathlib import Path
import numpy as np

from core.config import settings


class EvaluationMetrics:
    def __init__(self):
        self.metrics_history = []
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure metrics log directory exists"""
        log_path = Path(settings.METRICS_LOG_PATH)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def evaluate_retrieval(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        ground_truth: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Evaluate retrieval quality
        """
        metrics = {}
        
        # Relevance score based on similarity
        if retrieved_chunks:
            similarities = [
                1 - chunk.get('distance', 1)
                for chunk in retrieved_chunks
            ]
            metrics['avg_similarity'] = float(np.mean(similarities))
            metrics['min_similarity'] = float(np.min(similarities))
            metrics['max_similarity'] = float(np.max(similarities))
        else:
            metrics['avg_similarity'] = 0.0
            metrics['min_similarity'] = 0.0
            metrics['max_similarity'] = 0.0
        
        # If ground truth is provided, calculate precision/recall
        if ground_truth:
            retrieved_ids = {
                chunk['properties'].get('source_id')
                for chunk in retrieved_chunks
            }
            ground_truth_set = set(ground_truth)
            
            true_positives = len(retrieved_ids & ground_truth_set)
            
            metrics['precision'] = (
                true_positives / len(retrieved_ids)
                if retrieved_ids else 0.0
            )
            metrics['recall'] = (
                true_positives / len(ground_truth_set)
                if ground_truth_set else 0.0
            )
            metrics['f1_score'] = (
                2 * metrics['precision'] * metrics['recall'] /
                (metrics['precision'] + metrics['recall'])
                if (metrics['precision'] + metrics['recall']) > 0 else 0.0
            )
        
        return metrics
    
    async def evaluate_citations(
        self,
        response: str,
        citations: List[Dict[str, Any]],
        retrieved_chunks: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Evaluate citation quality and accuracy
        """
        metrics = {}
        
        # Citation coverage
        import re
        citation_pattern = r'\[(\d+)\]'
        cited_indices = set(re.findall(citation_pattern, response))
        
        metrics['num_citations'] = len(citations)
        metrics['unique_citations'] = len(cited_indices)
        
        # Citation density (citations per 100 words)
        words = response.split()
        metrics['citation_density'] = (
            len(cited_indices) / len(words) * 100
            if words else 0.0
        )
        
        # Citation precision (all cited sources exist in retrieved chunks)
        retrieved_source_ids = {
            chunk['properties'].get('source_id')
            for chunk in retrieved_chunks
        }
        cited_source_ids = {
            citation.get('source_id')
            for citation in citations
        }
        
        if cited_source_ids:
            valid_citations = cited_source_ids & retrieved_source_ids
            metrics['citation_precision'] = (
                len(valid_citations) / len(cited_source_ids)
            )
        else:
            metrics['citation_precision'] = 0.0
        
        # Average citation confidence
        if citations:
            metrics['avg_citation_confidence'] = float(np.mean([
                c.get('confidence_score', 0)
                for c in citations
            ]))
        else:
            metrics['avg_citation_confidence'] = 0.0
        
        return metrics
    
    async def evaluate_response_quality(
        self,
        query: str,
        response: str,
        retrieved_chunks: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Evaluate response quality metrics
        """
        metrics = {}
        
        # Response length
        metrics['response_length'] = len(response)
        metrics['response_words'] = len(response.split())
        
        # Query coverage (how many query terms appear in response)
        query_terms = set(query.lower().split())
        response_terms = set(response.lower().split())
        
        if query_terms:
            metrics['query_coverage'] = (
                len(query_terms & response_terms) / len(query_terms)
            )
        else:
            metrics['query_coverage'] = 0.0
        
        # Context utilization (how much of retrieved context is reflected)
        # This is a simplified metric
        if retrieved_chunks:
            context_terms = set()
            for chunk in retrieved_chunks:
                content = chunk['properties'].get('content', '')
                context_terms.update(content.lower().split())
            
            if context_terms:
                metrics['context_utilization'] = (
                    len(response_terms & context_terms) / len(response_terms)
                    if response_terms else 0.0
                )
            else:
                metrics['context_utilization'] = 0.0
        else:
            metrics['context_utilization'] = 0.0
        
        return metrics
    
    async def log_query_metrics(
        self,
        query: str,
        response_data: Dict[str, Any],
        additional_metrics: Optional[Dict[str, Any]] = None
    ):
        """
        Log comprehensive metrics for a query
        """
        if not settings.ENABLE_METRICS:
            return
        
        timestamp = datetime.utcnow()
        
        # Compile all metrics
        metrics_entry = {
            "timestamp": timestamp.isoformat(),
            "query": query,
            "query_type": response_data.get('metadata', {}).get('query_type', 'unknown'),
            "processing_time_ms": response_data.get('processing_time', 0) * 1000,
            "retrieved_chunks": response_data.get('retrieved_chunks', 0),
            "confidence_score": response_data.get('confidence_score', 0),
            "num_citations": len(response_data.get('citations', [])),
            "response_length": len(response_data.get('answer', '')),
        }
        
        # Add additional metrics if provided
        if additional_metrics:
            metrics_entry.update(additional_metrics)
        
        # Add to history
        self.metrics_history.append(metrics_entry)
        
        # Write to file
        try:
            with open(settings.METRICS_LOG_PATH, 'a') as f:
                f.write(json.dumps(metrics_entry) + '\n')
        except Exception as e:
            print(f"⚠️  Failed to write metrics: {e}")
    
    def get_aggregate_metrics(self, last_n: Optional[int] = None) -> Dict[str, Any]:
        """
        Get aggregate metrics over recent queries
        """
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        data = self.metrics_history[-last_n:] if last_n else self.metrics_history
        
        if not data:
            return {"error": "No metrics available"}
        
        return {
            "total_queries": len(data),
            "avg_processing_time_ms": float(np.mean([
                m['processing_time_ms'] for m in data
            ])),
            "avg_confidence_score": float(np.mean([
                m['confidence_score'] for m in data
            ])),
            "avg_retrieved_chunks": float(np.mean([
                m['retrieved_chunks'] for m in data
            ])),
            "avg_citations": float(np.mean([
                m['num_citations'] for m in data
            ])),
            "avg_response_length": float(np.mean([
                m['response_length'] for m in data
            ])),
            "query_type_distribution": self._get_distribution(
                data, 'query_type'
            )
        }
    
    def _get_distribution(
        self,
        data: List[Dict[str, Any]],
        field: str
    ) -> Dict[str, int]:
        """Get distribution of a field"""
        distribution = {}
        for entry in data:
            value = entry.get(field, 'unknown')
            distribution[value] = distribution.get(value, 0) + 1
        return distribution
    
    async def load_metrics_from_file(self):
        """Load metrics history from file"""
        try:
            if Path(settings.METRICS_LOG_PATH).exists():
                with open(settings.METRICS_LOG_PATH, 'r') as f:
                    for line in f:
                        if line.strip():
                            self.metrics_history.append(json.loads(line))
                print(f"✅ Loaded {len(self.metrics_history)} metrics entries")
        except Exception as e:
            print(f"⚠️  Failed to load metrics: {e}")
