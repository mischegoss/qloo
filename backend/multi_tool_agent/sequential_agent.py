"""
Updated Sequential Agent - Photo Analysis Data Flow Fixed
File: backend/multi_tool_agent/sequential_agent.py

UPDATED: Fixed data flow to pass photo_analysis from Agent 5 to Agent 6
- Agent 5 now analyzes place photos only (not theme photos)
- Agent 6 receives photo_analysis for Local Memory card creation
- Maintains all existing functionality and error handling
- Clean 6-agent pipeline execution
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Updated Sequential Agent with corrected photo analysis data flow.
    
    PIPELINE FLOW:
    Agent 1: Information Consolidator (with location prioritization)
    Agent 2: Cultural Profile Builder  
    Agent 3: Qloo Cultural Intelligence (places, artists, tv_shows)
    Agent 4: Sensory Content Generator (music, tv, recipes)
    Agent 5: Photo Cultural Analyzer (place photos from Qloo)
    Agent 6: Mobile Synthesizer (4 cards including Local Memory)
    """
    
    def __init__(self, agent1=None, agent2=None, agent3=None, agent4=None, agent5=None, agent6=None):
        self.agent1 = agent1  # Information Consolidator
        self.agent2 = agent2  # Cultural Profile Builder
        self.agent3 = agent3  # Qloo Cultural Intelligence  
        self.agent4 = agent4  # Sensory Content Generator
        self.agent5 = agent5  # Photo Cultural Analyzer (Places Only)
        self.agent6 = agent6  # Mobile Synthesizer
        
        self.agents_available = [
            f"Agent {i+1}" for i, agent in enumerate([agent1, agent2, agent3, agent4, agent5, agent6])
            if agent is not None
        ]
        
        logger.info(f"Sequential Agent initialized with: {', '.join(self.agents_available)}")
        logger.info("🎯 UPDATED: Agent 5 processes PLACE PHOTOS ONLY for Local Memory cards")
        logger.info("📷 Personal photos removed - hackathon focus on Places + Vision Analysis")
    
    def _transform_theme_data(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform theme data from Agent 1 format to downstream agent format
        
        Agent 1 format: daily_theme.theme.{id, name, description}
        Downstream format: theme_of_the_day.{id, name, description}
        """
        
        daily_theme = consolidated_info.get("daily_theme", {})
        theme_data = daily_theme.get("theme", {})
        theme_image = daily_theme.get("theme_image", {})
        
        return {
            "theme_of_the_day": {
                "id": theme_data.get("id", ""),
                "name": theme_data.get("name", "Unknown"),
                "description": theme_data.get("description", "")
            },
            "theme_image": theme_image
        }
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: str = "default",
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete 6-agent pipeline with UPDATED data flow for Local Memory cards.
        
        UPDATED DATA FLOW:
        - Agent 5 analyzes place photos from Qloo (not theme photos)
        - Agent 6 receives photo_analysis for Local Memory card creation
        - All agents receive appropriate inputs for enhanced functionality
        """
        
        logger.info("🚀 Starting UPDATED 6-agent pipeline with Place Photo Analysis")
        
        try:
            # ===== AGENT 1: Information Consolidator =====
            if not self.agent1:
                logger.error("❌ Agent 1 (Information Consolidator) not available")
                return {"success": False, "error": "Agent 1 not available"}
            
            logger.info("📋 Running Agent 1: Information Consolidator (with location prioritization)")
            consolidated_info = await self.agent1.run(
                patient_profile=patient_profile,
                request_type=request_type,
                session_id=session_id,
                feedback_data=feedback_data
            )
            
            if not consolidated_info:
                logger.error("❌ Agent 1 failed to produce consolidated information")
                return {"success": False, "error": "Information consolidation failed"}
            
            logger.info("✅ Agent 1 completed successfully")
            
            # ===== AGENT 2: Cultural Profile Builder =====
            if not self.agent2:
                logger.error("❌ Agent 2 (Cultural Profile Builder) not available")
                return {"success": False, "error": "Agent 2 not available"}
            
            logger.info("🧠 Running Agent 2: Cultural Profile Builder")
            cultural_profile = await self.agent2.run(consolidated_info)
            
            if not cultural_profile:
                logger.error("❌ Agent 2 failed to produce cultural profile")
                return {"success": False, "error": "Cultural profile building failed"}
            
            logger.info("✅ Agent 2 completed successfully")
            
            # ===== AGENT 3: Qloo Cultural Intelligence =====
            if not self.agent3:
                logger.error("❌ Agent 3 (Qloo Cultural Intelligence) not available")
                return {"success": False, "error": "Agent 3 not available"}
            
            logger.info("🎯 Running Agent 3: Qloo Cultural Intelligence (places, artists, tv_shows)")
            qloo_intelligence = await self.agent3.run(consolidated_info, cultural_profile)
            
            if not qloo_intelligence:
                logger.error("❌ Agent 3 failed to produce Qloo intelligence")
                return {"success": False, "error": "Qloo intelligence failed"}
            
            logger.info("✅ Agent 3 completed successfully")
            
            # ===== AGENT 4: Sensory Content Generator =====
            if not self.agent4:
                logger.error("❌ Agent 4 (Sensory Content Generator) not available")
                return {"success": False, "error": "Agent 4 not available"}
            
            logger.info("🎨 Running Agent 4: Sensory Content Generator")
            sensory_content = await self.agent4.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence
            )
            
            if not sensory_content:
                logger.error("❌ Agent 4 failed to produce sensory content")
                return {"success": False, "error": "Sensory content generation failed"}
            
            logger.info("✅ Agent 4 completed successfully")
            
            # ===== AGENT 5: Photo Cultural Analyzer (PLACES ONLY) =====
            if not self.agent5:
                logger.error("❌ Agent 5 (Photo Cultural Analyzer) not available")
                return {"success": False, "error": "Agent 5 not available"}
            
            logger.info("📸 Running Agent 5: Photo Cultural Analyzer (PLACE PHOTOS ONLY)")
            photo_analysis = await self.agent5.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence,
                sensory_content=sensory_content
            )
            
            if not photo_analysis:
                logger.warning("⚠️ Agent 5 produced no photo analysis - rural fallback will be used")
                photo_analysis = {"place_photo_analysis": {"available": False, "rural_fallback": True}}
            
            logger.info("✅ Agent 5 completed successfully")
            
            # ===== AGENT 6: Mobile Synthesizer (WITH PHOTO ANALYSIS) =====
            if not self.agent6:
                logger.error("❌ Agent 6 (Mobile Synthesizer) not available")
                return {"success": False, "error": "Agent 6 not available"}
            
            logger.info("📱 Running Agent 6: Mobile Synthesizer (with Local Memory card)")
            final_result = await self.agent6.run(
                consolidated_info=consolidated_info,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence,
                sensory_content=sensory_content,
                photo_analysis=photo_analysis  # CRITICAL: Pass photo analysis to Agent 6
            )
            
            if not final_result:
                logger.error("❌ Agent 6 failed to produce final dashboard")
                return {"success": False, "error": "Dashboard synthesis failed"}
            
            logger.info("✅ Agent 6 completed successfully")
            
            # ===== PIPELINE SUCCESS =====
            logger.info("🎉 Complete 6-agent pipeline executed successfully!")
            logger.info("📊 Dashboard generated with 4 cards: Music | TV | Recipe | Local Memory")
            
            # Add pipeline metadata to final result
            final_result["pipeline_metadata"] = {
                "agents_executed": len(self.agents_available),
                "execution_timestamp": datetime.now().isoformat(),
                "pipeline_version": "enhanced_with_local_memory",
                "photo_analysis_mode": "places_only",
                "location_prioritization": "hometown_preferred",
                "rural_area_support": True,
                "agents_summary": {
                    "agent1": "Information consolidation with location prioritization",
                    "agent2": "Cultural profile building", 
                    "agent3": "Qloo cultural intelligence (places, artists, tv_shows)",
                    "agent4": "Sensory content generation (music, tv, recipes)",
                    "agent5": "Place photo analysis with Google Vision",
                    "agent6": "Dashboard synthesis with Local Memory card"
                }
            }
            
            return final_result
            
        except Exception as e:
            logger.error(f"❌ Sequential agent pipeline failed: {e}")
            return {
                "success": False,
                "error": f"Pipeline execution failed: {str(e)}",
                "pipeline_stage": "unknown",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents in the pipeline"""
        
        agent_status = {
            "agent1_information_consolidator": self.agent1 is not None,
            "agent2_cultural_profile_builder": self.agent2 is not None,
            "agent3_qloo_cultural_intelligence": self.agent3 is not None,
            "agent4_sensory_content_generator": self.agent4 is not None,
            "agent5_photo_cultural_analyzer": self.agent5 is not None,
            "agent6_mobile_synthesizer": self.agent6 is not None
        }
        
        total_agents = len([agent for agent in agent_status.values() if agent])
        
        return {
            "total_agents_available": total_agents,
            "all_agents_ready": total_agents == 6,
            "agents": agent_status,
            "pipeline_mode": "enhanced_with_local_memory",
            "photo_analysis_mode": "places_only",
            "ready_for_execution": total_agents >= 4  # Minimum viable pipeline
        }
    
    async def run_individual_agent(self, agent_number: int, **kwargs) -> Dict[str, Any]:
        """
        Run individual agent for testing/debugging purposes
        
        Args:
            agent_number: Agent to run (1-6)
            **kwargs: Arguments for the specific agent
            
        Returns:
            Agent-specific results
        """
        
        agents = {
            1: self.agent1,
            2: self.agent2,
            3: self.agent3,
            4: self.agent4,
            5: self.agent5,
            6: self.agent6
        }
        
        agent = agents.get(agent_number)
        if not agent:
            return {"success": False, "error": f"Agent {agent_number} not available"}
        
        try:
            logger.info(f"🧪 Running individual Agent {agent_number} for testing")
            result = await agent.run(**kwargs)
            logger.info(f"✅ Agent {agent_number} individual test completed")
            return result
        except Exception as e:
            logger.error(f"❌ Agent {agent_number} individual test failed: {e}")
            return {"success": False, "error": f"Agent {agent_number} failed: {str(e)}"}

# Export the main class
__all__ = ["SequentialAgent"]