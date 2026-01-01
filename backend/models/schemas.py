"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    INVESTOR_SEARCH = "investor_search"
    STARTUP_SEARCH = "startup_search"
    FUNDING_ANALYSIS = "funding_analysis"
    MARKET_INTELLIGENCE = "market_intelligence"
    GENERAL = "general"


class SearchRequest(BaseModel):
    query: str = Field(..., description="User's search query")
    query_type: QueryType = Field(default=QueryType.GENERAL, description="Type of query")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters")
    top_k: Optional[int] = Field(default=10, description="Number of results to return")
    include_citations: bool = Field(default=True, description="Include citations in response")
    use_web_search: bool = Field(default=True, description="Enable real-time web search via Tavily")
    web_search_only: bool = Field(default=False, description="Use only web search (skip local DB)")
    response_language: Optional[str] = Field(default=None, description="Response language code (auto-detect if None). Supported: en, hi, ta, te, bn, mr, gu, kn, ml, pa, ur")


class Citation(BaseModel):
    source_id: str = Field(..., description="Unique identifier of the source document")
    source_type: str = Field(..., description="Type of source (article, pdf, report, etc.)")
    source_title: str = Field(..., description="Title of the source")
    source_url: Optional[str] = Field(None, description="URL to the source")
    excerpt: str = Field(..., description="Relevant excerpt from the source")
    confidence_score: float = Field(..., description="Confidence score for this citation")
    page_number: Optional[int] = Field(None, description="Page number if applicable")
    published_date: Optional[datetime] = Field(None, description="Publication date")


class SearchResponse(BaseModel):
    query: str
    answer: str = Field(..., description="Generated answer with context")
    citations: List[Citation] = Field(default_factory=list, description="List of citations")
    retrieved_chunks: int = Field(..., description="Number of chunks retrieved")
    processing_time: float = Field(..., description="Query processing time in seconds")
    confidence_score: float = Field(..., description="Overall confidence in the answer")
    sources: Optional[Dict[str, int]] = Field(default=None, description="Source breakdown (local vs web)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class IngestDocumentRequest(BaseModel):
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")
    document_type: str = Field(..., description="Type of document")
    source_url: Optional[str] = Field(None, description="Source URL if applicable")


class IngestDocumentResponse(BaseModel):
    document_id: str
    chunks_created: int
    status: str
    message: str


class StartupProfile(BaseModel):
    startup_id: str
    name: str
    description: str
    industry: List[str]
    stage: str
    funding_amount: Optional[float] = None
    location: str
    founded_year: Optional[int] = None
    website: Optional[str] = None
    team_size: Optional[int] = None


class InvestorProfile(BaseModel):
    investor_id: str
    name: str
    type: str  # VC, Angel, PE, etc.
    investment_thesis: Optional[str] = None
    industries: List[str]
    stages: List[str]
    ticket_size_min: Optional[float] = None
    ticket_size_max: Optional[float] = None
    portfolio_companies: List[str] = Field(default_factory=list)
    location: str


class FundingRound(BaseModel):
    round_id: str
    startup_id: str
    round_type: str  # Seed, Series A, B, C, etc.
    amount: float
    valuation: Optional[float] = None
    investors: List[str]
    date: datetime
    announcement_url: Optional[str] = None


class MatchRequest(BaseModel):
    entity_id: str = Field(..., description="ID of startup or investor")
    entity_type: str = Field(..., description="'startup' or 'investor'")
    top_k: int = Field(default=10, description="Number of matches to return")
    filters: Optional[Dict[str, Any]] = None


class Match(BaseModel):
    entity_id: str
    entity_name: str
    similarity_score: float
    reasoning: str
    key_alignments: List[str]


class MatchResponse(BaseModel):
    matches: List[Match]
    query_entity: Dict[str, Any]
    processing_time: float


class EvaluationMetrics(BaseModel):
    retrieval_accuracy: float = Field(..., description="Accuracy of retrieved documents")
    citation_precision: float = Field(..., description="Precision of citations")
    citation_recall: float = Field(..., description="Recall of citations")
    response_relevance: float = Field(..., description="Relevance of generated response")
    factual_accuracy: float = Field(..., description="Factual accuracy score")
    latency_ms: float = Field(..., description="Query latency in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
