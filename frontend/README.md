# LumiCue Frontend

## What the App Does

LumiCue is an AI-powered cultural intelligence solution designed to help those with memory loss or trouble communicating connect with their caregivers. The app creates culturally relevant, personalized curated conversation starters that engage the senses and feature music, recipes, photos, and stories tailored to the individual. A powerful feedback mechanism helps ensure that the recommendations improve over time.

**Core Features:**

- **Cultural Intelligence**: Uses Qloo's API to generate culturally relevant content recommendations
- **AI-Powered Personalization**: Leverages Google Gemini AI for content generation and photo analysis
- **Memory Care Focus**: Specifically designed to stimulate memories and provide conversation starters for elderly care
- **Multi-Modal Content**: Combines music (with YouTube integration), recipes, photos, and nostalgia news
- **Feedback System**: Collects user preferences to improve future recommendations
- **Demo Mode**: Showcases the AI pipeline with real-time processing visualization
- **Anonymized Data**: All data is anonymized before sending to the backend, ensuring privacy and PII compliance.

## Component Architecture

### Core Components

#### **App.js** - Main Application Container

- **Purpose**: Root component managing application state and routing
- **Key Features**:
  - State management for current page/view navigation
  - Profile management with localStorage persistence
  - Dashboard data loading with fallback system
  - Integration with API services and feedback collection
  - Navigation between app and demo modes

#### **Dashboard.js** - Main Content Hub

- **Purpose**: Primary interface displaying personalized content cards
- **Features**:
  - Grid layout with music, recipe, photo, and nostalgia news cards
  - Interactive cards with hover effects and click navigation
  - Patient profile integration for personalized greetings
  - Refresh dashboard functionality

#### **Detail Components** - Content Pages

- **MusicDetail.js**: Displays personalized music with YouTube integration and conversation starters
- **PhotoDetail.js**: Shows culturally analyzed photos with AI-generated descriptions
- **RecipeDetail.js**: Features traditional recipes with cultural context and instructions
- **NostalgiaDetail.js**: Presents personalized historical content and cultural stories

#### **ProfileInfo.js** - User Profile Management

- **Purpose**: Patient profile configuration and feedback review
- **Features**:
  - Locked/unlocked editing mode for safety
  - Cultural heritage configuration (up to 3 backgrounds)
  - Birth year, location, and interests management
  - Feedback history display (likes/dislikes)
  - Admin view for technical details

#### **Demo.js** - AI Pipeline Visualization

- **Purpose**: Showcases the AI processing pipeline for demonstrations
- **Features**:
  - Real-time agent execution visualization (6-step process)
  - Technical architecture display
  - API response preview
  - Return to dashboard integration

#### **LoadingSpinner.js** - Professional Loading UI

- **Purpose**: Branded loading experience with LumiCue animations
- **Features**:
  - Custom animations with brand colors
  - Progressive content loading visualization
  - Responsive design

### Service Layer

#### **apiService.js** - API Integration

- **Purpose**: Handles all backend communication with fallback
- **Key Features**:
  - Production API integration (`qloo-backend-225790768615.us-central1.run.app`)
  - Intelligent caching system with localStorage
  - Fallback data when API is unavailable
  - Session management and anonymized profile handling
  - Error handling and retry logic

#### **dashboardDataStore.js** - Global State Management

- **Purpose**: Centralized data store for dashboard content
- **Features**:
  - Singleton pattern for consistent data access
  - Bulletproof fallback integration
  - Component subscription system for reactive updates
  - Data validation and mapping

### Utility Layer

#### **feedbackManager.js** - User Preference Tracking

- **Purpose**: Collects and manages user feedback (likes/dislikes)
- **Features**:
  - Local storage of preferences
  - Category-based feedback (music, recipes, photos, nostalgia)
  - API formatting for backend integration
  - Feedback analytics and summary

#### **dataMappers.js** - Data Transformation

- **Purpose**: Maps API responses to UI-friendly data structures
- **Features**:
  - Safe data extraction with fallbacks
  - Type validation and conversion
  - UI-specific data formatting

## Technology Stack

- **Frontend**: React 18.2.0 
- **Styling**: Tailwind CSS 3.3.0 
- **HTTP Client**: Axios 1.6.0 

## AI Integration

- **Google Gemini AI**: Content generation and photo analysis
- **Qloo Cultural Intelligence API**: Cultural affinity recommendations
- **YouTube Data API**: Music video integration
- **Google Vision AI**: Image context analysis

## How to Start the Application

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation & Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The application will launch at `http://localhost:3000`

### Available Scripts

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

### Environment Configuration

The app automatically connects to the production backend, but you can override with:

```bash
# Optional: Set custom API URL
export REACT_APP_API_URL=https://your-backend-url.com
npm start
```

### Production Deployment

```bash
# Build optimized production bundle
npm run build

# The build folder contains the production-ready application
# Deploy the contents to your web hosting service
```
