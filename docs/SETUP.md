# Startup Investment Intelligence Platform - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **Node.js** v18+ (for local frontend development)
- **Python** 3.11+ (for local backend development)
- **Git** for version control

## API Keys Required

You'll need to obtain the following API keys:

1. **Google Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Create a project and enable Generative Language API
   - Generate an API key

2. **DeepSeek API Key** (Optional but recommended)
   - Visit: https://platform.deepseek.com/
   - Sign up and generate an API key
   - Note: Fallback embeddings are available if not provided

## Installation Options

Choose one of the following installation methods:

### Option 1: Docker Compose (Recommended for Quick Start)

This method starts all services with one command.

#### Step 1: Navigate to Project Directory

```powershell
cd "c:\Users\sriak\OneDrive\Desktop\Sem 6\Anokha4"
```

#### Step 2: Configure Backend Environment

```powershell
cd backend
cp .env.example .env
```

Edit `.env` file and add your API keys:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
DEEPSEEK_API_KEY=your_actual_deepseek_api_key
```

#### Step 3: Configure Frontend Environment

```powershell
cd ..\frontend
cp .env.example .env
```

The default configuration should work:
```env
VITE_API_URL=http://localhost:8000
```

#### Step 4: Start All Services

```powershell
cd ..
docker-compose up -d
```

This will start:
- **Weaviate** on port 8080
- **MongoDB** on port 27017
- **Backend API** on port 8000
- **Frontend** on port 3000

#### Step 5: Verify Services

Check if all containers are running:
```powershell
docker-compose ps
```

You should see all services as "Up".

#### Step 6: Access the Application

- **Frontend**: Open http://localhost:3000 in your browser
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Option 2: Manual Setup (For Development)

This method gives you more control and is better for development.

#### Step 1: Setup Backend

##### 1.1 Create Python Virtual Environment

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

##### 1.2 Install Dependencies

```powershell
pip install -r requirements.txt
```

##### 1.3 Configure Environment

```powershell
cp .env.example .env
# Edit .env with your API keys
```

##### 1.4 Start Required Services

Start Weaviate:
```powershell
docker run -d `
  --name weaviate `
  -p 8080:8080 `
  -e QUERY_DEFAULTS_LIMIT=25 `
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true `
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate `
  -e DEFAULT_VECTORIZER_MODULE=none `
  semitechnologies/weaviate:latest
```

Start MongoDB:
```powershell
docker run -d `
  --name mongodb `
  -p 27017:27017 `
  -e MONGO_INITDB_ROOT_USERNAME=admin `
  -e MONGO_INITDB_ROOT_PASSWORD=password `
  mongo:7.0
