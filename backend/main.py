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

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import CareConnect multi-agent system with fixed imports
try:
    from multi_tool_agent.tools import initialize_all_tools, test_all_tools
    logger.info("✅ Tools module imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import tools: {e}")
    initialize_all_tools = None
    test_all_tools = None

try:
    from multi_tool_agent.sequential_agent import CareConnectAgent
    logger.info("✅ CareConnectAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import CareConnectAgent: {e}")
    CareConnectAgent = None

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

# Fallback VisionAI class if import fails
class FallbackVisionAI:
    """Fallback vision analyzer for demo purposes"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        logger.info("Using fallback Vision AI analyzer")
    
    async def analyze_with_google_vision(self, image_base64):
        """Fallback analysis with demo data"""
        logger.info("Using fallback vision analysis")
        return {
            "success": True,
            "objects": ["photo", "people", "memory"],
            "labels": ["family", "personal", "meaningful"],
            "people": ["person"],
            "activities": ["remembering", "sharing"],
            "settings": ["home", "personal space"]
        }

# Demo Patient Manager with New File Structure
class DemoPatientManager:
    """Patient data manager for hackathon demo - NEW FILE STRUCTURE"""
    
    def __init__(self):
        # NEW PATHS - Updated for frontend/static/demo structure
        self.data_dir = Path("frontend/static/demo/data")
        self.images_dir = Path("frontend/static/demo/images")
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with demo patients
        self.patients_file = self.data_dir / "patients.json"
        self._initialize_demo_patients()
        
        # Cache for dashboard content
        self.dashboard_cache = {}
        
        # Initialize Vision AI for photo processing
        if config.GOOGLE_CLOUD_API_KEY:
            try:
                from multi_tool_agent.tools.vision_ai_tools import VisionAIAnalyzer
                self.vision_ai = VisionAIAnalyzer(config.GOOGLE_CLOUD_API_KEY)
                logger.info("✅ VisionAIAnalyzer initialized")
            except ImportError:
                self.vision_ai = FallbackVisionAI(config.GOOGLE_CLOUD_API_KEY)
                logger.warning("⚠️ Using fallback Vision AI - real VisionAIAnalyzer not available")
        else:
            self.vision_ai = None
            logger.warning("❌ Google Cloud API key not found - photo analysis disabled")
    
    def _initialize_demo_patients(self):
        """Initialize single demo patient if not exists"""
        if not self.patients_file.exists():
            demo_data = {
                "demo_patient": {
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
                        },
                        "static/demo/images/maria_sample_family.jpg": {
                            "vision_analysis": {
                                "objects": ["people", "table", "food", "kitchen"],
                                "labels": ["family", "gathering", "cooking", "home"],
                                "people": ["family_members"],
                                "activities": ["cooking", "gathering"],
                                "settings": ["kitchen", "home", "indoor"]
                            },
                            "processed_date": "2025-01-23T00:00:00Z"
                        }
                    },
                    "feedback_points": 3,
                    "demo_dislikes": [],
                    "last_photo_shown": None,
                    "photo_rotation_index": 0
                }
            }
            
            with open(self.patients_file, 'w') as f:
                json.dump(demo_data, f, indent=2)
            
            logger.info("✅ Single demo patient initialized with sample data")
    
    def get_patient(self):
        """Get the single demo patient"""
        try:
            with open(self.patients_file, 'r') as f:
                data = json.load(f)
                return data.get("demo_patient")
        except FileNotFoundError:
            return None
    
    def update_patient(self, updates: dict):
        """Update the single demo patient data"""
        try:
            with open(self.patients_file, 'r') as f:
                data = json.load(f)
            
            if "demo_patient" in data:
                data["demo_patient"].update(updates)
                with open(self.patients_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return data["demo_patient"]
            return None
        except FileNotFoundError:
            return None
    
    def cache_dashboard(self, content: dict):
        """Cache dashboard content for single patient"""
        self.dashboard_cache["demo_patient"] = {
            "content": content,
            "timestamp": "2025-01-23T00:00:00Z"
        }
    
    def get_cached_dashboard(self):
        """Get cached dashboard content for single patient"""
        return self.dashboard_cache.get("demo_patient")
    
    def select_photo_of_the_day(self) -> Optional[str]:
        """Select a photo for the daily dashboard with rotation"""
        patient = self.get_patient()
        if not patient or not patient.get("photo_library"):
            return None
        
        photo_library = patient["photo_library"]
        if not photo_library:
            return None
        
        # Simple rotation logic
        rotation_index = patient.get("photo_rotation_index", 0)
        selected_photo = photo_library[rotation_index % len(photo_library)]
        
        # Update rotation index for next time
        new_index = (rotation_index + 1) % len(photo_library)
        self.update_patient({"photo_rotation_index": new_index})
        
        logger.info(f"📷 Selected photo: {selected_photo}")
        return selected_photo
    
    async def process_uploaded_photo(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded photo immediately with Google Vision"""
        try:
            # Generate unique filename  
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            timestamp = int(time.time())
            filename = f"demo_patient_{timestamp}.{file_extension}"
            file_path = self.images_dir / filename
            
            # Save photo file
            content = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            # Photo URL for storage in patients.json
            photo_url = f"static/demo/images/{filename}"
            
            # Run Google Vision analysis if available
            vision_analysis = {}
            if self.vision_ai:
                try:
                    # Convert to base64 for Vision API
                    photo_base64 = base64.b64encode(content).decode()
                    
                    # Run Vision AI analysis
                    vision_result = await self.vision_ai.analyze_with_google_vision(photo_base64)
                    
                    if vision_result and vision_result.get("success"):
                        vision_analysis = {
                            "objects": vision_result.get("objects", []),
                            "labels": vision_result.get("labels", []),
                            "people": vision_result.get("people", []),
                            "activities": vision_result.get("activities", []),
                            "settings": vision_result.get("settings", [])
                        }
                        logger.info(f"✅ Vision analysis completed for {filename}")
                    else:
                        logger.warning(f"Vision analysis failed for {filename}")
                        # Fallback analysis
                        vision_analysis = {
                            "objects": ["photo"],
                            "labels": ["memory", "personal"],
                            "people": ["person"],
                            "activities": ["remembering"],
                            "settings": ["unknown"]
                        }
                        
                except Exception as e:
                    logger.error(f"Vision AI error: {e}")
                    # Fallback analysis
                    vision_analysis = {
                        "objects": ["photo"],
                        "labels": ["memory", "personal"],
                        "people": ["person"],
                        "activities": ["remembering"],
                        "settings": ["unknown"]
                    }
            else:
                # No Vision AI available - use basic fallback
                vision_analysis = {
                    "objects": ["photo"],
                    "labels": ["memory", "personal"],
                    "people": ["person"],
                    "activities": ["remembering"],
                    "settings": ["unknown"]
                }
            
            # Update patient data with new photo and analysis
            patient = self.get_patient()
            if patient:
                # Add to photo library
                photo_library = patient.get("photo_library", [])
                photo_library.append(photo_url)
                
                # Add analysis data
                photo_analyses = patient.get("photo_analyses", {})
                photo_analyses[photo_url] = {
                    "vision_analysis": vision_analysis,
                    "processed_date": "2025-01-23T00:00:00Z"
                }
                
                # Update patient record
                updates = {
                    "photo_library": photo_library,
                    "photo_analyses": photo_analyses
                }
                self.update_patient(updates)
                
                logger.info(f"📷 Photo processed and stored: {photo_url}")
                
                return {
                    "success": True,
                    "filename": filename,
                    "photo_url": photo_url,
                    "vision_analysis": vision_analysis,
                    "message": "Photo uploaded and analyzed successfully"
                }
            else:
                raise Exception("Demo patient not found")
                
        except Exception as e:
            logger.error(f"Photo processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Photo upload failed"
            }

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
    
    logger.info("🔽 Shutting down CareConnect API...")

# Create FastAPI app
app = FastAPI(
    title="CareConnect Cultural Intelligence API",
    description="AI-powered dementia care assistant with cultural intelligence",
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

# Static file serving - UPDATED PATHS
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ===== PHOTO UPLOAD ENDPOINT (NEW WITH PRE-PROCESSING) =====

@app.post("/upload-photo")
async def upload_photo(file: UploadFile = File(...)):
    """Upload and immediately process photo with Google Vision"""
    if not patient_manager.get_patient():
        raise HTTPException(status_code=404, detail="Demo patient not found")
    
    try:
        # Process photo with immediate Vision analysis
        result = await patient_manager.process_uploaded_photo(file)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "filename": result["filename"],
                "photo_url": result["photo_url"],
                "vision_summary": {
                    "objects_detected": len(result["vision_analysis"]["objects"]),
                    "labels_found": len(result["vision_analysis"]["labels"]),
                    "people_detected": len(result["vision_analysis"]["people"])
                }
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except Exception as e:
        logger.error(f"❌ Photo upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Photo upload failed: {str(e)}")

# ===== UI ENDPOINTS =====

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
            "dislikes_count": len(patient.get("demo_dislikes", [])),
            "photo_count": len(patient.get("photo_library", []))
        }
    }

@app.post("/patient")
async def update_patient_profile(updates: dict):
    """Update patient profile from profile page"""
    updated_patient = patient_manager.update_patient(updates)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Demo patient not found")
    
    return {
        "status": "success", 
        "message": "Profile updated successfully",
        "patient": updated_patient
    }

@app.get("/dashboard")
async def get_dashboard():
    """Get dashboard content (cached or generate new)"""
    cached = patient_manager.get_cached_dashboard()
    if cached:
        return {
            "status": "success",
            "source": "cached",
            "patient_name": patient_manager.get_patient()["first_name"],
            "content": cached["content"],
            "cached_at": cached["timestamp"]
        }
    
    # If no cache, generate new dashboard
    return await refresh_dashboard()

@app.post("/refresh-dashboard")
async def refresh_dashboard():
    """Refresh dashboard by running full CareConnect pipeline"""
    patient = patient_manager.get_patient()
    if not patient:
        raise HTTPException(status_code=404, detail="Demo patient not found")
    
    global careconnect_agent
    
    try:
        # Select photo of the day if available
        photo_of_the_day = None
        photo_analysis = None
        
        if patient.get("photo_library") and len(patient["photo_library"]) >= 1:
            selected_photo = patient_manager.select_photo_of_the_day()
            if selected_photo:
                photo_of_the_day = selected_photo
                # Get stored analysis
                photo_analyses = patient.get("photo_analyses", {})
                photo_analysis = photo_analyses.get(selected_photo, {})
                logger.info(f"📷 Using photo of the day: {selected_photo}")
        
        # Prepare pipeline inputs
        pipeline_input = {
            "patient_profile": patient,
            "request_type": "dashboard",
            "session_id": f"ui_session_demo",
            "feedback_data": None,
            "photo_of_the_day": photo_of_the_day,
            "photo_analysis": photo_analysis
        }
        
        # Run pipeline if agent available
        if careconnect_agent:
            result = await careconnect_agent.run(**pipeline_input)
        else:
            # Fallback content generation
            result = {
                "pipeline_result": "fallback",
                "message": "Generated basic content - CareConnect agent unavailable"
            }
        
        # Cache the result
        patient_manager.cache_dashboard(result)
        
        return {
            "status": "success",
            "source": "generated",
            "patient_name": patient["first_name"],
            "photo_of_the_day": photo_of_the_day,
            "content": result
        }
        
    except Exception as e:
        logger.error(f"❌ Dashboard refresh failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard refresh failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(feedback_data: dict):
    """Submit feedback for learning (thumbs up/down)"""
    patient = patient_manager.get_patient()
    if not patient:
        raise HTTPException(status_code=404, detail="Demo patient not found")
    
    try:
        feedback_type = feedback_data.get("feedback_type")  # 'like' or 'dislike'
        item_category = feedback_data.get("item_category")  # 'recipe', 'music', etc.
        
        # Update feedback points
        current_points = patient.get("feedback_points", 0)
        new_points = current_points + 1
        
        # Handle dislikes
        demo_dislikes = patient.get("demo_dislikes", [])
        if feedback_type == "dislike" and item_category:
            if item_category not in demo_dislikes:
                demo_dislikes.append(item_category)
        
        # Update patient
        updates = {
            "feedback_points": new_points,
            "demo_dislikes": demo_dislikes
        }
        patient_manager.update_patient(updates)
        
        return {
            "status": "success",
            "message": f"Feedback recorded: {feedback_type}",
            "feedback_type": feedback_type,
            "new_feedback_points": new_points,
            "personalization_improving": True
        }
        
    except Exception as e:
        logger.error(f"❌ Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback failed: {str(e)}")

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
        },
        "data_structure": {
            "patients_file": str(patient_manager.patients_file),
            "images_dir": str(patient_manager.images_dir),
            "demo_patient_loaded": patient_manager.get_patient() is not None
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
        "agent_available": careconnect_agent is not None,
        "file_structure": {
            "patients_json": str(patient_manager.patients_file),
            "images_directory": str(patient_manager.images_dir)
        }
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
        "upload_photo": "/upload-photo",
        "data_location": "frontend/static/demo/"
    }

if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting CareConnect API server on port {config.PORT}")
    logger.info(f"Data directory: {patient_manager.data_dir}")
    logger.info(f"Images directory: {patient_manager.images_dir}")
    logger.info("🎯 Single patient demo mode enabled")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )