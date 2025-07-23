"""
Fixed CareConnect Sequential Agent
File: backend/multi_tool_agent/sequential_agent.py

Orchestrates all 7 agents without inheriting from SequentialAgent
"""

import logging
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Import individual agents from agents subdirectory with error handling
# FIXED: Use relative imports (with .) instead of absolute imports (backend.)
try:
    from .agents.information_consolidator_agent import InformationConsolidatorAgent
    logger.info("✅ InformationConsolidatorAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import InformationConsolidatorAgent: {e}")
    InformationConsolidatorAgent = None

try:
    from .agents.cultural_profile_agent import CulturalProfileBuilderAgent
    logger.info("✅ CulturalProfileBuilderAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import CulturalProfileBuilderAgent: {e}")
    CulturalProfileBuilderAgent = None

try:
    from .agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
    logger.info("✅ QlooCulturalIntelligenceAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import QlooCulturalIntelligenceAgent: {e}")
    QlooCulturalIntelligenceAgent = None

try:
    from .agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
    logger.info("✅ SensoryContentGeneratorAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import SensoryContentGeneratorAgent: {e}")
    SensoryContentGeneratorAgent = None

try:
    from .agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
    logger.info("✅ PhotoCulturalAnalyzerAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import PhotoCulturalAnalyzerAgent: {e}")
    PhotoCulturalAnalyzerAgent = None

try:
    from .agents.mobile_synthesizer_agent import MobileSynthesizerAgent
    logger.info("✅ MobileSynthesizerAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import MobileSynthesizerAgent: {e}")
    MobileSynthesizerAgent = None

try:
    from .agents.feedback_learning_agent import FeedbackLearningSystemAgent
    logger.info("✅ FeedbackLearningSystemAgent imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import FeedbackLearningSystemAgent: {e}")
    FeedbackLearningSystemAgent = None

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
        """
        
        self.name = "careconnect_pipeline"
        self.description = "Complete CareConnect dementia care cultural intelligence pipeline"
        
        # Validate tools input
        if not isinstance(tools, dict):
            raise TypeError(f"Expected tools to be dict, got {type(tools)}")
        
        # Store tools dictionary
        self.tools = tools
        
        # Extract tools with safe access
        qloo_tool = tools.get("qloo_tool")
        youtube_tool = tools.get("youtube_tool")
        gemini_tool = tools.get("gemini_tool")
        vision_ai_tool = tools.get("vision_ai_tool")
        session_storage_tool = tools.get("session_storage_tool")
        
        # Initialize all agents with error handling
        self.agent1 = None
        self.agent2 = None
        self.agent3 = None
        self.agent4 = None
        self.agent5 = None
        self.agent6 = None
        self.agent7 = None
        
        # Agent 1: Information Consolidator (no tools required)
        if InformationConsolidatorAgent:
            try:
                self.agent1 = InformationConsolidatorAgent()
                logger.info("✅ Agent 1 (Information Consolidator) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 1: {e}")
        
        # Agent 2: Cultural Profile Builder (no tools required)
        if CulturalProfileBuilderAgent:
            try:
                self.agent2 = CulturalProfileBuilderAgent()
                logger.info("✅ Agent 2 (Cultural Profile Builder) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 2: {e}")
        
        # Agent 3: Qloo Cultural Intelligence (requires qloo_tool)
        if QlooCulturalIntelligenceAgent and qloo_tool:
            try:
                self.agent3 = QlooCulturalIntelligenceAgent(qloo_tool)
                logger.info("✅ Agent 3 (Qloo Cultural Intelligence) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 3: {e}")
        elif not qloo_tool:
            logger.warning("⚠️  Agent 3 disabled: qloo_tool not available")
        
        # Agent 4: Sensory Content Generator (requires youtube_tool and gemini_tool)
        if SensoryContentGeneratorAgent and youtube_tool and gemini_tool:
            try:
                self.agent4 = SensoryContentGeneratorAgent(gemini_tool, youtube_tool)
                logger.info("✅ Agent 4 (Sensory Content Generator) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 4: {e}")
        else:
            missing_tools = []
            if not youtube_tool:
                missing_tools.append("youtube_tool")
            if not gemini_tool:
                missing_tools.append("gemini_tool")
            if missing_tools:
                logger.warning(f"⚠️  Agent 4 disabled: {', '.join(missing_tools)} not available")
        
        # Agent 5: Photo Cultural Analyzer (requires vision_ai_tool)
        if PhotoCulturalAnalyzerAgent and vision_ai_tool:
            try:
                self.agent5 = PhotoCulturalAnalyzerAgent(vision_ai_tool)
                logger.info("✅ Agent 5 (Photo Cultural Analyzer) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 5: {e}")
        elif not vision_ai_tool:
            logger.warning("⚠️  Agent 5 disabled: vision_ai_tool not available")
        
        # Agent 6: Mobile Synthesizer (no tools required)
        if MobileSynthesizerAgent:
            try:
                self.agent6 = MobileSynthesizerAgent()
                logger.info("✅ Agent 6 (Mobile Synthesizer) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 6: {e}")
        
        # Agent 7: Feedback Learning System (requires session_storage_tool)
        if FeedbackLearningSystemAgent and session_storage_tool:
            try:
                self.agent7 = FeedbackLearningSystemAgent(session_storage_tool)
                logger.info("✅ Agent 7 (Feedback Learning System) initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Agent 7: {e}")
        elif not session_storage_tool:
            logger.warning("⚠️  Agent 7 disabled: session_storage_tool not available")
        
        logger.info(f"CareConnect Agent initialized with {sum(1 for agent in [self.agent1, self.agent2, self.agent3, self.agent4, self.agent5, self.agent6, self.agent7] if agent)} out of 7 agents")

    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete CareConnect pipeline with all 7 agents.
        """
        try:
            logger.info(f"Starting CareConnect pipeline for {request_type} request")
            
            # Initialize pipeline metadata
            pipeline_metadata = {
                "pipeline_start": "2025-01-23T00:00:00Z",
                "agents_executed": 0,
                "active_agents": [],
                "request_type": request_type,
                "session_id": session_id
            }
            
            # Initialize default outputs
            consolidated_info = {}
            cultural_profile = {}
            qloo_intelligence = {}
            sensory_content = {}
            photo_analysis = {}
            mobile_experience = {}
            updated_preferences = {}
            
            # AGENT 1: Information Consolidator
            if self.agent1:
                try:
                    logger.info("Executing Agent 1: Information Consolidator")
                    agent1_result = await self.agent1.run(
                        patient_profile=patient_profile,
                        request_type=request_type,
                        session_id=session_id,
                        feedback_data=feedback_data,
                        photo_data=photo_data
                    )
                    consolidated_info = agent1_result.get("consolidated_info", {})
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("information_consolidator")
                    logger.info("✅ Agent 1 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 1 failed: {e}")
                    consolidated_info = {"error": str(e), "request_type": request_type, "status": "basic_consolidation"}
            else:
                logger.warning("⚠️  Agent 1 not available - using basic consolidation")
                consolidated_info = {"request_type": request_type, "status": "basic_consolidation"}
            
            # AGENT 2: Cultural Profile Builder
            if self.agent2:
                try:
                    logger.info("Executing Agent 2: Cultural Profile Builder")
                    agent2_result = await self.agent2.run(
                        consolidated_info=consolidated_info
                    )
                    cultural_profile = agent2_result.get("cultural_profile", {})
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("cultural_profile_builder")
                    logger.info("✅ Agent 2 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 2 failed: {e}")
                    cultural_profile = {"error": str(e), "status": "fallback_profile"}
            else:
                logger.warning("⚠️  Agent 2 not available - using basic cultural profile")
                cultural_profile = {
                    "heritage": patient_profile.get("cultural_heritage"),
                    "languages": patient_profile.get("languages"),
                    "status": "basic_profile"
                }
            
            # AGENT 3: Qloo Cultural Intelligence
            if self.agent3:
                try:
                    logger.info("Executing Agent 3: Qloo Cultural Intelligence")
                    agent3_result = await self.agent3.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile
                    )
                    qloo_intelligence = agent3_result.get("qloo_intelligence", {})
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("qloo_cultural_intelligence")
                    logger.info("✅ Agent 3 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 3 failed: {e}")
                    qloo_intelligence = {"error": str(e), "status": "fallback_recommendations"}
            else:
                logger.warning("⚠️  Agent 3 not available - cultural intelligence disabled")
                qloo_intelligence = {"status": "disabled", "reason": "agent_unavailable"}
            
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
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("sensory_content_generator")
                    logger.info("✅ Agent 4 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 4 failed: {e}")
                    sensory_content = {"error": str(e), "status": "fallback_content"}
            else:
                logger.warning("⚠️  Agent 4 not available - sensory content disabled")
                sensory_content = {"status": "disabled", "reason": "agent_unavailable"}
            
            # AGENT 5: Photo Cultural Analyzer (only if photo provided)
            if self.agent5 and photo_data:
                try:
                    logger.info("Executing Agent 5: Photo Cultural Analyzer")
                    agent5_result = await self.agent5.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        photo_data=photo_data
                    )
                    photo_analysis = agent5_result.get("photo_analysis", {})
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("photo_cultural_analyzer")
                    logger.info("✅ Agent 5 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 5 failed: {e}")
                    photo_analysis = {"error": str(e), "status": "fallback_analysis"}
            else:
                reason = "no_photo_provided" if not photo_data else "agent_unavailable"
                logger.info(f"⚠️  Agent 5 skipped: {reason}")
                photo_analysis = {"status": "skipped", "reason": reason}
            
            # AGENT 6: Mobile Synthesizer
            if self.agent6:
                try:
                    logger.info("Executing Agent 6: Mobile Synthesizer")
                    agent6_result = await self.agent6.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_analysis=photo_analysis
                    )
                    mobile_experience = agent6_result.get("mobile_experience", {})
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("mobile_synthesizer")
                    logger.info("✅ Agent 6 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 6 failed: {e}")
                    mobile_experience = {"error": str(e), "status": "fallback_experience"}
            else:
                logger.warning("⚠️  Agent 6 not available - mobile synthesis disabled")
                mobile_experience = {"status": "disabled", "reason": "agent_unavailable"}
            
            # AGENT 7: Feedback Learning System (only if feedback data provided)
            if self.agent7 and feedback_data:
                try:
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
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("feedback_learning_system")
                    logger.info("✅ Agent 7 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 7 failed: {e}")
                    updated_preferences = {"error": str(e), "status": "fallback_preferences"}
            else:
                reason = "no_feedback_provided" if not feedback_data else "agent_unavailable"
                logger.info(f"⚠️  Agent 7 skipped: {reason}")
                updated_preferences = {"status": "skipped", "reason": reason}
            
            # Final pipeline results
            pipeline_metadata["pipeline_end"] = "2025-01-23T00:00:00Z"
            pipeline_metadata["total_agents_available"] = sum(1 for agent in [self.agent1, self.agent2, self.agent3, self.agent4, self.agent5, self.agent6, self.agent7] if agent)
            
            logger.info(f"🎯 CareConnect Pipeline completed: {pipeline_metadata['agents_executed']} agents executed")
            
            return {
                "pipeline_result": "success",
                "consolidated_info": consolidated_info,
                "cultural_profile": cultural_profile,
                "qloo_intelligence": qloo_intelligence,
                "sensory_content": sensory_content,
                "photo_analysis": photo_analysis,
                "mobile_experience": mobile_experience,
                "updated_preferences": updated_preferences,
                "pipeline_metadata": pipeline_metadata
            }
            
        except Exception as e:
            logger.error(f"❌ CareConnect pipeline failed: {e}")
            return {
                "pipeline_result": "error",
                "error": str(e),
                "pipeline_metadata": pipeline_metadata
            }