"""
Sequential Agent Runner - FIXED to Remove Personal Photos from Automatic Pipeline
File: backend/multi_tool_agent/sequential_agent.py

CHANGES:
- REMOVED personal photo parameters from automatic pipeline (photo_of_the_day, photo_analysis)
- Agent 5 now ALWAYS runs when theme is valid (theme photos always exist)
- Theme photos are the only "photo of the day" in automatic pipeline
- Personal photos are completely separate (on-demand only)
- All other functionality preserved
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Sequential agent runner that coordinates all 6 agents in order.
    FIXED: Personal photos removed from automatic pipeline, theme photos only.
    """
    
    def __init__(self, agent1=None, agent2=None, agent3=None, agent4=None, agent5=None, agent6=None):
        self.agent1 = agent1  # Information Consolidator
        self.agent2 = agent2  # Cultural Profile Builder (unchanged)
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
        theme = daily_theme.get("theme", {})
        theme_image = daily_theme.get("theme_image", {})  # NEW: Include theme image
        selection_metadata = daily_theme.get("selection_metadata", {})
        
        # Transform to expected downstream format
        transformed = {
            "theme_of_the_day": theme,
            "theme_image": theme_image,  # NEW: Theme image for Agent 5
            "selection_metadata": selection_metadata
        }
        
        return transformed
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None,
                  # REMOVED: photo_of_the_day parameter - no longer used in automatic pipeline
                  # REMOVED: photo_analysis parameter - no longer used in automatic pipeline
                  ) -> Dict[str, Any]:
        """
        FIXED: Run sequential agent pipeline with THEME PHOTOS ONLY
        Personal photos are no longer part of automatic pipeline
        
        Args:
            patient_profile: Patient information
            request_type: Type of request (dashboard, etc.)
            session_id: Session identifier
            feedback_data: Previous feedback for learning
            # REMOVED: photo_of_the_day - personal photos not in automatic pipeline
            # REMOVED: photo_analysis - personal photo analysis not in automatic pipeline
            
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
                    
                    # REMOVED: photo_data preparation - no personal photos in automatic pipeline
                    # photo_data = None  # REMOVED
                    # if photo_of_the_day and photo_analysis:  # REMOVED
                    #     photo_data = {...}  # REMOVED
                    
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
                    
                    # Extract theme information
                    theme_of_the_day = daily_theme_transformed.get("theme_of_the_day", {})
                    theme_image = daily_theme_transformed.get("theme_image", {})
                    theme_name = theme_of_the_day.get("name", "Unknown")
                    
                    logger.info(f"✅ Agent 1 completed successfully")
                    logger.info(f"🎯 Daily theme: {theme_name}")
                    logger.info(f"🖼️ Theme image: {theme_image.get('filename', 'Not found')}")
                    logger.info(f"📋 Theme image exists: {theme_image.get('exists', False)}")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 1 failed: {e}")
                    consolidated_info = {"error": str(e)}
                    daily_theme_transformed = {}
            
            # AGENT 2: Cultural Profile Builder (unchanged)
            if self.agent2 and consolidated_info:
                try:
                    logger.info("Executing Agent 2: Cultural Profile Builder")
                    agent2_result = await self.agent2.run(consolidated_info=consolidated_info)
                    cultural_profile = agent2_result.get("cultural_profile", {})
                    logger.info("✅ Agent 2 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 2 failed: {e}")
                    cultural_profile = {"error": str(e)}
            
            # AGENT 3: Qloo Cultural Intelligence (unchanged)
            if self.agent3 and consolidated_info and cultural_profile:
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
            
            # AGENT 4: Sensory Content Generator (unchanged)
            if self.agent4 and consolidated_info and cultural_profile and qloo_intelligence:
                try:
                    logger.info("Executing Agent 4: Sensory Content Generator")
                    
                    # Create consolidated_info with properly formatted theme for Agent 4
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
            
            # AGENT 5: Photo Cultural Analyzer (FIXED - THEME PHOTOS ONLY, ALWAYS RUNS)
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
                    
                    # FIXED: Agent 5 now runs with theme photos only
                    agent5_result = await self.agent5.run(
                        consolidated_info=consolidated_info_for_agent5,
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_of_the_day=None,  # REMOVED: No personal photos in automatic pipeline
                        stored_photo_analysis=None  # REMOVED: No personal photo analysis in automatic pipeline
                    )
                    photo_analysis_result = agent5_result.get("photo_analysis", {})
                    
                    # Enhanced logging for Agent 5 results
                    processing_metadata = photo_analysis_result.get("processing_metadata", {})
                    analysis_sources = processing_metadata.get("analysis_sources", [])
                    
                    logger.info("✅ Agent 5 completed successfully with THEME PHOTOS ONLY")
                    logger.info(f"   🔍 Analysis sources: {', '.join(analysis_sources)}")
                    logger.info(f"   💬 Total conversation starters: {processing_metadata.get('conversation_count', 0)}")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 5 failed: {e}")
                    photo_analysis_result = {"error": str(e)}
            else:
                # FIXED: Log why Agent 5 was skipped (should rarely happen now)
                theme_image_available = daily_theme_transformed.get("theme_image", {}).get("exists", False)
                
                logger.warning("⚠️ Agent 5 skipped:")
                logger.warning(f"   🎯 Theme image available: {theme_image_available}")
                logger.warning("   📷 Personal photos: NOT APPLICABLE (excluded from pipeline)")
                
                if not theme_image_available:
                    logger.error("❌ CRITICAL: Theme image should always be available!")
                
                photo_analysis_result = {"status": "skipped", "reason": "no_theme_image_available"}
            
            # AGENT 6: Mobile Synthesizer (FIXED - correct parameter names)
            if self.agent6:
                try:
                    logger.info("Executing Agent 6: Mobile Synthesizer with correct parameters")
                    
                    # FIXED: Use correct parameter names that match MobileSynthesizerAgent.run()
                    agent6_result = await self.agent6.run(
                        audio_content=qloo_intelligence,      # Music content
                        visual_content=qloo_intelligence,     # TV show content  
                        sensory_content=sensory_content,      # Recipe content
                        daily_theme=daily_theme_transformed   # Theme data
                    )
                    
                    # Calculate total pipeline time
                    pipeline_end_time = datetime.now()
                    total_time = (pipeline_end_time - pipeline_start_time).total_seconds()
                    
                    # Add pipeline metadata
                    agent6_result["pipeline_metadata"] = {
                        "total_processing_time_seconds": total_time,
                        "agents_executed": self.agents_available,
                        "pipeline_version": "fixed_theme_photos_only",
                        "personal_photos_excluded": True,  # NEW: Track that personal photos are excluded
                        "theme_photos_only": True  # NEW: Track that only theme photos are used
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
                    "pipeline_version": "fixed_theme_photos_only",
                    "personal_photos_excluded": True,
                    "theme_photos_only": True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Sequential agent pipeline failed: {e}")
            return {"error": f"Pipeline failed: {str(e)}"}