```

If using authentication, update `.env`:
```env
MONGODB_URL=mongodb://admin:password@localhost:27017
```

##### 1.5 Run Backend

```powershell
python main.py
```

The backend will start on http://localhost:8000

#### Step 2: Setup Frontend

Open a new terminal:

##### 2.1 Install Dependencies

```powershell
cd frontend
npm install
```

##### 2.2 Configure Environment

```powershell
cp .env.example .env
```

##### 2.3 Start Development Server

```powershell
npm run dev
```

The frontend will start on http://localhost:3000

## Verification Steps

### 1. Check Backend Health

```powershell
curl http://localhost:8000/api/v1/health
```

Expected response:
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

### 2. Check System Info

```powershell
curl http://localhost:8000/api/v1/info
```

### 3. Test Frontend

Open http://localhost:3000 in your browser. You should see the landing page.

## Initial Data Setup

### Option 1: Ingest Sample Documents via UI

1. Navigate to http://localhost:3000/ingest
2. Select "Text Input"
3. Add sample funding announcement:

```
Title: Series B Funding - TechCorp AI
Document Type: Funding Announcement
Content:
TechCorp AI, a leading artificial intelligence startup, announced today 
that it has raised $50 million in Series B funding. The round was led 
by Sequoia Capital, with participation from Index Ventures and previous 
investor Accel Partners. The company plans to use the funds to expand 
its engineering team and accelerate product development.
```

4. Click "Ingest Document"

### Option 2: Ingest via API

```powershell
$body = @{
    content = "Your document content here..."
    metadata = @{
        title = "Series B Funding - TechCorp AI"
        url = "https://example.com/article"
    }
    document_type = "announcement"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/api/v1/ingest/document" `
  -Body $body `
  -ContentType "application/json"
```

## Testing the System

### 1. Test Search

Navigate to http://localhost:3000/search and try these queries:

- "Tell me about TechCorp AI's recent funding"
- "Which investors focus on AI startups?"
- "What are recent funding trends?"

### 2. Check Analytics

Navigate to http://localhost:3000/analytics to view system metrics.

## Common Issues & Troubleshooting

### Issue 1: Port Already in Use

**Error**: "Port 8000 is already in use"

**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F
```

### Issue 2: Docker Service Won't Start

**Error**: "Cannot connect to Docker daemon"

**Solution**:
- Ensure Docker Desktop is running
- Check Docker service status
- Restart Docker Desktop

### Issue 3: API Keys Not Working

**Error**: "Authentication failed"

**Solution**:
- Verify API keys are correct in `.env` file
- Ensure no extra spaces or quotes around keys
- Restart the backend service after updating `.env`

### Issue 4: Weaviate Connection Failed

**Error**: "Failed to connect to Weaviate"

**Solution**:
```powershell
# Check if Weaviate is running
docker ps | findstr weaviate

# View Weaviate logs
docker logs weaviate

# Restart Weaviate
docker restart weaviate
```

### Issue 5: MongoDB Connection Failed

**Error**: "Failed to connect to MongoDB"

**Solution**:
```powershell
# Check if MongoDB is running
docker ps | findstr mongodb

# View MongoDB logs
docker logs mongodb

# Test connection
mongosh mongodb://localhost:27017
```

### Issue 6: Frontend Can't Connect to Backend

**Error**: "Network Error" or "CORS Error"

**Solution**:
1. Verify backend is running on port 8000
2. Check `VITE_API_URL` in frontend `.env`
3. Verify CORS settings in backend `config.py`
4. Clear browser cache

### Issue 7: Embeddings Generation Slow

**Issue**: Queries taking too long

**Solution**:
- DeepSeek API might be slow; this is normal
- Fallback embeddings are used if API fails
- Consider batching ingestion for large documents

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Backend**: Uvicorn auto-reloads on file changes
- **Frontend**: Vite hot module replacement (HMR)

### Viewing Logs

**Docker Compose**:
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

**Manual Setup**:
- Backend logs appear in terminal
- Frontend logs in browser console

### Database Management

**MongoDB**:
```powershell
# Connect to MongoDB
docker exec -it mongodb mongosh

# Use database
use startup_intelligence

# List collections
show collections

# Query documents
db.documents.find().limit(5)
```

**Weaviate**:
```powershell
# Check Weaviate health
curl http://localhost:8080/v1/meta

# Query schema
curl http://localhost:8080/v1/schema
```

### Resetting Everything

**Docker Compose**:
```powershell
# Stop and remove everything
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

**Manual Setup**:
```powershell
# Stop services
docker stop weaviate mongodb

# Remove containers and volumes
docker rm -v weaviate mongodb

# Restart from scratch
# Follow manual setup steps again
```

## Next Steps

1. **Explore the UI**: Navigate through all pages
2. **Ingest More Documents**: Add various types of content
3. **Test Different Queries**: Try different query types
4. **View Analytics**: Monitor system performance
5. **Read Documentation**: Check `README.md` and `ARCHITECTURE.md`

## Production Deployment

For production deployment:

1. **Security**:
   - Use strong API keys
   - Enable HTTPS
   - Configure firewalls
   - Set `DEBUG=False`

2. **Performance**:
   - Scale backend with multiple instances
   - Use load balancer
   - Enable caching
   - Optimize database indexes

3. **Monitoring**:
   - Set up Prometheus + Grafana
   - Configure log aggregation
   - Enable health checks
   - Set up alerts

4. **Backup**:
   - Schedule database backups
   - Version control configuration
   - Document recovery procedures

## Getting Help

If you encounter issues not covered here:

1. Check the logs for error messages
2. Review the API documentation at http://localhost:8000/docs
3. Open an issue in the repository
4. Check the architecture documentation

## Summary

You should now have a fully functional Startup Investment Intelligence Platform running locally. The system is ready to:

- ✅ Ingest documents (text and PDF)
- ✅ Generate embeddings and store vectors
- ✅ Perform semantic search with citations
- ✅ Track and display metrics
- ✅ Provide investment intelligence

Happy analyzing! 🚀
