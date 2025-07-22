"""
CareConnect Sequential Agent - Simple Implementation
Location: backend/multi_tool_agent/sequential_agent.py

Orchestrates all 7 agents without inheriting from SequentialAgent
"""

import logging
from typing import Dict, Any, Optional

# Import individual agents from agents subdirectory
from .agents.information_consolidator_agent import InformationConsolidatorAgent
from .agents.cultural_profile_agent import CulturalProfileBuilderAgent  
from .agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
from .agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
from .agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
from .agents.mobile_synthesizer_agent import MobileSynthesizerAgent
from .agents.feedback_learning_agent import FeedbackLearningSystemAgent

logger = logging.getLogger(__name__)

class CareConnectAgent:
    """
    CareConnect Sequential Agent - Main Orchestrator
    
    Coordinates all 7 agents in the dementia care cultural intelligence pipeline:
    1. Information Consolidator → consolidated_info
    2. Cultural Profile Builder → cultural_profile  
    3. Qloo Cultural Intelligence → qloo_intelligence
    4. Sensory Content Generator → sensory_content
    5. Photo Cultural Analyzer → photo_analysis
    6. Mobile Synthesizer → mobile_experience
    7. Feedback Learning System → updated_preferences
    
    Follows Responsible Development Guide principles throughout.
    """
    
    def __init__(self, tools: Dict[str, Any]):
        """
        Initialize CareConnect Sequential Agent with required tools.
        
        Args:
            tools: Dictionary containing all required tools for agents
                - qloo_tool: Qloo API interface
                - youtube_tool: YouTube search interface  
                - gemini_tool: Gemini recipe generator
                - vision_ai_tool: Vision AI analyzer
                - session_storage_tool: Session storage manager
        """
        
        self.name = "careconnect_pipeline"
        self.description = "Complete CareConnect dementia care cultural intelligence pipeline"
        
        # Extract tools
        qloo_tool = tools["qloo_tool"]
        youtube_tool = tools["youtube_tool"]
        gemini_tool = tools["gemini_tool"]
        vision_ai_tool = tools["vision_ai_tool"]
        session_storage_tool = tools["session_storage_tool"]
        
        # Initialize all agents
        self.agent1 = InformationConsolidatorAgent()
        self.agent2 = CulturalProfileBuilderAgent()
        self.agent3 = QlooCulturalIntelligenceAgent(qloo_tool)
        self.agent4 = SensoryContentGeneratorAgent(youtube_tool, gemini_tool)
        self.agent5 = PhotoCulturalAnalyzerAgent(vision_ai_tool)
        self.agent6 = MobileSynthesizerAgent()
        self.agent7 = FeedbackLearningSystemAgent(session_storage_tool)
        
        logger.info("CareConnect Sequential Agent initialized with 7-agent pipeline")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_history: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete CareConnect 7-agent pipeline manually.
        
        Args:
            patient_profile: Patient information from caregiver
            request_type: Type of request (dashboard, meal, conversation, etc.)
            session_id: Session identifier
            feedback_history: Historical feedback data
            photo_data: Photo analysis data if provided
            feedback_data: Current feedback data if provided
            
        Returns:
            Complete pipeline results with mobile experience
        """
        
        try:
            logger.info(f"Starting CareConnect pipeline for {request_type} request")
            
            pipeline_metadata = {
                "pipeline_start": "2025-07-21T00:00:00Z",
                "agents_executed": 0,
                "pipeline_status": "running"
            }
            
            # AGENT 1: Information Consolidator
            logger.info("Executing Agent 1: Information Consolidator")
            agent1_result = await self.agent1.run(
                patient_profile=patient_profile,
                request_type=request_type,
                session_id=session_id,
                feedback_history=feedback_history,
                photo_data=photo_data
            )
            consolidated_info = agent1_result.get("consolidated_info", {})
            pipeline_metadata["agents_executed"] = 1
            
            # AGENT 2: Cultural Profile Builder  
            logger.info("Executing Agent 2: Cultural Profile Builder")
            agent2_result = await self.agent2.run(
                consolidated_info=consolidated_info
            )
            cultural_profile = agent2_result.get("cultural_profile", {})
            pipeline_metadata["agents_executed"] = 2
            
            # AGENT 3: Qloo Cultural Intelligence
            logger.info("Executing Agent 3: Qloo Cultural Intelligence")
            agent3_result = await self.agent3.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile
            )
            qloo_intelligence = agent3_result.get("qloo_intelligence", {})
            pipeline_metadata["agents_executed"] = 3
            
            # AGENT 4: Sensory Content Generator
            logger.info("Executing Agent 4: Sensory Content Generator")
            agent4_result = await self.agent4.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence
            )
            sensory_content = agent4_result.get("sensory_content", {})
            pipeline_metadata["agents_executed"] = 4
            
            # AGENT 5: Photo Cultural Analyzer (conditional)
            logger.info("Executing Agent 5: Photo Cultural Analyzer")
            agent5_result = await self.agent5.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence,
                sensory_content=sensory_content
            )
            photo_analysis = agent5_result.get("photo_analysis", {})
            pipeline_metadata["agents_executed"] = 5
            
            # AGENT 6: Mobile Synthesizer
            logger.info("Executing Agent 6: Mobile Synthesizer")
            agent6_result = await self.agent6.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence,
                sensory_content=sensory_content,
                photo_analysis=photo_analysis
            )
            mobile_experience = agent6_result.get("mobile_experience", {})
            pipeline_metadata["agents_executed"] = 6
            
            # AGENT 7: Feedback Learning System
            logger.info("Executing Agent 7: Feedback Learning System")
            agent7_result = await self.agent7.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence,
                sensory_content=sensory_content,
                photo_analysis=photo_analysis,
                mobile_experience=mobile_experience,
                feedback_data=feedback_data
            )
            updated_preferences = agent7_result.get("updated_preferences", {})
            pipeline_metadata["agents_executed"] = 7
            pipeline_metadata["pipeline_status"] = "completed"
            
            # Compile complete pipeline results
            complete_results = {
                "pipeline_metadata": pipeline_metadata,
                "consolidated_info": consolidated_info,
                "cultural_profile": cultural_profile,
                "qloo_intelligence": qloo_intelligence,
                "sensory_content": sensory_content,
                "photo_analysis": photo_analysis,
                "mobile_experience": mobile_experience,
                "updated_preferences": updated_preferences,
                "request_metadata": {
                    "patient_profile": patient_profile,
                    "request_type": request_type,
                    "session_id": session_id,
                    "pipeline_success": True
                }
            }
            
            logger.info("CareConnect pipeline completed successfully")
            return complete_results
            
        except Exception as e:
            logger.error(f"CareConnect pipeline error: {str(e)}")
            
            # Return partial results with error information
            error_results = {
                "pipeline_metadata": {
                    "pipeline_status": "error",
                    "agents_executed": pipeline_metadata.get("agents_executed", 0),
                    "error_message": str(e)
                },
                "request_metadata": {
                    "patient_profile": patient_profile,
                    "request_type": request_type,
                    "session_id": session_id,
                    "pipeline_success": False
                },
                "error_details": {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "fallback_mode": True
                }
            }
            
            # Add any partial results that were completed
            if pipeline_metadata.get("agents_executed", 0) >= 1:
                error_results["consolidated_info"] = locals().get("consolidated_info", {})
            if pipeline_metadata.get("agents_executed", 0) >= 2:
                error_results["cultural_profile"] = locals().get("cultural_profile", {})
            if pipeline_metadata.get("agents_executed", 0) >= 3:
                error_results["qloo_intelligence"] = locals().get("qloo_intelligence", {})
            if pipeline_metadata.get("agents_executed", 0) >= 4:
                error_results["sensory_content"] = locals().get("sensory_content", {})
            if pipeline_metadata.get("agents_executed", 0) >= 5:
                error_results["photo_analysis"] = locals().get("photo_analysis", {})
            if pipeline_metadata.get("agents_executed", 0) >= 6:
                error_results["mobile_experience"] = locals().get("mobile_experience", {})
            
            return error_results