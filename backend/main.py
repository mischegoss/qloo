"""
Updated main.py - 6 Agent Pipeline with Nostalgia News Integration
File: backend/main.py

UPDATED: Integrates the new 6-agent pipeline with Nostalgia News Generator
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

# Import configuration and managers
from config.settings import config
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

# Import tools
from multi_tool_agent.tools import initialize_all_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
app = FastAPI(
    title="Enhanced CareConnect API with Nostalgia News",
    description="Personalized dementia care dashboard with cultural storytelling",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
tools = None
sequential_agent = None
patient_manager = None

@app.on_event("startup")
async def startup():
    """Initialize the application with 6-agent pipeline"""
    global tools, sequential_agent, patient_manager
    
    try:
        logger.info("🚀 Starting Enhanced CareConnect API with Nostalgia News...")
        
        # Initialize patient manager
        patient_manager = DemoPatientManager()
        logger.info("✅ Patient manager initialized")
        
        # Initialize all tools
        tools = initialize_all_tools()
        logger.info("✅ Tools initialized successfully")
        logger.info(f"📊 Available tools: {list(tools.keys())}")
        
        # Initialize all 8 agents for the 6-agent pipeline
        logger.info("🤖 Initializing 6-agent pipeline...")
        
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
    
    logger.info("📱 Dashboard generation request received")
    
    try:
        # Validate request
        if not sequential_agent:
            raise HTTPException(status_code=503, detail="Sequential agent not initialized")
        
        if not patient_manager:
            raise HTTPException(status_code=503, detail="Patient manager not initialized")
        
        # Extract request parameters
        patient_id = request_data.get("patient_id", "demo_patient")
        request_type = request_data.get("request_type", "dashboard")
        session_id = request_data.get("session_id", f"session_{int(datetime.now().timestamp())}")
        feedback_data = request_data.get("feedback_data")
        
        logger.info(f"📋 Processing request: patient={patient_id}, type={request_type}, session={session_id}")
        
        # Get patient profile
        patient_profile = patient_manager.get_patient_profile(patient_id)
        if not patient_profile:
            raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
        
        logger.info(f"👤 Patient: {patient_profile.get('first_name')} ({patient_profile.get('cultural_heritage')})")
        
        # Run the complete 6-agent pipeline
        logger.info("🚀 Starting 6-agent pipeline with Nostalgia News...")
        
        dashboard_result = await sequential_agent.run(
            patient_profile=patient_profile,
            request_type=request_type,
            session_id=session_id,
            feedback_data=feedback_data
        )
        
        # Check for success
        if not dashboard_result.get("success", True):
            logger.error(f"❌ Pipeline failed: {dashboard_result.get('error')}")
            raise HTTPException(status_code=500, detail=dashboard_result.get("error", "Pipeline execution failed"))
        
        # Log success
        logger.info("✅ Dashboard generated successfully!")
        
        # Log Nostalgia News status
        nostalgia_news = dashboard_result.get("nostalgia_news", {})
        if nostalgia_news.get("title"):
            logger.info(f"📰 Nostalgia News: {nostalgia_news['title']}")
            logger.info("🌟 Star feature successfully generated!")
        
        # Update patient feedback (background task)
        if feedback_data:
            patient_manager.update_patient_feedback(patient_id, feedback_data)
            logger.info("💡 Patient feedback updated")
        
        return dashboard_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Dashboard generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"Dashboard generation failed: {str(e)}"
        )

@app.get("/patient/{patient_id}")
async def get_patient_profile(patient_id: str):
    """Get patient profile information"""
    
    if not patient_manager:
        raise HTTPException(status_code=503, detail="Patient manager not initialized")
    
    patient_profile = patient_manager.get_patient_profile(patient_id)
    if not patient_profile:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    
    return patient_profile

@app.post("/patient/{patient_id}/feedback")
async def update_patient_feedback(patient_id: str, feedback_data: Dict[str, Any]):
    """Update patient feedback"""
    
    if not patient_manager:
        raise HTTPException(status_code=503, detail="Patient manager not initialized")
    
    try:
        result = patient_manager.update_patient_feedback(patient_id, feedback_data)
        return {"success": True, "feedback_summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_system_status():
    """Get detailed system status"""
    
    agent_status = sequential_agent.get_agent_status() if sequential_agent else {}
    
    return {
        "system_status": "operational",
        "pipeline_version": "6_agent_nostalgia_news",
        "star_feature": "Nostalgia News Generator",
        "timestamp": datetime.now().isoformat(),
        "pipeline": agent_status,
        "tools_available": {
            "qloo_insights": tools.get("qloo_tool") is not None if tools else False,
            "youtube_api": tools.get("youtube_tool") is not None if tools else False,
            "gemini_ai": tools.get("gemini_tool") is not None if tools else False,
            "google_vision": tools.get("vision_ai_tool") is not None if tools else False
        },
        "patient_manager_ready": patient_manager is not None,
        "total_agents_available": agent_status.get("total_agents_available", 0),
        "ready_for_production": agent_status.get("ready_for_execution", False)
    }

def get_learning_insight(feedback_points: int) -> str:
    """Generate learning insight based on feedback points"""
    
    if feedback_points == 0:
        return "I'm just getting to know Maria's preferences."
    elif feedback_points < 3:
        return "I'm starting to learn what Maria enjoys most."
    elif feedback_points < 7:
        return "I'm getting better at personalizing content for Maria."
    else:
        return "I know Maria's preferences well and am tailoring content accordingly."

if __name__ == "__main__":
    # Run the server
    logger.info(f"🚀 Starting Enhanced CareConnect API with Nostalgia News on port {config.PORT}")
    logger.info(f"📁 Data directory: {patient_manager.data_dir if patient_manager else 'Not initialized'}")
    logger.info("🌟 STAR FEATURE: Nostalgia News Generator with Gemini AI")
    logger.info("📰 Personalized cultural storytelling for dementia care")
    logger.info("🎯 6-agent pipeline: Info → Photo → Qloo → Content → Nostalgia News → Dashboard")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    )