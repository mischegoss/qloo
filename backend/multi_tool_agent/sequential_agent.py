"""
Enhanced Sequential Agent with 6-Agent Pipeline + Nostalgia News
File: backend/multi_tool_agent/sequential_agent.py

FIXED: DashboardSynthesizer method signature mismatch
- Added _create_final_enhanced_profile method
- Agent 6 now receives single enhanced_profile parameter
- All agent outputs properly combined before final synthesis

PIPELINE:
Agent 1: Information Consolidator → Agent 2: Photo Analysis → Agent 3: Qloo Cultural
→ Agents 4A/4B/4C: Content Generation (parallel) → Agent 5: Nostalgia News → Agent 6: Dashboard Synthesis
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Enhanced Sequential Agent with 6-Agent Pipeline
    
    FIXED: Method signature mismatch for DashboardSynthesizer
    """
    
    def __init__(self, agent1=None, agent2=None, agent3=None, 
                 agent4a=None, agent4b=None, agent4c=None, 
                 agent5=None, agent6=None):
        
        # Store all agents
        self.agent1 = agent1  # Information Consolidator
        self.agent2 = agent2  # Simple Photo Analysis
        self.agent3 = agent3  # Qloo Cultural Intelligence
        self.agent4a = agent4a  # Music Curation
        self.agent4b = agent4b  # Recipe Selection
        self.agent4c = agent4c  # Photo Description
        self.agent5 = agent5  # Nostalgia News Generator
        self.agent6 = agent6  # Dashboard Synthesizer
        
        # Track available agents
        self.agents_available = [
            agent for agent in [self.agent1, self.agent2, self.agent3, 
                              self.agent4a, self.agent4b, self.agent4c,
                              self.agent5, self.agent6] 
            if agent is not None
        ]
        
        logger.info(f"🤖 Sequential Agent initialized with {len(self.agents_available)}/8 agents")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete 6-agent pipeline with Nostalgia News
        
        Args:
            patient_profile: Patient information from UI
            request_type: Type of request
            session_id: Session identifier
            feedback_data: User feedback data
            
        Returns:
            Complete dashboard with Nostalgia News
        """
        
        logger.info("🚀 Starting 6-agent pipeline with Nostalgia News")
        logger.info(f"📋 Pipeline: Info → Photo → Qloo → Content(4A/4B/4C) → Nostalgia News → Dashboard")
        
        try:
            # ===== AGENT 1: Information Consolidator =====
            if not self.agent1:
                return {"success": False, "error": "Agent 1 (Information Consolidator) not available"}
            
            logger.info("📋 Running Agent 1: Information Consolidator")
            agent1_output = await self.agent1.run(
                patient_profile=patient_profile,
                request_type=request_type,
                session_id=session_id,
                feedback_data=feedback_data
            )
            
            if not agent1_output:
                return {"success": False, "error": "Information consolidation failed"}
            
            logger.info("✅ Agent 1 completed")
            
            # ===== AGENT 2: Simple Photo Analysis =====
            if not self.agent2:
                return {"success": False, "error": "Agent 2 (Simple Photo Analysis) not available"}
            
            logger.info("📸 Running Agent 2: Simple Photo Analysis")
            agent2_output = await self.agent2.run(agent1_output)
            
            if not agent2_output:
                logger.warning("⚠️ Agent 2 failed, using fallback photo analysis")
                agent2_output = {"photo_analysis": {"analysis_method": "fallback", "success": False}}
            
            logger.info("✅ Agent 2 completed")
            
            # ===== AGENT 3: Qloo Cultural Intelligence =====
            if not self.agent3:
                return {"success": False, "error": "Agent 3 (Qloo Cultural Intelligence) not available"}
            
            logger.info("🎯 Running Agent 3: Qloo Cultural Intelligence")
            agent3_output = await self.agent3.run(agent1_output, agent2_output)
            
            if not agent3_output:
                logger.warning("⚠️ Agent 3 failed, using fallback cultural data")
                agent3_output = {"qloo_intelligence": {"cultural_recommendations": {}, "metadata": {"fallback_used": True}}}
            
            logger.info("✅ Agent 3 completed")
            
            # ===== AGENTS 4A, 4B, 4C: Content Generation (Parallel) =====
            logger.info("🎨 Running Agents 4A/4B/4C: Content Generation (parallel)")
            
            # Create enhanced profile for content agents
            enhanced_profile = self._create_enhanced_profile(agent1_output, agent2_output, agent3_output)
            
            # Agent 4A: Music Curation
            if not self.agent4a:
                return {"success": False, "error": "Agent 4A (Music Curation) not available"}
            
            logger.info("🎵 Running Agent 4A: Music Curation")
            agent4a_output = await self.agent4a.run(enhanced_profile)
            
            if not agent4a_output:
                agent4a_output = self._create_fallback_music()
                logger.warning("⚠️ Agent 4A failed, using music fallback")
            
            # Agent 4B: Recipe Selection
            if not self.agent4b:
                return {"success": False, "error": "Agent 4B (Recipe Selection) not available"}
            
            logger.info("🍽️ Running Agent 4B: Recipe Selection")
            agent4b_output = await self.agent4b.run(enhanced_profile)
            
            if not agent4b_output:
                agent4b_output = self._create_fallback_recipe()
                logger.warning("⚠️ Agent 4B failed, using recipe fallback")
            
            # Agent 4C: Photo Description
            if not self.agent4c:
                return {"success": False, "error": "Agent 4C (Photo Description) not available"}
            
            logger.info("📷 Running Agent 4C: Photo Description")
            agent4c_output = await self.agent4c.run(enhanced_profile)
            
            if not agent4c_output:
                agent4c_output = self._create_fallback_photo_description(agent1_output)
                logger.warning("⚠️ Agent 4C failed, using photo description fallback")
            
            logger.info("✅ Agents 4A/4B/4C completed")
            
            # ===== AGENT 5: Nostalgia News Generator =====
            if not self.agent5:
                return {"success": False, "error": "Agent 5 (Nostalgia News Generator) not available"}
            
            logger.info("📰 Running Agent 5: Nostalgia News Generator (STAR FEATURE)")
            agent5_output = await self.agent5.run(
                agent1_output=agent1_output,
                agent2_output=agent2_output,
                agent3_output=agent3_output,
                agent4a_output=agent4a_output,
                agent4b_output=agent4b_output,
                agent4c_output=agent4c_output
            )
            
            if not agent5_output:
                agent5_output = self._create_fallback_nostalgia_news(agent1_output)
                logger.warning("⚠️ Agent 5 failed, using nostalgia news fallback")
            
            logger.info("✅ Agent 5 completed - Nostalgia News generated!")
            
            # ===== AGENT 6: Dashboard Synthesizer =====
            if not self.agent6:
                return {"success": False, "error": "Agent 6 (Dashboard Synthesizer) not available"}
            
            logger.info("🎨 Running Agent 6: Dashboard Synthesizer (Final Assembly)")
            
            # FIXED: Create final enhanced profile that combines ALL agent outputs
            final_enhanced_profile = self._create_final_enhanced_profile(
                agent1_output, agent2_output, agent3_output,
                agent4a_output, agent4b_output, agent4c_output, agent5_output
            )
            
            # FIXED: Call Agent 6 with single enhanced profile parameter
            final_dashboard = await self.agent6.run(final_enhanced_profile)
            
            if not final_dashboard:
                return {"success": False, "error": "Dashboard synthesis failed"}
            
            logger.info("✅ Agent 6 completed - Final dashboard assembled!")
            
            # ===== PIPELINE SUCCESS =====
            logger.info("🎉 Complete 6-agent pipeline executed successfully!")
            logger.info("📰 Dashboard includes personalized Nostalgia News!")
            
            # Add pipeline metadata
            final_dashboard["pipeline_metadata"] = {
                **final_dashboard.get("pipeline_metadata", {}),
                "agents_executed": len(self.agents_available),
                "execution_timestamp": datetime.now().isoformat(),
                "pipeline_version": "6_agent_nostalgia_news",
                "star_feature": "nostalgia_news_generator",
                "cultural_intelligence": "qloo_powered",
                "personalization": "gemini_enhanced",
                "agents_summary": {
                    "agent1": "Information consolidation with theme selection",
                    "agent2": "Simple photo analysis (theme-based)",
                    "agent3": "Qloo cultural intelligence (heritage-driven)",
                    "agent4a": "Music curation with YouTube integration",
                    "agent4b": "Recipe selection (microwave-safe)",
                    "agent4c": "Photo description with cultural context",
                    "agent5": "Nostalgia News generation (Gemini AI)",
                    "agent6": "Dashboard synthesis and final assembly"
                }
            }
            
            return final_dashboard
            
        except Exception as e:
            logger.error(f"❌ Sequential agent pipeline failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            return {
                "success": False,
                "error": f"Pipeline execution failed: {str(e)}",
                "pipeline_stage": "unknown",
                "timestamp": datetime.now().isoformat()
            }
    
    def _create_enhanced_profile(self, agent1_output: Dict[str, Any], 
                                agent2_output: Dict[str, Any],
                                agent3_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced profile for content agents (4A/4B/4C) - FIXED heritage flow"""
        
        # Start with Agent 1 output
        enhanced_profile = agent1_output.copy()
        
        # FIXED: Ensure cultural heritage flows through properly to Agents 4A/4B/4C
        patient_info = enhanced_profile.get("patient_info", {})
        cultural_heritage = patient_info.get("cultural_heritage", "")
        
        # Add heritage to multiple places for maximum compatibility
        enhanced_profile["cultural_heritage"] = cultural_heritage
        enhanced_profile["heritage"] = cultural_heritage
        
        # Ensure patient_info has complete heritage info
        if "patient_info" in enhanced_profile:
            enhanced_profile["patient_info"]["heritage"] = cultural_heritage
            enhanced_profile["patient_info"]["cultural_background"] = cultural_heritage
        
        # Add photo analysis from Agent 2
        enhanced_profile["photo_analysis"] = agent2_output.get("photo_analysis", {})
        
        # Add Qloo intelligence from Agent 3
        enhanced_profile["qloo_intelligence"] = agent3_output.get("qloo_intelligence", {})
        
        # Add pipeline state
        enhanced_profile["pipeline_state"] = {
            "current_step": "content_generation",
            "agents_completed": ["1", "2", "3"],
            "next_agents": ["4A", "4B", "4C"],
            "ready_for_content": True
        }
        
        logger.info(f"✅ Enhanced profile created with heritage: {cultural_heritage}")
        
        return enhanced_profile
    
    def _create_final_enhanced_profile(self, 
                                     agent1_output: Dict[str, Any],
                                     agent2_output: Dict[str, Any], 
                                     agent3_output: Dict[str, Any],
                                     agent4a_output: Dict[str, Any],
                                     agent4b_output: Dict[str, Any],
                                     agent4c_output: Dict[str, Any],
                                     agent5_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Create final enhanced profile combining ALL agent outputs for Agent 6
        
        This method creates the comprehensive profile that Agent 6 expects,
        with proper field name mapping and data structure conversion.
        """
        
        logger.info("🔄 Creating final enhanced profile for Dashboard Synthesizer")
        
        # Extract patient info from Agent 1 and map field names correctly
        agent1_patient_info = agent1_output.get("patient_info", {})
        
        # FIXED: Map field names to what DashboardSynthesizer expects
        mapped_patient_info = {
            "name": agent1_patient_info.get("first_name", "Unknown"),  # first_name → name
            "cultural_heritage": agent1_patient_info.get("cultural_heritage", ""),
            "age": agent1_patient_info.get("current_age", 0),  # current_age → age
            "birth_year": agent1_patient_info.get("birth_year"),
            "age_group": agent1_patient_info.get("age_group", "senior")
        }
        
        # Extract theme info and map correctly
        theme_info = agent1_output.get("theme_info", {})
        daily_theme = theme_info.get("name", "Universal")
        
        # Extract and map content from each agent
        music_data = agent4a_output.get("music_content", {})
        recipe_data = agent4b_output.get("recipe_content", {})
        
        # FIXED: Map photo content fields correctly
        agent4c_photo_data = agent4c_output.get("photo_content", {})
        photo_data = {
            "filename": agent4c_photo_data.get("image_name", agent4c_photo_data.get("filename", "")),  # image_name OR filename
            "description": agent4c_photo_data.get("description", ""),
            "cultural_context": agent4c_photo_data.get("cultural_context", agent4c_photo_data.get("heritage_connection", "")),
            "conversation_starters": agent4c_photo_data.get("conversation_starters", [])
        }
        
        # If photo_data is still empty, try to get theme photo
        if not photo_data["filename"]:
            photo_data["filename"] = theme_info.get("photo_filename", "")
        
        # FIXED: Extract and convert nostalgia news data structure
        agent5_nostalgia_raw = agent5_output.get("nostalgia_news", {})
        
        # Convert complex Agent 5 structure to simple Agent 6 structure
        nostalgia_data = self._convert_nostalgia_structure(agent5_nostalgia_raw, mapped_patient_info["name"])
        
        # Create the final enhanced profile with correct structure
        final_profile = {
            # FIXED: Use mapped patient_info with correct field names
            "patient_info": mapped_patient_info,
            
            # Theme information
            "daily_theme": daily_theme,
            "theme_info": theme_info,
            
            # Content from agents 4A/4B/4C/5
            "music_content": music_data,
            "recipe_content": recipe_data,
            "photo_content": photo_data,
            "nostalgia_news": nostalgia_data,  # FIXED: Converted structure
            
            # Additional data for analysis
            "photo_analysis": agent2_output.get("photo_analysis", {}),
            "qloo_intelligence": agent3_output.get("qloo_intelligence", {}),
            
            # Feedback and session info
            "feedback_info": agent1_output.get("feedback_info", {}),
            "session_metadata": agent1_output.get("session_metadata", {}),
            
            # Pipeline state
            "pipeline_state": {
                "current_step": "dashboard_synthesis",
                "agents_completed": ["1", "2", "3", "4A", "4B", "4C", "5"],
                "next_step": "complete",
                "ready_for_synthesis": True,
                "all_content_available": True
            }
        }
        
        # Safe fallback: ensure required keys exist for Agent 6
        safe_fallbacks = {
            "music_content": {},
            "recipe_content": {},
            "photo_content": {"filename": "", "description": "", "conversation_starters": []},
            "nostalgia_news": {"headline": "", "content": "", "conversation_starters": []},
            "patient_info": {"name": "Unknown", "cultural_heritage": "", "age": 0},
            "qloo_intelligence": {}
        }
        
        for key, fallback_value in safe_fallbacks.items():
            if key not in final_profile or not final_profile[key]:
                final_profile[key] = fallback_value
                logger.warning(f"⚠️ Added safe fallback for {key}")
        
        # Log the mapping for debugging
        logger.info("✅ Final enhanced profile created successfully")
        logger.info(f"   Patient: {mapped_patient_info['name']} (age: {mapped_patient_info['age']})")
        logger.info(f"   Theme: {daily_theme}")
        logger.info(f"   Music: {music_data.get('artist', 'N/A')}")
        logger.info(f"   Recipe: {recipe_data.get('name', 'N/A')}")
        logger.info(f"   Photo: {photo_data.get('filename', 'N/A')}")
        logger.info(f"   News: {nostalgia_data.get('headline', 'N/A')}")
        
        return final_profile
    
    def _convert_nostalgia_structure(self, agent5_data: Dict[str, Any], patient_name: str) -> Dict[str, Any]:
        """
        FIXED: Convert complex Agent 5 nostalgia structure to simple Agent 6 format
        
        Agent 5 outputs: {"title": ..., "sections": {...}, "conversation_questions": [...]}
        Agent 6 expects: {"headline": ..., "content": ..., "conversation_starters": [...]}
        """
        
        if not agent5_data:
            return {"headline": "", "content": "", "conversation_starters": []}
        
        # Extract title as headline
        headline = agent5_data.get("title", f"{patient_name}'s Special Day")
        
        # Convert complex sections to simple content
        sections = agent5_data.get("sections", {})
        content_parts = []
        
        # Extract content from different sections
        if "on_this_day" in sections:
            content_parts.append(sections["on_this_day"].get("content", ""))
        
        if "era_spotlight" in sections:
            content_parts.append(sections["era_spotlight"].get("content", ""))
            
        if "heritage_traditions" in sections:
            content_parts.append(sections["heritage_traditions"].get("content", ""))
        
        # Join all content with proper spacing
        content = " ".join([part for part in content_parts if part]).strip()
        if not content:
            content = f"Today is a special day filled with wonderful memories and traditions, {patient_name}!"
        
        # Extract conversation starters
        conversation_starters = []
        
        # Get from conversation_questions field
        questions = agent5_data.get("conversation_questions", [])
        if isinstance(questions, list):
            conversation_starters.extend(questions)
        
        # Get from conversation_corner if it exists
        corner = sections.get("conversation_corner", {})
        if "questions" in corner:
            corner_questions = corner["questions"]
            if isinstance(corner_questions, list):
                conversation_starters.extend(corner_questions)
        
        # Fallback conversation starters if none found
        if not conversation_starters:
            conversation_starters = [
                f"What's your favorite holiday memory, {patient_name}?",
                "Tell me about a special tradition your family had",
                "What always makes you smile when you think back?"
            ]
        
        # Extract themes if available
        themes = agent5_data.get("themes", [])
        if not themes:
            themes = ["memories", "traditions", "family"]
        
        return {
            "headline": headline,
            "content": content,
            "themes": themes,
            "conversation_starters": conversation_starters[:3]  # Limit to 3
        }
    
    def _create_fallback_music(self) -> Dict[str, Any]:
        """Create fallback music content"""
        
        return {
            "music_content": {
                "artist": "Classical Music",
                "piece_title": "Beautiful Melodies",
                "youtube_url": "",
                "fun_fact": "Music brings joy to the heart",
                "conversation_starters": [
                    "What music do you enjoy?",
                    "Do you have a favorite song?"
                ]
            },
            "metadata": {
                "heritage_match": False,
                "selection_method": "emergency_fallback",
                "agent": "4A_fallback"
            }
        }
    
    def _create_fallback_recipe(self) -> Dict[str, Any]:
        """Create fallback recipe content"""
        
        return {
            "recipe_content": {
                "name": "Comfort Food",
                "ingredients": ["Simple ingredients", "Love", "Care"],
                "instructions": ["Prepare with love", "Share with family"],
                "heritage_tags": ["comfort"],
                "theme_tags": ["family"],
                "fun_fact": "Food made with love tastes the best",
                "conversation_starters": [
                    "What's your favorite comfort food?",
                    "Do you enjoy cooking?"
                ]
            },
            "metadata": {
                "heritage_match": False,
                "theme_match": False,
                "selection_method": "emergency_fallback",
                "agent": "4B_fallback"
            }
        }
    
    def _create_fallback_photo_description(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback photo description"""
        
        theme_info = agent1_output.get("theme_info", {})
        theme_name = theme_info.get("name", "Memory")
        photo_filename = theme_info.get("photo_filename", "default.png")
        
        return {
            "photo_content": {
                "image_name": photo_filename,
                "theme": theme_name,
                "description": f"A special moment celebrating {theme_name.lower()}",
                "heritage_connection": "Universal human experiences",
                "era_context": "Timeless memories",
                "conversation_starters": [
                    "What does this photo remind you of?",
                    "Share a story from the good old days"
                ]
            },
            "metadata": {
                "heritage_match": False,
                "theme_match": True,
                "selection_method": "emergency_fallback",
                "agent": "4C_fallback"
            }
        }
    
    def _create_fallback_nostalgia_news(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback nostalgia news content - ENHANCED"""
        
        patient_info = agent1_output.get("patient_info", {})
        theme_info = agent1_output.get("theme_info", {})
        
        patient_name = patient_info.get("first_name", "Friend")
        theme_name = theme_info.get("name", "Memory Lane")
        cultural_heritage = patient_info.get("cultural_heritage", "")
        
        # Create rich fallback content based on theme
        if "holiday" in theme_name.lower():
            headline = f"Holiday Memories Bring Joy to {patient_name}"
            content = f"The holiday season has always been a time of special gatherings and cherished traditions. {patient_name}, your holiday memories are filled with the warmth of family, the joy of celebrations, and the magic of special moments shared with loved ones."
            themes = ["family", "traditions", "celebrations", "joy"]
        elif "travel" in theme_name.lower():
            headline = f"Adventures and Journeys with {patient_name}"  
            content = f"Travel opens our hearts to new experiences and creates memories that last a lifetime. {patient_name}, your journeys have taken you to wonderful places and introduced you to amazing people along the way."
            themes = ["adventure", "discovery", "experiences", "journeys"]
        else:
            headline = f"Beautiful Memories from {theme_name}"
            content = f"Life's most precious moments come from the simple joys we share together. {patient_name}, your memories from {theme_name.lower()} remind us of the beauty in everyday moments and the love that surrounds us."
            themes = ["memories", "joy", "love", "life"]
        
        # Add cultural context if available
        if cultural_heritage and cultural_heritage != "American":
            content += f" Your {cultural_heritage} heritage has enriched these experiences with wonderful traditions and cultural wisdom."
            themes.append("heritage")
        
        return {
            "nostalgia_news": {
                "headline": headline,
                "content": content,
                "themes": themes,
                "conversation_starters": [
                    f"What's your favorite memory from {theme_name.lower()}, {patient_name}?",
                    "Tell me about a special moment that always makes you smile",
                    "What traditions were most important to your family?"
                ],
                "metadata": {
                    "generation_method": "enhanced_fallback",
                    "personalized": True,
                    "agent": "5_fallback",
                    "cultural_context": cultural_heritage
                }
            }
        }

# Export the main class
__all__ = ["SequentialAgent"]