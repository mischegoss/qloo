"""
Complete Fixed main.py with Theme Image Support - ENHANCED VERSION
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
        self.dashboard_cache = {
            "content": None,
            "timestamp": None,
            "expiry_minutes": 5  # Cache expires in 5 minutes
        }
        
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
    
    def select_photo_of_the_day(self):
        """Rotate through available photos"""
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
            file_path = self.images_dir / filename
            
            # Save file
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Process with Vision AI
            google_cloud_api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
            if google_cloud_api_key:
                vision_analyzer = VisionAIAnalyzer(google_cloud_api_key)
                image_base64 = base64.b64encode(content).decode('utf-8')
                vision_result = await vision_analyzer.analyze_with_google_vision(image_base64)
                
                if vision_result and vision_result.get("success"):
                    vision_analysis = {
                        "objects": vision_result.get("objects", []),
                        "labels": vision_result.get("labels", []),
                        "people": vision_result.get("people", []),
                        "activities": vision_result.get("activities", []),
                        "settings": vision_result.get("settings", [])
                    }
                else:
                    logger.warning("Vision AI analysis failed, using fallback")
                    vision_analysis = {
                        "objects": ["photo", "uploaded_image"],
                        "labels": ["personal", "memory"],
                        "people": [],
                        "activities": [],
                        "settings": []
                    }
            else:
                logger.warning("No Google Cloud API key, using fallback analysis")
                vision_analysis = {
                    "objects": ["photo", "uploaded_image"],
                    "labels": ["personal", "memory"],
                    "people": [],
                    "activities": [],
                    "settings": []
                }
            
            # Update patient data
            patient = self.get_patient()
            if patient:
                photo_url = f"static/demo/images/{filename}"
                
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
    
    def _initialize_demo_patients(self):
        """Initialize demo patient data if not exists"""
        if self.patients_file.exists():
            return
        
        # Create sample demo patient
        demo_data = {
            "demo_patient": {
                "first_name": "Maria",
                "birth_year": 1950,
                "birth_month": "June",
                "city": "San Antonio",
                "state": "Texas",
                "cultural_heritage": "Mexican",
                "languages": "Spanish, English",
                "spiritual_traditions": "Catholic",
                "additional_context": "Loves cooking traditional Mexican food, especially for family gatherings. Has 4 children and 7 grandchildren.",
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
        except Exception as e:
            logger.error(f"Failed to update patient: {e}")
            return None

# Global variables for multi-agent system
tools = None
sequential_agent = None
patient_manager = DemoPatientManager()

# NEW: Function to setup and validate backend data directories
def setup_backend_data_directories():
    """Set up and validate backend data directories including theme images"""
    
    # Set up backend/data/images directory for theme images
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
    global tools, sequential_agent
    
    logger.info("🚀 Starting CareConnect Cultural Intelligence API...")
    
    # NEW: Setup backend data directories and theme images
    backend_images_dir = setup_backend_data_directories()
    
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
    
    # Initialize Enhanced Sequential Agent
    if SequentialAgent and tools:
        try:
            # Import agents with error handling
            try:
                from multi_tool_agent.agents.information_consolidator_agent import InformationConsolidatorAgent
            except ImportError:
                InformationConsolidatorAgent = None
                
            try:
                from multi_tool_agent.agents.cultural_profile_agent import CulturalProfileBuilderAgent
            except ImportError:
                CulturalProfileBuilderAgent = None
                
            try:
                from multi_tool_agent.agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
            except ImportError:
                QlooCulturalIntelligenceAgent = None
                
            try:
                from multi_tool_agent.agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
            except ImportError:
                SensoryContentGeneratorAgent = None
                
            try:
                from multi_tool_agent.agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
            except ImportError:
                PhotoCulturalAnalyzerAgent = None
                
            try:
                from multi_tool_agent.agents.mobile_synthesizer_agent import MobileSynthesizerAgent
            except ImportError:
                MobileSynthesizerAgent = None
            
            # Extract tools
            qloo_tool = tools.get("qloo_tool")
            youtube_tool = tools.get("youtube_tool") 
            gemini_tool = tools.get("gemini_tool")
            vision_ai_tool = tools.get("vision_ai_tool")
            session_storage_tool = tools.get("session_storage_tool")
            
            # Create individual agents with proper method checking
            agent1 = InformationConsolidatorAgent() if InformationConsolidatorAgent else None
            agent2 = CulturalProfileBuilderAgent() if CulturalProfileBuilderAgent else None
            agent3 = QlooCulturalIntelligenceAgent(qloo_tool) if QlooCulturalIntelligenceAgent and qloo_tool else None
            
            # Agent 4: Check if it has 'run' method, otherwise skip
            agent4 = None
            if SensoryContentGeneratorAgent and gemini_tool:
                temp_agent4 = SensoryContentGeneratorAgent(gemini_tool, youtube_tool)
                if hasattr(temp_agent4, 'run'):
                    agent4 = temp_agent4
                    logger.info("✅ Agent 4 (SensoryContentGenerator) - has 'run' method")
                else:
                    logger.warning("⚠️ Agent 4 (SensoryContentGenerator) - no 'run' method, skipping")
            
            agent5 = PhotoCulturalAnalyzerAgent(vision_ai_tool) if PhotoCulturalAnalyzerAgent and vision_ai_tool else None
            
            # Agent 6: Check if it has 'run' method, otherwise skip  
            agent6 = None
            if MobileSynthesizerAgent:
                temp_agent6 = MobileSynthesizerAgent()
                if hasattr(temp_agent6, 'run'):
                    agent6 = temp_agent6
                    logger.info("✅ Agent 6 (MobileSynthesizer) - has 'run' method")
                else:
                    logger.warning("⚠️ Agent 6 (MobileSynthesizer) - no 'run' method, skipping")
            
            # Initialize Enhanced Sequential Agent with individual agents
            sequential_agent = SequentialAgent(
                agent1=agent1,
                agent2=agent2, 
                agent3=agent3,
                agent4=agent4,
                agent5=agent5,
                agent6=agent6
            )
            
            # NEW: Inject theme manager into the sequential agent for proper theme integration
            if theme_manager:
                sequential_agent.theme_manager = theme_manager
                # Test theme integration
                test_theme = theme_manager.get_daily_theme()
                test_theme_name = test_theme.get("theme_of_the_day", {}).get("name", "Unknown")
                logger.info(f"✅ Theme manager injected: Today's theme = {test_theme_name}")
            else:
                logger.warning("⚠️ Theme manager not available for injection")
            
            # Count active agents and verify methods
            active_agents = sum(1 for agent in [agent1, agent2, agent3, agent4, agent5, agent6] if agent is not None)
            logger.info(f"✅ Enhanced Sequential Agent initialized with {active_agents}/6 agents active")
            
            # Debug: Check which agents have run methods
            agent_methods = []
            for i, agent in enumerate([agent1, agent2, agent3, agent4, agent5, agent6], 1):
                if agent:
                    has_run = hasattr(agent, 'run')
                    agent_methods.append(f"Agent{i}:{'✅' if has_run else '❌'}")
            logger.info(f"🔍 Agent methods check: {', '.join(agent_methods)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Enhanced Sequential Agent: {e}")
            sequential_agent = None
    else:
        logger.warning("⚠️  Enhanced Sequential Agent not available")
        sequential_agent = None
    
    # NEW: Validate theme manager and log theme status
    if theme_manager:
        try:
            daily_theme = theme_manager.get_daily_theme()
            theme_name = daily_theme.get("theme_of_the_day", {}).get("name", "Unknown")
            theme_image = daily_theme.get("theme_image", {})
            
            logger.info(f"🎯 Theme system ready:")
            logger.info(f"   📅 Today's theme: {theme_name}")
            logger.info(f"   🖼️ Theme image: {theme_image.get('filename', 'Not found')} (exists: {theme_image.get('exists', False)})")
            logger.info(f"   📚 Total themes available: {len(theme_manager.themes_list)}")
        except Exception as e:
            logger.error(f"❌ Theme manager validation failed: {e}")
    else:
        logger.warning("⚠️ Theme manager not available")
    
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
    
    global sequential_agent
    
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
        
        # Run pipeline if agent available
        if sequential_agent:
            result = await sequential_agent.run_full_pipeline(
                patient_profile=patient,
                request_type="dashboard",
                session_id=f"ui_session_demo",
                feedback_data=None,
                photo_of_the_day=photo_of_the_day,
                photo_analysis=photo_analysis
            )
            
            if result.get("status") == "success":
                # Cache the result
                patient_manager.cache_dashboard(result["content"])
                
                return {
                    "status": "success",
                    "source": "generated",
                    "patient_name": patient["first_name"],
                    "content": result["content"],
                    "pipeline_metadata": result["content"].get("pipeline_metadata", {}),
                    "message": "Dashboard refreshed successfully!"
                }
            else:
                raise HTTPException(status_code=500, detail="Pipeline execution failed")
        else:
            # Fallback dashboard if no agent
            fallback_content = {
                "consolidated_info": {"patient_profile": patient},
                "cultural_profile": {"heritage": patient.get("cultural_heritage", "American")},
                "qloo_intelligence": {"music": {"artist": "Elvis Presley", "genre": "Rock"}},
                "sensory_content": {"recipe": {"name": "Traditional Soup", "description": "A comforting recipe"}},
                "photo_analysis": {"conversation_starters": [{"starter": "Tell me about your family", "type": "general"}]},
                "mobile_experience": {"status": "demo_mode"}
            }
            
            return {
                "status": "success",
                "source": "fallback",
                "patient_name": patient["first_name"],
                "content": fallback_content,
                "message": "Using demo data (agent not available)"
            }
            
    except Exception as e:
        logger.error(f"❌ Dashboard refresh failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard refresh failed: {str(e)}")

# ===== API ENDPOINTS =====

@app.post("/careconnect")
async def careconnect_endpoint(request: CareConnectRequest):
    """Main CareConnect pipeline endpoint"""
    global sequential_agent
    
    if not sequential_agent:
        raise HTTPException(status_code=503, detail="Sequential agent not initialized")
    
    try:
        # Run the enhanced sequential agent pipeline
        result = await sequential_agent.run_full_pipeline(
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
        "theme_images": theme_images_status  # NEW: Theme images directory status
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
    
    # NEW: Log theme images directory on startup
    if theme_manager:
        logger.info(f"🎯 Theme images directory: {theme_manager.theme_images_dir}")
    
    logger.info("🎯 Single patient demo mode enabled")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )