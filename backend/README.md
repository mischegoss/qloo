# LumiCue Backend

## What the API Does

LumiCue Backend is a sophisticated 8-agent AI processing pipeline that powers the cultural intelligence behind LumiCue's personalized recommendations. The API orchestrates multiple AI services to generate culturally relevant, personalized content while maintaining strict data privacy and anonymization protocols.

**Core Features:**

- **8-Agent AI Pipeline**: Sophisticated multi-step processing system for content generation
- **Cultural Intelligence Integration**: Deep integration with Qloo's Taste AI for cultural grounding
- **PII Compliance**: Complete data anonymization and privacy protection
- **Multi-Modal Processing**: Handles music, recipes, photos, and story generation
- **Real-time Generation**: Live content creation with efficient caching
- **Safety-First Design**: Microwave-only recipes and dementia-appropriate content filtering

## Pipeline Architecture

### Core Agents

#### **Agent 1: Information Consolidator**

- **Purpose**: Verify data anonymization and theme selection (Data is anonymized in frontend)
- **Key Features**:
  - Ensures patient data anonymization and PII removal
  - Daily theme generation and selection
  - Profile data structuring for downstream agents

#### **Agent 2: Simple Photo Analysis**

- **Purpose**: Image processing and theme-appropriate photo selection
- **Features**:
  - Google Vision AI integration for image analysis (for new images and as backup, current images are preprocessed by Google Vision AI)
  - Theme-based photo selection algorithm
  - Cultural context analysis for images
  - Metadata extraction and description generation

#### **Agent 3: Qloo Cultural Intelligence**

- **Purpose**: Cultural preference grounding and taste intelligence
- **Features**:
  - Qloo Taste AI integration for cultural affinities
  - Anonymous profile mapping to cultural preferences
  - This data becomes the basis for the content curation below
 

#### **Agent 4: Music Curation**

- **Purpose**: Creative Commons music discovery and curation
- **Features**:
  - YouTube Data API integration for music search
  - Creative Commons license filtering and validation
  - Cultural music preference matching
  - Conversation starter generation for music content

#### **Agent 5: Recipe Selection**

- **Purpose**: Safe, culturally relevant recipe curation
- **Features**:
  - Curated JSON database of microwave-only recipes
  - Cultural heritage recipe matching
  - Safety filtering (no sharp objects, stoves, or complex procedures)
  - Ingredient simplification (3-5 items maximum)
  - Memory-triggering recipe selection 

#### **Agent 6: Photo Description**

- **Purpose**: Relevant photo storytelling
- **Features**:
  - Theme-appropriate narrative creation with Google Gemini AI
  - Conversation starter generation around images
  - Memory care appropriate content validation

#### **Agent 7: Nostalgia News Generator** ⭐ **Star Feature**

- **Purpose**: Personalized historical and cultural story generation
- **Features**:
  - Google Gemini AI integration for story generation
  - Historical event personalization 
  - Cultural bridge creation between past and present
  - Memory-safe content generation with appropriate complexity

#### **Agent 8: Dashboard Synthesizer**

- **Purpose**: Final content assembly and API response formatting
- **Features**:
  - Multi-agent output integration and synthesis
  - JSON response formatting and validation
  - Content quality assurance and filtering
  - Metadata generation for frontend consumption


## Technology Stack

- **Backend Framework**: FastAPI
- **Programming Language**: Python 3.9+
- **AI Services**: Google Gemini AI, Google Vision AI
- **Cultural Intelligence**: Qloo Taste AI integration
- **HTTP Client**: httpx for async API communication
- **Data Validation**: Pydantic models for request/response validation
- **Environment Management**: python-dotenv for configuration
- **YouTube Data API v3**: Creative Commons music discovery and curation

## AI Integration

- **Google Gemini AI (Flash)**: Content generation and storytelling
- **Qloo Cultural Intelligence API**: Cultural preference mapping and recommendations that serve as grounding for content creation
- **Google Vision AI**: Image analysis and cultural context extraction


## How to Start the Application

### Prerequisites

- Python 3.9+ installed
- pip package manager
- API keys for Qloo, Google Gemini, Google Vision, and YouTube Data API

### Installation & Setup

```bash
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

The API will be available at `http://localhost:8000`

### Available Scripts

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

### Environment Configuration

Create a `.env` file with the following variables:

```bash
# API Keys
QLOO_API_KEY=your_qloo_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Environment
ENVIRONMENT=development
DEBUG=True

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

## API Endpoints

### Core Application Endpoints

- `POST /api/dashboard` - Generate personalized dashboard content using the 8-agent pipeline
- `GET /api/status` - Get detailed API status including agent and tool status


### API Features

- **Dashboard Generation**: The primary `/api/dashboard` endpoint orchestrates the complete 8-agent pipeline
- **Real-time Status**: The `/api/status` endpoint provides live system health and agent readiness
- **Demo Integration**: Built-in demo patient management for testing and demonstrations
- **Error Handling**: Comprehensive HTTP status codes and error messages
- **CORS Support**: Cross-origin resource sharing configured for frontend integration
