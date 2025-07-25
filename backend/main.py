"""
Enhanced LumiCue Main Application with Simple Profile-Based Feedback
File: backend/main.py

CHANGES MADE:
- Enhanced /feedback endpoint to track likes and update learning insights
- Enhanced /patient endpoint to return learning insights
- Added simple learning messages to dashboard
- All changes are additive - no existing functionality removed
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

# Enhanced Demo Patient Manager class
class DemoPatientManager:
    """Enhanced demo patient manager with learning insights"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "frontend" / "static" / "demo" / "data"
        self.patients_file = self.data_dir / "patients.json"
        self.dashboard_cache = {"content": None, "timestamp": None, "expiry_minutes": 5}
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 Enhanced demo patient manager initialized")
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
            logger.error(f"Error loading patient: {e}")
            return self._create_demo_patient()
    
    def update_patient(self, patient_data):
        """Update the demo patient data"""
        try:
            # Read existing data
            if self.patients_file.exists():
                with open(self.patients_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            # Update demo patient
            data["demo_patient"] = patient_data
            
            # Write back to file
            with open(self.patients_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info("✅ Patient data updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating patient: {e}")
    
    def get_dashboard_cache(self):
        """Get cached dashboard if valid"""
        try:
            cache = self.dashboard_cache
            if cache["content"] and cache["timestamp"]:
                cache_time = datetime.fromisoformat(cache["timestamp"])
                expiry_time = cache_time + timedelta(minutes=cache["expiry_minutes"])
                
                if datetime.now() < expiry_time:
                    logger.info("📊 Returning cached dashboard")
                    return cache["content"]
                else:
                    logger.info("📊 Dashboard cache expired")
                    return None
            return None
            
        except Exception as e:
            logger.error(f"Error checking dashboard cache: {e}")
            return None
    
    def update_dashboard_cache(self, dashboard_data):
        """Update dashboard cache"""
        try:
            self.dashboard_cache = {
                "content": dashboard_data,
                "timestamp": datetime.now().isoformat(),
                "expiry_minutes": 5
            }
            logger.info("✅ Dashboard cache updated")
            
        except Exception as e:
            logger.error(f"Error updating dashboard cache: {e}")
    
    def _create_demo_patient(self):
        """Create demo patient with enhanced fields"""
        demo_patient = {
            "first_name": "Maria",
            "birth_year": 1945,
            "birth_month": "March",
            "cultural_heritage": "Italian-American",
            "city": "Brooklyn",
            "state": "New York",
            "additional_context": "Loves music and cooking",
            "caregiver_notes": "Enjoys family activities and traditional Italian recipes",
            "photo_library": [
                "static/demo/images/maria_sample_wedding.jpg",
                "static/demo/images/maria_sample_family.jpg"
            ],
            "photo_analyses": {
                "static/demo/images/maria_sample_wedding.jpg": {
                    "vision_analysis": {
                        "objects": ["dress", "flowers", "church", "people"],
                        "labels": ["wedding", "celebration", "formal wear", "ceremony"],
                        "people": ["bride", "groom"],
                        "activities": ["celebration", "ceremony"],
                        "settings": ["church", "indoor"]
                    },
                    "processed_date": "2025-01-23T00:00:00Z"
                }
            },
            "feedback_points": 3,
            "demo_dislikes": [],
            "liked_items": [],
            "learning_insights": {
                "avoiding": [],
                "prefers": [],
                "last_updated": "2025-01-23T00:00:00Z"
            },
            "last_photo_shown": None,
            "photo_rotation_index": 1,
            "created_date": datetime.now().isoformat()
        }
        
        # Save demo patient
        self.update_patient(demo_patient)
        logger.info("👤 Enhanced demo patient created: Maria")
        return demo_patient

# Startup function
async def startup():
    """Initialize the application"""
    global tools, sequential_agent, patient_manager
    
    logger.info("🚀 Starting Enhanced CareConnect API...")
    
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
            logger.info("✅ Enhanced sequential agent initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Sequential agent initialization failed: {e}")
            sequential_agent = None
    
    logger.info("🎯 Enhanced CareConnect API startup complete - Hackathon mode with Learning")

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield

# FastAPI app
app = FastAPI(
    title="Enhanced CareConnect Cultural Intelligence API",
    description="AI-powered dementia care assistant with learning feedback - Enhanced Version",
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

# Static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ===== MAIN ENDPOINTS =====

@app.get("/dashboard")
async def get_dashboard():
    """Get cached dashboard or return simple fallback with learning message"""
    try:
        # Check for cached dashboard first
        cached_dashboard = patient_manager.get_dashboard_cache()
        if cached_dashboard:
            logger.info("📊 Returning cached dashboard")
            return cached_dashboard
        
        # Simple fallback if no cache
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Demo patient not found")
        
        # Generate learning message based on feedback
        learning_message = _generate_learning_message(patient)
        
        fallback_dashboard = {
            "success": True,
            "dashboard_data": {
                "theme_name": "Memory Lane",
                "learning_message": learning_message,
                "cards": [
                    {
                        "type": "music",
                        "title": "Music for Today",
                        "content": "Classical Italian songs"
                    },
                    {
                        "type": "recipe", 
                        "title": "Recipe Suggestion",
                        "content": "Traditional pasta recipe"
                    },
                    {
                        "type": "tv_show",
                        "title": "TV Show",
                        "content": "Classic Italian cinema"
                    },
                    {
                        "type": "place",
                        "title": "Memory Place",
                        "content": "Brooklyn neighborhood"
                    }
                ]
            }
        }
        
        return fallback_dashboard
        
    except Exception as e:
        logger.error(f"❌ Dashboard retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard retrieval failed: {str(e)}")

@app.post("/refresh-dashboard")
async def refresh_dashboard():
    """Run the complete agent pipeline to generate new dashboard content"""
    try:
        if not sequential_agent:
            raise HTTPException(status_code=503, detail="Sequential agent not initialized")
        
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Demo patient not found")
        
        # Run the complete pipeline
        logger.info("🚀 Running enhanced 6-agent pipeline...")
        result = await sequential_agent.run(
            patient_profile=patient,
            request_type="dashboard",
            session_id="demo_session"
        )
        
        if result and result.get("success"):
            logger.info("✅ Enhanced pipeline execution successful")
            
            # Add learning message to result
            learning_message = _generate_learning_message(patient)
            if "dashboard_data" in result:
                result["dashboard_data"]["learning_message"] = learning_message
            
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
    """Get patient profile for profile page with enhanced learning insights"""
    patient = patient_manager.get_patient()
    if not patient:
        raise HTTPException(status_code=404, detail="Demo patient not found")
    
    # Generate learning insights summary
    learning_insights = patient.get("learning_insights", {})
    avoiding = learning_insights.get("avoiding", [])
    prefers = learning_insights.get("prefers", [])
    
    return {
        "status": "success",
        "patient": patient,
        "personalization_status": {
            "feedback_points": patient.get("feedback_points", 0),
            "status": "Getting started!" if patient.get("feedback_points", 0) < 3 else "Learning well!",
            "blocked_items_count": len(patient.get("demo_dislikes", [])),
            "liked_items_count": len(patient.get("liked_items", [])),
            "learning_summary": {
                "avoiding": avoiding,
                "prefers": prefers,
                "total_feedback": patient.get("feedback_points", 0)
            }
        }
    }

@app.post("/feedback")
async def submit_feedback(request: Dict[str, Any]):
    """Submit user feedback for learning - Enhanced with profile insights"""
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
        
        # Initialize new fields if they don't exist
        if "liked_items" not in patient:
            patient["liked_items"] = []
        if "learning_insights" not in patient:
            patient["learning_insights"] = {"avoiding": [], "prefers": [], "last_updated": datetime.now().isoformat()}
        
        # Handle feedback
        if feedback_type == "like":
            like_entry = {
                "type": item_type,
                "name": item_name,
                "timestamp": datetime.now().isoformat()
            }
            patient["liked_items"].append(like_entry)
            
            # Update learning insights - prefers
            category_name = f"{item_type.title()}: {item_name}"
            if category_name not in patient["learning_insights"]["prefers"]:
                patient["learning_insights"]["prefers"].append(category_name)
            
            logger.info(f"➕ Added like: {item_type} - {item_name}")
            
        elif feedback_type == "dislike":
            if "demo_dislikes" not in patient:
                patient["demo_dislikes"] = []
            
            dislike_entry = {
                "type": item_type,
                "name": item_name,
                "timestamp": datetime.now().isoformat()
            }
            patient["demo_dislikes"].append(dislike_entry)
            
            # Update learning insights - avoiding
            category_name = f"{item_type.title()}: {item_name}"
            if category_name not in patient["learning_insights"]["avoiding"]:
                patient["learning_insights"]["avoiding"].append(category_name)
            
            logger.info(f"➖ Added dislike: {item_type} - {item_name}")
        
        # Update timestamp
        patient["learning_insights"]["last_updated"] = datetime.now().isoformat()
        
        # Save updated patient
        patient_manager.update_patient(patient)
        
        return {
            "success": True,
            "message": f"Feedback recorded: {feedback_type} for {item_type}",
            "feedback_points": patient["feedback_points"],
            "learning_updated": True
        }
        
    except Exception as e:
        logger.error(f"❌ Enhanced feedback submission failed: {e}")
        return {"error": f"Feedback submission failed: {str(e)}"}

# ===== HELPER FUNCTIONS =====

def _generate_learning_message(patient: Dict[str, Any]) -> str:
    """Generate a simple learning message based on patient feedback"""
    try:
        demo_dislikes = patient.get("demo_dislikes", [])
        liked_items = patient.get("liked_items", [])
        feedback_points = patient.get("feedback_points", 0)
        
        if feedback_points == 0:
            return "We're ready to learn your preferences!"
        
        if len(demo_dislikes) > 0:
            recent_dislike = demo_dislikes[-1]
            return f"Based on your feedback, we're avoiding {recent_dislike['type']} like '{recent_dislike['name']}'"
        
        if len(liked_items) > 0:
            recent_like = liked_items[-1]
            return f"Great! We're finding more {recent_like['type']} similar to '{recent_like['name']}'"
        
        return f"Learning from {feedback_points} feedback points to personalize your experience"
        
    except Exception as e:
        logger.error(f"Error generating learning message: {e}")
        return "Personalizing your experience based on your feedback"

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
        "pipeline_mode": "enhanced_with_profile_feedback",
        "learning_system": "active"
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
        "message": "Enhanced CareConnect Cultural Intelligence API - Hackathon Version",
        "version": "1.0.0",
        "description": "AI-powered dementia care assistant with learning feedback",
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
            "feedback_learning": "Enhanced caregiver feedback adaptation",
            "profile_insights": "Learning insights and preferences tracking"
        },
        "pipeline_mode": "enhanced_with_learning_feedback",
        "demo_patient": "Maria - Italian-American from Brooklyn, NY"
    }

if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting Enhanced CareConnect API server on port {config.PORT}")
    logger.info(f"Data directory: {patient_manager.data_dir if patient_manager else 'Not initialized'}")
    logger.info("🎯 ENHANCED: Profile-based learning feedback system active")
    logger.info("📍 Places with Google Vision analysis enabled")
    logger.info("🎯 Single patient demo mode with learning insights")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )