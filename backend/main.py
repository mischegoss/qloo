"""
CareConnect FastAPI Main Application - UPDATED VERSION
File: backend/main.py

Updated to handle the curl input format and integrate the simplified agent pipeline.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import our tools
from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
from multi_tool_agent.tools.youtube_tools import YouTubeAPI
from multi_tool_agent.tools.gemini_tools import GeminiRecipeGenerator
from multi_tool_agent.tools.vision_ai_tools import VisionAIAnalyzer
from multi_tool_agent.tools.session_storage_tools import SessionStorageManager

# Import sequential agent coordinator
from multi_tool_agent.sequential_agent import SequentialAgentCoordinator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CareConnect - Simplified Backend API",
    description="AI-powered dementia care assistant with simplified Qloo integration",
    version="2.0.0-simplified"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for tools and coordinator
qloo_tool = None
youtube_tool = None
gemini_tool = None
vision_ai_tool = None
session_storage_tool = None
agent_coordinator = None

# Pydantic models for request/response
class PatientProfile(BaseModel):
    """Patient profile matching the curl input format."""
    cultural_heritage: str = Field(..., description="Cultural heritage (e.g., 'Italian-American')")
    birth_year: int = Field(..., description="Year of birth for age calculation")
    city: Optional[str] = Field(None, description="City of residence")
    state: Optional[str] = Field(None, description="State of residence")
    additional_context: Optional[str] = Field(None, description="Additional context about preferences")
    caregiver_notes: Optional[str] = Field(None, description="Notes from caregiver")
    age: Optional[int] = Field(None, description="Direct age if birth_year not available")

class CareConnectRequest(BaseModel):
    """Main request model matching curl format."""
    patient_profile: PatientProfile
    request_type: str = Field(default="dashboard", description="Type of request")
    feedback_data: Optional[Dict[str, Any]] = Field(None, description="Optional feedback data")
    photo_data: Optional[Dict[str, Any]] = Field(None, description="Optional photo data")

class CareConnectResponse(BaseModel):
    """Response model for CareConnect API."""
    success: bool
    pipeline_results: Dict[str, Any]
    pipeline_metadata: Dict[str, Any]
    error: Optional[str] = None
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """Initialize tools and agent coordinator on startup."""
    global qloo_tool, youtube_tool, gemini_tool, vision_ai_tool, session_storage_tool, agent_coordinator
    
    logger.info("🚀 Starting CareConnect Backend with Simplified Architecture")
    
    # Load environment variables
    qloo_api_key = os.getenv("QLOO_API_KEY")
    google_api_key = os.getenv("GOOGLE_CLOUD_API_KEY") 
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    # Initialize tools
    tool_status = {}
    
    # Initialize Qloo tool
    if qloo_api_key:
        try:
            qloo_tool = QlooInsightsAPI(qloo_api_key)
            # Test connection
            connection_test = await qloo_tool.test_connection()
            tool_status["qloo"] = "✅ Available" if connection_test else "❌ Connection failed"
        except Exception as e:
            logger.error(f"Qloo tool initialization failed: {e}")
            tool_status["qloo"] = "❌ Failed"
    else:
        tool_status["qloo"] = "❌ No API key"
    
    # Initialize YouTube tool  
    if google_api_key:
        try:
            youtube_tool = YouTubeMusicSearchTool(google_api_key)
            # Test connection
            test_result = await youtube_tool.search_music("test", max_results=1)
            tool_status["youtube"] = "✅ Available" if test_result.get("success") else "❌ Connection failed"
        except Exception as e:
            logger.error(f"YouTube tool initialization failed: {e}")
            tool_status["youtube"] = "❌ Failed"
    else:
        tool_status["youtube"] = "❌ No API key"
    
    # Initialize Gemini tool
    if gemini_api_key:
        try:
            gemini_tool = GeminiRecipeGenerator(gemini_api_key)
            tool_status["gemini"] = "✅ Available"
        except Exception as e:
            logger.error(f"Gemini tool initialization failed: {e}")
            tool_status["gemini"] = "❌ Failed"
    else:
        tool_status["gemini"] = "❌ No API key"
    
    # Initialize Vision AI tool
    if google_api_key:
        try:
            vision_ai_tool = VisionAIAnalyzer(google_api_key)
            tool_status["vision_ai"] = "✅ Available"
        except Exception as e:
            logger.error(f"Vision AI tool initialization failed: {e}")
            tool_status["vision_ai"] = "❌ Failed"
    else:
        tool_status["vision_ai"] = "❌ No API key"
    
    # Initialize session storage tool
    try:
        session_storage_tool = SessionStorageTool()
        tool_status["session_storage"] = "✅ Available"
    except Exception as e:
        logger.error(f"Session storage tool initialization failed: {e}")
        tool_status["session_storage"] = "❌ Failed"
    
    # Log tool status
    logger.info("🔧 Tool Status:")
    for tool_name, status in tool_status.items():
        logger.info(f"   - {tool_name.title()}: {status}")
    
    # Initialize agent coordinator
    try:
        agent_coordinator = SequentialAgentCoordinator(
            qloo_tool=qloo_tool,
            youtube_tool=youtube_tool,
            gemini_tool=gemini_tool,
            vision_ai_tool=vision_ai_tool,
            session_storage_tool=session_storage_tool
        )
        logger.info("🎉 CareConnect agent pipeline initialized successfully")
    except Exception as e:
        logger.error(f"❌ Agent coordinator initialization failed: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "CareConnect Backend API",
        "version": "2.0.0-simplified",
        "status": "active",
        "architecture": "simplified_tag_based",
        "endpoints": {
            "dashboard": "/api/v1/dashboard",
            "status": "/api/v1/status",
            "health": "/health"
        },
        "documentation": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global agent_coordinator
    
    health_status = {
        "status": "healthy" if agent_coordinator else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0-simplified"
    }
    
    if agent_coordinator:
        health_status["agents"] = agent_coordinator.get_agent_status()
    
    return health_status

@app.get("/api/v1/status")
async def get_api_status():
    """Get detailed API and tool status."""
    global qloo_tool, youtube_tool, gemini_tool, vision_ai_tool, session_storage_tool, agent_coordinator
    
    # Test tool connections
    tool_tests = {}
    
    if qloo_tool:
        tool_tests["qloo"] = await qloo_tool.test_connection()
    else:
        tool_tests["qloo"] = False
    
    if youtube_tool:
        test_result = await youtube_tool.search_music("test", max_results=1)
        tool_tests["youtube"] = test_result.get("success", False)
    else:
        tool_tests["youtube"] = False
    
    tool_tests["gemini"] = gemini_tool is not None
    tool_tests["vision_ai"] = vision_ai_tool is not None
    tool_tests["session_storage"] = session_storage_tool is not None
    
    status = {
        "api_status": "active",
        "tools": {
            "qloo_api": "✅ Connected" if tool_tests["qloo"] else "❌ Disconnected",
            "youtube_api": "✅ Connected" if tool_tests["youtube"] else "❌ Disconnected", 
            "gemini_api": "✅ Available" if tool_tests["gemini"] else "❌ Unavailable",
            "vision_ai": "✅ Available" if tool_tests["vision_ai"] else "❌ Unavailable",
            "session_storage": "✅ Available" if tool_tests["session_storage"] else "❌ Unavailable"
        },
        "agents": agent_coordinator.get_agent_status() if agent_coordinator else {},
        "architecture": "simplified_tag_based",
        "timestamp": datetime.now().isoformat()
    }
    
    return status

@app.post("/api/v1/dashboard", response_model=CareConnectResponse)
async def generate_dashboard(request: CareConnectRequest):
    """
    Generate CareConnect dashboard using the simplified agent pipeline.
    
    This endpoint matches the curl format from the simplification plan.
    """
    global agent_coordinator
    
    if not agent_coordinator:
        raise HTTPException(status_code=500, detail="Agent coordinator not initialized")
    
    try:
        logger.info(f"Dashboard request for {request.patient_profile.cultural_heritage} heritage")
        
        # Convert Pydantic model to dict for agent processing
        patient_profile_dict = request.patient_profile.dict(exclude_none=True)
        
        # Execute the simplified agent pipeline
        pipeline_result = await agent_coordinator.execute_pipeline(
            patient_profile=patient_profile_dict,
            request_type=request.request_type,
            feedback_data=request.feedback_data,
            photo_data=request.photo_data
        )
        
        # Build response
        if pipeline_result.get("status") == "success":
            response = CareConnectResponse(
                success=True,
                pipeline_results=pipeline_result.get("pipeline_results", {}),
                pipeline_metadata=pipeline_result.get("pipeline_metadata", {}),
                timestamp=datetime.now().isoformat()
            )
            
            logger.info("✅ Dashboard generation completed successfully")
            return response
        
        else:
            # Pipeline failed
            error_msg = pipeline_result.get("pipeline_metadata", {}).get("error", "Unknown pipeline error")
            raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {error_msg}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Dashboard generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/test-curl")
async def test_curl_format(request: Dict[str, Any]):
    """
    Test endpoint for the exact curl format from the simplification plan.
    
    Example curl:
    curl -X POST http://localhost:8000/api/v1/test-curl \
      -H "Content-Type: application/json" \
      -d '{
        "patient_profile": {
          "cultural_heritage": "Italian-American",
          "birth_year": 1945,
          "city": "Brooklyn",
          "state": "New York",
          "additional_context": "Loves music and cooking"
        },
        "request_type": "dashboard"
      }'
    """
    global agent_coordinator
    
    if not agent_coordinator:
        return {"error": "Agent coordinator not initialized", "status": "failed"}
    
    try:
        logger.info("Processing test curl request")
        
        # Extract patient profile
        patient_profile = request.get("patient_profile", {})
        request_type = request.get("request_type", "dashboard")
        
        # Log the input analysis as per the plan
        heritage = patient_profile.get("cultural_heritage", "Unknown")
        birth_year = patient_profile.get("birth_year")
        age = 2024 - birth_year if birth_year else "Unknown"
        city = patient_profile.get("city", "Unknown")
        state = patient_profile.get("state", "Unknown")
        context = patient_profile.get("additional_context", "")
        
        logger.info("Input Analysis:")
        logger.info(f"  Cultural Heritage: {heritage}")
        logger.info(f"  Birth Year: {birth_year} → Age: {age}")
        logger.info(f"  Location: {city}, {state}")
        logger.info(f"  Additional Context: {context}")
        logger.info(f"  Request Type: {request_type}")
        
        # Execute pipeline
        pipeline_result = await agent_coordinator.execute_pipeline(
            patient_profile=patient_profile,
            request_type=request_type
        )
        
        # Build test response
        if pipeline_result.get("status") == "success":
            # Extract key results for testing
            metadata = pipeline_result.get("pipeline_metadata", {})
            cultural_profile = pipeline_result.get("pipeline_results", {}).get("cultural_profile", {})
            qloo_intelligence = pipeline_result.get("pipeline_results", {}).get("qloo_intelligence", {})
            
            test_response = {
                "status": "success",
                "input_analysis": {
                    "cultural_heritage": heritage,
                    "age": age,
                    "age_demographic": "55_and_older" if age != "Unknown" and age >= 55 else "younger",
                    "location": f"{city}, {state}",
                    "preferences_parsed": context.split() if context else []
                },
                "pipeline_execution": {
                    "agents_executed": metadata.get("agents_executed", 0),
                    "active_agents": metadata.get("active_agents", []),
                    "pipeline_success": metadata.get("pipeline_success", False)
                },
                "cultural_intelligence": {
                    "heritage_mapped": cultural_profile.get("cultural_elements", {}).get("heritage"),
                    "qloo_tag_mappings": cultural_profile.get("qloo_tag_mappings", {}),
                    "qloo_calls_successful": qloo_intelligence.get("metadata", {}).get("successful_calls", 0),
                    "qloo_total_results": qloo_intelligence.get("metadata", {}).get("total_results", 0)
                },
                "expected_qloo_calls": [
                    f"filter.type=urn:entity:place, filter.tags=urn:tag:cuisine:italian, age=55_and_older",
                    f"filter.type=urn:entity:artist, filter.tags=urn:tag:genre:music:classical, age=55_and_older",
                    f"filter.type=urn:entity:movie, filter.tags=urn:tag:genre:media:family, age=55_and_older"
                ] if heritage == "Italian-American" else ["Heritage-specific calls based on input"],
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Test curl request completed successfully")
            return test_response
        
        else:
            return {
                "status": "failed",
                "error": pipeline_result.get("pipeline_metadata", {}).get("error", "Pipeline failed"),
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"❌ Test curl request failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = os.getenv("BACKEND_HOST", "localhost")
    port = int(os.getenv("BACKEND_PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    logger.info(f"Starting CareConnect Backend on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )