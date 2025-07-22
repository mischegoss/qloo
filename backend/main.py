import os
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import CareConnect multi-agent system
from multi_tool_agent.tools import initialize_tools, test_all_tools, get_tool_status
from multi_tool_agent.sequential_agent import CareConnectAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Initialize FastAPI app
app = FastAPI(
    title="CareConnect Cultural Intelligence API",
    description="AI-powered dementia care assistant with 7-agent cultural intelligence pipeline",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Startup event to initialize multi-agent system
@app.on_event("startup")
async def startup_event():
    """Initialize the CareConnect multi-agent system on startup."""
    global tools, careconnect_agent
    
    try:
        logger.info("Initializing CareConnect multi-agent system...")
        
        # Initialize all tools
        tools = initialize_tools()
        logger.info("Tools initialized successfully")
        
        # Test tools (optional but recommended)
        logger.info("Testing tool connections...")
        test_results = await test_all_tools(tools)
        
        working_tools = sum(1 for result in test_results.values() if result)
        total_tools = len(test_results)
        logger.info(f"Tool test results: {working_tools}/{total_tools} tools working")
        
        if working_tools < total_tools:
            logger.warning(f"Some tools failed: {test_results}")
        
        # Initialize CareConnect agent
        careconnect_agent = CareConnectAgent(tools)
        logger.info("CareConnect 7-agent pipeline initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize CareConnect system: {str(e)}")
        # Continue without multi-agent system (fallback mode)
        tools = None
        careconnect_agent = None

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
        "timestamp": "2025-07-21",
        "multi_agent_system": "active" if careconnect_agent else "inactive"
    }

@app.get("/api/v1/system-status")
async def system_status():
    """Detailed system status including tool status."""
    tool_status = get_tool_status() if tools else {}
    
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
        logger.error("CareConnect agent not initialized - using fallback")
        return await fallback_response(request)
    
    try:
        logger.info(f"Processing CareConnect request: {request.request_type}")
        
        # Convert Pydantic model to dict for agent processing
        patient_profile_dict = request.patient_profile.dict()
        
        # Run the complete 7-agent pipeline
        result = await careconnect_agent.run(
            patient_profile=patient_profile_dict,
            request_type=request.request_type,
            session_id=request.session_id,
            feedback_history=request.feedback_history,
            photo_data=None,  # Photo handling in separate endpoint
            feedback_data=None
        )
        
        # Extract mobile experience for response
        mobile_experience = result.get("mobile_experience", {})
        pipeline_metadata = result.get("pipeline_metadata", {})
        
        logger.info(f"CareConnect pipeline completed successfully for {request.request_type}")
        
        return {
            "status": "success",
            "request_type": request.request_type,
            "patient_id": patient_profile_dict.get("first_name", "unknown"),
            "pipeline_metadata": pipeline_metadata,
            "mobile_experience": mobile_experience,
            "session_info": {
                "session_id": request.session_id,
                "agents_executed": pipeline_metadata.get("agents_executed", 7)
            }
        }
        
    except Exception as e:
        logger.error(f"CareConnect pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

@app.post("/api/v1/photo-analysis")
async def photo_analysis(
    patient_profile: str,  # JSON string of patient profile
    request_type: str = "photo_analysis",
    session_id: Optional[str] = None,
    photo: UploadFile = File(...)
):
    """
    Photo analysis endpoint - includes photo in the 7-agent pipeline.
    
    Processes uploaded photo through Agent 5 (Photo Cultural Analyzer)
    along with the complete pipeline.
    """
    
    if not careconnect_agent:
        raise HTTPException(status_code=503, detail="CareConnect agent not available")
    
    try:
        import json
        
        # Parse patient profile
        patient_profile_dict = json.loads(patient_profile)
        
        # Process uploaded photo
        photo_content = await photo.read()
        photo_data = {
            "type": "family_photo",
            "description": f"Uploaded photo: {photo.filename}",
            "timestamp": "2025-07-21",
            "content": photo_content  # In production, would process this properly
        }
        
        logger.info(f"Processing photo analysis request with {photo.filename}")
        
        # Run pipeline with photo data
        result = await careconnect_agent.run(
            patient_profile=patient_profile_dict,
            request_type=request_type,
            session_id=session_id,
            feedback_history=None,
            photo_data=photo_data,
            feedback_data=None
        )
        
        # Extract photo analysis results
        photo_analysis_result = result.get("photo_analysis", {})
        mobile_experience = result.get("mobile_experience", {})
        
        return {
            "status": "success",
            "request_type": "photo_analysis",
            "photo_filename": photo.filename,
            "photo_analysis": photo_analysis_result,
            "mobile_experience": mobile_experience,
            "session_info": {"session_id": session_id}
        }
        
    except Exception as e:
        logger.error(f"Photo analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Photo analysis error: {str(e)}")

@app.post("/api/v1/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit user feedback - processes through Agent 7 (Feedback Learning System).
    
    This endpoint handles emoji feedback and blocking choices to improve
    future recommendations.
    """
    
    if not careconnect_agent:
        raise HTTPException(status_code=503, detail="CareConnect agent not available")
    
    try:
        logger.info(f"Processing feedback: {feedback.feedback_type} for {feedback.content_category}")
        
        # Create feedback data structure
        feedback_data = {
            "session_id": feedback.session_id,
            "content_id": feedback.content_id,
            "feedback_type": feedback.feedback_type,
            "content_category": feedback.content_category,
            "content_details": feedback.content_details,
            "blocking_scope": feedback.blocking_scope,
            "timestamp": "2025-07-21"
        }
        
        # Process feedback through the agent pipeline
        # Note: This would typically run just Agent 7, but for simplicity
        # we're running the full pipeline with feedback data
        result = await careconnect_agent.run(
            patient_profile={"first_name": "feedback_user"},  # Minimal profile for feedback
            request_type="feedback_processing",
            session_id=feedback.session_id,
            feedback_history=None,
            photo_data=None,
            feedback_data=feedback_data
        )
        
        # Extract feedback learning results
        updated_preferences = result.get("updated_preferences", {})
        
        return {
            "status": "success",
            "message": "Feedback processed successfully",
            "session_id": feedback.session_id,
            "feedback_type": feedback.feedback_type,
            "updated_preferences": updated_preferences,
            "learning_applied": True
        }
        
    except Exception as e:
        logger.error(f"Feedback processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")

# Legacy compatibility endpoints (simplified versions)
@app.post("/api/v1/daily-dashboard")
async def legacy_daily_dashboard(request: CareConnectRequest):
    """Legacy daily dashboard endpoint - redirects to main CareConnect pipeline."""
    
    # Convert to CareConnect request format
    request.request_type = "dashboard"
    
    return await careconnect_pipeline(request)

# Test endpoints for individual components
@app.get("/api/v1/test-agents")
async def test_agents():
    """Test the multi-agent system with a simple request."""
    
    if not careconnect_agent:
        return {"status": "error", "message": "CareConnect agent not initialized"}
    
    try:
        # Simple test patient profile
        test_profile = {
            "first_name": "TestUser",
            "birth_year": 1950,
            "city": "Brooklyn",
            "cultural_heritage": "Italian-American"
        }
        
        # Run a simple dashboard request
        result = await careconnect_agent.run(
            patient_profile=test_profile,
            request_type="dashboard",
            session_id="test_session",
            feedback_history=None,
            photo_data=None,
            feedback_data=None
        )
        
        pipeline_metadata = result.get("pipeline_metadata", {})
        
        return {
            "status": "success",
            "message": "Agent pipeline test completed",
            "agents_executed": pipeline_metadata.get("agents_executed", 0),
            "pipeline_status": pipeline_metadata.get("pipeline_status", "unknown"),
            "test_completed": True
        }
        
    except Exception as e:
        logger.error(f"Agent test error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/test-tools")
async def test_tools_endpoint():
    """Test all tools individually."""
    
    if not tools:
        return {"status": "error", "message": "Tools not initialized"}
    
    try:
        test_results = await test_all_tools(tools)
        
        return {
            "status": "success",
            "message": "Tool tests completed",
            "test_results": test_results,
            "working_tools": sum(1 for result in test_results.values() if result),
            "total_tools": len(test_results)
        }
        
    except Exception as e:
        logger.error(f"Tool test error: {str(e)}")
        return {"status": "error", "message": str(e)}

# Fallback function for when multi-agent system is unavailable
async def fallback_response(request: CareConnectRequest):
    """Fallback response when multi-agent system is unavailable."""
    
    logger.warning("Using fallback response - multi-agent system unavailable")
    
    patient_profile = request.patient_profile
    
    return {
        "status": "fallback_mode",
        "request_type": request.request_type,
        "patient_id": patient_profile.first_name,
        "message": "Multi-agent system unavailable - using simple fallback",
        "mobile_experience": {
            "page_structure": {"structure_type": "simple_fallback"},
            "mobile_content": {
                "primary_content": {
                    "content_type": "basic_activities",
                    "activities": [
                        f"Listen to music from the {patient_profile.birth_year or 1950}s",
                        "Look at family photos together",
                        "Have a conversation about favorite memories",
                        "Enjoy a simple, familiar meal together"
                    ]
                }
            },
            "caregiver_guide": {
                "caregiver_authority_note": {
                    "principle": "You know them best - use your caring judgment",
                    "approach": "Focus on simple, familiar activities they enjoy"
                }
            }
        },
        "fallback_reason": "Multi-agent system initialization failed"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=config.PORT, 
        reload=True
    )