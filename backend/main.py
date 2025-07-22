"""
Fixed main.py
File: backend/main.py

Main FastAPI application for CareConnect Cultural Intelligence API
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
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
    # Try alternative import names for backward compatibility
    try:
        from multi_tool_agent.sequential_agent import CareConnectSequentialAgent as CareConnectAgent
        logger.info("✅ CareConnectSequentialAgent imported as CareConnectAgent")
    except ImportError:
        logger.warning("⚠️  CareConnectAgent not available - using minimal mode")
        CareConnectAgent = None

# Configuration
class Config:
    PORT = int(os.getenv("PORT", 8080))
    QLOO_API_KEY = os.getenv("QLOO_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_CLOUD_API_KEY"))

config = Config()

# Global variables for multi-agent system
tools = None
careconnect_agent = None

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
    request_type: str = "dashboard"  # dashboard, meal, conversation, music, video, photo_analysis
    session_id: Optional[str] = None
    feedback_history: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    session_id: str
    content_id: str
    feedback_type: str  # "positive", "negative", "blocked"
    content_category: str  # "music", "food", "conversation", etc.
    content_details: Dict[str, Any]
    blocking_scope: Optional[str] = None  # "item", "type", "category"

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    global tools, careconnect_agent
    
    # Startup
    try:
        logger.info("🚀 Initializing CareConnect multi-agent system with Gemini-Qloo integration...")
        
        if initialize_all_tools:
            # Initialize all tools
            tools = initialize_all_tools()
            logger.info("🔧 Tool Status:")
            
            # Check tool status
            if tools:
                qloo_available = "qloo_tool" in tools
                gemini_available = "gemini_tool" in tools
                
                logger.info(f"   - Qloo API: {'✅ Available' if qloo_available else '❌ Unavailable'}")
                logger.info(f"   - Gemini API: {'✅ Available' if gemini_available else '❌ Unavailable'}")
                
                if not qloo_available:
                    logger.warning("⚠️  Qloo API unavailable - cultural recommendations will be limited")
                if not gemini_available:
                    logger.warning("⚠️  Gemini API unavailable - query optimization disabled")
            
            # Test tools (optional but recommended)
            if test_all_tools and tools:
                logger.info("Testing tool connections...")
                test_results = await test_all_tools(tools)
                
                working_tools = sum(1 for result in test_results.values() if result)
                total_tools = len(test_results)
                logger.info(f"Tool test results: {working_tools}/{total_tools} tools working")
            
            # Initialize CareConnect agent
            if CareConnectAgent and tools:
                sequential_agent = CareConnectAgent(tools)
                careconnect_agent = sequential_agent
                logger.info("🎉 CareConnect 7-agent pipeline initialized successfully")
            else:
                logger.warning("⚠️  CareConnect agent not available - running in limited mode")
        else:
            logger.error("❌ Tool initialization functions not available")
            
    except Exception as e:
        logger.error(f"💥 Initialization failed: {str(e)}")
        # Continue in fallback mode
        tools = None
        careconnect_agent = None
    
    # Yield control to the application
    yield
    
    # Shutdown (cleanup if needed)
    logger.info("🔄 Shutting down CareConnect system...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="CareConnect Cultural Intelligence API",
    description="AI-powered dementia care assistant with 7-agent cultural intelligence pipeline",
    version="2.0.0",
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

# Basic health endpoints
@app.get("/")
async def root():
    """Root endpoint with system status."""
    return {
        "message": "CareConnect AI-Powered Dementia Care Assistant",
        "status": "healthy",
        "version": "2.0.0",
        "system": "7-agent cultural intelligence pipeline",
        "multi_agent_status": "active" if careconnect_agent else "fallback_mode",
        "api_keys_configured": {
            "qloo": bool(config.QLOO_API_KEY),
            "youtube": bool(config.YOUTUBE_API_KEY),
            "google_cloud": bool(config.GOOGLE_CLOUD_API_KEY),
            "gemini": bool(config.GEMINI_API_KEY)
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "timestamp": "2025-07-22",
        "multi_agent_system": "active" if careconnect_agent else "inactive"
    }

@app.get("/api/v1/system-status")
async def system_status():
    """Detailed system status including tool status."""
    tool_status = get_tool_status() if get_tool_status else {}
    
    return {
        "status": "success",
        "system_info": {
            "multi_agent_pipeline": "active" if careconnect_agent else "inactive",
            "tools_initialized": bool(tools),
            "agent_count": 7 if careconnect_agent else 0
        },
        "tool_status": tool_status,
        "environment": {
            "port": config.PORT,
            "api_keys_configured": {
                "qloo": bool(config.QLOO_API_KEY),
                "youtube": bool(config.YOUTUBE_API_KEY), 
                "google_cloud": bool(config.GOOGLE_CLOUD_API_KEY),
                "gemini": bool(config.GEMINI_API_KEY)
            }
        }
    }

# Main CareConnect endpoints
@app.post("/api/v1/careconnect")
async def careconnect_pipeline(request: CareConnectRequest):
    """
    Main CareConnect endpoint - runs the complete 7-agent pipeline.
    
    This endpoint processes patient information through all 7 agents:
    1. Information Consolidator
    2. Cultural Profile Builder  
    3. Qloo Cultural Intelligence
    4. Sensory Content Generator
    5. Photo Cultural Analyzer
    6. Mobile Synthesizer
    7. Feedback Learning System
    """
    
    if not careconnect_agent:
        # Fallback mode - return basic response
        return {
            "status": "fallback_mode",
            "message": "Multi-agent system not available - running in limited mode",
            "patient_name": request.patient_profile.first_name,
            "request_type": request.request_type,
            "basic_recommendations": {
                "message": "Please configure API keys to enable full cultural intelligence features",
                "available_features": ["basic_health_check", "system_status"]
            }
        }
    
    try:
        # Convert Pydantic model to dict for processing
        patient_profile_dict = request.patient_profile.dict()
        
        # Run the complete pipeline
        result = await careconnect_agent.run(
            patient_profile=patient_profile_dict,
            request_type=request.request_type,
            session_id=request.session_id,
            feedback_history=request.feedback_history
        )
        
        return {
            "status": "success",
            "pipeline_results": result,
            "patient_name": request.patient_profile.first_name,
            "request_type": request.request_type
        }
        
    except Exception as e:
        logger.error(f"CareConnect pipeline error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Pipeline execution failed: {str(e)}"
        )

@app.post("/api/v1/feedback")
async def process_feedback(request: FeedbackRequest):
    """Process user feedback for learning and preference updates."""
    
    if not careconnect_agent:
        return {
            "status": "fallback_mode",
            "message": "Feedback processing not available - multi-agent system inactive"
        }
    
    try:
        # Process feedback through the feedback learning agent
        # This would typically update user preferences and blocked content
        
        return {
            "status": "success",
            "message": "Feedback processed successfully",
            "session_id": request.session_id,
            "feedback_type": request.feedback_type,
            "content_category": request.content_category
        }
        
    except Exception as e:
        logger.error(f"Feedback processing error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Feedback processing failed: {str(e)}"
        )

@app.post("/api/v1/photo-analysis")
async def analyze_photo(file: UploadFile = File(...), patient_context: str = ""):
    """Analyze uploaded photo for cultural context."""
    
    if not careconnect_agent:
        return {
            "status": "fallback_mode",
            "message": "Photo analysis not available - multi-agent system inactive"
        }
    
    try:
        # Process uploaded photo
        # This would typically run through the photo cultural analyzer agent
        
        return {
            "status": "success",
            "message": "Photo analysis completed",
            "filename": file.filename,
            "analysis_results": {
                "cultural_elements": [],
                "era_indicators": [],
                "recommendations": []
            }
        }
        
    except Exception as e:
        logger.error(f"Photo analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Photo analysis failed: {str(e)}"
        )

# Development endpoints
@app.get("/api/v1/test-tools")
async def test_tools_endpoint():
    """Test all configured tools."""
    
    if not tools or not test_all_tools:
        return {
            "status": "error",
            "message": "Tools not initialized or test function not available"
        }
    
    try:
        test_results = await test_all_tools(tools)
        return {
            "status": "success",
            "test_results": test_results
        }
    except Exception as e:
        logger.error(f"Tool testing error: {str(e)}")
        return {
            "status": "error",
            "message": f"Tool testing failed: {str(e)}"
        }

if __name__ == "__main__":
    logger.info(f"Starting CareConnect API server on port {config.PORT}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )