"""
Sequential Agent Runner - FIXED Theme Data Structure Mapping
File: backend/multi_tool_agent/sequential_agent.py

CHANGES:
- FIXED: Corrected theme data structure mapping between agents
- Agent 1 returns theme in 'daily_theme.theme' structure
- Downstream agents expect 'theme_of_the_day' structure
- Added proper data transformation to ensure theme flows correctly
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Sequential agent runner that coordinates all 6 agents in order.
    FIXED: Proper theme data structure mapping between agents.
    """
    
    def __init__(self, agent1=None, agent2=None, agent3=None, agent4=None, agent5=None, agent6=None):
        self.agent1 = agent1  # Information Consolidator
        self.agent2 = agent2  # Cultural Profile Builder (unchanged)
        self.agent3 = agent3  # Qloo Cultural Intelligence  
        self.agent4 = agent4  # Sensory Content Generator
        self.agent5 = agent5  # Photo Cultural Analyzer (ENHANCED for theme images)
        self.agent6 = agent6  # Mobile Synthesizer
        
        self.agents_available = [
            f"Agent {i+1}" for i, agent in enumerate([agent1, agent2, agent3, agent4, agent5, agent6])
            if agent is not None
        ]
        
        logger.info(f"Sequential Agent initialized with: {', '.join(self.agents_available)}")
        logger.info("🎯 ENHANCED: Agent 5 will process both personal photos AND theme images")
        logger.info("🔧 FIXED: Theme data structure mapping between agents")
    
    def _transform_theme_data(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Transform theme data from Agent 1 format to downstream agent format
        
        Agent 1 format: daily_theme.theme.{id, name, description}
        Downstream format: theme_of_the_day.{id, name, description}
        """
        daily_theme_raw = consolidated_info.get("daily_theme", {})
        theme_data = daily_theme_raw.get("theme", {})
        theme_image = daily_theme_raw.get("theme_image", {})
        
        # Transform to expected format
        transformed_theme = {
            "theme_of_the_day": {
                "id": theme_data.get("id", "unknown"),
                "name": theme_data.get("name", "Unknown"),
                "description": theme_data.get("description", "Today's theme"),
                "conversation_prompts": theme_data.get("conversation_prompts", []),
                "recipe_keywords": theme_data.get("recipe_keywords", []),
                "content_preferences": theme_data.get("content_preferences", {})
            },
            "theme_image": theme_image,
            "selection_metadata": daily_theme_raw.get("selection_metadata", {}),
            "application_note": daily_theme_raw.get("application_note", "")
        }
        
        logger.info(f"🔧 FIXED: Transformed theme '{theme_data.get('name', 'Unknown')}' to downstream format")
        return transformed_theme
    
    async def run_full_pipeline(self, 
                               patient_profile: Dict[str, Any],
                               request_type: str = "dashboard",
                               session_id: Optional[str] = None,
                               feedback_data: Optional[Dict[str, Any]] = None,
                               photo_of_the_day: Optional[str] = None,
                               photo_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete 6-agent pipeline with FIXED theme data flow.
        """
        
        logger.info("🚀 Starting ENHANCED sequential agent pipeline")
        logger.info(f"📋 Request type: {request_type}")
        logger.info(f"👤 Patient: {patient_profile.get('first_name', 'Unknown')}")
        logger.info(f"📷 Personal photo: {photo_of_the_day or 'None'}")
        
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
                    logger.info("Executing Agent 1: Information Consolidator with ENHANCED theme support")
                    
                    # Prepare photo data for Agent 1 (existing logic)
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
                        photo_data=photo_data
                    )
                    consolidated_info = agent1_result.get("consolidated_info", {})
                    
                    # FIXED: Transform theme data to downstream format
                    daily_theme_transformed = self._transform_theme_data(consolidated_info)
                    
                    # FIXED: Extract theme information using correct structure
                    theme_of_the_day = daily_theme_transformed.get("theme_of_the_day", {})
                    theme_image = daily_theme_transformed.get("theme_image", {})
                    theme_name = theme_of_the_day.get("name", "Unknown")
                    
                    logger.info("✅ Agent 1 completed successfully")
                    logger.info(f"🎯 Daily theme: {theme_name}")
                    logger.info(f"🖼️ Theme image: {theme_image.get('filename', 'Not found')} (exists: {theme_image.get('exists', False)})")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 1 failed: {e}")
                    consolidated_info = {"error": str(e), "request_type": request_type}
                    daily_theme_transformed = {"theme_of_the_day": {"name": "Unknown", "id": "unknown"}}
            
            # AGENT 2: Cultural Profile Builder (UNCHANGED)
            if self.agent2:
                try:
                    logger.info("Executing Agent 2: Cultural Profile Builder")
                    agent2_result = await self.agent2.run(consolidated_info=consolidated_info)
                    cultural_profile = agent2_result.get("cultural_profile", {})
                    logger.info("✅ Agent 2 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 2 failed: {e}")
                    cultural_profile = {"error": str(e)}
            
            # AGENT 3: Qloo Cultural Intelligence (UNCHANGED)
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
            
            # AGENT 4: Sensory Content Generator (FIXED - now gets proper theme data) 
            if self.agent4:
                try:
                    logger.info("Executing Agent 4: Sensory Content Generator")
                    
                    # FIXED: Create consolidated_info with properly formatted theme for Agent 4
                    consolidated_info_for_agent4 = consolidated_info.copy()
                    consolidated_info_for_agent4["daily_theme"] = daily_theme_transformed
                    
                    agent4_result = await self.agent4.run(
                        consolidated_info=consolidated_info_for_agent4,  # FIXED: Includes transformed theme
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence
                    )
                    sensory_content = agent4_result.get("sensory_content", {})
                    logger.info("✅ Agent 4 completed successfully")
                except Exception as e:
                    logger.error(f"❌ Agent 4 failed: {e}")
                    sensory_content = {"error": str(e)}
            
            # AGENT 5: Photo Cultural Analyzer (ENHANCED - now receives theme image data)
            if self.agent5 and (photo_of_the_day or daily_theme_transformed.get("theme_image", {}).get("exists")):
                try:
                    # Enhanced logging for Agent 5
                    theme_image_available = daily_theme_transformed.get("theme_image", {}).get("exists", False)
                    personal_photo_available = bool(photo_of_the_day and photo_analysis)
                    
                    logger.info(f"Executing Agent 5: ENHANCED Photo Cultural Analyzer")
                    logger.info(f"   📷 Personal photo available: {personal_photo_available}")
                    logger.info(f"   🎯 Theme image available: {theme_image_available}")
                    
                    if personal_photo_available:
                        logger.info(f"   📷 Personal photo: {photo_of_the_day}")
                    if theme_image_available:
                        theme_image = daily_theme_transformed.get("theme_image", {})
                        logger.info(f"   🖼️ Theme image: {theme_image.get('filename', 'Unknown')}")
                    
                    # FIXED: Create consolidated_info with properly formatted theme for Agent 5
                    consolidated_info_for_agent5 = consolidated_info.copy()
                    consolidated_info_for_agent5["daily_theme"] = daily_theme_transformed
                    
                    # ENHANCED: Agent 5 now processes both personal photos AND theme images
                    agent5_result = await self.agent5.run(
                        consolidated_info=consolidated_info_for_agent5,  # FIXED: Includes transformed theme
                        cultural_profile=cultural_profile,
                        qloo_intelligence=qloo_intelligence,
                        sensory_content=sensory_content,
                        photo_of_the_day=photo_of_the_day,  # Existing: personal photo
                        stored_photo_analysis=photo_analysis  # Existing: personal photo analysis
                    )
                    photo_analysis_result = agent5_result.get("photo_analysis", {})
                    
                    # Enhanced logging for Agent 5 results
                    processing_metadata = photo_analysis_result.get("processing_metadata", {})
                    analysis_sources = processing_metadata.get("analysis_sources", [])
                    
                    logger.info("✅ Agent 5 completed successfully with ENHANCED analysis")
                    logger.info(f"   🔍 Analysis sources: {', '.join(analysis_sources)}")
                    logger.info(f"   💬 Total conversation starters: {processing_metadata.get('conversation_count', 0)}")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 5 failed: {e}")
                    photo_analysis_result = {"error": str(e)}
            else:
                # Log why Agent 5 was skipped
                theme_image_available = daily_theme_transformed.get("theme_image", {}).get("exists", False)
                personal_photo_available = bool(photo_of_the_day and photo_analysis)
                
                logger.info("⚠️  Agent 5 skipped:")
                logger.info(f"   📷 Personal photo available: {personal_photo_available}")
                logger.info(f"   🎯 Theme image available: {theme_image_available}")
                
                photo_analysis_result = {"status": "skipped", "reason": "no_visual_content_available"}
            
            # AGENT 6: Mobile Synthesizer (FIXED - now gets proper theme data)
            if self.agent6:
                try:
                    logger.info("Executing Agent 6: Mobile Synthesizer with ENHANCED theme image support")
                    
                    # FIXED: Pass properly formatted theme data to Agent 6
                    agent6_result = await self.agent6.run(
                        audio_content=qloo_intelligence,  # Music content
                        visual_content=qloo_intelligence,  # TV show content
                        sensory_content=sensory_content,  # Recipe content
                        daily_theme=daily_theme_transformed  # FIXED: Properly formatted theme data
                    )
                    mobile_experience = agent6_result.get("dashboard_content", {})
                    
                    # Enhanced logging for Agent 6
                    theme_image = daily_theme_transformed.get("theme_image", {})
                    if theme_image.get("exists"):
                        logger.info(f"✅ Agent 6 completed with theme image: {theme_image.get('filename')}")
                    else:
                        logger.info("✅ Agent 6 completed (no theme image)")
                    
                except Exception as e:
                    logger.error(f"❌ Agent 6 failed: {e}")
                    mobile_experience = {"error": str(e)}
            
            # Calculate pipeline timing
            pipeline_end_time = datetime.now()
            pipeline_duration = (pipeline_end_time - pipeline_start_time).total_seconds()
            
            # ENHANCED: Compile complete results with theme image integration
            complete_results = {
                "status": "success",
                "pipeline_result": "success",
                "content": {
                    "consolidated_info": consolidated_info,
                    "cultural_profile": cultural_profile,
                    "qloo_intelligence": qloo_intelligence,
                    "sensory_content": sensory_content,
                    "photo_analysis": photo_analysis_result,  # ENHANCED: Now includes theme image analysis
                    "mobile_experience": mobile_experience,
                    "pipeline_metadata": {
                        "execution_time_seconds": round(pipeline_duration, 2),
                        "agents_executed": len(self.agents_available),
                        "timestamp": datetime.now().isoformat(),
                        "enhanced_features": [
                            "theme_image_analysis",
                            "combined_visual_intelligence",
                            "personal_plus_theme_photos",
                            "fixed_theme_data_flow"  # NEW
                        ],
                        "visual_analysis_summary": {
                            "personal_photo_processed": bool(photo_of_the_day),
                            "theme_image_processed": daily_theme_transformed.get("theme_image", {}).get("exists", False),
                            "combined_analysis": photo_analysis_result.get("processing_metadata", {}).get("enhanced_approach", False)
                        }
                    }
                }
            }
            
            logger.info(f"🎉 ENHANCED pipeline completed successfully in {pipeline_duration:.2f}s")
            logger.info(f"🔍 Visual analysis summary:")
            visual_summary = complete_results["content"]["pipeline_metadata"]["visual_analysis_summary"]
            logger.info(f"   📷 Personal photo: {visual_summary['personal_photo_processed']}")
            logger.info(f"   🎯 Theme image: {visual_summary['theme_image_processed']}")
            logger.info(f"   🔗 Combined analysis: {visual_summary['combined_analysis']}")
            
            return complete_results
            
        except Exception as e:
            logger.error(f"💥 ENHANCED pipeline failed: {e}")
            return {
                "status": "error",
                "pipeline_result": "error",
                "error": str(e),
                "content": {
                    "pipeline_metadata": {
                        "execution_time_seconds": (datetime.now() - pipeline_start_time).total_seconds(),
                        "agents_executed": 0,
                        "timestamp": datetime.now().isoformat(),
                        "failure_point": "pipeline_exception"
                    }
                }
            }