"""
Updated main.py - 6 Agent Pipeline with Nostalgia News Integration
File: backend/main.py

FIXED: Corrected config import from lowercase 'config' to uppercase 'Config'
- Agent 1: Information Consolidator
- Agent 2: Simple Photo Analysis  
- Agent 3: Qloo Cultural Intelligence
- Agents 4A/4B/4C: Content Generation
- Agent 5: Nostalgia News Generator (STAR FEATURE)
- Agent 6: Dashboard Synthesizer
"""

import logging
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import os
from datetime import datetime

# FIXED: Import configuration with correct case
from config.settings import Config
from patient_data.demo_patient_manager import DemoPatientManager

# Import the updated sequential agent and all individual agents
from multi_tool_agent.sequential_agent import SequentialAgent
from multi_tool_agent.agents.information_consolidator_agent import InformationConsolidatorAgent
from multi_tool_agent.agents.simple_photo_analysis_agent import SimplePhotoAnalysisAgent
from multi_tool_agent.agents.qloo_cultural_analysis_agent import QlooCulturalAnalysisAgent
from multi_tool_agent.agents.music_curation_agent import MusicCurationAgent
from multi_tool_agent.agents.recipe_selection_agent import RecipeSelectionAgent
from multi_tool_agent.agents.photo_description_agent import PhotoDescriptionAgent
from multi_tool_agent.agents.nostalgia_news_generator import NostalgiaNewsGenerator
from multi_tool_agent.agents.dashboard_synthesizer import DashboardSynthesizer

# Import tools for initialization
from multi_tool_agent.tools import initialize_all_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Enhanced CareConnect API",
    description="6-Agent Pipeline with Nostalgia News Generator",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for agents and tools
sequential_agent = None
demo_manager = None
tools = None

@app.on_event("startup")
async def startup_event():
    """Initialize the enhanced CareConnect API with 6-agent pipeline"""
    
    global sequential_agent, demo_manager, tools
    
    try:
        logger.info("🚀 Starting Enhanced CareConnect API with Nostalgia News")
        logger.info("📰 Star Feature: Personalized cultural storytelling")
        
        # Validate configuration
        logger.info("🔧 Validating configuration...")
        config_status = Config.get_status()
        logger.info(f"📊 Configuration: {config_status}")
        
        # Initialize demo patient manager
        demo_manager = DemoPatientManager()
        logger.info("✅ Demo patient manager initialized")
        
        # Initialize tools with safe fallbacks
        logger.info("🛠️ Initializing tools...")
        tools = initialize_all_tools()
        
        # Log tool status
        available_tools = [name for name, tool in tools.items() if tool is not None]
        logger.info(f"🛠️ Available tools: {', '.join(available_tools)}")
        
        # Initialize all agents
        logger.info("🤖 Initializing agents...")
        
        # Agent 1: Information Consolidator
        agent1 = InformationConsolidatorAgent()
        logger.info("✅ Agent 1 (Information Consolidator) initialized")
        
        # Agent 2: Simple Photo Analysis
        vision_tool = tools.get("vision_ai_tool")
        agent2 = SimplePhotoAnalysisAgent(vision_tool=vision_tool)
        logger.info("✅ Agent 2 (Simple Photo Analysis) initialized")
        
        # Agent 3: Qloo Cultural Intelligence
        qloo_tool = tools.get("qloo_tool")
        agent3 = QlooCulturalAnalysisAgent(qloo_tool=qloo_tool)
        logger.info("✅ Agent 3 (Qloo Cultural Intelligence) initialized")
        
        # Agent 4A: Music Curation
        youtube_tool = tools.get("youtube_tool")
        gemini_tool = tools.get("gemini_tool")  # This could be simple_gemini_tool
        agent4a = MusicCurationAgent(youtube_tool=youtube_tool, gemini_tool=gemini_tool)
        logger.info("✅ Agent 4A (Music Curation) initialized")
        
        # Agent 4B: Recipe Selection
        agent4b = RecipeSelectionAgent()
        logger.info("✅ Agent 4B (Recipe Selection) initialized")
        
        # Agent 4C: Photo Description
        agent4c = PhotoDescriptionAgent(gemini_tool=gemini_tool)
        logger.info("✅ Agent 4C (Photo Description) initialized")
        
        # Agent 5: Nostalgia News Generator (STAR FEATURE)
        # Uses simple_gemini_tools for consistency
        agent5 = NostalgiaNewsGenerator(gemini_tool=gemini_tool)
        logger.info("✅ Agent 5 (Nostalgia News Generator) initialized - STAR FEATURE!")
        
        # Agent 6: Dashboard Synthesizer
        agent6 = DashboardSynthesizer()
        logger.info("✅ Agent 6 (Dashboard Synthesizer) initialized")
        
        # Initialize Sequential Agent with all 8 agents
        sequential_agent = SequentialAgent(
            agent1=agent1,   # Information Consolidator
            agent2=agent2,   # Simple Photo Analysis
            agent3=agent3,   # Qloo Cultural Intelligence
            agent4a=agent4a, # Music Curation
            agent4b=agent4b, # Recipe Selection
            agent4c=agent4c, # Photo Description
            agent5=agent5,   # Nostalgia News Generator
            agent6=agent6    # Dashboard Synthesizer
        )
        logger.info("✅ Sequential agent initialized with 6-agent pipeline")
        
        # Log agent status
        agent_status = sequential_agent.get_agent_status()
        logger.info(f"🤖 Pipeline Status: {agent_status['total_agents_available']}/8 agents ready")
        logger.info(f"🌟 Star Feature: {agent_status['star_feature']}")
        logger.info(f"📰 Ready for Nostalgia News generation!")
        
        logger.info("🎉 Enhanced CareConnect API startup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Enhanced CareConnect API with Nostalgia News",
        "version": "2.0.0",
        "star_feature": "Nostalgia News Generator",
        "pipeline": "6-agent cultural storytelling",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    agent_status = sequential_agent.get_agent_status() if sequential_agent else {}
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "pipeline_ready": agent_status.get("ready_for_execution", False),
        "star_feature_ready": agent_status.get("star_feature") == "nostalgia_news_generator",
        "agents_available": agent_status.get("total_agents_available", 0),
        "tools_available": {
            "qloo_insights": tools.get("qloo_tool") is not None if tools else False,
            "youtube_api": tools.get("youtube_tool") is not None if tools else False,
            "gemini_ai": tools.get("gemini_tool") is not None if tools else False,
            "google_vision": tools.get("vision_ai_tool") is not None if tools else False
        }
    }

@app.post("/dashboard")
async def generate_dashboard(request_data: Dict[str, Any]):
    """
    Generate personalized dashboard with Nostalgia News
    
    Main endpoint that runs the complete 6-agent pipeline to create
    a personalized dashboard including the star Nostalgia News feature.
    """
    
    try:
        logger.info("📋 Dashboard generation request received")
        
        if not sequential_agent:
            raise HTTPException(status_code=503, detail="Sequential agent not initialized")
        
        # Extract patient profile from request
        patient_profile = request_data.get("patient_profile", {})
        session_id = request_data.get("session_id", "default")
        feedback_data = request_data.get("feedback_data")
        
        # Validate required fields
        if not patient_profile:
            raise HTTPException(status_code=400, detail="Patient profile is required")
        
        logger.info(f"👤 Generating dashboard for: {patient_profile.get('first_name', 'Unknown')}")
        
        # Run the complete 6-agent pipeline
        result = await sequential_agent.run(
            patient_profile=patient_profile,
            request_type="dashboard",
            session_id=session_id,
            feedback_data=feedback_data
        )
        
        if result.get("success"):
            logger.info("✅ Dashboard generated successfully with Nostalgia News!")
            return JSONResponse(content=result)
        else:
            logger.error(f"❌ Pipeline failed: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Pipeline execution failed"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Dashboard generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/demo/patients")
async def get_demo_patients():
    """Get list of demo patients"""
    
    if not demo_manager:
        raise HTTPException(status_code=503, detail="Demo manager not initialized")
    
    patients = demo_manager.get_all_patients()
    return {"patients": patients}

@app.get("/demo/patients/{patient_id}")
async def get_demo_patient(patient_id: str):
    """Get specific demo patient"""
    
    if not demo_manager:
        raise HTTPException(status_code=503, detail="Demo manager not initialized")
    
    patient = demo_manager.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient

@app.get("/api/status")
async def api_status():
    """Get detailed API status including agent and tool status"""
    
    agent_status = sequential_agent.get_agent_status() if sequential_agent else {}
    config_status = Config.get_status()
    
    return {
        "api_version": "2.0.0",
        "status": "ready" if sequential_agent else "initializing",
        "timestamp": datetime.now().isoformat(),
        "pipeline": agent_status,
        "configuration": config_status,
        "tools": {
            name: tool is not None for name, tool in (tools.items() if tools else {})
        },
        "star_feature": {
            "name": "Nostalgia News Generator",
            "status": "ready" if agent_status.get("star_feature") == "nostalgia_news_generator" else "not_ready",
            "description": "Personalized cultural storytelling with Gemini AI"
        }
    }

if __name__ == "__main__":
    # Use Config class methods for server configuration
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )