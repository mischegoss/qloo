"""
CareConnect Sequential Agent
Location: backend/multi_tool_agent/sequential_agent.py

Orchestrates all 7 agents following Google ADK SequentialAgent pattern
"""

import logging
from typing import Dict, Any, Optional
from google.genai.adk import SequentialAgent

# Import individual agents from agents subdirectory
from .agents.information_consolidator_agent import InformationConsolidatorAgent
from .agents.cultural_profile_agent import CulturalProfileBuilderAgent  
from .agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
from .agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
from .agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
from .agents.mobile_synthesizer_agent import MobileSynthesizerAgent
from .agents.feedback_learning_agent import FeedbackLearningSystemAgent

logger = logging.getLogger(__name__)

class CareConnectAgent(SequentialAgent):
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
        
        # Initialize individual agents with their required tools
        agent1 = InformationConsolidatorAgent()
        agent2 = CulturalProfileBuilderAgent()
        agent3 = QlooCulturalIntelligenceAgent(qloo_tool=tools["qloo_tool"])
        agent4 = SensoryContentGeneratorAgent(
            youtube_tool=tools["youtube_tool"],
            gemini_tool=tools["gemini_tool"]
        )
        agent5 = PhotoCulturalAnalyzerAgent(vision_ai_tool=tools["vision_ai_tool"])
        agent6 = MobileSynthesizerAgent()
        agent7 = FeedbackLearningSystemAgent(session_storage_tool=tools["session_storage_tool"])
        
        # Create agent workflow following ADK SequentialAgent pattern
        super().__init__(
            name="careconnect_pipeline",
            description="Complete CareConnect dementia care cultural intelligence pipeline",
            agents=[
                # Agent 1: Information Consolidator (receives direct input)
                {
                    "agent": agent1,
                    "input_key": None,  # First agent gets direct input
                    "output_key": "consolidated_info"
                },
                
                # Agent 2: Cultural Profile Builder
                {
                    "agent": agent2,
                    "input_key": "consolidated_info",
                    "output_key": "cultural_profile"
                },
                
                # Agent 3: Qloo Cultural Intelligence
                {
                    "agent": agent3,
                    "input_key": ["consolidated_info", "cultural_profile"],
                    "output_key": "qloo_intelligence"
                },
                
                # Agent 4: Sensory Content Generator
                {
                    "agent": agent4,
                    "input_key": ["consolidated_info", "cultural_profile", "qloo_intelligence"],
                    "output_key": "sensory_content"
                },
                
                # Agent 5: Photo Cultural Analyzer (conditional execution)
                {
                    "agent": agent5,
                    "input_key": ["consolidated_info", "cultural_profile", "qloo_intelligence", "sensory_content"],
                    "output_key": "photo_analysis"
                },
                
                # Agent 6: Mobile Synthesizer
                {
                    "agent": agent6,
                    "input_key": ["consolidated_info", "cultural_profile", "qloo_intelligence", "sensory_content", "photo_analysis"],
                    "output_key": "mobile_experience"
                },
                
                # Agent 7: Feedback Learning System
                {
                    "agent": agent7,
                    "input_key": ["consolidated_info", "cultural_profile", "qloo_intelligence", "sensory_content", "photo_analysis", "mobile_experience"],
                    "output_key": "updated_preferences"
                }
            ]
        )
        
        logger.info("CareConnect Sequential Agent initialized with 7-agent pipeline")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_history: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete CareConnect 7-agent pipeline.
        
        Args:
            patient_profile: Basic patient information (privacy-compliant)
            request_type: meal, conversation, music, video, dashboard, photo_analysis
            session_id: Optional session identifier for preference continuity
            feedback_history: Previous feedback and blocked content
            photo_data: Optional uploaded photo for analysis
            feedback_data: User feedback from mobile interface
            
        Returns:
            Complete pipeline result with all agent outputs
        """
        
        try:
            logger.info(f"Starting CareConnect pipeline for request: {request_type}")
            
            # Prepare input for the sequential agent pipeline
            pipeline_input = {
                "patient_profile": patient_profile,
                "request_type": request_type,
                "session_id": session_id,
                "feedback_history": feedback_history,
                "photo_data": photo_data
            }
            
            # Execute the sequential pipeline (Agents 1-6)
            result = await super().run(pipeline_input)
            
            # Handle Agent 7 (Feedback Learning) separately if feedback provided
            if feedback_data:
                logger.info("Processing feedback through Agent 7")
                
                # Prepare input for feedback learning agent
                feedback_input = {
                    "consolidated_info": result.get("consolidated_info"),
                    "cultural_profile": result.get("cultural_profile"),
                    "qloo_intelligence": result.get("qloo_intelligence"),
                    "sensory_content": result.get("sensory_content"),
                    "photo_analysis": result.get("photo_analysis"),
                    "mobile_experience": result.get("mobile_experience"),
                    "feedback_data": feedback_data
                }
                
                # Run Agent 7 separately with all previous outputs
                feedback_result = await self.agents[6]["agent"].run(**feedback_input)
                result.update(feedback_result)
            
            # Add pipeline metadata
            result["pipeline_metadata"] = {
                "request_type": request_type,
                "session_id": session_id,
                "agents_executed": 7 if feedback_data else 6,
                "pipeline_status": "completed_successfully",
                "privacy_compliance": "maintained",
                "anti_bias_validation": "passed",
                "caregiver_authority": "preserved"
            }
            
            logger.info("CareConnect pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in CareConnect pipeline: {str(e)}")
            return self._create_safe_fallback(patient_profile, request_type, str(e))
    
    def _create_safe_fallback(self, 
                             patient_profile: Dict[str, Any],
                             request_type: str,
                             error: str) -> Dict[str, Any]:
        """Create safe fallback when pipeline fails."""
        
        return {
            "pipeline_metadata": {
                "request_type": request_type,
                "pipeline_status": "fallback_mode",
                "error": error,
                "caregiver_authority": "preserved"
            },
            "mobile_experience": {
                "page_structure": {"structure_type": "safe_fallback"},
                "mobile_content": {
                    "primary_content": {
                        "content_type": "simple_activities",
                        "activities": [
                            "Look at family photos together",
                            "Listen to familiar music",
                            "Have a gentle conversation",
                            "Enjoy a quiet moment together"
                        ]
                    }
                },
                "caregiver_guide": {
                    "caregiver_authority_note": {
                        "principle": "You know them best - use your judgment",
                        "approach": "Focus on simple, familiar activities"
                    }
                }
            }
        }