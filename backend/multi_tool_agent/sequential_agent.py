"""
Enhanced Sequential Agent with 6-Agent Pipeline + Nostalgia News
File: backend/multi_tool_agent/sequential_agent.py

FIXED: Updated Agent 5 nostalgia news structure handling
- Agent 5 now returns proper sections format
- Updated _convert_nostalgia_structure to handle sections
- Maintains all existing functionality
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Enhanced Sequential Agent with 6-Agent Pipeline
    
    FIXED: Updated nostalgia news structure handling for sections format
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
        
        # Ensure patient_info has complete heritage info with all possible field names
        if "patient_info" in enhanced_profile:
            enhanced_profile["patient_info"]["heritage"] = cultural_heritage
            enhanced_profile["patient_info"]["cultural_background"] = cultural_heritage
            # Keep the original field name too
            enhanced_profile["patient_info"]["cultural_heritage"] = cultural_heritage
        
        # CRITICAL: Add debug logging to track heritage flow
        logger.info(f"✅ Enhanced profile created with heritage: '{cultural_heritage}'")
        logger.info(f"   Heritage available in: patient_info.cultural_heritage, patient_info.heritage, heritage, cultural_heritage")
        
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
        
        # FIXED: Map photo content fields correctly with theme filename priority
        agent4c_photo_data = agent4c_output.get("photo_content", {})
        
        # CRITICAL FIX: Ensure theme photo filename is preserved for UI
        theme_photo_filename = theme_info.get("photo_filename", "")
        agent_photo_filename = agent4c_photo_data.get("image_name", agent4c_photo_data.get("filename", ""))
        
        # Priority: Theme photo filename (for UI consistency) > Agent photo filename
        correct_filename = theme_photo_filename if theme_photo_filename else agent_photo_filename
        
        photo_data = {
            "filename": correct_filename,  # FIXED: Use correct theme-based filename
            "description": agent4c_photo_data.get("description", ""),
            "cultural_context": agent4c_photo_data.get("cultural_context", agent4c_photo_data.get("heritage_connection", "")),
            "conversation_starters": agent4c_photo_data.get("conversation_starters", [])
        }
        
        # Debug logging for photo filename
        logger.info(f"📷 Photo filename mapping:")
        logger.info(f"   Theme photo: {theme_photo_filename}")
        logger.info(f"   Agent photo: {agent_photo_filename}")
        logger.info(f"   Final photo: {correct_filename}")
        
        # Final fallback if still empty
        if not photo_data["filename"]:
            photo_data["filename"] = f"{daily_theme.lower().replace(' ', '_')}.png"
            logger.warning(f"⚠️ Using theme-based fallback filename: {photo_data['filename']}")
        
        # FIXED: Extract nostalgia news data structure (PASS THROUGH SECTIONS)
        agent5_nostalgia_raw = agent5_output.get("nostalgia_news", {})
        
        # CRITICAL FIX: Don't convert! Pass through the sections structure directly
        # The frontend expects the sections format, not the old flat format
        nostalgia_data = agent5_nostalgia_raw if agent5_nostalgia_raw else self._create_empty_nostalgia_sections()
        
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
            "nostalgia_news": self._create_empty_nostalgia_sections(),  # FIXED: Use sections structure
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
        FIXED: Convert new Agent 5 sections structure to Agent 6 format
        
        Agent 5 NEW output: {"title": ..., "sections": {"memory_spotlight": {...}, "era_highlights": {...}, ...}, "themes": [...]}
        Agent 6 expects: {"headline": ..., "content": ..., "conversation_starters": [...], "themes": [...]}
        """
        
        if not agent5_data:
            return {"headline": "", "content": "", "conversation_starters": [], "themes": []}
        
        logger.info("🔄 Converting Agent 5 sections structure to Agent 6 format")
        logger.info(f"   Agent 5 keys: {list(agent5_data.keys())}")
        
        # Extract title as headline
        headline = agent5_data.get("title", f"Today's Special News")
        
        # Extract sections and convert to content
        sections = agent5_data.get("sections", {})
        content_parts = []
        
        logger.info(f"   Sections found: {list(sections.keys()) if sections else 'None'}")
        
        # Extract content from different sections in logical order
        section_order = ["memory_spotlight", "era_highlights", "heritage_traditions"]
        
        for section_name in section_order:
            if section_name in sections:
                section_data = sections[section_name]
                if isinstance(section_data, dict):
                    section_content = section_data.get("content", "")
                    if section_content:
                        content_parts.append(section_content)
                        logger.info(f"   Added content from {section_name}: {len(section_content)} chars")
        
        # Join all content with proper spacing
        content = " ".join(content_parts).strip()
        if not content:
            content = f"Today brings wonderful opportunities for meaningful moments and beautiful memories that enrich our lives."
            logger.warning("⚠️ No content found in sections, using fallback")
        
        # Extract conversation starters
        conversation_starters = []
        
        # Get from conversation_starters section
        if "conversation_starters" in sections:
            starters_section = sections["conversation_starters"]
            if isinstance(starters_section, dict):
                questions = starters_section.get("questions", [])
                if isinstance(questions, list):
                    conversation_starters.extend(questions)
                    logger.info(f"   Found {len(questions)} conversation starters")
        
        # Fallback conversation starters if none found
        if not conversation_starters:
            conversation_starters = [
                "What brings you joy when you think about those wonderful days?",
                "Tell me about a happy memory from your younger years",
                "What traditions were most important to your family?"
            ]
            logger.warning("⚠️ No conversation starters found, using fallback")
        
        # Extract themes
        themes = agent5_data.get("themes", [])
        if not themes:
            themes = ["memories", "traditions", "heritage"]
            logger.warning("⚠️ No themes found, using fallback")
        
        result = {
            "headline": headline,
            "content": content,
            "themes": themes,
            "conversation_starters": conversation_starters[:3]  # Limit to 3
        }
        
        logger.info("✅ Nostalgia structure conversion completed")
        logger.info(f"   Headline: {headline}")
        logger.info(f"   Content length: {len(content)} chars")
        logger.info(f"   Themes: {themes}")
        logger.info(f"   Conversation starters: {len(conversation_starters)}")
        
        return result
    
    def _create_empty_nostalgia_sections(self) -> Dict[str, Any]:
        """Create empty nostalgia news with sections structure"""
        
        return {
            "title": "Today's Special News",
            "subtitle": "Daily Edition",
            "date": datetime.now().strftime("%B %d, %Y"),
            "sections": {
                "memory_spotlight": {
                    "headline": "📚 Memory Spotlight",
                    "content": "Today brings wonderful opportunities for meaningful moments and beautiful memories.",
                    "fun_fact": "Every day brings new possibilities for joy and connection."
                },
                "era_highlights": {
                    "headline": "🎵 Era Highlights",
                    "content": "Throughout history, music and traditions have brought people together in celebration.",
                    "fun_fact": "Music is a universal language that speaks to every heart."
                },
                "heritage_traditions": {
                    "headline": "🏛️ Heritage Traditions",
                    "content": "Cultural traditions connect us to our roots and enrich our lives with meaning.",
                    "fun_fact": "Every culture has beautiful traditions that celebrate life's important moments."
                },
                "conversation_starters": {
                    "headline": "💬 Conversation Starters",
                    "questions": [
                        "What brings you joy today?",
                        "Tell me about a happy memory",
                        "What traditions are important to you?"
                    ]
                }
            },
            "themes": ["Connection", "Joy", "Memories"]
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
        """Create fallback photo description - FIXED to respect theme filename"""
        
        theme_info = agent1_output.get("theme_info", {})
        theme_name = theme_info.get("name", "Memory")
        theme_id = theme_info.get("id", "memory_lane")
        
        # CRITICAL FIX: Use theme-based photo filename, not hardcoded "default.png"
        photo_filename = theme_info.get("photo_filename", f"{theme_id.lower()}.png")
        
        logger.info(f"🔄 Creating fallback photo description for theme: {theme_name}")
        logger.info(f"📷 Using photo filename: {photo_filename}")
        
        return {
            "photo_content": {
                "image_name": photo_filename,  # FIXED: Use correct theme filename
                "filename": photo_filename,    # FIXED: Add both field names for compatibility
                "theme": theme_name,
                "description": f"A special moment celebrating {theme_name.lower()}",
                "heritage_connection": "Universal human experiences",
                "cultural_context": "Enhanced for cultural relevance",
                "era_context": "Timeless memories",
                "conversation_starters": [
                    "What does this photo remind you of?",
                    "Share a story from the good old days",
                    f"Tell me about a special {theme_name.lower()} memory"
                ]
            },
            "metadata": {
                "heritage_match": False,
                "theme_match": True,
                "selection_method": "emergency_fallback",
                "agent": "4C_fallback",
                "filename_source": "theme_based"
            }
        }
    
    def _create_fallback_nostalgia_news(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Create fallback nostalgia news with new sections structure
        """
        
        patient_info = agent1_output.get("patient_info", {})
        theme_info = agent1_output.get("theme_info", {})
        
        patient_name = patient_info.get("first_name", "Friend")
        theme_name = theme_info.get("name", "Memory Lane")
        cultural_heritage = patient_info.get("cultural_heritage", "")
        
        logger.info(f"🔄 Creating fallback nostalgia news with sections structure")
        logger.info(f"   Theme: {theme_name}, Heritage: {cultural_heritage}")
        
        # Create newsletter-style content based on theme
        if "holiday" in theme_name.lower():
            memory_content = "Remember those wonderful holiday celebrations when families gathered together? The warmth of the season brought everyone closer, creating memories filled with joy, laughter, and cherished traditions."
            era_content = "Back in the 1940s and 50s, holiday seasons were magical times filled with homemade decorations, family recipes, and the gentle sounds of holiday music playing in the background."
            heritage_content = f"Holiday traditions have always brought families together, and {cultural_heritage} families created their own special ways of celebrating that honored both old customs and new American traditions."
            themes = ["holidays", "family", "traditions", "celebrations"]
        elif "travel" in theme_name.lower():
            memory_content = "Remember those exciting family trips and adventures? Travel has always opened our hearts to new experiences, creating lasting memories of discovery and the joy of exploring new places together."
            era_content = "In past decades, family travel was a grand adventure filled with scenic drives, roadside diners, and the excitement of seeing new places. Every journey was an opportunity to create stories that would be shared for years to come."
            heritage_content = f"Travel traditions often reflected cultural heritage, with {cultural_heritage} families bringing their own perspectives to exploration and creating unique travel experiences that honored their roots."
            themes = ["travel", "adventure", "discovery", "family"]
        else:
            memory_content = f"Remember those beautiful moments celebrating {theme_name.lower()}? Life's most precious memories come from the simple joys we share together, creating connections that warm the heart for years to come."
            era_content = f"In those wonderful days, {theme_name.lower()} was celebrated with family gatherings, community events, and traditions that brought people together in joy and celebration."
            heritage_content = f"Every family brought their own special traditions to {theme_name.lower()}, and {cultural_heritage} families created unique cultural experiences that honored their heritage while embracing new traditions."
            themes = ["memories", "joy", "family", "traditions"]
        
        # Create the new sections structure
        nostalgia_news = {
            "title": f"Nostalgia News – {datetime.now().strftime('%B %d')}",
            "subtitle": f"{theme_name} Edition", 
            "date": datetime.now().strftime("%B %d, %Y"),
            "personalized_for": patient_name,
            "sections": {
                "memory_spotlight": {
                    "headline": "📚 Memory Spotlight",
                    "content": memory_content,
                    "fun_fact": "Historical moments create our most treasured memories."
                },
                "era_highlights": {
                    "headline": "🎵 Era Highlights",
                    "content": era_content,
                    "fun_fact": "Music has always been central to life's celebrations."
                },
                "heritage_traditions": {
                    "headline": "🏛️ Heritage Traditions",
                    "content": heritage_content,
                    "fun_fact": "Cultural traditions connect us to our roots."
                },
                "conversation_starters": {
                    "headline": "💬 Conversation Starters",
                    "questions": [
                        f"What memories about {theme_name.lower()} are most special to you?",
                        "Tell me about a wonderful time that always makes you smile",
                        "What traditions were most important to your family?"
                    ]
                }
            },
            "themes": themes,
            "metadata": {
                "generated_by": "sequential_fallback_sections",
                "generation_timestamp": datetime.now().isoformat(),
                "theme_integrated": theme_name,
                "heritage_featured": cultural_heritage,
                "safety_level": "dementia_friendly",
                "structure_verified": True,
                "sections_count": 4,
                "newsletter_tone": True
            }
        }
        
        logger.info("✅ Fallback nostalgia news with sections structure created")
        logger.info(f"   Sections: {list(nostalgia_news['sections'].keys())}")
        
        return {
            "nostalgia_news": nostalgia_news
        }

# Export the main class
__all__ = ["SequentialAgent"]