"""
Complete Cleaned main.py - Photo Uploads Removed for Hackathon
File: backend/main.py

Main FastAPI application for CareConnect Cultural Intelligence API
CLEANED: All personal photo upload endpoints removed for hackathon focus
"""

import os
import logging
import time
import json
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import CareConnect multi-agent system
try:
    from multi_tool_agent.tools import initialize_all_tools, test_all_tools
    logger.info("✅ Tools module imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import tools: {e}")
    initialize_all_tools = None
    test_all_tools = None

try:
    from multi_tool_agent.sequential_agent import SequentialAgent
    logger.info("✅ SequentialAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import SequentialAgent: {e}")
    SequentialAgent = None

# Import enhanced theme manager
try:
    from config.theme_config import theme_manager
    logger.info("✅ Enhanced theme manager imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import theme manager: {e}")
    theme_manager = None

# Configuration
class Config:
    PORT = int(os.getenv("PORT", 8000))
    QLOO_API_KEY = os.getenv("QLOO_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

config = Config()

# Request models
class PatientProfile(BaseModel):
    first_name: str
    birth_year: Optional[int] = None
    birth_month: Optional[str] = None
    cultural_heritage: Optional[str] = None
    hometown: Optional[str] = None  # NEW: Hometown preference
    location: Optional[str] = None  # Current location fallback
    city: Optional[str] = None      # Legacy support
    state: Optional[str] = None     # Legacy support
    additional_context: Optional[str] = None

class CareConnectRequest(BaseModel):
    patient_profile: PatientProfile
    request_type: str = "dashboard"
    session_id: Optional[str] = None
    feedback_history: Optional[Dict[str, Any]] = None

# Global variables
tools = None
sequential_agent = None
patient_manager = None

# Cleaned Demo Patient Manager class
class DemoPatientManager:
    """Cleaned demo patient manager - photo uploads removed for hackathon"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "frontend" / "static" / "demo" / "data"
        self.patients_file = self.data_dir / "patients.json"
        self.dashboard_cache = {"content": None, "timestamp": None, "expiry_minutes": 5}
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 Demo patient manager initialized")
        logger.info(f"📄 Patients file: {self.patients_file}")
    
    def get_patient(self):
        """Get the demo patient"""
        try:
            if self.patients_file.exists():
                with open(self.patients_file, 'r') as f:
                    data = json.load(f)
                    return data.get("demo_patient")
            return self._create_demo_patient()
        except Exception as e:
            logger.error(f"❌ Failed to load patient: {e}")
            return self._create_demo_patient()
    
    def update_patient(self, patient_data):
        """Update patient data"""
        try:
            data = {"demo_patient": patient_data}
            with open(self.patients_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("✅ Patient data updated")
        except Exception as e:
            logger.error(f"❌ Failed to update patient: {e}")
    
    def get_cached_dashboard(self):
        """Get cached dashboard if still valid"""
        if not self.dashboard_cache["content"]:
            return None
        
        if self.dashboard_cache["timestamp"]:
            cache_time = datetime.fromisoformat(self.dashboard_cache["timestamp"])
            if datetime.now() - cache_time > timedelta(minutes=self.dashboard_cache["expiry_minutes"]):
                logger.info("⏰ Dashboard cache expired")
                return None
        
        return self.dashboard_cache
    
    def update_dashboard_cache(self, content):
        """Update dashboard cache"""
        self.dashboard_cache = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "expiry_minutes": 5
        }
        logger.info("📊 Dashboard cache updated")
    
    def _create_demo_patient(self):
        """Create demo patient data if none exists"""
        demo_patient = {
            "first_name": "Maria",
            "birth_year": 1945,
            "birth_month": "March",
            "cultural_heritage": "Italian-American",
            "hometown": "Brooklyn, NY",  # NEW: Hometown preference
            "city": "Brooklyn",
            "state": "New York",
            "additional_context": "Loves music and cooking. Has 4 children and 7 grandchildren.",
            "caregiver_notes": "Responds well to music from the 1960s-70s. Enjoys looking at family photos.",
            "demo_dislikes": [],
            "feedback_points": 0,
            "created_date": datetime.now().isoformat()
        }
        
        # Save demo patient
        self.update_patient(demo_patient)
        logger.info("👤 Demo patient created: Maria")
        return demo_patient

# Startup function
async def startup():
    """Initialize the application"""
    global tools, sequential_agent, patient_manager
    
    logger.info("🚀 Starting CareConnect API...")
    
    # Initialize patient manager
    patient_manager = DemoPatientManager()
    
    # Initialize tools
    if initialize_all_tools:
        logger.info("🔧 Initializing tools...")
        tools = initialize_all_tools()
        if tools:
            logger.info("✅ All tools initialized successfully")
            
            # Test tools
            if test_all_tools:
                logger.info("🧪 Testing tools...")
                test_results = await test_all_tools(tools)
                logger.info(f"🧪 Tool test results: {test_results}")
        else:
            logger.error("❌ Tool initialization failed")
    
    # Initialize sequential agent
    if tools and SequentialAgent:
        try:
            from multi_tool_agent.agents.information_consolidator_agent import InformationConsolidatorAgent
            from multi_tool_agent.agents.cultural_profile_agent import CulturalProfileBuilderAgent
            from multi_tool_agent.agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
            from multi_tool_agent.agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
            from multi_tool_agent.agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
            from multi_tool_agent.agents.mobile_synthesizer_agent import MobileSynthesizerAgent
            
            # Initialize agents
            agent1 = InformationConsolidatorAgent()
            agent2 = CulturalProfileBuilderAgent()
            agent3 = QlooCulturalIntelligenceAgent(tools['qloo_tool'])
            agent4 = SensoryContentGeneratorAgent(tools['gemini_tool'], tools['youtube_tool'])
            agent5 = PhotoCulturalAnalyzerAgent(tools['vision_ai_tool'])  # Places photo analysis only
            agent6 = MobileSynthesizerAgent()
            
            sequential_agent = SequentialAgent(agent1, agent2, agent3, agent4, agent5, agent6)
            logger.info("✅ Sequential agent initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Sequential agent initialization failed: {e}")
            sequential_agent = None
    
    logger.info("🎯 CareConnect API startup complete - Hackathon mode: Places with Vision Analysis")

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield

# FastAPI app
app = FastAPI(
    title="CareConnect Cultural Intelligence API",
    description="AI-powered dementia care assistant with cultural intelligence - Hackathon Version",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ===== MAIN DASHBOARD ENDPOINT =====

@app.get("/dashboard")
async def get_dashboard():
    """Generate dashboard with Places Vision Analysis"""
    global patient_manager, sequential_agent
    
    if not sequential_agent:
        return {"error": "Sequential agent not initialized"}
    
    try:
        # Check for cached dashboard
        cached_dashboard = patient_manager.get_cached_dashboard()
        if cached_dashboard and cached_dashboard.get("content"):
            logger.info("📊 Returning cached dashboard")
            return cached_dashboard["content"]
        
        # If no cache, generate new dashboard
        return await refresh_dashboard()
        
    except Exception as e:
        logger.error(f"❌ Dashboard generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

@app.post("/refresh-dashboard")
async def refresh_dashboard():
    """Refresh dashboard with Places Vision Analysis"""
    global patient_manager, sequential_agent
    
    if not sequential_agent:
        raise HTTPException(status_code=500, detail="Sequential agent not initialized")
    
    try:
        logger.info("🔄 Refreshing dashboard...")
        
        # Get patient profile
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Demo patient not found")
        
        # Run the complete pipeline
        logger.info("🚀 Running 6-agent pipeline...")
        result = await sequential_agent.run(
            patient_profile=patient,
            request_type="dashboard",
            session_id="demo_session"
        )
        
        if result and result.get("success"):
            logger.info("✅ Pipeline execution successful")
            
            # Cache the result
            patient_manager.update_dashboard_cache(result)
            
            return result
        else:
            logger.error("❌ Pipeline execution failed")
            raise HTTPException(status_code=500, detail="Pipeline execution failed")
            
    except Exception as e:
        logger.error(f"❌ Dashboard refresh failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard refresh failed: {str(e)}")

# ===== PATIENT AND FEEDBACK ENDPOINTS =====

@app.get("/patient")  
async def get_patient_profile():
    """Get patient profile for profile page"""
    patient = patient_manager.get_patient()
    if not patient:
        raise HTTPException(status_code=404, detail="Demo patient not found")
    
    return {
        "status": "success",
        "patient": patient,
        "personalization_status": {
            "feedback_points": patient.get("feedback_points", 0),
            "status": "Getting started!" if patient.get("feedback_points", 0) < 3 else "Learning well!",
            "blocked_items_count": len(patient.get("demo_dislikes", []))
        }
    }

@app.post("/feedback")
async def submit_feedback(request: Dict[str, Any]):
    """Submit user feedback for learning"""
    global patient_manager
    
    try:
        feedback_type = request.get("feedback_type")  # "like" or "dislike"
        item_type = request.get("item_type")  # "music", "recipe", "tv_show", "place"
        item_name = request.get("item_name", "Unknown")
        
        patient = patient_manager.get_patient()
        if not patient:
            return {"error": "No patient found"}
        
        # Update feedback points
        patient["feedback_points"] = patient.get("feedback_points", 0) + 1
        
        # Handle dislikes
        if feedback_type == "dislike":
            if "demo_dislikes" not in patient:
                patient["demo_dislikes"] = []
            
            dislike_entry = {
                "type": item_type,
                "name": item_name,
                "timestamp": datetime.now().isoformat()
            }
            patient["demo_dislikes"].append(dislike_entry)
            
            logger.info(f"➖ Added dislike: {item_type} - {item_name}")
        
        # Save updated patient
        patient_manager.update_patient(patient)
        
        return {
            "success": True,
            "message": f"Feedback recorded: {feedback_type} for {item_type}",
            "feedback_points": patient["feedback_points"]
        }
        
    except Exception as e:
        logger.error(f"❌ Feedback submission failed: {e}")
        return {"error": f"Feedback submission failed: {str(e)}"}

# ===== HEALTH AND STATUS ENDPOINTS =====

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_keys_configured": {
            "qloo": bool(config.QLOO_API_KEY),
            "youtube": bool(config.YOUTUBE_API_KEY),
            "google_cloud": bool(config.GOOGLE_CLOUD_API_KEY),
            "gemini": bool(config.GEMINI_API_KEY)
        },
        "port": config.PORT,
        "tools_initialized": tools is not None,
        "agent_available": sequential_agent is not None,
        "pipeline_mode": "places_with_vision_analysis"
    }

@app.get("/tools/status")
async def tools_status():
    """Get status of all tools"""
    if not tools:
        return {"error": "Tools not initialized"}
    
    try:
        # Run tool tests
        test_results = await test_all_tools(tools)
        return {
            "tools_available": list(tools.keys()) if tools else [],
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Tools status check failed: {e}")
        return {"error": f"Tools status check failed: {str(e)}"}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CareConnect Cultural Intelligence API - Hackathon Version",
        "version": "1.0.0",
        "description": "AI-powered dementia care assistant with Places + Vision Analysis",
        "endpoints": {
            "dashboard": "/dashboard",
            "refresh": "/refresh-dashboard",
            "patient": "/patient",
            "feedback": "/feedback",
            "health": "/health",
            "tools_status": "/tools/status"
        },
        "features": {
            "qloo_cultural_intelligence": "Multi-domain cultural recommendations",
            "vision_analysis": "Google Vision analysis of place photos",
            "theme_integration": "Daily themed conversations",
            "feedback_learning": "Caregiver feedback adaptation"
        },
        "pipeline_mode": "places_with_vision_analysis",
        "demo_patient": "Maria - Italian-American from Brooklyn, NY"
    }

if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting CareConnect API server on port {config.PORT}")
    logger.info(f"Data directory: {patient_manager.data_dir if patient_manager else 'Not initialized'}")
    logger.info("🎯 CLEANED: Photo upload endpoints removed for hackathon focus")
    logger.info("📍 NEW: Places with Google Vision analysis enabled")
    logger.info("🎯 Single patient demo mode enabled")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )