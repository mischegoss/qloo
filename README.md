# LumiCue - AI-Powered Cultural Intelligence for Memory Care

## The Story of LumiCue

At the end of her life, finding meaningful connection with my Grandmother was difficult and the silence between us was painful for both of us. We both sought out connection, but it was often elusive.

It turns out, I was not alone. In America, 12 million caregivers provide unpaid care for those with dementia at home (Alzheimer's Association, 2024). And that number is expected to grow. By 2050, the number of people living with dementia could exceed 152 million (Alzheimer's Association, 2024).

The inspiration for LumiCue came from recognizing the power of a tool that can make personalized suggestions could help bridge the communication gap.

**LumiCue is an AI-powered app that uses Qloo's Taste AI to help caregivers and those they care for spark meaningful encounters.** By combining cultural intelligence with personalized recommendations, LumiCue transforms everyday moments into sparks of connection.

When AI works to improve all lives, technology is at its best. And that is the power of LumiCue.

## Project Architecture

LumiCue consists of two main components working together to deliver culturally intelligent memory care solutions:

### 🎨 Frontend Application

**React-based user interface for caregivers and memory care patients**

The LumiCue frontend is an AI-powered cultural intelligence solution designed to help those with memory loss or trouble communicating connect with their caregivers. The app creates culturally relevant, personalized curated conversation starters that engage the senses and feature music, recipes, photos, and stories tailored to the individual.

