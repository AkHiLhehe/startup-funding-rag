# Startup Investment Intelligence Platform

## 🚀 Production-Grade RAG System for Startup & Investor Intelligence

A comprehensive AI-powered platform that transforms fragmented startup and funding data into actionable intelligence using advanced RAG (Retrieval-Augmented Generation) technology.

## 📋 Overview

The startup ecosystem generates millions of data points daily—funding announcements, investor theses, policy changes, and market signals—yet this information is scattered across news sites, PDFs, and unstructured reports. This platform solves this problem by providing:

- **For Founders**: Find compatible investors, analyze investment theses, research funding trends
- **For VCs**: Discover breakout startups, track market signals, perform due diligence

## ✨ Key Features

### 🎯 Advanced RAG Pipeline
- **Gemini LLM** for reasoning and multilingual generation
- **Voyage AI Embeddings** for dense vector representations
- **Weaviate Vector DB** for semantic search
- **MongoDB** for data storage
- **Tavily** for real time search
- Hybrid search combining vector and keyword matching

### 📚 Strict Citation & Provenance
- Every claim backed by source citations
- Confidence scores for each citation
- Full document provenance tracking
- Eliminates LLM hallucinations

### 📊 Comprehensive Evaluation Metrics
- Retrieval accuracy measurement
- Citation quality tracking
- Response relevance scoring
- Performance monitoring
- Query analytics

### 🎨 Modern UI
- React + TypeScript frontend
- Tailwind CSS for beautiful, responsive design
- Real-time search interface
- Interactive analytics dashboard
- Document ingestion portal

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Python 3.11+**: Core language
- **Motor**: Async MongoDB driver
- **Google Generative AI**: Gemini LLM integration
- **Weaviate Client**: Vector database operations

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **Heroicons**: Beautiful icons

### Infrastructure
- **Weaviate**: Vector database
- **MongoDB**: Document store
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📦 Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Gemini API Key
- DeepSeek API Key (optional)

### Quick Start with Docker

1. **Clone the repository**
```bash
cd Anokha4
```

2. **Configure environment variables**

Backend:
```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys
```

Frontend:
```bash
cd ../frontend
cp .env.example .env
```

3. **Start all services**
```bash
cd ..
docker-compose up -d
```

This will start:
- Weaviate (port 8080)
- MongoDB (port 27017)
- Backend API (port 8000)
- Frontend (port 3000)

4. **Access the application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- API Health: http://localhost:8000/api/v1/health

### Manual Setup (Development)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services (Weaviate & MongoDB)
# Using Docker:
docker run -d -p 8080:8080 semitechnologies/weaviate:latest
docker run -d -p 27017:27017 mongo:7.0

# Run the backend
python main.py
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm run dev
```

## 🎯 Usage Guide

### 1. Ingest Documents

**Via UI:**
- Navigate to "Ingest" page
- Choose between text input or PDF upload
- Add metadata (title, source URL, entity type)
- Submit for processing

**Via API:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/ingest/document",
    json={
        "content": "Your document content here...",
        "metadata": {
            "title": "Series B Funding - TechCorp",
            "url": "https://example.com/article",
            "startup_id": "techcorp_123"
        },
        "document_type": "announcement"
    }
)
```

### 2. Search Intelligence

**Via UI:**
- Navigate to "Search" page
- Select query type (investor, startup, funding, etc.)
- Enter your question
- View results with citations

**Via API:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/search/",
    json={
        "query": "Which investors focus on early-stage AI startups?",
        "query_type": "investor_search",
        "top_k": 10,
        "include_citations": True
    }
)
```

### 3. View Analytics

Navigate to the Analytics page to see:
- System statistics (documents, startups, investors)
- Query performance metrics
- Response quality indicators
- Citation coverage

## 🏗️ Architecture

### System Components

```
┌─────────────┐
│   Frontend  │ (React + Tailwind)
│  (Port 3000)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Backend    │ (FastAPI)
│  (Port 8000)│
└──────┬──────┘
       │
       ├──────────────┬─────────────┐
       ▼              ▼             ▼
┌───────────┐  ┌──────────┐  ┌──────────┐
│ Weaviate  │  │ MongoDB  │  │  Gemini  │
│Vector DB  │  │Document  │  │   LLM    │
│(Port 8080)│  │   Store  │  │   API    │
└───────────┘  └──────────┘  └──────────┘
```

### RAG Pipeline Flow

1. **Document Ingestion**
   - Document chunking (1000 chars, 200 overlap)
   - Generate embeddings (DeepSeek)
   - Store in Weaviate with metadata
   - Index in MongoDB

2. **Query Processing**
   - Generate query embedding
   - Hybrid search (vector + keyword)
   - Rank and filter results
   - Build context with citations

3. **Response Generation**
   - Gemini LLM with context
   - Strict citation instructions
   - Extract and validate citations
   - Return with confidence scores

## 📁 Project Structure

```
Anokha4/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── core/
│   │   └── config.py          # Configuration management
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── weaviate_service.py    # Vector DB operations
│   │   ├── mongodb_service.py     # Document storage
│   │   ├── embedding_service.py   # DeepSeek embeddings
│   │   ├── llm_service.py         # Gemini LLM
│   │   ├── rag_pipeline.py        # RAG orchestration
│   │   └── evaluation_service.py  # Metrics tracking
│   ├── api/
│   │   └── routes/
│   │       ├── search.py          # Search endpoints
│   │       ├── ingest.py          # Ingestion endpoints
│   │       ├── analytics.py       # Analytics endpoints
│   │       └── health.py          # Health checks
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── SearchPage.tsx
│   │   │   ├── IngestPage.tsx
│   │   │   └── AnalyticsPage.tsx
│   │   ├── services/
│   │   │   └── api.ts             # API client
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

```env
# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Gemini API
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-pro
GEMINI_TEMPERATURE=0.2

# DeepSeek
DEEPSEEK_API_KEY=your_key_here
EMBEDDING_DIMENSION=1536

# Weaviate
WEAVIATE_URL=http://localhost:8080

# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=startup_intelligence

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=10
SIMILARITY_THRESHOLD=0.7
```

## 📊 API Documentation

### Search Endpoint

**POST** `/api/v1/search/`

Request:
```json
{
  "query": "Which VCs focus on Series A fintech?",
  "query_type": "investor_search",
  "top_k": 10,
  "include_citations": true
}
```

Response:
```json
{
  "query": "Which VCs focus on Series A fintech?",
  "answer": "Based on the available data, several VCs focus on Series A fintech...[1][2]",
  "citations": [
    {
      "source_id": "doc_123",
      "source_title": "Sequoia's Fintech Thesis",
      "excerpt": "We invest in Series A fintech...",
      "confidence_score": 0.92
    }
  ],
  "retrieved_chunks": 8,
  "processing_time": 2.34,
  "confidence_score": 0.87
}
```

### Ingest Document

**POST** `/api/v1/ingest/document`

### Get Analytics

**GET** `/api/v1/analytics/metrics`

Full API documentation available at: `http://localhost:8000/docs`

## 🎯 Evaluation Metrics

The system tracks:

- **Retrieval Accuracy**: Quality of retrieved documents
- **Citation Precision**: Accuracy of citations
- **Response Relevance**: Relevance to query
- **Confidence Scores**: System confidence
- **Latency**: Query processing time
- **Query Distribution**: Query type analytics

## 🔐 Security Considerations

- API keys stored in environment variables
- No hardcoded credentials
- CORS configured for frontend
- Input validation on all endpoints
- MongoDB connection secured
- Rate limiting recommended for production

## 🚀 Deployment

### Production Deployment Checklist

- [ ] Configure production API keys
- [ ] Set `DEBUG=False`
- [ ] Configure proper CORS origins
- [ ] Set up persistent volumes for databases
- [ ] Configure backup strategy
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Set up logging aggregation
- [ ] Configure autoscaling

### Docker Production Build

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose -f docker-compose.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Performance Optimization

- Batch embedding generation (32 documents at a time)
- Async database operations
- Connection pooling
- Vector index optimization
- Query result caching
- Lazy loading in frontend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is built for the Anokha Generative AI track challenge.

## 🙋 Support

For issues, questions, or contributions, please open an issue in the repository.

## 🎉 Acknowledgments

- **Gemini** for powerful LLM capabilities
- **DeepSeek** for embedding generation
- **Weaviate** for vector search
- **MongoDB** for data persistence
- **FastAPI** for the backend framework
- **React** for the frontend

---

**Built with ❤️ for the Anokha Generative AI Track**

Transform fragmented data into actionable intelligence. 🚀
