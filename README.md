# Startup Investment Intelligence Platform
This project is built for the Anokha Generative AI track challenge and is an updated version of the submission
As of Now it hit the rate limit so 


## Production-Grade RAG System for Startup & Investor Intelligence

A comprehensive AI-powered platform that transforms fragmented startup and funding data into actionable intelligence using advanced RAG (Retrieval-Augmented Generation) technology.

## Overview

The startup ecosystem generates millions of data points daily—funding announcements, investor theses, policy changes, and market signals—yet this information is scattered across news sites, PDFs, and unstructured reports. This platform solves this problem by providing:

- **For Founders**: Find compatible investors, analyze investment theses, research funding trends
- **For VCs**: Discover breakout startups, track market signals, perform due diligence

##  Key Features

###  Advanced RAG Pipeline
- **Gemini LLM** for reasoning and multilingual generation
- **Voyage AI Embeddings** for dense vector representations
- **Weaviate Vector DB** for semantic search
- **MongoDB** for data storage
- **Tavily** for real time search
- Hybrid search combining vector and keyword matching

###  Strict Citation & Provenance
- Every claim backed by source citations
- Confidence scores for each citation
- Full document provenance tracking
- Eliminates LLM hallucinations

###  Comprehensive Evaluation Metrics
- Retrieval accuracy measurement
- Citation quality tracking
- Response relevance scoring
- Performance monitoring
- Query analytics

##  Tech Stack

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

##  Installation & Setup

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
- Frontend: localhost:3000
- API Docs: refer to port 8000 in localhost(localhost:8000)

### Manual Setup (Development)

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt


cp .env.example .env
# Edit .env with your settings


#Use Docker:
docker run -d -p 8080:8080 semitechnologies/weaviate:latest
docker run -d -p 27017:27017 mongo:7.0

python main.py
```

#### Frontend Setup

```bash
cd frontend

npm install

cp .env.example .env

npm run dev
```

##  Usage Guide

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

### 2. Search

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

##  Architecture

### System Components
- **Gemini** for powerful LLM capabilities
- **Voyage AI** for embedding generation
- **Weaviate** for vector search
- **MongoDB** for data persistence
- **FastAPI** for the backend framework
- **React** for the frontend

### System Architecture

<img width="632" height="1032" alt="_- visual selection (2)" src="https://github.com/user-attachments/assets/1d3f5b77-b6cd-4a72-a231-8e93fc4527d2" />


### Workflow
<img width="720" height="1098" alt="_- visual selection (2)" src="https://github.com/user-attachments/assets/f3922a12-c291-446f-8d69-eb16c39caae2" />



##  API Documentation

Full API documentation available at: `http://localhost:8000/docs`

##  Evaluation Metrics

The system tracks:

- **Retrieval Accuracy**: Quality of retrieved documents
- **Citation Precision**: Accuracy of citations
- **Response Relevance**: Relevance to query
- **Confidence Scores**: System confidence
- **Latency**: Query processing time
- **Query Distribution**: Query type analytics

##  Deployment


### Docker Production Build

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose -f docker-compose.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

##  Testing

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



This project is built for the Anokha Generative AI track challenge.

##  Support

For issues, questions, or contributions, please open an issue in the repository.