**Repository**: [LumiCue Frontend](https://github.com/your-username/lumicue-frontend)

**Core Features:**

- **Cultural Intelligence**: Uses Qloo's API to generate culturally relevant content recommendations
- **AI-Powered Personalization**: Leverages Google Gemini AI for content generation and photo analysis
- **Memory Care Focus**: Specifically designed to stimulate memories and provide conversation starters for elderly care
- **Multi-Modal Content**: Combines music (with YouTube integration), recipes, photos, and nostalgia news
- **Feedback System**: Collects user preferences to improve future recommendations
- **Demo Mode**: Showcases the AI pipeline with real-time processing visualization

**Technology Stack:**

- React 18.2.0 with functional components and hooks
- Tailwind CSS 3.3.0 with custom brand colors
- Axios 1.6.0 for API communication
- Lucide React 0.263.1 for icons
- React Testing Library with comprehensive test coverage
- Create React App (react-scripts 5.0.1) for build tooling

### 🤖 Backend API

**8-agent AI processing pipeline powered by cultural intelligence**

LumiCue Backend is a sophisticated 8-agent AI processing pipeline that powers the cultural intelligence behind LumiCue's personalized memory care recommendations. The API orchestrates multiple AI services to generate culturally relevant, personalized content while maintaining strict data privacy and anonymization protocols.

**Repository**: [LumiCue Backend](https://github.com/your-username/lumicue-backend)

**Core Features:**

- **8-Agent AI Pipeline**: Sophisticated multi-step processing system for content generation
- **Cultural Intelligence Integration**: Deep integration with Qloo's Taste AI for cultural grounding
- **PII Compliance**: Complete data anonymization and privacy protection
- **Multi-Modal Processing**: Handles music, recipes, photos, and story generation
- **Real-time Generation**: Live content creation with efficient caching
- **Safety-First Design**: Microwave-only recipes and dementia-appropriate content filtering

**Technology Stack:**

- FastAPI with async/await support
- Python 3.9+
- Google Gemini AI (Flash) for content generation
- Qloo Cultural Intelligence API for cultural preference mapping
- Google Vision AI for image analysis
- YouTube Data API v3 for Creative Commons music discovery

**8-Agent Pipeline:**

1. **Information Consolidator** - Data anonymization and theme selection
2. **Simple Photo Analysis** - Image processing with Google Vision AI
3. **Qloo Cultural Intelligence** - Cultural preference grounding
4. **Music Curation (4A)** - Creative Commons music discovery
5. **Recipe Selection (4B)** - Safe, culturally relevant recipe curation
6. **Photo Description (4C)** - Culturally relevant photo storytelling
7. **Nostalgia News Generator (⭐ Star Feature)** - Personalized historical storytelling
8. **Dashboard Synthesizer** - Final content assembly and formatting

## Complete Installation Instructions

### Prerequisites

- **Node.js 16+** installed
- **Python 3.9+** installed
- **npm or yarn** package manager
- **pip** package manager
- API keys for Qloo, Google Gemini, Google Vision, and YouTube Data API

### Frontend Setup

```bash
# Clone the frontend repository
git clone https://github.com/your-username/lumicue-frontend.git
cd lumicue-frontend

# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend application will launch at `http://localhost:3000`

#### Frontend Available Scripts

```bash
# Development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject configuration (not recommended)
npm run eject
```

#### Frontend Environment Configuration

The app automatically connects to the production backend, but you can override with:

```bash
# Optional: Set custom API URL
export REACT_APP_API_URL=https://your-backend-url.com
npm start
```

#### Frontend Production Deployment

```bash
# Build optimized production bundle
npm run build

# The build folder contains the production-ready application
# Deploy the contents to your web hosting service
```

### Backend Setup

```bash
# Clone the backend repository
git clone https://github.com/your-username/lumicue-backend.git
cd lumicue-backend

# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

#### Backend Available Scripts

```bash
# Development server with hot reload
uvicorn main:app --reload

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000

# Run tests
pytest

# Check code formatting
black .

# Lint code
flake8 .
```

#### Backend Environment Configuration

Create a `.env` file with the following variables:

```bash
# API Keys
QLOO_API_KEY=your_qloo_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Environment
ENVIRONMENT=development
DEBUG=True

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

#### Backend Production Deployment

```bash
# Build for Google Cloud Run
docker build -t lumicue-backend .

# Deploy to Google Cloud Run
gcloud run deploy lumicue-backend \
  --image gcr.io/your-project/lumicue-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2

# The API will be deployed to:
# https://qloo-backend-225790768615.us-central1.run.app
```

## Full System Integration

### Running Both Frontend and Backend

1. **Start the backend** (Terminal 1):

```bash
cd lumicue-backend/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start the frontend** (Terminal 2):

```bash
cd lumicue-frontend/frontend
npm start
```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Status: http://localhost:8000/api/status

### API Integration

The frontend automatically connects to the backend through the following endpoints:

- `POST /api/dashboard` - Generate personalized dashboard content
- `GET /api/status` - Get system health and agent status
- `GET /demo/patients` - Get list of demo patients
- `GET /demo/patients/{patient_id}` - Get specific demo patient

## AI Services Required

LumiCue integrates with multiple AI services. You'll need API keys for:

1. **Qloo Taste AI** - Cultural intelligence and recommendations
2. **Google Gemini AI** - Content generation and storytelling
3. **Google Vision AI** - Image analysis and cultural context
4. **YouTube Data API** - Creative Commons music discovery

## Project Features

### For Caregivers

- **Simple Interface**: Clean, intuitive design prioritizing accessibility
- **Cultural Intelligence**: Content that respects and celebrates diverse backgrounds
- **Safety-First**: All recommendations prioritize patient safety and dignity
- **Conversation Starters**: Guided prompts to facilitate meaningful interactions

### For Memory Care Patients

- **Multi-Sensory Engagement**: Music, recipes, photos, and stories
- **Culturally Relevant**: Content tailored to personal heritage and preferences
- **Memory-Safe**: Appropriate complexity and familiar references
- **Personalized**: AI-driven recommendations that adapt over time

### Technical Highlights

- **8-Agent AI Pipeline**: Sophisticated orchestration of multiple AI services
- **Real-time Processing**: Live demonstration of AI agent execution
- **Bulletproof Fallbacks**: System works even when APIs are unavailable
- **Privacy-First**: Complete data anonymization and PII compliance
- **Production-Ready**: Deployed on Google Cloud with enterprise-grade reliability

## References

Alzheimer's Association. (2024). 2024 Alzheimer's Disease Facts and Figures. Retrieved from https://www.alz.org/alzheimers-dementia/facts-figures

---
