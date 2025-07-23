"""
Sequential Agent Coordinator - UPDATED VERSION
File: backend/multi_tool_agent/sequential_agent.py

Updated to handle the simplified agent pipeline with proper data flow.
Ensures cultural mappings flow through the pipeline correctly.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Import all agents
from backend.multi_tool_agent.agents.information_consolidator_agent import InformationConsolidatorAgent
from backend.multi_tool_agent.agents.cultural_profile_agent import CulturalProfileBuilderAgent  
from backend.multi_tool_agent.agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
from backend.multi_tool_agent.agents.sensory_content_generator_agent import SensoryContentGeneratorAgent
from backend.multi_tool_agent.agents.photo_cultural_analyzer_agent import PhotoCulturalAnalyzerAgent
from backend.multi_tool_agent.agents.mobile_synthesizer_agent import MobileSynthesizerAgent
from backend.multi_tool_agent.agents.feedback_learning_agent import FeedbackLearningAgent

logger = logging.getLogger(__name__)

class SequentialAgentCoordinator:
    """
    Coordinates the execution of all 7 agents in the CareConnect pipeline.
    
    UPDATED FOR SIMPLIFIED APPROACH:
    - Handles new cultural heritage → tag mapping flow
    - Processes curl input format
    - Ensures proper data flow between simplified agents
    - Adds better error handling for missing Qloo results
    """
    
    def __init__(self, 
                 qloo_tool=None, 
                 youtube_tool=None, 
                 gemini_tool=None,
                 vision_ai_tool=None,
                 session_storage_tool=None):
        """Initialize all agents with available tools."""
        
        # Initialize agents
        self.agent1 = InformationConsolidatorAgent()
        self.agent2 = CulturalProfileBuilderAgent()
        
        # Agent 3 requires qloo_tool
        if qloo_tool:
            self.agent3 = QlooCulturalIntelligenceAgent(qloo_tool)
        else:
            self.agent3 = None
            logger.warning("⚠️  Agent 3 disabled: qloo_tool not available")
        
        # Agent 4 requires youtube_tool and gemini_tool
        if youtube_tool and gemini_tool:
            self.agent4 = SensoryContentGeneratorAgent(youtube_tool, gemini_tool)
        else:
            self.agent4 = None
            missing = []
            if not youtube_tool: missing.append("youtube_tool")
            if not gemini_tool: missing.append("gemini_tool") 
            logger.warning(f"⚠️  Agent 4 disabled: {', '.join(missing)} not available")
        
        # Agent 5 requires vision_ai_tool
        if vision_ai_tool:
            self.agent5 = PhotoCulturalAnalyzerAgent(vision_ai_tool)
        else:
            self.agent5 = None
            logger.warning("⚠️  Agent 5 disabled: vision_ai_tool not available")
        
        # Agent 6 (Mobile Synthesizer) - always available
        self.agent6 = MobileSynthesizerAgent()
        
        # Agent 7 requires session_storage_tool
        if session_storage_tool:
            self.agent7 = FeedbackLearningAgent(session_storage_tool)
        else:
            self.agent7 = None
            logger.warning("⚠️  Agent 7 disabled: session_storage_tool not available")
        
        # Count active agents
        active_agents = sum(1 for agent in [self.agent1, self.agent2, self.agent3, 
                                          self.agent4, self.agent5, self.agent6, self.agent7] 
                          if agent is not None)
        
        logger.info(f"CareConnect Sequential Agent initialized with {active_agents}/7 agents active")
    
    async def execute_pipeline(self,
                             patient_profile: Dict[str, Any],
                             request_type: str = "dashboard",
                             feedback_data: Optional[Dict[str, Any]] = None,
                             photo_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete 7-agent pipeline with updated data flow.
        
        Args:
            patient_profile: Patient information (from curl request)
            request_type: Type of request (dashboard, activity, etc.)
            feedback_data: Optional feedback history
            photo_data: Optional photo data
            
        Returns:
            Complete pipeline results with mobile experience
        """
        
        try:
            logger.info(f"Starting CareConnect pipeline for {request_type} request")
            
            pipeline_metadata = {
                "pipeline_start_time": datetime.now().isoformat(),
                "request_type": request_type,
                "agents_executed": 0,
                "active_agents": [],
                "pipeline_version": "simplified_tag_based"
            }
            
            # AGENT 1: Information Consolidator (Always runs)
            logger.info("Executing Agent 1: Information Consolidator")
            agent1_result = await self.agent1.run(
                patient_profile=patient_profile,
                request_type=request_type,
                feedback_data=feedback_data,
                photo_data=photo_data
            )
            consolidated_info = agent1_result.get("consolidated_info", {})
            pipeline_metadata["agents_executed"] += 1
            pipeline_metadata["active_agents"].append("information_consolidator")
            logger.info("✅ Agent 1 completed successfully")
            
            # AGENT 2: Cultural Profile Builder (Always runs)
            logger.info("Executing Agent 2: Cultural Profile Builder")
            agent2_result = await self.agent2.run(
                consolidated_info=consolidated_info
            )
            cultural_profile = agent2_result.get("cultural_profile", {})
            pipeline_metadata["agents_executed"] += 1
            pipeline_metadata["active_agents"].append("cultural_profile_builder")
            logger.info("✅ Agent 2 completed successfully")
            
            # AGENT 3: Qloo Cultural Intelligence (Conditional)
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
                    qloo_intelligence = self._create_empty_qloo_intelligence()
            else:
                logger.warning("⚠️  Agent 3 not available - using empty cultural intelligence")
                qloo_intelligence = self._create_empty_qloo_intelligence()
            
            # AGENT 4: Sensory Content Generator (Conditional)
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
                    sensory_content = self._create_empty_sensory_content()
            else:
                logger.warning("⚠️  Agent 4 not available - sensory content disabled")
                sensory_content = self._create_empty_sensory_content()
            
            # AGENT 5: Photo Cultural Analyzer (Conditional)
            if self.agent5 and photo_data:
                try:
                    logger.info("Executing Agent 5: Photo Cultural Analyzer")
                    agent5_result = await self.agent5.run(
                        consolidated_info=consolidated_info,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content
                    )
                    photo_analysis = agent5_result.get("photo_analysis", {})
                    pipeline_metadata["agents_executed"] += 1
                    pipeline_metadata["active_agents"].append("photo_cultural_analyzer")
                    logger.info("✅ Agent 5 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 5 failed: {e}")
                    photo_analysis = {"status": "failed", "error": str(e)}
            else:
                reason = "no_photo_data" if not photo_data else "vision_ai_unavailable"
                logger.info(f"⚠️  Agent 5 skipped: {reason}")
                photo_analysis = {"status": "skipped", "reason": reason}
            
            # AGENT 6: Mobile Synthesizer (Always runs)
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
                mobile_experience = {"status": "failed", "error": str(e)}
            
            # AGENT 7: Feedback Learning System (Conditional)
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
                    updated_preferences = {"status": "failed", "error": str(e)}
            else:
                reason = "no_feedback_data" if not feedback_data else "session_storage_unavailable"
                logger.info(f"⚠️  Agent 7 skipped: {reason}")
                updated_preferences = {"status": "skipped", "reason": reason}
            
            # Complete pipeline metadata
            pipeline_metadata["pipeline_end_time"] = datetime.now().isoformat()
            pipeline_metadata["total_execution_time"] = "calculated_by_client"
            pipeline_metadata["pipeline_success"] = True
            
            # Build final response
            final_response = {
                "pipeline_results": {
                    "consolidated_info": consolidated_info,
                    "cultural_profile": cultural_profile,
                    "qloo_intelligence": qloo_intelligence,
                    "sensory_content": sensory_content,
                    "photo_analysis": photo_analysis,
                    "mobile_experience": mobile_experience,
                    "updated_preferences": updated_preferences
                },
                "pipeline_metadata": pipeline_metadata,
                "status": "success"
            }
            
            logger.info(f"🎉 CareConnect pipeline completed: {pipeline_metadata['agents_executed']} agents executed")
            
            return final_response
            
        except Exception as e:
            logger.error(f"❌ Pipeline execution failed: {e}")
            return self._create_pipeline_error_response(str(e))
    
    def _create_empty_qloo_intelligence(self) -> Dict[str, Any]:
        """Create empty Qloo intelligence when Agent 3 is unavailable."""
        
        return {
            "success": False,
            "cultural_recommendations": {
                "places": {"available": False, "entities": []},
                "artists": {"available": False, "entities": []},
                "movies": {"available": False, "entities": []}
            },
            "metadata": {
                "successful_calls": 0,
                "total_calls": 0,
                "approach": "agent_unavailable"
            },
            "status": "agent_disabled"
        }
    
    def _create_empty_sensory_content(self) -> Dict[str, Any]:
        """Create empty sensory content when Agent 4 is unavailable."""
        
        return {
            "content_by_sense": {
                "auditory": {"sense_type": "auditory", "available": False},
                "gustatory": {"sense_type": "gustatory", "available": False},
                "olfactory": {"sense_type": "olfactory", "available": False},
                "visual": {"sense_type": "visual", "available": False},
                "tactile": {"sense_type": "tactile", "available": False}
            },
            "sensory_summary": {
                "total_senses_activated": 0,
                "generation_success": False
            },
            "generation_metadata": {
                "agent_version": "agent_unavailable"
            }
        }
    
    def _create_pipeline_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response when pipeline fails."""
        
        return {
            "pipeline_results": {},
            "pipeline_metadata": {
                "pipeline_success": False,
                "error": error_message,
                "error_timestamp": datetime.now().isoformat()
            },
            "status": "error"
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        
        return {
            "agent_1_information_consolidator": "active",
            "agent_2_cultural_profile_builder": "active", 
            "agent_3_qloo_cultural_intelligence": "active" if self.agent3 else "disabled",
            "agent_4_sensory_content_generator": "active" if self.agent4 else "disabled",
            "agent_5_photo_cultural_analyzer": "active" if self.agent5 else "disabled",
            "agent_6_mobile_synthesizer": "active",
            "agent_7_feedback_learning_system": "active" if self.agent7 else "disabled",
            "total_active_agents": sum(1 for agent in [self.agent1, self.agent2, self.agent3, 
                                                     self.agent4, self.agent5, self.agent6, self.agent7] 
                                     if agent is not None)
        }

# Test function
async def test_sequential_agent():
    """Test the updated sequential agent coordinator."""
    
    # Create coordinator (without tools for basic testing)
    coordinator = SequentialAgentCoordinator()
    
    # Test data matching curl example
    test_patient_profile = {
        "cultural_heritage": "Italian-American",
        "birth_year": 1945,
        "city": "Brooklyn", 
        "state": "New York",
        "additional_context": "Loves music and cooking"
    }
    
    # Run pipeline
    logger.info("Testing sequential agent pipeline...")
    result = await coordinator.execute_pipeline(
        patient_profile=test_patient_profile,
        request_type="dashboard"
    )
    
    # Display results
    metadata = result.get("pipeline_metadata", {})
    print("Sequential Agent Test Results:")
    print(f"Agents executed: {metadata.get('agents_executed')}")
    print(f"Active agents: {metadata.get('active_agents')}")
    print(f"Success: {metadata.get('pipeline_success')}")
    
    # Show cultural profile results
    cultural_profile = result.get("pipeline_results", {}).get("cultural_profile", {})
    if cultural_profile:
        elements = cultural_profile.get("cultural_elements", {})
        print(f"Heritage: {elements.get('heritage')}")
        print(f"Tag mappings: {cultural_profile.get('qloo_tag_mappings', {})}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_sequential_agent())