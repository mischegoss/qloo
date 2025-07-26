from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
import logging
import json
import os
import uvicorn
from pathlib import Path
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the sequential agent and tools
from multi_tool_agent.sequential_agent import SequentialAgent
from multi_tool_agent.tools import initialize_all_tools

# Patient profile model
class PatientProfile(BaseModel):
    first_name: Optional[str] = None
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
    """Enhanced demo patient manager - NO CACHING"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "frontend" / "static" / "demo" / "data"
        self.patients_file = self.data_dir / "patients.json"
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 Enhanced demo patient manager initialized - NO CACHING")
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
                "static/demo/images/maria_brooklyn_street.jpg",
                "static/demo/images/maria_family_dinner.jpg",
                "static/demo/images/maria_italian_market.jpg"
            ],
            "feedback_points": 0,
            "learning_insights": {
                "prefers": [],
                "avoiding": []
            }
        }
        
        # Save to file
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            with open(self.patients_file, 'w') as f:
                json.dump({"demo_patient": demo_patient}, f, indent=2)
            logger.info("✅ Demo patient created and saved")
        except Exception as e:
            logger.error(f"Error saving demo patient: {e}")
        
        return demo_patient

def _generate_learning_message(patient: Dict[str, Any]) -> str:
    """Generate learning message based on feedback points"""
    feedback_points = patient.get("feedback_points", 0)
    
    if feedback_points == 0:
        return "I'm just getting to know Maria's preferences!"
    elif feedback_points < 3:
        return "I'm starting to learn what Maria enjoys most."
    elif feedback_points < 7:
        return "I'm getting better at personalizing content for Maria."
    else:
        return "I know Maria's preferences well and am tailoring content accordingly."

async def startup():
    """Initialize the application"""
    global tools, sequential_agent, patient_manager
    
    try:
        logger.info("🚀 Starting Enhanced CareConnect API...")
        
        # Initialize patient manager
        patient_manager = DemoPatientManager()
        logger.info("✅ Patient manager initialized")
        
        # Create tools
        tools = initialize_all_tools()
        logger.info("✅ Tools created successfully")
        
        # Initialize sequential agent with all 6 agents
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
        agent5 = PhotoCulturalAnalyzerAgent(tools['vision_ai_tool'])
        agent6 = MobileSynthesizerAgent()
        
        sequential_agent = SequentialAgent(agent1, agent2, agent3, agent4, agent5, agent6)
        logger.info("✅ Sequential agent initialized")
        
        logger.info("🎯 Enhanced CareConnect API startup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield

# FastAPI app
app = FastAPI(
    title="Enhanced CareConnect Cultural Intelligence API",
    description="AI-powered dementia care assistant - NO CACHING for Hackathon Demo",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_path = Path(__file__).parent / "frontend" / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"📁 Static files mounted from: {static_path}")

@app.get("/")
async def root():
    """Root endpoint with enhanced API information"""
    return {
        "message": "Enhanced CareConnect Cultural Intelligence API - Hackathon Version - NO CACHING",
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
        "pipeline_mode": "enhanced_with_learning_feedback_no_caching",
        "demo_patient": "Maria - Italian-American from Brooklyn, NY",
        "caching_status": "DISABLED for fresh content generation"
    }

# ===== DASHBOARD ENDPOINTS =====

@app.get("/dashboard")
async def get_dashboard():
    """Get dashboard - NO CACHING, always run pipeline"""
    try:
        if not sequential_agent:
            raise HTTPException(status_code=503, detail="Sequential agent not initialized")
        
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Demo patient not found")
        
        # Always run the complete pipeline - NO CACHING
        logger.info("🚀 Running enhanced 6-agent pipeline (NO CACHING)...")
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
            
            return result
        else:
            logger.error("❌ Pipeline execution failed")
            raise HTTPException(status_code=500, detail="Pipeline execution failed")
        
    except Exception as e:
        logger.error(f"❌ Dashboard retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard retrieval failed: {str(e)}")

@app.post("/refresh-dashboard")
async def refresh_dashboard():
    """Run the complete agent pipeline to generate NEW dashboard content - NO CACHING"""
    try:
        if not sequential_agent:
            raise HTTPException(status_code=503, detail="Sequential agent not initialized")
        
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Demo patient not found")
        
        # Run the complete pipeline - NO CACHING
        logger.info("🚀 Running enhanced 6-agent pipeline for FRESH content (NO CACHING)...")
        result = await sequential_agent.run(
            patient_profile=patient,
            request_type="dashboard",
            session_id="demo_session"
        )
        
        if result and result.get("success"):
            logger.info("✅ Enhanced pipeline execution successful - NEW CONTENT GENERATED")
            
            # Add learning message to result
            learning_message = _generate_learning_message(patient)
            if "dashboard_data" in result:
                result["dashboard_data"]["learning_message"] = learning_message
            
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
            "insights_summary": {
                "total_preferences": len(prefers),
                "total_avoiding": len(avoiding),
                "recent_feedback": "Active learning mode" if patient.get("feedback_points", 0) > 0 else "No feedback yet"
            }
        }
    }

@app.post("/feedback")
async def submit_feedback():
    """Submit feedback for learning enhancement"""
    try:
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Demo patient not found")
        
        # Increment feedback points
        patient["feedback_points"] = patient.get("feedback_points", 0) + 1
        
        # Update patient data
        patient_manager.update_patient(patient)
        
        return {
            "status": "success",
            "message": "Feedback received and learning updated",
            "feedback_points": patient["feedback_points"],
            "learning_status": _generate_learning_message(patient)
        }
        
    except Exception as e:
        logger.error(f"❌ Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

# ===== UTILITY ENDPOINTS =====

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
        "pipeline_mode": "enhanced_with_profile_feedback_no_caching",
        "learning_system": "active",
        "caching_status": "DISABLED"
    }

@app.get("/tools/status")
async def get_tools_status():
    """Get status of all tools and agents"""
    if not sequential_agent:
        return {"error": "Sequential agent not initialized"}
    
    agent_status = sequential_agent.get_agent_status()
    
    return {
        "tools_status": "operational" if tools else "not_initialized",
        "agent_pipeline": agent_status,
        "tools_available": {
            "qloo_insights": tools.get("qloo_insights") is not None if tools else False,
            "youtube_api": tools.get("youtube_api") is not None if tools else False,
            "gemini_recipe": tools.get("gemini_recipe") is not None if tools else False,
            "google_vision": tools.get("google_vision") is not None if tools else False
        },
        "caching_status": "DISABLED for fresh content generation"
    }

if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting Enhanced CareConnect API server on port {config.PORT}")
    logger.info(f"Data directory: {patient_manager.data_dir if patient_manager else 'Not initialized'}")
    logger.info("🎯 ENHANCED: Profile-based learning feedback system active")
    logger.info("📍 Places with Google Vision analysis enabled")
    logger.info("🎯 Single patient demo mode with learning insights")
    logger.info("🚫 CACHING DISABLED for hackathon demo - fresh content every time")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )