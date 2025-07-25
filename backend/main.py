"""
Complete Fixed main.py with Theme Image Support - ENHANCED VERSION
File: backend/main.py

Main FastAPI application for CareConnect Cultural Intelligence API
FIXED: Personal photos removed from automatic pipeline, theme photos only
"""

import os
import logging
import time
import json
import base64
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
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
    from multi_tool_agent.sequential_agent import SequentialAgent
    logger.info("✅ SequentialAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import SequentialAgent: {e}")
    SequentialAgent = None

# NEW: Import enhanced theme manager with image support
try:
    from config.theme_config import theme_manager
    logger.info("✅ Enhanced theme manager imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import theme manager: {e}")
    theme_manager = None

# NEW: Import personal photo analyzer (will be added separately)
try:
    from multi_tool_agent.personal_photo_analyzer import PersonalPhotoAnalyzer
    logger.info("✅ Personal photo analyzer imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Personal photo analyzer not yet available: {e}")
    PersonalPhotoAnalyzer = None

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
    city: Optional[str] = None
    state: Optional[str] = None
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
personal_photo_analyzer = None  # NEW: For on-demand personal photo analysis

# Demo Patient Manager class with enhanced photo handling
class DemoPatientManager:
    """Enhanced demo patient manager with theme image support"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "frontend" / "static" / "demo" / "data"
        self.images_dir = Path(__file__).parent / "frontend" / "static" / "demo" / "images"
        self.patients_file = self.data_dir / "patients.json"
        self.dashboard_cache = {"content": None, "timestamp": None, "expiry_minutes": 5}
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎯 Demo Patient Manager initialized")
        logger.info(f"📂 Data directory: {self.data_dir}")
        logger.info(f"📷 Images directory: {self.images_dir}")
    
    def get_cached_dashboard(self):
        """Get cached dashboard if valid"""
        if self.dashboard_cache["content"] and self.dashboard_cache["timestamp"]:
            cached_time = datetime.fromisoformat(self.dashboard_cache["timestamp"])
            if datetime.now() - cached_time < timedelta(minutes=self.dashboard_cache["expiry_minutes"]):
                return self.dashboard_cache
        return None
    
    def cache_dashboard(self, content):
        """Cache dashboard content"""
        self.dashboard_cache = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "expiry_minutes": 5
        }
    
    def get_patient(self):
        """Get the demo patient data"""
        if not self.patients_file.exists():
            return self._create_demo_patient()
        
        try:
            with open(self.patients_file, 'r') as f:
                data = json.load(f)
                return data.get("demo_patient")
        except Exception as e:
            logger.error(f"❌ Failed to load patient data: {e}")
            return self._create_demo_patient()
    
    def update_patient(self, updates: Dict[str, Any]):
        """Update patient data"""
        current_data = {"demo_patient": self.get_patient() or {}}
        current_data["demo_patient"].update(updates)
        
        try:
            with open(self.patients_file, 'w') as f:
                json.dump(current_data, f, indent=2)
            logger.info("✅ Patient data updated")
        except Exception as e:
            logger.error(f"❌ Failed to update patient data: {e}")
    
    def select_photo_of_the_day(self):
        """KEPT FOR MANUAL USE ONLY - Not used in automatic pipeline"""
        patient = self.get_patient()
        if not patient or not patient.get("photo_library"):
            return None
        
        photos = patient["photo_library"]
        current_index = patient.get("photo_rotation_index", 0)
        
        if current_index >= len(photos):
            current_index = 0
        
        selected_photo = photos[current_index]
        
        # Update rotation index for next time
        next_index = (current_index + 1) % len(photos)
        self.update_patient({"photo_rotation_index": next_index})
        
        return selected_photo
    
    async def process_uploaded_photo(self, file: UploadFile):
        """Process uploaded photo with immediate Vision analysis"""
        from multi_tool_agent.tools.vision_ai_tools import VisionAIAnalyzer
        
        try:
            # Validate file
            if not file.content_type.startswith("image/"):
                raise Exception("File must be an image")
            
            # Generate unique filename
            timestamp = int(time.time())
            file_extension = Path(file.filename).suffix or ".jpg"
            filename = f"user_upload_{timestamp}{file_extension}"
            
            # Save file
            file_path = self.images_dir / filename
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Immediate Vision analysis
            vision_analyzer = VisionAIAnalyzer(config.GOOGLE_CLOUD_API_KEY)
            vision_result = await vision_analyzer.analyze_image(str(file_path))
            
            if "error" in vision_result:
                logger.warning(f"⚠️ Vision analysis failed: {vision_result['error']}")
            
            # Update patient photo library and analysis
            patient = self.get_patient()
            if not patient:
                patient = self._create_demo_patient()
            
            photo_url = f"static/demo/images/{filename}"
            
            # Add to photo library
            if "photo_library" not in patient:
                patient["photo_library"] = []
            patient["photo_library"].append(photo_url)
            
            # Store vision analysis
            if "photo_analyses" not in patient:
                patient["photo_analyses"] = {}
            
            patient["photo_analyses"][photo_url] = {
                "vision_analysis": vision_result,
                "processed_date": datetime.now().isoformat()
            }
            
            # Save updated patient data
            self.update_patient(patient)
            
            return {
                "success": True,
                "message": "Photo uploaded and analyzed successfully",
                "filename": filename,
                "photo_url": photo_url,
                "vision_analysis": vision_result
            }
            
        except Exception as e:
            logger.error(f"❌ Photo upload failed: {e}")
            return {
                "success": False,
                "message": f"Upload failed: {str(e)}"
            }
    
    def _create_demo_patient(self):
        """Create demo patient data if none exists"""
        demo_patient = {
            "first_name": "Maria",
            "birth_year": 1945,
            "birth_month": "March",
            "cultural_heritage": "Italian-American",
            "city": "Brooklyn",
            "state": "New York",
            "additional_context": "Loves music and cooking. Has 4 children and 7 grandchildren.",
            "caregiver_notes": "Responds well to music from the 1960s-70s. Enjoys looking at family photos.",
            "photo_library": [
                "static/demo/images/maria_sample_wedding.jpg",
                "static/demo/images/maria_sample_family.jpg"
            ],
            "photo_analyses": {
                "static/demo/images/maria_sample_wedding.jpg": {
                    "vision_analysis": {
                        "objects": ["people", "dress", "church", "flowers"],
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
        
        # Save demo patient data
        patient_data = {"demo_patient": demo_patient}
        try:
            with open(self.patients_file, 'w') as f:
                json.dump(patient_data, f, indent=2)
            logger.info("✅ Demo patient data created")
        except Exception as e:
            logger.error(f"❌ Failed to create demo patient data: {e}")
        
        return demo_patient

# Tool initialization functions
def initialize_tools():
    """Initialize all tools"""
    if not initialize_all_tools:
        logger.error("❌ initialize_all_tools not available")
        return None
    
    try:
        tools = initialize_all_tools()  # REMOVED: await - this is not an async function
        logger.info(f"✅ Initialized {len(tools)} tools")
        return tools
    except Exception as e:
        logger.error(f"❌ Tool initialization failed: {e}")
        return None

def initialize_sequential_agent(tools):
    """Initialize sequential agent with all agents"""
    if not SequentialAgent or not tools:
        logger.error("❌ SequentialAgent or tools not available")
        return None
    
    try:
        from multi_tool_agent.agents.information_consolidator_agent import InformationConsolidatorAgent
        from multi_tool_agent.agents.cultural_profile_agent import CulturalProfileBuilderAgent  # FIXED: correct module name
        from multi_tool_agent.agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
        from multi_tool_agent.agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
        from multi_tool_agent.agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
        from multi_tool_agent.agents.mobile_synthesizer_agent import MobileSynthesizerAgent
        
        # Initialize all agents with correct import paths
        agent1 = InformationConsolidatorAgent()
        agent2 = CulturalProfileBuilderAgent()
        agent3 = QlooCulturalIntelligenceAgent(tools.get("qloo_tool"))  # FIXED: tool name
        agent4 = SensoryContentGeneratorAgent(
            tools.get("youtube_tool"),  # FIXED: tool name
            tools.get("gemini_tool")    # FIXED: tool name
        )
        agent5 = PhotoCulturalAnalyzerAgent(tools.get("vision_ai_tool"))  # FIXED: tool name
        agent6 = MobileSynthesizerAgent()
        
        # Create sequential agent
        sequential_agent = SequentialAgent(agent1, agent2, agent3, agent4, agent5, agent6)
        logger.info("✅ Sequential agent initialized with all 6 agents")
        return sequential_agent
        
    except Exception as e:
        logger.error(f"❌ Sequential agent initialization failed: {e}")
        return None

def initialize_patient_manager():
    """Initialize patient manager"""
    try:
        patient_manager = DemoPatientManager()
        logger.info("✅ Patient manager initialized")
        return patient_manager
    except Exception as e:
        logger.error(f"❌ Patient manager initialization failed: {e}")
        return None

def setup_backend_directories():
    """Setup backend data directories including theme images"""
    # Create backend data directories
    backend_images_dir = Path(__file__).parent / "data" / "images"
    backend_images_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"🗂️ Backend data directories setup:")
    logger.info(f"   📂 Patient data: {patient_manager.data_dir}")
    logger.info(f"   📷 Personal images: {patient_manager.images_dir}")
    logger.info(f"   🎯 Theme images: {backend_images_dir}")
    
    # NEW: Check theme images directory status
    if theme_manager:
        theme_status = theme_manager.debug_theme_status()
        logger.info(f"🎯 Theme images directory status:")
        logger.info(f"   📍 Path: {theme_status.get('theme_images_dir', 'Unknown')}")
        logger.info(f"   ✅ Exists: {theme_status.get('theme_images_dir_exists', False)}")
        
        # Count available theme images
        if backend_images_dir.exists():
            image_files = list(backend_images_dir.glob("*.png")) + list(backend_images_dir.glob("*.jpg")) + list(backend_images_dir.glob("*.jpeg"))
            logger.info(f"   🖼️ Available theme images: {len(image_files)}")
            if image_files:
                sample_files = [f.name for f in image_files[:3]]
                logger.info(f"   📋 Sample files: {', '.join(sample_files)}")
        else:
            logger.warning(f"   ⚠️ Theme images directory not found")
    else:
        logger.warning("⚠️ Theme manager not available for directory validation")
    
    return backend_images_dir

# Startup and shutdown handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize tools and agents on startup."""
    global tools, sequential_agent, patient_manager, personal_photo_analyzer
    
    try:
        logger.info("🚀 Initializing CareConnect API...")
        
        # Initialize tools
        tools = initialize_tools()  # REMOVED: await - this is now synchronous
        if not tools:
            logger.error("❌ Failed to initialize tools")
            yield
            return
        
        # Initialize sequential agent
        sequential_agent = initialize_sequential_agent(tools)
        if not sequential_agent:
            logger.error("❌ Failed to initialize sequential agent")
            yield  
            return
        
        # NEW: Initialize personal photo analyzer (if available)
        vision_ai_tool = tools.get("vision_ai_analyzer")
        if PersonalPhotoAnalyzer and vision_ai_tool:
            personal_photo_analyzer = PersonalPhotoAnalyzer(vision_ai_tool)
            logger.info("✅ Personal photo analyzer initialized")
        else:
            logger.warning("⚠️ Personal photo analyzer not available - some features disabled")
        
        # Initialize patient manager and setup directories
        patient_manager = initialize_patient_manager()
        setup_backend_directories()
        
        logger.info("✅ CareConnect API initialization complete")
        yield
        
    except Exception as e:
        logger.error(f"❌ API initialization failed: {e}")
        yield
    finally:
        logger.info("🔄 CareConnect API shutting down")

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

# Static file serving
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ===== MAIN DASHBOARD ENDPOINT (FIXED - THEME PHOTOS ONLY) =====

@app.get("/dashboard")
async def get_dashboard():
    """FIXED: Generate dashboard with THEME PHOTOS ONLY (no personal photos in automatic pipeline)"""
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
    """FIXED: Refresh dashboard with THEME PHOTOS ONLY (no personal photos in automatic pipeline)"""
    global patient_manager, sequential_agent
    
    if not sequential_agent:
        return {"error": "Sequential agent not initialized"}
    
    try:
        # Get patient profile
        patient = patient_manager.get_patient()
        if not patient:
            return {"error": "No patient data found"}
        
        # FIXED: NO personal photo selection in automatic pipeline
        logger.info("🎯 Refreshing dashboard with THEME PHOTOS ONLY")
        logger.info("📷 Personal photos: EXCLUDED from automatic pipeline")
        
        # Generate session ID for this request
        session_id = f"refresh_{int(time.time())}"
        
        # FIXED: Run sequential agent pipeline with theme photos only
        result = await sequential_agent.run(
            patient_profile=patient,
            request_type="dashboard", 
            session_id=session_id
            # REMOVED: photo_of_the_day parameter (no personal photos)
            # REMOVED: photo_analysis parameter (no personal photos)
        )
        
        if result and "error" not in result:
            # Cache the result
            patient_manager.cache_dashboard(result)
            
            logger.info("✅ Dashboard refreshed successfully with THEME PHOTOS ONLY")
            return {
                "status": "success",
                "source": "generated",
                "patient_name": patient["first_name"],
                "content": result,
                "generation_mode": "theme_photos_only",
                "personal_photos_excluded": True,
                "message": "Dashboard refreshed successfully!"
            }
        else:
            logger.error("❌ Pipeline execution failed")
            raise HTTPException(status_code=500, detail="Pipeline execution failed")
            
    except Exception as e:
        logger.error(f"❌ Dashboard refresh failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard refresh failed: {str(e)}")

# ===== PERSONAL PHOTO ENDPOINTS (NEW - ON-DEMAND ONLY) =====

@app.get("/personal-photos")
async def get_personal_photos():
    """Get list of available personal photos for UI buttons (on-demand analysis only)"""
    global patient_manager
    
    try:
        patient = patient_manager.get_patient()
        if not patient:
            return {"error": "No patient data found"}
        
        photo_library = patient.get("photo_library", [])
        photo_analyses = patient.get("photo_analyses", {})
        
        # Format photo information for UI
        available_photos = []
        for photo_path in photo_library:
            photo_info = {
                "photo_path": photo_path,
                "filename": Path(photo_path).name,
                "display_name": Path(photo_path).stem.replace("_", " ").title(),
                "has_analysis": photo_path in photo_analyses,
                "frontend_path": photo_path  # For displaying in UI
            }
            available_photos.append(photo_info)
        
        return {
            "personal_photos": available_photos,
            "total_count": len(available_photos),
            "analysis_mode": "on_demand_only",
            "note": "These photos are analyzed only when user clicks 'Discuss this photo' button"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get personal photos: {e}")
        return {"error": f"Failed to get personal photos: {str(e)}"}

@app.post("/analyze-personal-photo")
async def analyze_personal_photo(request: Dict[str, Any]):
    """Analyze personal photo on-demand (when user clicks button)"""
    global patient_manager, personal_photo_analyzer
    
    if not personal_photo_analyzer:
        return {"error": "Personal photo analyzer not available - feature disabled"}
    
    try:
        photo_path = request.get("photo_path")
        if not photo_path:
            return {"error": "No photo path provided"}
        
        # Get patient profile
        patient = patient_manager.get_patient()
        if not patient:
            return {"error": "No patient data found"}
        
        # Get stored analysis for this photo (if available)
        stored_analyses = patient.get("photo_analyses", {})
        stored_analysis = stored_analyses.get(photo_path)
        
        logger.info(f"🔍 Processing on-demand personal photo analysis: {Path(photo_path).name}")
        
        # Run dedicated personal photo analysis
        result = await personal_photo_analyzer.analyze_personal_photo(
            photo_path=photo_path,
            patient_profile=patient,
            stored_analysis=stored_analysis
        )
        
        logger.info(f"✅ Personal photo analysis completed for: {Path(photo_path).name}")
        
        return {
            "success": True,
            "personal_photo_analysis": result,
            "analysis_mode": "on_demand_user_request",
            "trigger": "user_button_click"
        }
        
    except Exception as e:
        logger.error(f"❌ Personal photo analysis failed: {e}")
        return {"error": f"Personal photo analysis failed: {str(e)}"}

# ===== PHOTO UPLOAD ENDPOINT =====

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
                },
                "note": "Photo added to personal library - use 'Discuss this photo' button for conversation analysis"
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
            "blocked_items_count": len(patient.get("demo_dislikes", [])),
            "photo_library_count": len(patient.get("photo_library", []))
        }
    }

@app.post("/feedback")
async def submit_feedback(request: Dict[str, Any]):
    """Submit user feedback for learning"""
    global patient_manager
    
    try:
        feedback_type = request.get("feedback_type")  # "like" or "dislike"
        item_type = request.get("item_type")  # "music", "recipe", "tv_show", etc.
        item_id = request.get("item_id")
        
        if not all([feedback_type, item_type, item_id]):
            raise HTTPException(status_code=400, detail="Missing required feedback fields")
        
        patient = patient_manager.get_patient()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Update feedback points
        current_points = patient.get("feedback_points", 0)
        patient["feedback_points"] = current_points + 1
        
        # Track dislikes for demo purposes
        if feedback_type == "dislike":
            if "demo_dislikes" not in patient:
                patient["demo_dislikes"] = []
            
            dislike_entry = f"{item_type}:{item_id}"
            if dislike_entry not in patient["demo_dislikes"]:
                patient["demo_dislikes"].append(dislike_entry)
        
        # Save updated patient data
        patient_manager.update_patient(patient)
        
        return {
            "status": "success",
            "message": f"Feedback recorded: {feedback_type} for {item_type}",
            "feedback_points": patient["feedback_points"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

# ===== API ENDPOINTS =====

@app.post("/careconnect")
async def careconnect_endpoint(request: CareConnectRequest):
    """Main CareConnect pipeline endpoint"""
    global sequential_agent
    
    if not sequential_agent:
        raise HTTPException(status_code=503, detail="Sequential agent not initialized")
    
    try:
        # Run the enhanced sequential agent pipeline
        result = await sequential_agent.run(
            patient_profile=request.patient_profile.dict(),
            request_type=request.request_type,
            session_id=request.session_id,
            feedback_data=request.feedback_history
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ CareConnect pipeline error: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")

# ===== HEALTH CHECK ENDPOINTS =====

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint including theme images directory status"""
    global tools, sequential_agent
    
    # NEW: Get theme images directory status
    theme_images_status = {}
    if theme_manager:
        try:
            backend_images_dir = Path(__file__).parent / "data" / "images"
            theme_images_status = {
                "theme_manager_available": True,
                "backend_images_dir": str(backend_images_dir),
                "backend_images_dir_exists": backend_images_dir.exists(),
                "theme_images_dir": str(theme_manager.theme_images_dir),
                "theme_images_dir_exists": theme_manager.theme_images_dir.exists(),
                "themes_loaded": len(theme_manager.themes_list),
                "daily_theme": theme_manager.get_daily_theme().get("theme_of_the_day", {}).get("name", "Unknown")
            }
        except Exception as e:
            theme_images_status = {
                "theme_manager_available": False,
                "error": str(e)
            }
    else:
        theme_images_status = {"theme_manager_available": False}
    
    return {
        "status": "healthy",
        "timestamp": "2025-01-23T00:00:00Z",
        "tools_available": len(tools) if tools else 0,
        "agent_available": sequential_agent is not None,
        "personal_photo_analyzer_available": personal_photo_analyzer is not None,
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
        },
        "theme_images": theme_images_status,  # NEW: Theme images directory status
        "pipeline_mode": {
            "automatic_photos": "theme_only",
            "personal_photos": "on_demand_only"
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
        "agent_available": sequential_agent is not None,
        "personal_photo_analyzer_available": personal_photo_analyzer is not None,
        "file_structure": {
            "patients_json": str(patient_manager.patients_file),
            "images_directory": str(patient_manager.images_dir)
        },
        "pipeline_configuration": {
            "automatic_pipeline": "theme_photos_only",
            "personal_photos": "on_demand_button_click_only"
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
        "personal_photos": "/personal-photos",
        "analyze_personal_photo": "/analyze-personal-photo",
        "data_location": "frontend/static/demo/",
        "pipeline_mode": {
            "automatic_dashboard": "theme_photos_only",
            "personal_photos": "on_demand_analysis_only"
        }
    }

if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting CareConnect API server on port {config.PORT}")
    logger.info(f"Data directory: {patient_manager.data_dir if patient_manager else 'Not initialized'}")
    logger.info(f"Images directory: {patient_manager.images_dir if patient_manager else 'Not initialized'}")
    
    # NEW: Log theme images directory on startup
    if theme_manager:
        logger.info(f"🎯 Theme images directory: {theme_manager.theme_images_dir}")
    
    logger.info("🎯 FIXED: Personal photos removed from automatic pipeline")
    logger.info("📷 Personal photos available via on-demand analysis only")
    logger.info("🎯 Single patient demo mode enabled")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )
