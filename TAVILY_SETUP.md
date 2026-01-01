# Tavily Real-Time Search Integration

## ✅ What's Been Added

Your RAG system now supports **real-time web search** alongside local vector database search!

### Features:
- 🌐 **Real-time web search** for latest startup/investor news
- 🔀 **Hybrid mode**: Combines local DB + live web results
- 🎯 **Specialized searches**: Separate endpoints for startup vs investor queries
- 📊 **Source tracking**: Shows how many results came from local DB vs web

## 🔑 Get Your Tavily API Key

1. Go to: https://tavily.com/
2. Sign up (free tier available)
3. Navigate to API Keys section
4. Copy your API key

## ⚙️ Configuration

Add your Tavily API key to `.env`:

```bash
TAVILY_API_KEY=tvly-YOUR_KEY_HERE
```

## 🚀 Usage Examples

### 1. Search with Web (Default - Hybrid Mode)
```bash
POST /api/v1/search/
{
  "query": "What is OpenAI's latest funding round?",
  "use_web_search": true
}
```
✅ Searches both local DB + live web
📊 Response includes: `sources: {local: 3, web: 5}`

### 2. Web Search Only (Fresh Data)
```bash
POST /api/v1/search/
{
  "query": "Latest AI startup funding news today",
  "web_search_only": true
}
```
✅ Only searches live web (ignores local DB)
🔥 Perfect for breaking news queries

### 3. Local DB Only (No Web)
```bash
POST /api/v1/search/
{
  "query": "Tell me about TechCorp AI",
  "use_web_search": false
}
```
✅ Only searches your local vector database
⚡ Faster, uses your curated data

### 4. Investor Search (Real-time)
```bash
GET /api/v1/search/investor/Sequoia Capital?web_search=true
```
✅ Searches: Crunchbase, Bloomberg, Reuters, WSJ, etc.

### 5. Startup Search (Real-time)
```bash
GET /api/v1/search/startup/OpenAI?web_search=true
```
✅ Searches: TechCrunch, VentureBeat, Forbes, etc.

## 📋 Search Modes Comparison

| Mode | Local DB | Web Search | Use Case |
|------|----------|------------|----------|
| **Hybrid** (default) | ✅ | ✅ | Best of both worlds |
| **Web Only** | ❌ | ✅ | Breaking news, latest info |
| **Local Only** | ✅ | ❌ | Your curated data, faster |

## 🎯 Domain Targeting

### Startup News Sources:
- techcrunch.com
- crunchbase.com
- venturebeat.com
- reuters.com
- bloomberg.com
- forbes.com

### Investor Info Sources:
- pitchbook.com
- crunchbase.com
- bloomberg.com
- wsj.com

## 💡 Example Queries

**Hybrid Search (Local + Web):**
```json
{
  "query": "Which VCs invested in AI startups in 2024?",
  "use_web_search": true,
  "web_search_only": false
}
```

**Web-Only Search (Latest News):**
```json
{
  "query": "What startups raised funding this week?",
  "use_web_search": true,
  "web_search_only": true
}
```

## 📊 Response Format

```json
{
  "query": "...",
  "answer": "Generated answer with real-time data...",
  "citations": [
    {
      "source_title": "OpenAI Raises $10B",
      "source_url": "https://techcrunch.com/...",
      "source_type": "web_search",
      "excerpt": "...",
      "confidence_score": 0.89
    }
  ],
  "retrieved_chunks": 8,
  "sources": {
    "local": 3,
    "web": 5
  },
  "processing_time": 2.3,
  "metadata": {
    "search_mode": "hybrid"
  }
}
```

## 🔧 Rate Limits (Tavily)

**Free Tier:**
- 1,000 requests/month
- Advanced search mode available

**Paid Tier:**
- Unlimited requests
- ~$0.002 per search

## 🚀 Next Steps

1. Get your Tavily API key: https://tavily.com/
2. Add to `.env` file
3. Rebuild containers: `docker-compose down && docker-compose up -d --build`
4. Test: Search for "latest AI startup funding"

## 🎉 Benefits

✅ **Real-time data**: Get latest news without manual data ingestion
✅ **Source diversity**: Combines your curated DB + live web
✅ **Citation tracking**: All web sources properly cited
✅ **Flexible**: Choose mode per query
