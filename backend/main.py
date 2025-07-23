"""
Complete Fixed main.py with Photo Analysis Endpoint
File: backend/main.py

Main FastAPI application for CareConnect Cultural Intelligence API
"""

import os
import logging
import time
import json
import base64
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import CareConnect multi-agent system with fixed imports
try:
    from multi_tool_agent.tools import initialize_all_tools, test_all_tools, get_tool_status
    logger.info("✅ Tools module imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import tools: {e}")
    initialize_all_tools = None
    test_all_tools = None
    get_tool_status = None

try:
    from multi_tool_agent.sequential_agent import CareConnectAgent
    logger.info("✅ CareConnectAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import CareConnectAgent: {e}")
    CareConnectAgent = None

# Configuration
class Config:
    PORT = int(os.getenv("PORT", 8080))
    QLOO_API_KEY = os.getenv("QLOO_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_CLOUD_API_KEY"))

config = Config()

# Request models
class PatientProfile(BaseModel):
    first_name: str
    birth_year: Optional[int] = None
    birth_month: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cultural_heritage: Optional[str] = None
    languages: Optional[str] = None
    spiritual_traditions: Optional[str] = None
    additional_context: Optional[str] = None
    caregiver_notes: Optional[str] = None

class CareConnectRequest(BaseModel):
    patient_profile: PatientProfile
    request_type: str = "dashboard"
    session_id: Optional[str] = None
    feedback_history: Optional[Dict[str, Any]] = None

class PhotoAnalysisRequest(BaseModel):
    patient_profile: PatientProfile
    session_id: Optional[str] = None

# Demo Patient Manager
class DemoPatientManager:
    """Simple patient data manager for hackathon demo"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.photos_dir = Path("static/photos")
        self.data_dir.mkdir(exist_ok=True)
        self.photos_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with demo patients
        self.patients_file = self.data_dir / "patients.json"
        self._initialize_demo_patients()
        
        # Cache for dashboard content
        self.dashboard_cache = {}
    
    def _initialize_demo_patients(self):
        """Initialize demo patients if not exists"""
        if not self.patients_file.exists():
            demo_patients = {
                "maria_1945": {
                    "patient_id": "maria_1945",
                    "first_name": "Maria",
                    "birth_year": 1945,
                    "birth_month": "april",
                    "city": "Brooklyn",
                    "state": "New York",
                    "cultural_heritage": "Italian-American",
                    "languages": "English, Italian",
                    "spiritual_traditions": "Catholic",
                    "additional_context": "Loves music and cooking",
                    "caregiver_notes": "Enjoys family activities",
                    "tags": ["music", "cooking", "family"],
                    "photo_library": [],
                    "feedback_points": 0,
                    "demo_dislikes": []
                },
                "rose_1942": {
                    "patient_id": "rose_1942", 
                    "first_name": "Rose",
                    "birth_year": 1942,
                    "birth_month": "june",
                    "city": "Chicago",
                    "state": "Illinois",
                    "cultural_heritage": "Irish-American",
                    "languages": "English",
                    "spiritual_traditions": "Methodist",
                    "additional_context": "Loves gardening and old movies",
                    "caregiver_notes": "Enjoys quiet activities",
                    "tags": ["gardening", "movies", "reading"],
                    "photo_library": [],
                    "feedback_points": 3,
                    "demo_dislikes": ["jazz"]
                }
            }
            
            with open(self.patients_file, 'w') as f:
                json.dump(demo_patients, f, indent=2)
    
    def get_all_patients(self):
        """Get all patients"""
        with open(self.patients_file, 'r') as f:
            return json.load(f)
    
    def get_patient(self, patient_id: str):
        """Get specific patient"""
        patients = self.get_all_patients()
        return patients.get(patient_id)
    
    def update_patient(self, patient_id: str, updates: dict):
        """Update patient data"""
        patients = self.get_all_patients()
        if patient_id in patients:
            patients[patient_id].update(updates)
            with open(self.patients_file, 'w') as f:
                json.dump(patients, f, indent=2)
            return patients[patient_id]
        return None
    
    def cache_dashboard(self, patient_id: str, content: dict):
        """Cache dashboard content"""
        self.dashboard_cache[patient_id] = {
            "content": content,
            "timestamp": "2025-01-23T00:00:00Z"
        }
    
    def get_cached_dashboard(self, patient_id: str):
        """Get cached dashboard content"""
        return self.dashboard_cache.get(patient_id)

# Global variables for multi-agent system
tools = None
careconnect_agent = None
patient_manager = DemoPatientManager()

# Startup and shutdown handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize tools and agents on startup."""
    global tools, careconnect_agent
    
    logger.info("🚀 Starting CareConnect Cultural Intelligence API...")
    
    # Initialize tools
    if initialize_all_tools:
        try:
            tools = initialize_all_tools()
            logger.info(f"✅ Initialized {len(tools)} tools")
            
            # Test tools
            if test_all_tools:
                test_results = await test_all_tools(tools)
                working_tools = sum(1 for result in test_results.values() if result)
                logger.info(f"✅ {working_tools}/{len(test_results)} tools are working")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize tools: {e}")
            tools = {}
    else:
        logger.warning("⚠️  Tools initialization not available")
        tools = {}
    
    # Initialize CareConnect agent
    if CareConnectAgent and tools:
        try:
            careconnect_agent = CareConnectAgent(tools)
            logger.info("✅ CareConnect agent initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize CareConnect agent: {e}")
            careconnect_agent = None
    else:
        logger.warning("⚠️  CareConnect agent not available")
        careconnect_agent = None
    
    logger.info("🎯 CareConnect API ready!")
    
    yield
    
    # Cleanup on shutdown
    logger.info("🛑 Shutting down CareConnect API...")

# Create FastAPI app
app = FastAPI(
    title="CareConnect Cultural Intelligence API",
    description="AI-powered cultural intelligence for dementia care",
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

# Add static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== DEBUG ENDPOINTS =====

@app.get("/debug/agents")
async def debug_agents():
    """Debug agent initialization status"""
    global careconnect_agent
    
    if not careconnect_agent:
        return {
            "error": "No careconnect_agent",
            "careconnect_agent_exists": False
        }
    
    agent_status = {
        "agent1": careconnect_agent.agent1 is not None,
        "agent2": careconnect_agent.agent2 is not None, 
        "agent3": careconnect_agent.agent3 is not None,
        "agent4": careconnect_agent.agent4 is not None,
        "agent5": careconnect_agent.agent5 is not None,
        "agent6": careconnect_agent.agent6 is not None,
        "agent7": careconnect_agent.agent7 is not None,
    }
    
    return {
        "careconnect_agent_exists": True,
        "individual_agents": agent_status,
        "total_available": sum(agent_status.values()),
        "tools_available": list(careconnect_agent.tools.keys()) if careconnect_agent.tools else [],
        "tools_count": len(careconnect_agent.tools) if careconnect_agent.tools else 0,
        "agent_object_info": {
            "name": getattr(careconnect_agent, 'name', 'unknown'),
            "description": getattr(careconnect_agent, 'description', 'unknown')
        }
    }

@app.get("/debug/imports")
async def debug_imports():
    """Debug import status of agent classes"""
    try:
        from multi_tool_agent.sequential_agent import (
            InformationConsolidatorAgent,
            CulturalProfileBuilderAgent, 
            QlooCulturalIntelligenceAgent,
            SensoryContentGeneratorAgent,
            PhotoCulturalAnalyzerAgent,
            MobileSynthesizerAgent,
            FeedbackLearningSystemAgent
        )
        
        import_status = {
            "InformationConsolidatorAgent": InformationConsolidatorAgent is not None,
            "CulturalProfileBuilderAgent": CulturalProfileBuilderAgent is not None,
            "QlooCulturalIntelligenceAgent": QlooCulturalIntelligenceAgent is not None,
            "SensoryContentGeneratorAgent": SensoryContentGeneratorAgent is not None,
            "PhotoCulturalAnalyzerAgent": PhotoCulturalAnalyzerAgent is not None,
            "MobileSynthesizerAgent": MobileSynthesizerAgent is not None,
            "FeedbackLearningSystemAgent": FeedbackLearningSystemAgent is not None
        }
        
        return {
            "import_success": True,
            "individual_imports": import_status,
            "successful_imports": sum(import_status.values())
        }
        
    except ImportError as e:
        return {
            "import_success": False,
            "error": str(e),
            "message": "Failed to import individual agent classes"
        }

# ===== UI ENDPOINTS =====

@app.get("/patients")
async def get_patients():
    """Get all available demo patients for login selection"""
    patients = patient_manager.get_all_patients()
    return {
        "patients": [
            {
                "patient_id": pid,
                "first_name": data["first_name"],
                "birth_year": data["birth_year"],
                "heritage": data["cultural_heritage"]
            }
            for pid, data in patients.items()
        ]
    }

@app.get("/patients/{patient_id}")  
async def get_patient_profile(patient_id: str):
    """Get full patient profile for profile page"""
    patient = patient_manager.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "status": "success",
        "patient": patient,
        "personalization_status": {
            "feedback_points": patient.get("feedback_points", 0),
            "status": "Getting started!" if patient.get("feedback_points", 0) < 3 else "Learning well!",
            "dislikes_count": len(patient.get("demo_dislikes", []))
        }
    }

@app.post("/patients/{patient_id}")
async def update_patient_profile(patient_id: str, updates: dict):
    """Update patient profile from profile page"""
    updated_patient = patient_manager.update_patient(patient_id, updates)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "status": "success", 
        "message": "Profile updated successfully",
        "patient": updated_patient
    }

@app.get("/dashboard/{patient_id}")
async def get_dashboard(patient_id: str):
    """Get dashboard content (cached or generate new)"""
    cached = patient_manager.get_cached_dashboard(patient_id)
    if cached:
        return {
            "status": "success",
            "source": "cached",
            "patient_id": patient_id,
            "content": cached["content"],
            "cached_at": cached["timestamp"]
        }
    
    # If no cache, generate new dashboard
    return await refresh_dashboard(patient_id)

@app.post("/refresh-dashboard/{patient_id}")
async def refresh_dashboard(patient_id: str):
    """Refresh dashboard by running full CareConnect pipeline"""
    patient = patient_manager.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if not careconnect_agent:
        raise HTTPException(status_code=503, detail="CareConnect agent not available")
    
    try:
        # Create patient profile for your existing system
        patient_profile_dict = {
            "first_name": patient["first_name"],
            "birth_year": patient.get("birth_year"),
            "birth_month": patient.get("birth_month"),
            "city": patient.get("city"),
            "state": patient.get("state"),
            "cultural_heritage": patient.get("cultural_heritage"),
            "languages": patient.get("languages"),
            "spiritual_traditions": patient.get("spiritual_traditions"),
            "additional_context": patient.get("additional_context"),
            "caregiver_notes": patient.get("caregiver_notes")
        }
        
        # Run your existing CareConnect pipeline
        result = await careconnect_agent.run(
            patient_profile=patient_profile_dict,
            request_type="dashboard",
            session_id=f"ui_session_{patient_id}"
        )
        
        # Cache the result
        patient_manager.cache_dashboard(patient_id, result)
        
        return {
            "status": "success",
            "source": "generated",
            "patient_id": patient_id,
            "patient_name": patient["first_name"],
            "content": result
        }
        
    except Exception as e:
        logger.error(f"Dashboard generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(feedback_data: dict):
    """Handle thumbs up/down feedback from UI"""
    patient_id = feedback_data.get("patient_id")
    feedback_type = feedback_data.get("feedback_type")  # "like" or "dislike" 
    category = feedback_data.get("category")
    
    if not patient_id:
        raise HTTPException(status_code=400, detail="Patient ID required")
    
    patient = patient_manager.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Simple demo feedback processing
    updates = {}
    
    # Increment feedback points
    current_points = patient.get("feedback_points", 0)
    updates["feedback_points"] = current_points + 1
    
    # Add to dislikes if negative feedback
    if feedback_type == "dislike":
        demo_dislikes = patient.get("demo_dislikes", [])
        if category and category not in demo_dislikes:
            demo_dislikes.append(category)
            updates["demo_dislikes"] = demo_dislikes
    
    # Update patient
    patient_manager.update_patient(patient_id, updates)
    
    return {
        "status": "success",
        "message": "Thank you for your feedback!",
        "feedback_type": feedback_type,
        "new_feedback_points": updates["feedback_points"],
        "personalization_improving": True
    }

@app.post("/upload-photo/{patient_id}")
async def upload_photo(patient_id: str, file: UploadFile = File(...)):
    """Handle photo upload"""
    patient = patient_manager.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    try:
        # Save photo to static directory
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{patient_id}_{len(patient.get('photo_library', []))}_{int(time.time())}.{file_extension}"
        file_path = patient_manager.photos_dir / filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Update patient photo library
        photo_library = patient.get("photo_library", [])
        photo_library.append(f"photos/{filename}")
        patient_manager.update_patient(patient_id, {"photo_library": photo_library})
        
        return {
            "status": "success",
            "message": "Photo uploaded successfully",
            "filename": filename,
            "photo_url": f"/static/photos/{filename}"
        }
        
    except Exception as e:
        logger.error(f"Photo upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Photo upload failed: {str(e)}")

# ===== CORE API ENDPOINTS =====

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global tools, careconnect_agent
    
    return {
        "status": "healthy",
        "timestamp": "2025-01-23T00:00:00Z",
        "tools_available": len(tools) if tools else 0,
        "agent_available": careconnect_agent is not None,
        "config": {
            "qloo_api_configured": bool(config.QLOO_API_KEY),
            "youtube_api_configured": bool(config.YOUTUBE_API_KEY),
            "google_cloud_configured": bool(config.GOOGLE_CLOUD_API_KEY),
            "gemini_api_configured": bool(config.GEMINI_API_KEY)
        }
    }

@app.get("/tools/status")
async def get_tools_status():
    """Get status of all tools."""
    global tools
    
    if not tools:
        return {"error": "No tools initialized"}
    
    if test_all_tools:
        try:
            test_results = await test_all_tools(tools)
            return {
                "tools_count": len(tools),
                "test_results": test_results,
                "working_tools": sum(1 for result in test_results.values() if result)
            }
        except Exception as e:
            return {"error": f"Failed to test tools: {e}"}
    else:
        return {
            "tools_count": len(tools),
            "tools_available": list(tools.keys()),
            "note": "Tool testing not available"
        }

@app.post("/careconnect")
async def process_careconnect_request(request: CareConnectRequest):
    """Process a CareConnect cultural intelligence request."""
    global careconnect_agent
    
    if not careconnect_agent:
        raise HTTPException(
            status_code=503, 
            detail="CareConnect agent not available - check tool initialization"
        )
    
    try:
        # Convert Pydantic model to dict
        patient_profile = request.patient_profile.model_dump()
        
        # Execute CareConnect pipeline
        result = await careconnect_agent.run(
            patient_profile=patient_profile,
            request_type=request.request_type,
            session_id=request.session_id,
            feedback_data=request.feedback_history
        )
        
        return {
            "success": True,
            "request_type": request.request_type,
            "session_id": request.session_id,
            "result": result,
            "timestamp": "2025-01-23T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"❌ CareConnect request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/analyze-photo")
async def analyze_photo(
    file: UploadFile = File(...),
    patient_profile: str = None,
    session_id: str = None
):
    """Analyze a photo using the full cultural intelligence pipeline with Agent 5."""
    global careconnect_agent
    
    if not careconnect_agent:
        raise HTTPException(
            status_code=503, 
            detail="CareConnect agent not available"
        )
    
    try:
        # Read and encode photo as base64
        photo_bytes = await file.read()
        photo_base64 = base64.b64encode(photo_bytes).decode()
        
        # Parse patient profile if provided
        if patient_profile:
            try:
                profile_dict = json.loads(patient_profile)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid patient_profile JSON")
        else:
            profile_dict = {
                "first_name": "Anonymous", 
                "cultural_heritage": "American", 
                "birth_year": 1950
            }
        
        # Create photo_data as SEPARATE parameter (KEY FIX!)
        photo_data = {
            "has_photo": True,
            "photo_metadata": {
                "image_bytes": photo_base64,
                "mime_type": file.content_type,
                "description": f"Uploaded photo: {file.filename}",
                "filename": file.filename
            }
        }
        
        # Debug logging
        logger.info(f"DEBUG: Processing photo analysis for {profile_dict.get('cultural_heritage', 'Unknown')} heritage")
        logger.info(f"DEBUG: Photo size: {len(photo_base64)} chars, MIME: {file.content_type}")
        
        # Run the full pipeline with photo_data as separate parameter
        result = await careconnect_agent.run(
            patient_profile=profile_dict,
            request_type="photo_analysis",
            session_id=session_id or f"photo_session_{int(time.time())}",
            photo_data=photo_data  # ✅ Pass as separate parameter
        )
        
        return {
            "success": True,
            "filename": file.filename,
            "session_id": session_id,
            "photo_analysis": result.get("photo_analysis", {}),
            "cultural_context": result.get("cultural_profile", {}),
            "conversation_starters": result.get("mobile_experience", {}).get("conversation_starters", []),
            "memory_triggers": result.get("photo_analysis", {}).get("memory_triggers", []),
            "era_analysis": result.get("photo_analysis", {}).get("era_analysis", {}),
            "result": result,
            "timestamp": "2025-01-23T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"❌ Photo analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Photo analysis failed: {str(e)}")

@app.get("/config")
async def get_configuration():
    """Get API configuration status."""
    return {
        "api_keys_configured": {
            "qloo": bool(config.QLOO_API_KEY),
            "youtube": bool(config.YOUTUBE_API_KEY),
            "google_cloud": bool(config.GOOGLE_CLOUD_API_KEY),
            "gemini": bool(config.GEMINI_API_KEY)
        },
        "port": config.PORT,
        "tools_initialized": tools is not None,
        "agent_available": careconnect_agent is not None
    }

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CareConnect Cultural Intelligence API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "tools_status": "/tools/status",
        "photo_analysis": "/analyze-photo"
    }

if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting CareConnect API server on port {config.PORT}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )