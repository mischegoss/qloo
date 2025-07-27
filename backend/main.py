"""
Updated main.py - FIXED: Theme Manager Import Issue
File: backend/main.py

CRITICAL FIXES:
- Added SimplifiedThemeManager import and initialization
- Fixed theme manager being passed to Agent 1 properly
- Ensured all agents get proper dependencies
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

# CRITICAL FIX: Import the theme manager
from config.theme_config import simplified_theme_manager

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
        logger.info("✅ Demo Patient Manager initialized")
        logger.info(f"📊 Loaded {len(demo_manager.get_all_patients())} demo patients")
        
        # Initialize tools with safe fallbacks
        logger.info("🛠️ Initializing tools...")
        tools = initialize_all_tools()
        
        # Log tool status
        available_tools = [name for name, tool in tools.items() if tool is not None]
        logger.info(f"🛠️ Available tools: {', '.join(available_tools)}")
        
        # CRITICAL FIX: Initialize agents with proper dependencies
        logger.info("🤖 Initializing agents...")
        
        # Agent 1: Information Consolidator with theme manager
        agent1 = InformationConsolidatorAgent(theme_manager=simplified_theme_manager)
        logger.info("✅ Agent 1 (Information Consolidator) initialized")
        
        # Agent 2: Simple Photo Analysis
        agent2 = SimplePhotoAnalysisAgent(vision_tool=tools.get("vision_ai_tool"))
        logger.info("✅ Agent 2 (Simple Photo Analysis) initialized")
        
        # Agent 3: Qloo Cultural Intelligence
        agent3 = QlooCulturalAnalysisAgent(qloo_tool=tools.get("qloo_tool"))
        logger.info("✅ Agent 3 (Qloo Cultural Intelligence) initialized")
        
        # Agent 4A: Music Curation
        agent4a = MusicCurationAgent(
            youtube_tool=tools.get("youtube_tool"),
            gemini_tool=tools.get("gemini_tool")
        )
        logger.info("✅ Agent 4A (Music Curation) initialized")
        
        # Agent 4B: Recipe Selection
        agent4b = RecipeSelectionAgent()
        logger.info("✅ Agent 4B (Recipe Selection) initialized")
        
        # Agent 4C: Photo Description
        agent4c = PhotoDescriptionAgent(gemini_tool=tools.get("gemini_tool"))
        logger.info("✅ Agent 4C (Photo Description) initialized")
        
        # Agent 5: Nostalgia News Generator
        agent5 = NostalgiaNewsGenerator(gemini_tool=tools.get("gemini_tool"))
        logger.info("✅ Agent 5 (Nostalgia News Generator) initialized - STAR FEATURE!")
        
        # Agent 6: Dashboard Synthesizer
        agent6 = DashboardSynthesizer()
        logger.info("✅ Agent 6 (Dashboard Synthesizer) initialized")
        
        # Initialize sequential agent with all components
        sequential_agent = SequentialAgent(
            agent1=agent1,
            agent2=agent2,
            agent3=agent3,
            agent4a=agent4a,
            agent4b=agent4b,
            agent4c=agent4c,
            agent5=agent5,
            agent6=agent6
        )
        
        logger.info("✅ Sequential agent initialized with 6-agent pipeline")
        logger.info("🤖 Pipeline Status: 6/6 agents ready")
        logger.info("🌟 Star Feature: nostalgia_news_generator")
        logger.info("📰 Ready for Nostalgia News generation!")
        
        logger.info("🎉 Enhanced CareConnect API startup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


@app.post("/api/dashboard")
async def generate_dashboard(request: Dict[str, Any]):
    """Generate personalized dashboard for patient"""
    
    if not sequential_agent:
        raise HTTPException(status_code=503, detail="Sequential agent not initialized")
    
    try:
        logger.info("📋 Dashboard generation request received")
        
        # Extract request data
        session_id = request.get("session_id", "default")
        feedback_data = request.get("feedback", {})
        
        # FIXED: Accept patient_profile directly from request OR fallback to demo lookup
        patient_profile = request.get("patient_profile")
        
        if not patient_profile:
            # Fallback: try to get from demo manager if patient_id provided
            patient_id = request.get("patient_id")
            if patient_id and demo_manager:
                patient_profile = demo_manager.get_patient(patient_id)
                if not patient_profile:
                    raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
            else:
                raise HTTPException(status_code=400, detail="Either 'patient_profile' or 'patient_id' must be provided")
        
        logger.info(f"👤 Generating dashboard for: {patient_profile.get('first_name', 'Unknown')}")
        
        # Run the sequential agent pipeline
        logger.info("🚀 Starting 6-agent pipeline with Nostalgia News")
        logger.info("📋 Pipeline: Info → Photo → Qloo → Content(4A/4B/4C) → Nostalgia News → Dashboard")
        
        result = await sequential_agent.run(
            patient_profile=patient_profile,
            request_type="dashboard",
            session_id=session_id,
            feedback_data=feedback_data
        )
        
        if result.get("success", True):
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