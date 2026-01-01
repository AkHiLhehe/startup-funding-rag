# System Architecture Documentation

## Overview

The Startup Investment Intelligence Platform is a production-grade RAG (Retrieval-Augmented Generation) system designed to transform fragmented startup and funding data into actionable intelligence.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│              (React + TypeScript + Tailwind)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                         │
│                      (FastAPI)                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   Search     │ │   Ingest     │ │  Analytics   │       │
│  │   Routes     │ │   Routes     │ │   Routes     │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                       │
│                  (RAG Pipeline & Services)                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │     RAG      │ │  Embedding   │ │     LLM      │       │
│  │   Pipeline   │ │   Service    │ │   Service    │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└───────────────────────────┬─────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    Weaviate     │ │    MongoDB      │ │  External APIs  │
│  (Vector DB)    │ │ (Document DB)   │ │ (Gemini/DeepSeek│
│  Port 8080      │ │  Port 27017     │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Component Details

### 1. Frontend Layer

**Technology**: React 18 + TypeScript + Tailwind CSS

**Components**:
- `HomePage`: Landing page with feature overview
- `SearchPage`: Main search interface with citation display
- `IngestPage`: Document ingestion portal (text/PDF)
- `AnalyticsPage`: Metrics dashboard with charts

**Responsibilities**:
- User interface rendering
- Form handling and validation
- API communication
- State management
- Responsive design

### 2. API Gateway Layer

**Technology**: FastAPI (Python)

**Routes**:
- `/api/v1/search/`: Search and query endpoints
- `/api/v1/ingest/`: Document ingestion endpoints
- `/api/v1/analytics/`: Metrics and statistics
- `/api/v1/health/`: Health checks and system info

**Features**:
- Request validation (Pydantic)
- CORS middleware
- Error handling
- API documentation (OpenAPI/Swagger)
- Async request handling

### 3. RAG Pipeline

**Core Components**:

#### 3.1 Document Ingestion
```python
Document → Chunking → Embedding → Vector Storage + Metadata Storage
```

**Steps**:
1. **Chunking**: Break documents into 1000-char chunks with 200-char overlap
2. **Embedding**: Generate vector embeddings using DeepSeek
3. **Storage**: 
   - Vectors → Weaviate collections
   - Metadata → MongoDB documents
4. **Indexing**: Create searchable indexes

#### 3.2 Query Processing
```python
Query → Embedding → Hybrid Search → Ranking → Context Building
```

**Steps**:
1. **Embedding**: Convert query to vector
2. **Hybrid Search**: 
   - Vector similarity search (0.7 weight)
   - Keyword matching (0.3 weight)
3. **Filtering**: Apply similarity threshold (0.7)
4. **Ranking**: Sort by relevance score
5. **Context Building**: Prepare context with source markers

#### 3.3 Response Generation
```python
Context + Query → LLM → Citation Extraction → Validation → Response
```

**Steps**:
1. **Prompt Engineering**: Build prompt with system instructions
2. **LLM Call**: Generate response using Gemini
3. **Citation Extraction**: Parse citation markers [1], [2], etc.
4. **Validation**: Verify citations against source map
5. **Scoring**: Calculate confidence scores

### 4. Service Layer

#### 4.1 Weaviate Service
- Manages vector database connections
- Creates and maintains collections
- Performs vector and hybrid search
- Handles batch operations

**Collections**:
- `StartupDocument`: Startup-related documents
- `InvestorDocument`: Investor and VC documents
- `FundingDocument`: Funding announcements and rounds

#### 4.2 MongoDB Service
- Manages document database
- CRUD operations for entities
- Query logging
- Analytics data aggregation

**Collections**:
- `startups`: Startup profiles
- `investors`: Investor profiles
- `funding_rounds`: Funding data
- `documents`: Document metadata
- `query_logs`: Query history

#### 4.3 Embedding Service (DeepSeek)
- Generates vector embeddings
- Batch processing (32 documents)
- Fallback mechanisms
- Rate limiting handling

#### 4.4 LLM Service (Gemini)
- Response generation
- Citation-aware prompting
- Match analysis
- Context-aware reasoning

#### 4.5 Evaluation Service
- Metrics collection
- Performance tracking
- Quality assessment
- Analytics aggregation

### 5. Data Flow

#### Search Query Flow

```
1. User enters query in frontend
   ↓
2. Frontend sends POST to /api/v1/search/
   ↓
3. API validates request
   ↓
4. RAG Pipeline processes:
   a. Generate query embedding
   b. Search Weaviate (hybrid search)
   c. Filter and rank results
   d. Build context with citations
   e. Call Gemini LLM
   f. Extract citations
   g. Calculate confidence
   ↓
5. Log metrics and query
   ↓
6. Return response to frontend
   ↓
7. Frontend displays results with citations
```

#### Document Ingestion Flow

```
1. User submits document (text/PDF)
   ↓
2. Frontend sends POST to /api/v1/ingest/
   ↓
3. API validates and extracts content
   ↓
4. RAG Pipeline processes:
   a. Generate source ID
   b. Check for duplicates
   c. Chunk document
   d. Generate embeddings (batch)
   e. Store in Weaviate
   f. Store metadata in MongoDB
   ↓
5. Return ingestion result
   ↓
6. Frontend shows success message
```

## Database Schemas

### Weaviate Schema

```json
{
  "class": "StartupDocument",
  "properties": [
    {"name": "content", "dataType": ["text"]},
    {"name": "source_id", "dataType": ["text"]},
    {"name": "source_type", "dataType": ["text"]},
    {"name": "source_title", "dataType": ["text"]},
    {"name": "source_url", "dataType": ["text"]},
    {"name": "chunk_index", "dataType": ["int"]},
    {"name": "startup_id", "dataType": ["text"]},
    {"name": "published_date", "dataType": ["date"]},
    {"name": "metadata", "dataType": ["object"]}
  ],
  "vectorizer": "none"
}
```

### MongoDB Schema

```javascript
// startups collection
{
  startup_id: String,
  name: String,
  description: String,
  industry: [String],
  stage: String,
  funding_amount: Number,
  location: String,
  founded_year: Number,
  created_at: Date,
  updated_at: Date
}

// investors collection
{
  investor_id: String,
  name: String,
  type: String,
  investment_thesis: String,
  industries: [String],
  stages: [String],
  ticket_size_min: Number,
  ticket_size_max: Number,
  portfolio_companies: [String],
  location: String
}

// documents collection
{
  source_id: String,
  source_type: String,
  title: String,
  url: String,
  published_date: Date,
  num_chunks: Number,
  metadata: Object,
  created_at: Date
}
```

## Evaluation Metrics

### Tracked Metrics

1. **Retrieval Quality**
   - Average similarity score
   - Number of chunks retrieved
   - Precision/Recall (when ground truth available)

2. **Citation Quality**
   - Citation precision
   - Citation density
   - Average confidence score

3. **Response Quality**
   - Query coverage
   - Context utilization
   - Response length

4. **Performance**
   - Processing time (ms)
   - Query latency
   - System throughput

### Metric Calculation

```python
# Confidence Score
confidence = (avg_similarity * 0.7) + (citation_score * 0.3)

# Citation Precision
citation_precision = valid_citations / total_citations

# Citation Density
citation_density = citations / words * 100
```

## Scalability Considerations

### Horizontal Scaling
- Multiple FastAPI instances behind load balancer
- Weaviate clustering
- MongoDB replica sets
- Redis for caching

### Optimization Strategies
1. **Caching**: Query result caching
2. **Batching**: Batch embedding generation
3. **Async Operations**: All I/O operations async
4. **Connection Pooling**: Database connection pools
5. **Lazy Loading**: Frontend lazy loading

### Resource Requirements

**Minimum**:
- CPU: 4 cores
- RAM: 8GB
- Storage: 20GB SSD

**Recommended**:
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 100GB+ SSD
- GPU: Optional for embeddings

## Security Architecture

### Authentication & Authorization
- API key authentication for external APIs
- Environment variable management
- No hardcoded credentials

### Data Security
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS prevention (React escaping)
- CORS configuration

### Network Security
- HTTPS in production
- Firewall rules
- Rate limiting
- DDoS protection

## Monitoring & Logging

### Metrics Collection
- Prometheus metrics endpoint
- Custom business metrics
- System health indicators

### Logging
- Structured logging
- Log aggregation (ELK stack recommended)
- Error tracking
- Audit logs

## Disaster Recovery

### Backup Strategy
- Daily MongoDB backups
- Weaviate snapshots
- Configuration backups
- Code versioning (Git)

### Recovery Procedures
1. Stop affected services
2. Restore from latest backup
3. Verify data integrity
4. Restart services
5. Validate functionality

---

This architecture provides a robust, scalable foundation for the Startup Investment Intelligence Platform, ensuring high performance, reliability, and maintainability.
