# 🚀 Quick Start Guide

Get the Startup Investment Intelligence Platform running in 5 minutes!

## Prerequisites

- Docker Desktop installed and running
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation Steps

### 1. Navigate to Project
```powershell
cd "c:\Users\sriak\OneDrive\Desktop\Sem 6\Anokha4"
```

### 2. Configure API Keys
```powershell
# Backend configuration
cd backend
cp .env.example .env
```

Edit `backend\.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Start All Services
```powershell
cd ..
docker-compose up -d
```

Wait 30-60 seconds for all services to initialize.

### 4. Verify Installation
```powershell
# Check if services are running
docker-compose ps

# Test backend
curl http://localhost:8000/api/v1/health
```

### 5. Access the Application

Open your browser:
- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## Seed Sample Data

To populate the system with example data:

```powershell
# Enter backend container
docker-compose exec backend python seed_data.py
```

Or if running locally:
```powershell
cd backend
python seed_data.py
```

## Try It Out!

1. **Search for Information**
   - Go to http://localhost:3000/search
   - Try: "Tell me about TechCorp AI's recent funding"
   - Or: "Which investors focus on AI startups?"

2. **Ingest a Document**
   - Go to http://localhost:3000/ingest
   - Paste any startup news article
   - Click "Ingest Document"

3. **View Analytics**
   - Go to http://localhost:3000/analytics
   - See system metrics and performance

## Example Queries

After seeding data, try these queries:

```
"What is Sequoia Capital's investment thesis?"
"Tell me about TechCorp AI's Series B funding round"
"Which investors focus on early-stage fintech?"
"Compare FintechPlus and HealthTech Solutions"
```

## Troubleshooting

**Services won't start?**
```powershell
docker-compose down
docker-compose up -d --build
```

**Port conflicts?**
```powershell
# Stop conflicting services or change ports in docker-compose.yml
netstat -ano | findstr :8000
```

**Can't access frontend?**
- Wait 1-2 minutes for npm install to complete
- Check logs: `docker-compose logs frontend`

## Next Steps

- Read the full [README.md](../README.md)
- Check [SETUP.md](SETUP.md) for detailed instructions
- Explore [ARCHITECTURE.md](ARCHITECTURE.md) for system design

## Stopping the System

```powershell
# Stop all services
docker-compose down

# Stop and remove volumes (full reset)
docker-compose down -v
```

---

**That's it!** You now have a production-grade RAG system running locally. 🎉
