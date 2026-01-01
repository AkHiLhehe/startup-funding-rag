# 🚀 Push to GitHub - Complete Guide

## Step 1: Initialize Git Repository

```powershell
cd "C:\Users\sriak\OneDrive\Desktop\Sem 6\Anokha4"
git init
```

## Step 2: Add All Files

```powershell
git add .
```

## Step 3: Create Initial Commit

```powershell
git commit -m "Production-grade RAG system with Voyage AI embeddings and Tavily real-time search"
```

## Step 4: Connect to GitHub Repository

**Option A: If you already have a GitHub repo, replace with your repo URL:**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

**Option B: If you need to create a new repo:**
1. Go to https://github.com/new
2. Create a new repository (e.g., "startup-rag-system")
3. Copy the repository URL
4. Run:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Step 5: Force Push (Replace Everything)

**⚠️ This will REPLACE all files in the remote repository:**

```powershell
git branch -M main
git push -u origin main --force
```

## 📋 Complete Commands (Copy-Paste Ready)

```powershell
# Navigate to project
cd "C:\Users\sriak\OneDrive\Desktop\Sem 6\Anokha4"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Production RAG system: Voyage AI + Tavily + Weaviate + MongoDB + React"

# Add your GitHub remote (REPLACE WITH YOUR REPO URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Force push to replace everything
git branch -M main
git push -u origin main --force
```

## 🔐 If You Need Authentication

**For private repos, you'll need a Personal Access Token:**

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy the token
5. When prompted for password, use the token instead

## ✅ What Gets Pushed

Your complete RAG system:
- ✅ Backend (FastAPI + Python)
  - Voyage AI embeddings (1024-dim)
  - Tavily real-time search
  - Weaviate vector DB integration
  - MongoDB document storage
  - Gemini LLM integration
- ✅ Frontend (React + TypeScript + Tailwind)
- ✅ Docker configuration
- ✅ All services and routes
- ✅ Documentation

## 🚫 What Gets Ignored (.gitignore)

- ❌ `.env` files (API keys protected)
- ❌ `node_modules/`
- ❌ `__pycache__/`
- ❌ Docker volumes
- ❌ Log files
- ❌ IDE configs

## 📝 Next Steps After Push

1. **Add Secrets to GitHub** (for CI/CD):
   - Go to: Settings → Secrets and variables → Actions
   - Add: `VOYAGE_API_KEY`, `TAVILY_API_KEY`, `GEMINI_API_KEY`

2. **Update README.md** with:
   - Setup instructions
   - API key requirements
   - Docker commands

3. **Create `.env.example`**:
```bash
# Copy this to .env and fill in your keys
VOYAGE_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

## 🔄 To Update Repository Later

```powershell
# After making changes
git add .
git commit -m "Your update message"
git push origin main
```

## ❓ Need the Repo URL?

Tell me your GitHub username and I'll help format the commands!
