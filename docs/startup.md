# CareConnect - Getting Started Guide

> Complete development environment setup for the AI-powered dementia care assistant

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Git** installed
- **Google Cloud account** with billing enabled
- **Qloo hackathon API key**

## 🔑 API Keys Required

You'll need keys from these services:

- [ ] **Qloo Hackathon API** - [Get key here](https://forms.gle/K1LVBUWReabqA3wQ8)
- [ ] **Google Cloud API** - [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- [ ] **Google AI Studio** - [ai.google.dev](https://ai.google.dev) (for Gemini)

## 🚀 Quick Setup (5 Minutes)

### 1. Clone and Setup Project Structure

```bash
# Clone the repository
git clone <your-repo-url>
cd careconnect

# Verify project structure
ls -la
# Should see: frontend/, backend/, docs/, tests/, .env, README.md
```

### 2. Environment Variables Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your actual API keys
nano .env  # or code .env
```

**Required .env configuration:**

```bash
# Qloo API
QLOO_API_KEY=your_qloo_hackathon_key_here

# Google Cloud APIs (same key for all)
GOOGLE_CLOUD_API_KEY=your_google_cloud_key_here
YOUTUBE_API_KEY=your_google_cloud_key_here

# Google AI Studio (Gemini)
GEMINI_API_KEY=your_gemini_key_here

# React Frontend
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_YOUTUBE_API_KEY=your_google_cloud_key_here

# Database
DATABASE_URL=sqlite:///./backend/careconnect.db

# Development Settings
DEBUG=True
BACKEND_HOST=localhost
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### 3. Backend Setup (Python/FastAPI)

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# If requirements.txt doesn't exist yet, install core packages:
pip install fastapi uvicorn python-dotenv requests

# Generate requirements.txt
pip freeze > requirements.txt

# Test API integrations
cd ..
python tests/api_integration_test.py
```

### 4. Frontend Setup (React)

```bash
# Navigate to frontend (if not created yet)
cd frontend

# If frontend doesn't exist, create it:
# npx create-react-app .

# Install dependencies
npm install

# Install additional CareConnect dependencies
npm install @mui/material @emotion/react @emotion/styled axios lucide-react

# Start development server
npm start
```

## 🛠️ Google Cloud Setup

### Enable Required APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   ```
   Cloud Vision API
   YouTube Data API v3
   Generative Language API (if using Vertex AI)
   ```

### Create API Key

```bash
# In Google Cloud Console:
# 1. Go to APIs & Services > Credentials
# 2. Click "Create Credentials" > "API Key"
# 3. Restrict the key to your APIs
# 4. Add HTTP referrers: localhost:*/*
```

### Set API Restrictions

**Application restrictions:**

- Type: HTTP referrers
- Referrers:
  ```
  localhost:3000/*
  localhost:8000/*
  127.0.0.1:3000/*
  127.0.0.1:8000/*
  ```

**API restrictions:**

- Cloud Vision API
- YouTube Data API v3

## 🧪 Verify Installation

### Test Backend APIs

```bash
# From project root
source backend/.venv/bin/activate
python tests/api_integration_test.py

# Expected output:
# ✅ Qloo API: WORKING
# ✅ Vision AI: WORKING
# ✅ YouTube API: WORKING
# ✅ MusicBrainz API: WORKING
# 🚀 PERFECT: All APIs working!
```

### Test Frontend

```bash
cd frontend
npm start

# Browser should open to http://localhost:3000
# Should see CareConnect landing page
```

### Test Backend Server

```bash
cd backend
source .venv/bin/activate
python main.py

# Should see:
# INFO: Uvicorn running on http://127.0.0.1:8000
# Visit http://localhost:8000/docs for API documentation
```

## 🔄 Daily Development Workflow

### Start Backend Server

```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate
python main.py

# Server runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Start Frontend Development

```bash
# Terminal 2: Frontend
cd frontend
npm start

# React app runs on http://localhost:3000
# Auto-reloads on file changes
```

### Run Tests

```bash
# Terminal 3: Testing
source backend/.venv/bin/activate

# Test API integrations
python tests/api_integration_test.py

# Test backend functionality
pytest backend/tests/

# Test frontend
cd frontend
npm test
```

## 🐛 Troubleshooting

### Virtual Environment Issues

```bash
# If .venv activation fails:
rm -rf backend/.venv
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### API Key Issues

```bash
# Verify .env file is in root directory
cat .env | grep API_KEY

# Check environment loading
cd backend
source .venv/bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv('../.env')
print('QLOO_API_KEY:', bool(os.getenv('QLOO_API_KEY')))
print('GOOGLE_CLOUD_API_KEY:', bool(os.getenv('GOOGLE_CLOUD_API_KEY')))
"
```

### Google Cloud API Errors

```bash
# Common "API key expired" error usually means:
# 1. Wrong API key (check you're using Google Cloud Console key, not AI Studio)
# 2. APIs not enabled in Google Cloud Console
# 3. Key restrictions too strict

# Test direct API access:
curl "https://vision.googleapis.com/v1/images:annotate?key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"requests":[{"image":{"content":"test"},"features":[{"type":"LABEL_DETECTION"}]}]}'
```

### Frontend Connection Issues

```bash
# If frontend can't connect to backend:
# 1. Verify backend is running on port 8000
# 2. Check REACT_APP_BACKEND_URL in .env
# 3. Disable CORS temporarily for testing

# Test backend connectivity:
curl http://localhost:8000/health
```

## 📦 Package Management

### Adding New Python Dependencies

```bash
cd backend
source .venv/bin/activate

# Install new package
pip install new-package

# Update requirements
pip freeze > requirements.txt

# Commit requirements.txt
git add requirements.txt
git commit -m "Add new-package dependency"
```

### Adding New Frontend Dependencies

```bash
cd frontend

# Install new package
npm install new-package

# Package.json automatically updated
git add package.json package-lock.json
git commit -m "Add new-package frontend dependency"
```

## 🚀 Deployment Preparation

### Backend Build

```bash
cd backend
source .venv/bin/activate

# Create production requirements
pip freeze > requirements.txt

# Test production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Build

```bash
cd frontend

# Create production build
npm run build

# Test production build locally
npx serve -s build -l 3000
```

## 🔗 Useful Commands Reference

```bash
# Quick restart everything
npm run dev:all          # If you set up npm scripts

# Manual restart
pkill -f "python main.py" && pkill -f "npm start"
cd backend && source .venv/bin/activate && python main.py &
cd frontend && npm start &

# View logs
tail -f backend/logs/app.log
npm run build --verbose

# Check ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Environment debugging
env | grep API_KEY
python -c "import os; print([k for k in os.environ.keys() if 'API' in k])"
```
