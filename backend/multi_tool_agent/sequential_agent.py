"""
Clean CareConnectAgent - No SequentialAgentCoordinator references
File: backend/multi_tool_agent/sequential_agent.py
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Import agents safely
try:
    from .agents.information_consolidator_agent import InformationConsolidatorAgent
except ImportError as e:
    logger.error(f"❌ Failed to import InformationConsolidatorAgent: {e}")
    InformationConsolidatorAgent = None

try:
    from .agents.cultural_profile_agent import CulturalProfileBuilderAgent
except ImportError as e:
    logger.error(f"❌ Failed to import CulturalProfileBuilderAgent: {e}")
    CulturalProfileBuilderAgent = None

try:
    from .agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
except ImportError as e:
    logger.error(f"❌ Failed to import QlooCulturalIntelligenceAgent: {e}")
    QlooCulturalIntelligenceAgent = None

try:
    from .agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
except ImportError as e:
    logger.error(f"❌ Failed to import SensoryContentGeneratorAgent: {e}")
    SensoryContentGeneratorAgent = None

try:
    from .agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
except ImportError as e:
    logger.error(f"❌ Failed to import PhotoCulturalAnalyzerAgent: {e}")
    PhotoCulturalAnalyzerAgent = None

try:
    from .agents.mobile_synthesizer_agent import MobileSynthesizerAgent
except ImportError as e:
    logger.error(f"❌ Failed to import MobileSynthesizerAgent: {e}")
    MobileSynthesizerAgent = None

try:
    from .agents.feedback_learning_system_agent import FeedbackLearningSystemAgent
except ImportError as e:
    logger.error(f"❌ Failed to import FeedbackLearningSystemAgent: {e}")
    FeedbackLearningSystemAgent = None

class CareConnectAgent:
    """CareConnect Agent - Clean implementation without SequentialAgentCoordinator"""
    
    def __init__(self, tools: Dict[str, Any]):
        self.name = "careconnect_pipeline"
        self.description = "Complete CareConnect dementia care cultural intelligence pipeline"
        self.tools = tools
        
        # Extract tools
        qloo_tool = tools.get("qloo_tool")
        youtube_tool = tools.get("youtube_tool")
        gemini_tool = tools.get("gemini_tool")
        vision_ai_tool = tools.get("vision_ai_tool")
        session_storage_tool = tools.get("session_storage_tool")
        
        # Initialize agents
        self.agent1 = InformationConsolidatorAgent() if InformationConsolidatorAgent else None
        self.agent2 = CulturalProfileBuilderAgent() if CulturalProfileBuilderAgent else None
        self.agent3 = QlooCulturalIntelligenceAgent(qloo_tool) if QlooCulturalIntelligenceAgent and qloo_tool else None
        self.agent4 = SensoryContentGeneratorAgent(gemini_tool, youtube_tool) if SensoryContentGeneratorAgent and youtube_tool and gemini_tool else None
        self.agent5 = PhotoCulturalAnalyzerAgent(vision_ai_tool) if PhotoCulturalAnalyzerAgent and vision_ai_tool else None
        self.agent6 = MobileSynthesizerAgent() if MobileSynthesizerAgent else None
        self.agent7 = FeedbackLearningSystemAgent(session_storage_tool) if FeedbackLearningSystemAgent and session_storage_tool else None
        
        active_agents = sum(1 for agent in [self.agent1, self.agent2, self.agent3, self.agent4, self.agent5, self.agent6, self.agent7] if agent)
        logger.info(f"CareConnect Sequential Agent initialized with {active_agents}/7 agents active")
    
    async def run(self, 
                 patient_profile: Dict[str, Any],
                 request_type: str = "dashboard",
                 session_id: Optional[str] = None,
                 feedback_data: Optional[Dict[str, Any]] = None,
                 photo_of_the_day: Optional[str] = None,
                 photo_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the complete CareConnect pipeline"""
        
        logger.info(f"🚀 CareConnect Agent executing {request_type} request")
        
        try:
            # Initialize outputs
            consolidated_info = {}
            cultural_profile = {}
            qloo_intelligence = {}
            sensory_content = {}
            photo_analysis_result = {}
            mobile_experience = {}
            updated_preferences = {}
            
            # AGENT 1: Information Consolidator
            if self.agent1:
                try:
                    logger.info("Executing Agent 1: Information Consolidator")
                    
                    # FIXED: Prepare photo_data for Agent 1 (it expects photo_data, not photo_of_the_day)
                    photo_data = None
                    if photo_of_the_day and photo_analysis:
                        photo_data = {
                            "photo_url": photo_of_the_day,
                            "analysis": photo_analysis,
                            "type": "family_photo",
                            "timestamp": datetime.now().isoformat()
                        }
                    
                    agent1_result = await self.agent1.run(
                        patient_profile=patient_profile,
                        request_type=request_type,
                        session_id=session_id,
                        feedback_data=feedback_data,
                        photo_data=photo_data  # FIXED: Use photo_data instead of photo_of_the_day
                    )
                    consolidated_info = agent1_result.get("consolidated_info", {})
                    logger.info("✅ Agent 1 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 1 failed: {e}")
                    consolidated_info = {"error": str(e), "request_type": request_type}
            
            # AGENT 2: Cultural Profile Builder
            if self.agent2:
                try:
                    logger.info("Executing Agent 2: Cultural Profile Builder")
                    agent2_result = await self.agent2.run(consolidated_info=consolidated_info)
                    cultural_profile = agent2_result.get("cultural_profile", {})
                    logger.info("✅ Agent 2 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 2 failed: {e}")
                    cultural_profile = {"error": str(e)}
            
            # AGENT 3: Qloo Cultural Intelligence
            if self.agent3:
                try:
                    logger.info("Executing Agent 3: Qloo Cultural Intelligence")
                    agent3_result = await self.agent3.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile
                    )
                    qloo_intelligence = agent3_result.get("qloo_intelligence", {})
                    logger.info("✅ Agent 3 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 3 failed: {e}")
                    qloo_intelligence = {"error": str(e)}
            
            # AGENT 4: Sensory Content Generator
            if self.agent4:
                try:
                    logger.info("Executing Agent 4: Sensory Content Generator")
                    agent4_result = await self.agent4.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence
                    )
                    sensory_content = agent4_result.get("sensory_content", {})
                    logger.info("✅ Agent 4 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 4 failed: {e}")
                    sensory_content = {"error": str(e)}
            
            # AGENT 5: Photo Cultural Analyzer
            if self.agent5 and photo_of_the_day and photo_analysis:
                try:
                    logger.info(f"Executing Agent 5: Photo Cultural Analyzer with photo: {photo_of_the_day}")
                    agent5_result = await self.agent5.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_of_the_day=photo_of_the_day,
                        stored_photo_analysis=photo_analysis
                    )
                    photo_analysis_result = agent5_result.get("photo_analysis", {})
                    logger.info("✅ Agent 5 completed successfully with photo")
                except Exception as e:
                    logger.error(f"❌ Agent 5 failed: {e}")
                    photo_analysis_result = {"error": str(e)}
            else:
                logger.info("⚠️  Agent 5 skipped: no photo available")
                photo_analysis_result = {"status": "skipped"}
            
            # AGENT 6: Mobile Synthesizer
            if self.agent6:
                try:
                    logger.info("Executing Agent 6: Mobile Synthesizer")
                    agent6_result = await self.agent6.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_analysis=photo_analysis_result
                    )
                    mobile_experience = agent6_result.get("mobile_experience", {})
                    logger.info("✅ Agent 6 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 6 failed: {e}")
                    mobile_experience = {"error": str(e)}
            
            # AGENT 7: Feedback Learning System
            if self.agent7 and feedback_data:
                try:
                    logger.info("Executing Agent 7: Feedback Learning System")
                    agent7_result = await self.agent7.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_analysis=photo_analysis_result,
                        mobile_experience=mobile_experience,
                        feedback_data=feedback_data
                    )
                    updated_preferences = agent7_result.get("updated_preferences", {})
                    logger.info("✅ Agent 7 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 7 failed: {e}")
                    updated_preferences = {"error": str(e)}
            else:
                logger.info("⚠️  Agent 7 skipped: no feedback data")
                updated_preferences = {"status": "skipped"}
            
            logger.info("🎯 CareConnect Pipeline completed successfully")
            
            return {
                "pipeline_result": "success",
                "consolidated_info": consolidated_info,
                "cultural_profile": cultural_profile,
                "qloo_intelligence": qloo_intelligence,
                "sensory_content": sensory_content,
                "photo_analysis": photo_analysis_result,
                "mobile_experience": mobile_experience,
                "updated_preferences": updated_preferences
            }
            
        except Exception as e:
            logger.error(f"❌ CareConnect pipeline failed: {e}")
            return {
                "pipeline_result": "error",
                "error": str(e)
            }