"""
Sequential Agent Runner - FIXED All Agent Parameter Names
File: backend/multi_tool_agent/sequential_agent.py

CRITICAL FIXES:
- Fixed Agent 2 parameter: patient_profile + consolidated_info → consolidated_info only
- Fixed Agent 5 parameters: photo_data → photo_of_the_day, stored_photo_analysis
- CulturalProfileBuilderAgent.run() expects only: consolidated_info
- PhotoCulturalAnalyzerAgent.run() expects: photo_of_the_day, stored_photo_analysis
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Sequential agent runner that coordinates all 6 agents in order.
    FIXED: Correct parameter names for Agent 2 and Agent 5.
    """
    
    def __init__(self, agent1=None, agent2=None, agent3=None, agent4=None, agent5=None, agent6=None):
        self.agent1 = agent1  # Information Consolidator
        self.agent2 = agent2  # Cultural Profile Builder
        self.agent3 = agent3  # Qloo Cultural Intelligence  
        self.agent4 = agent4  # Sensory Content Generator
        self.agent5 = agent5  # Photo Cultural Analyzer (THEME PHOTOS ONLY)
        self.agent6 = agent6  # Mobile Synthesizer
        
        self.agents_available = [
            f"Agent {i+1}" for i, agent in enumerate([agent1, agent2, agent3, agent4, agent5, agent6])
            if agent is not None
        ]
        
        logger.info(f"Sequential Agent initialized with: {', '.join(self.agents_available)}")
        logger.info("🎯 FIXED: Agent 5 processes THEME PHOTOS ONLY in automatic pipeline")
        logger.info("📷 Personal photos are now on-demand only (separate from pipeline)")
    
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
        Run the complete 6-agent pipeline with FIXED Agent 5 parameter names.
        
        Args:
            patient_profile: Patient demographic and preference data
            request_type: Type of request (dashboard, recipe, music, etc.)
            session_id: Session identifier
            feedback_data: Previous feedback for learning
            
        Returns:
            Complete cultural intelligence pipeline result with theme photos
        """
        
        logger.info("🚀 Starting FIXED sequential agent pipeline - THEME PHOTOS ONLY")
        logger.info(f"📋 Request type: {request_type}")
        logger.info(f"👤 Patient: {patient_profile.get('first_name', 'Unknown')}")
        logger.info("📷 Personal photos: REMOVED from automatic pipeline (on-demand only)")
        
        pipeline_start_time = datetime.now()
        
        try:
            # Initialize variables for pipeline state
            consolidated_info = {}
            cultural_profile = {}
            qloo_intelligence = {}
            sensory_content = {}
            photo_analysis_result = {}
            
            # AGENT 1: Information Consolidator (ENHANCED to include theme images)
            if self.agent1:
                try:
                    logger.info("Executing Agent 1: Information Consolidator with theme support")
                    
                    agent1_result = await self.agent1.run(
                        patient_profile=patient_profile,
                        request_type=request_type,
                        session_id=session_id,
                        feedback_data=feedback_data,
                        photo_data=None  # FIXED: No personal photos in automatic pipeline
                    )
                    consolidated_info = agent1_result.get("consolidated_info", {})
                    
                    # Transform theme data for downstream agents
                    daily_theme_transformed = self._transform_theme_data(consolidated_info)
                    
                    logger.info("✅ Agent 1 completed successfully")
                    logger.info(f"🎯 Daily theme: {daily_theme_transformed.get('theme_of_the_day', {}).get('name', 'Unknown')}")
                    logger.info(f"🖼️ Theme image: {daily_theme_transformed.get('theme_image', {}).get('filename', 'None')}")
                    logger.info(f"📋 Theme image exists: {daily_theme_transformed.get('theme_image', {}).get('exists', False)}")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 1 failed: {e}")
                    consolidated_info = {"error": str(e)}
                    daily_theme_transformed = {}
            
            # AGENT 2: Cultural Profile Builder (FIXED - Correct parameter)
            if self.agent2:
                try:
                    logger.info("Executing Agent 2: Cultural Profile Builder")
                    
                    # CRITICAL FIX: Agent 2 only expects consolidated_info parameter
                    # Patient profile data is already inside consolidated_info from Agent 1
                    agent2_result = await self.agent2.run(
                        consolidated_info=consolidated_info  # ✅ CORRECT: only parameter needed
                    )
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
                    
                    # Create properly formatted consolidated_info for Agent 4
                    consolidated_info_for_agent4 = consolidated_info.copy()
                    consolidated_info_for_agent4["daily_theme"] = daily_theme_transformed
                    
                    agent4_result = await self.agent4.run(
                        consolidated_info=consolidated_info_for_agent4,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence
                    )
                    sensory_content = agent4_result.get("sensory_content", {})
                    logger.info("✅ Agent 4 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 4 failed: {e}")
                    sensory_content = {"error": str(e)}
            
            # AGENT 5: Photo Cultural Analyzer (FIXED - Correct parameter names)
            if self.agent5 and daily_theme_transformed.get("theme_image", {}).get("exists"):
                try:
                    # FIXED: Agent 5 now only runs with theme photos, always executes when theme is valid
                    theme_image_available = daily_theme_transformed.get("theme_image", {}).get("exists", False)
                    
                    logger.info(f"Executing Agent 5: Photo Cultural Analyzer - THEME PHOTOS ONLY")
                    logger.info(f"   🎯 Theme image available: {theme_image_available}")
                    logger.info("   📷 Personal photos: EXCLUDED from automatic pipeline")
                    
                    if theme_image_available:
                        theme_image = daily_theme_transformed.get("theme_image", {})
                        logger.info(f"   🖼️ Theme image: {theme_image.get('filename', 'Unknown')}")
                    
                    # Create consolidated_info with properly formatted theme for Agent 5
                    consolidated_info_for_agent5 = consolidated_info.copy()
                    consolidated_info_for_agent5["daily_theme"] = daily_theme_transformed
                    
                    # CRITICAL FIX: Use correct parameter names
                    agent5_result = await self.agent5.run(
                        consolidated_info=consolidated_info_for_agent5,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_of_the_day=None,           # ✅ CORRECT: was photo_data
                        stored_photo_analysis=None       # ✅ CORRECT: added missing parameter
                    )
                    photo_analysis_result = agent5_result.get("photo_analysis", {})
                    
                    logger.info("✅ Agent 5 completed successfully with THEME PHOTOS ONLY")
                    logger.info(f"   🔍 Analysis sources: {photo_analysis_result.get('analysis_sources', 'unknown')}")
                    logger.info(f"   💬 Total conversation starters: {len(photo_analysis_result.get('conversation_starters', []))}")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 5 failed: {e}")
                    photo_analysis_result = {"error": str(e)}
            else:
                # No theme image available
                logger.info("Agent 5: Photo Cultural Analyzer - SKIPPED (no theme image available)")
                photo_analysis_result = {"status": "skipped", "reason": "no_theme_image_available"}
            
            # AGENT 6: Mobile Synthesizer (CRITICAL FIX - Correct data structure)
            if self.agent6:
                try:
                    logger.info("Executing Agent 6: Mobile Synthesizer with correct parameters")
                    
                    # CRITICAL FIX: Wrap qloo_intelligence in expected data structure
                    # Mobile Synthesizer expects audio_content/visual_content to contain "qloo_intelligence" key
                    # But we were passing qloo_intelligence directly, causing the double-nesting issue
                    
                    agent6_result = await self.agent6.run(
                        audio_content={"qloo_intelligence": qloo_intelligence},    # FIXED: Wrapped properly
                        visual_content={"qloo_intelligence": qloo_intelligence},   # FIXED: Wrapped properly
                        sensory_content=sensory_content,
                        daily_theme=daily_theme_transformed
                    )
                    
                    # Calculate total pipeline time
                    pipeline_end_time = datetime.now()
                    total_time = (pipeline_end_time - pipeline_start_time).total_seconds()
                    
                    # Add pipeline metadata
                    agent6_result["pipeline_metadata"] = {
                        "total_processing_time_seconds": total_time,
                        "agents_executed": self.agents_available,
                        "pipeline_version": "fixed_all_agent_parameters",
                        "personal_photos_excluded": True,
                        "theme_photos_only": True,
                        "agent5_parameter_fix_applied": True,  # Agent 5 parameters fixed
                        "agent2_parameter_fix_applied": True   # NEW: Agent 2 parameters fixed
                    }
                    
                    logger.info(f"✅ Agent 6 completed successfully")
                    logger.info(f"⏱️ Total pipeline time: {total_time:.2f} seconds")
                    logger.info("🎯 Pipeline completed with THEME PHOTOS ONLY")
                    
                    return agent6_result
                    
                except Exception as e:
                    logger.error(f"❌ Agent 6 failed: {e}")
                    return {"error": f"Agent 6 failed: {str(e)}"}
            
            # Fallback if Agent 6 not available
            logger.warning("⚠️ Agent 6 not available, returning combined results")
            return {
                "consolidated_info": consolidated_info,
                "cultural_profile": cultural_profile,
                "qloo_intelligence": qloo_intelligence,
                "sensory_content": sensory_content,
                "photo_analysis": photo_analysis_result,
                "pipeline_metadata": {
                    "agents_executed": self.agents_available,
                    "pipeline_version": "fixed_all_agent_parameters",
                    "personal_photos_excluded": True,
                    "theme_photos_only": True,
                    "agent5_parameter_fix_applied": True,
                    "agent2_parameter_fix_applied": True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Sequential agent pipeline failed: {e}")
            return {"error": f"Pipeline failed: {str(e)}"}

# Export the main class
__all__ = ["SequentialAgent"]