# API Reference Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API does not require authentication for development. For production, implement API key authentication.

---

## Health & Info Endpoints

### Health Check
Check if the system is operational.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "services": {
    "weaviate": "connected",
    "mongodb": "connected"
  }
}
```

### System Information
Get system configuration and features.

**Endpoint:** `GET /info`

**Response:**
```json
{
  "app_name": "Startup Investment Intelligence",
  "version": "1.0.0",
  "features": {
    "rag_pipeline": true,
    "citation_tracking": true,
    "evaluation_metrics": true
  },
  "models": {
    "llm": "gemini-1.5-pro",
    "embeddings": "deepseek-chat"
  }
}
```

---

## Search Endpoints

### General Search
Perform a search query with RAG.

**Endpoint:** `POST /search/`

**Request Body:**
```json
{
  "query": "Which investors focus on Series A fintech startups?",
  "query_type": "investor_search",
  "top_k": 10,
  "include_citations": true,
  "filters": {
    "industry": "fintech",
    "stage": "Series A"
  }
}
```

**Query Types:**
- `general`: General queries
- `investor_search`: Search for investors
- `startup_search`: Search for startups
- `funding_analysis`: Analyze funding trends
- `market_intelligence`: Market insights

**Response:**
```json
{
  "query": "Which investors focus on Series A fintech startups?",
  "answer": "Based on the available data, several investors focus on Series A fintech startups. Accel Partners [1] has a strong focus on early-stage fintech companies...",
  "citations": [
    {
      "source_id": "doc_123",
      "source_type": "article",
      "source_title": "Accel's Fintech Investment Strategy",
      "source_url": "https://example.com/article",
      "excerpt": "Accel Partners focuses on Series A fintech...",
      "confidence_score": 0.92,
      "page_number": null,
      "published_date": "2024-01-15T00:00:00Z"
    }
  ],
  "retrieved_chunks": 8,
  "processing_time": 2.34,
  "confidence_score": 0.87,
  "metadata": {
    "query_type": "investor_search",
    "collections_searched": ["InvestorDocument", "FundingDocument"]
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request
- `500`: Server error

### Search Investor
Search for specific investor information.

**Endpoint:** `GET /search/investor/{investor_name}`

**Parameters:**
- `investor_name` (path): Name of the investor

**Example:**
```bash
GET /search/investor/Sequoia Capital
```

**Response:** Same format as general search

### Search Startup
Search for specific startup information.

**Endpoint:** `GET /search/startup/{startup_name}`

**Parameters:**
- `startup_name` (path): Name of the startup

**Example:**
```bash
GET /search/startup/TechCorp AI
```

**Response:** Same format as general search

---

## Ingestion Endpoints

### Ingest Text Document
Add a text document to the knowledge base.

**Endpoint:** `POST /ingest/document`

**Request Body:**
```json
{
  "content": "Full document content here...",
  "metadata": {
    "title": "Series B Funding - TechCorp AI",
    "url": "https://example.com/article",
    "startup_id": "techcorp_ai",
    "published_date": "2024-01-15"
  },
  "document_type": "announcement",
  "source_url": "https://example.com/article"
}
```

**Document Types:**
- `article`: News article
- `report`: Research report
- `announcement`: Funding announcement
- `thesis`: Investment thesis
- `policy`: Policy document
- `other`: Other types

**Response:**
```json
{
  "document_id": "abc123def456",
  "chunks_created": 5,
  "status": "success",
  "message": "Document ingested successfully"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request
- `500`: Server error

### Ingest PDF Document
Upload and ingest a PDF file.

**Endpoint:** `POST /ingest/pdf`

**Request:** Multipart form data
- `file`: PDF file (required)
- `metadata`: JSON string with metadata (optional)

**Example using curl:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/ingest/pdf \
  -F "file=@document.pdf" \
  -F 'metadata={"title":"Investment Report","startup_id":"techcorp_ai"}'
```

**Response:**
```json
{
  "document_id": "pdf_abc123",
  "chunks_created": 12,
  "status": "success",
  "message": "PDF ingested successfully"
}
```

### Batch Ingest
Ingest multiple documents at once.

**Endpoint:** `POST /ingest/batch`

**Request Body:**
```json
[
  {
    "content": "Document 1 content...",
    "metadata": {"title": "Doc 1"},
    "document_type": "article"
  },
  {
    "content": "Document 2 content...",
    "metadata": {"title": "Doc 2"},
    "document_type": "report"
  }
]
```

**Response:**
```json
{
  "total": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "status": "success",
      "document_id": "doc1_id",
      "chunks": 5
    },
    {
      "status": "success",
      "document_id": "doc2_id",
      "chunks": 7
    }
  ]
}
```

---

## Analytics Endpoints

### Get Metrics
Retrieve system evaluation metrics.

**Endpoint:** `GET /analytics/metrics`

**Query Parameters:**
- `last_n` (optional): Number of recent queries to analyze

**Example:**
```bash
GET /analytics/metrics?last_n=100
```

**Response:**
```json
{
  "total_queries": 150,
  "avg_processing_time_ms": 2340.5,
  "avg_confidence_score": 0.84,
  "avg_retrieved_chunks": 8.5,
  "avg_citations": 4.2,
  "avg_response_length": 856.3,
  "query_type_distribution": {
    "general": 50,
    "investor_search": 45,
    "startup_search": 30,
    "funding_analysis": 25
  }
}
```

### Get Statistics
Get database statistics.

**Endpoint:** `GET /analytics/statistics`

**Response:**
```json
{
  "startups": 150,
  "investors": 85,
  "funding_rounds": 320,
  "documents": 1250
}
```

### Get Query History
Retrieve recent query logs.

**Endpoint:** `GET /analytics/queries`

**Query Parameters:**
- `limit` (optional, default: 100): Number of queries to return

**Example:**
```bash
GET /analytics/queries?limit=50
```

**Response:**
```json
{
  "total": 50,
  "queries": [
    {
      "_id": "query_id_1",
      "query": "Tell me about Sequoia Capital",
      "query_type": "investor_search",
      "response": {...},
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Match Entities
Find matching investors for startups or vice versa.

**Endpoint:** `POST /analytics/match`

**Request Body:**
```json
{
  "entity_id": "techcorp_ai",
  "entity_type": "startup",
  "top_k": 10
}
```

**Entity Types:**
- `startup`: Find investors for a startup
- `investor`: Find startups for an investor

**Response:**
```json
{
  "entity_id": "techcorp_ai",
  "entity_type": "startup",
  "message": "Matching functionality requires further implementation"
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `400`: Bad Request - Invalid input
- `404`: Not Found - Resource doesn't exist
- `422`: Validation Error - Request body validation failed
- `500`: Internal Server Error - Server-side error

**Example Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:
- Implement rate limiting per IP/API key
- Recommended: 100 requests per minute per user
- Use Redis for distributed rate limiting

---

## Code Examples

### Python

```python
import requests

# Search
response = requests.post(
    "http://localhost:8000/api/v1/search/",
    json={
        "query": "Which VCs invest in AI startups?",
        "query_type": "investor_search",
        "include_citations": True
    }
)
result = response.json()
print(result["answer"])

# Ingest document
response = requests.post(
    "http://localhost:8000/api/v1/ingest/document",
    json={
        "content": "Document content here...",
        "metadata": {"title": "My Document"},
        "document_type": "article"
    }
)
print(response.json())
```

### JavaScript

```javascript
// Search
const searchResponse = await fetch(
  'http://localhost:8000/api/v1/search/',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: 'Which VCs invest in AI startups?',
      query_type: 'investor_search',
      include_citations: true
    })
  }
);
const result = await searchResponse.json();
console.log(result.answer);

// Ingest document
const ingestResponse = await fetch(
  'http://localhost:8000/api/v1/ingest/document',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: 'Document content here...',
      metadata: { title: 'My Document' },
      document_type: 'article'
    })
  }
);
console.log(await ingestResponse.json());
```

### cURL

```bash
# Search
curl -X POST http://localhost:8000/api/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which VCs invest in AI startups?",
    "query_type": "investor_search",
    "include_citations": true
  }'

# Ingest document
curl -X POST http://localhost:8000/api/v1/ingest/document \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Document content here...",
    "metadata": {"title": "My Document"},
    "document_type": "article"
  }'

# Get metrics
curl http://localhost:8000/api/v1/analytics/metrics
```

---

## WebSocket Support

WebSocket support for real-time updates is not currently implemented but can be added for:
- Real-time search results streaming
- Live metrics updates
- Document ingestion progress

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can:
- Try out all API endpoints
- See detailed request/response schemas
- Generate code examples
- Test authentication

Alternative: http://localhost:8000/redoc for ReDoc documentation

---

## Best Practices

1. **Always include citations**: Set `include_citations: true` for verifiable results
2. **Use appropriate query types**: Choose the right query_type for better results
3. **Batch ingestion**: Use `/ingest/batch` for multiple documents
4. **Error handling**: Always check response status codes
5. **Metadata**: Provide rich metadata for better search results
6. **Monitor metrics**: Regularly check `/analytics/metrics` for system health

---

For more information, see:
- [README.md](../README.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [SETUP.md](SETUP.md)
