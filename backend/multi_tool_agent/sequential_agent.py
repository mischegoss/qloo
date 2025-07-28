"""
Enhanced Sequential Agent with 6-Agent Pipeline + Nostalgia News - ANONYMIZED PROFILE COMPATIBLE
File: backend/multi_tool_agent/sequential_agent.py

CRITICAL FIXES FOR PII COMPLIANCE:
- Updated to work with anonymized profile format (no names, no location)
- Fixed field mapping for age_group, cultural_heritage, interests
- Removed all PII references in fallbacks and data flow
- Added anonymized profile validation
- Maintains full functionality with privacy compliance
- FIXED: Removed age calculation method that was causing AttributeError
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Enhanced Sequential Agent with 6-Agent Pipeline - PII COMPLIANT
    
    UPDATED: Works with anonymized profiles only - no names, no location data
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
        
        logger.info(f"🤖 PII-Compliant Sequential Agent initialized with {len(self.agents_available)}/8 agents")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete 6-agent pipeline with anonymized profile
        
        Args:
            patient_profile: ANONYMIZED patient information (no PII)
            request_type: Type of request
            session_id: Session identifier
            feedback_data: User feedback data
            
        Returns:
            Complete dashboard with Nostalgia News (PII-compliant)
        """
        
        logger.info("🚀 Starting PII-compliant 6-agent pipeline with Nostalgia News")
        logger.info(f"📋 Pipeline: Info → Photo → Qloo → Content(4A/4B/4C) → Nostalgia News → Dashboard")
        
        # VALIDATE ANONYMIZED PROFILE
        if not self._validate_anonymized_profile(patient_profile):
            logger.error("🚨 Profile validation failed - contains PII or invalid format")
            return {"success": False, "error": "Profile contains PII or invalid format"}
        
        try:
            # ===== AGENT 1: Information Consolidator =====
            if not self.agent1:
                return {"success": False, "error": "Agent 1 (Information Consolidator) not available"}
            
            logger.info("📋 Running Agent 1: Information Consolidator (PII-compliant)")
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
            
            logger.info("🎯 Running Agent 3: Qloo Cultural Intelligence (PII-compliant)")
            agent3_output = await self.agent3.run(agent1_output, agent2_output)
            
            if not agent3_output:
                logger.warning("⚠️ Agent 3 failed, using fallback cultural data")
                agent3_output = {"qloo_intelligence": {"cultural_recommendations": {}, "metadata": {"fallback_used": True}}}
            
            logger.info("✅ Agent 3 completed")
            
            # ===== AGENTS 4A, 4B, 4C: Content Generation (Parallel) =====
            logger.info("🎨 Running Agents 4A/4B/4C: Content Generation (parallel, PII-compliant)")
            
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
            
            logger.info("📰 Running Agent 5: Nostalgia News Generator (STAR FEATURE, PII-compliant)")
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
            
            logger.info("✅ Agent 5 completed - PII-compliant Nostalgia News generated!")
            
            # ===== AGENT 6: Dashboard Synthesizer =====
            if not self.agent6:
                return {"success": False, "error": "Agent 6 (Dashboard Synthesizer) not available"}
            
            logger.info("🎨 Running Agent 6: Dashboard Synthesizer (Final Assembly, PII-compliant)")
            
            # Create final enhanced profile that combines ALL agent outputs
            final_enhanced_profile = self._create_final_enhanced_profile(
                agent1_output, agent2_output, agent3_output,
                agent4a_output, agent4b_output, agent4c_output, agent5_output
            )
            
            # Call Agent 6 with single enhanced profile parameter
            final_dashboard = await self.agent6.run(final_enhanced_profile)
            
            if not final_dashboard:
                return {"success": False, "error": "Dashboard synthesis failed"}
            
            logger.info("✅ Agent 6 completed - PII-compliant final dashboard assembled!")
            
            # ===== PIPELINE SUCCESS =====
            logger.info("🎉 Complete PII-compliant 6-agent pipeline executed successfully!")
            logger.info("📰 Dashboard includes personalized Nostalgia News (no PII)!")
            
            # Add pipeline metadata
            final_dashboard["pipeline_metadata"] = {
                **final_dashboard.get("pipeline_metadata", {}),
                "agents_executed": len(self.agents_available),
                "execution_timestamp": datetime.now().isoformat(),
                "pipeline_version": "6_agent_nostalgia_news_pii_compliant",
                "star_feature": "nostalgia_news_generator",
                "cultural_intelligence": "qloo_powered",
                "personalization": "gemini_enhanced",
                "pii_compliant": True,
                "anonymized_profile": True,
                "agents_summary": {
                    "agent1": "Information consolidation with theme selection (anonymized)",
                    "agent2": "Simple photo analysis (theme-based)",
                    "agent3": "Qloo cultural intelligence (heritage-driven, PII-compliant)",
                    "agent4a": "Music curation with YouTube integration",
                    "agent4b": "Recipe selection (microwave-safe)",
                    "agent4c": "Photo description with cultural context",
                    "agent5": "Nostalgia News generation (Gemini AI, PII-compliant)",
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
    
    def _validate_anonymized_profile(self, patient_profile: Dict[str, Any]) -> bool:
        """
        Validate that profile is properly anonymized and contains no PII
        """
        
        # Check for PII fields that should not be present
        pii_fields = ["first_name", "last_name", "name", "full_name", "email", "phone", 
                     "address", "city", "state", "zip_code", "coordinates"]
        
        detected_pii = [field for field in pii_fields if patient_profile.get(field)]
        
        if detected_pii:
            logger.error(f"🚨 PII detected in profile: {detected_pii}")
            return False
        
        # Check for required anonymized fields
        required_fields = ["cultural_heritage", "age_group"]
        missing_fields = [field for field in required_fields if not patient_profile.get(field)]
        
        if missing_fields:
            logger.error(f"🚨 Missing required anonymized fields: {missing_fields}")
            return False
        
        logger.info("✅ Profile anonymization validation passed")
        return True
    
    def _create_enhanced_profile(self, agent1_output: Dict[str, Any], 
                                agent2_output: Dict[str, Any],
                                agent3_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced profile for content agents (4A/4B/4C) - PII COMPLIANT"""
        
        # Start with Agent 1 output
        enhanced_profile = agent1_output.copy()
        
        # Extract anonymized patient info safely
        patient_info = enhanced_profile.get("patient_info", {})
        cultural_heritage = patient_info.get("cultural_heritage", "American")
        age_group = patient_info.get("age_group", "senior")
        
        # Add heritage to multiple places for maximum compatibility
        enhanced_profile["cultural_heritage"] = cultural_heritage
        enhanced_profile["heritage"] = cultural_heritage
        enhanced_profile["age_group"] = age_group
        
        # Ensure patient_info has complete anonymized info with all possible field names
        if "patient_info" in enhanced_profile:
            enhanced_profile["patient_info"]["heritage"] = cultural_heritage
            enhanced_profile["patient_info"]["cultural_background"] = cultural_heritage
            enhanced_profile["patient_info"]["cultural_heritage"] = cultural_heritage
            enhanced_profile["patient_info"]["age_group"] = age_group
        
        # CRITICAL: Add debug logging to track heritage flow (no PII)
        logger.info(f"✅ Enhanced profile created with anonymized data:")
        logger.info(f"   Heritage: '{cultural_heritage}', Age group: '{age_group}'")
        logger.info(f"   Heritage available in: patient_info.cultural_heritage, heritage, cultural_heritage")
        
        # Add photo analysis from Agent 2
        enhanced_profile["photo_analysis"] = agent2_output.get("photo_analysis", {})
        
        # Add Qloo intelligence from Agent 3
        enhanced_profile["qloo_intelligence"] = agent3_output.get("qloo_intelligence", {})
        
        # Add pipeline state
        enhanced_profile["pipeline_state"] = {
            "current_step": "content_generation",
            "agents_completed": ["1", "2", "3"],
            "next_agents": ["4A", "4B", "4C"],
            "ready_for_content": True,
            "pii_compliant": True
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
        Create final enhanced profile combining ALL agent outputs for Agent 6 - PII COMPLIANT
        """
        
        logger.info("🔄 Creating PII-compliant final enhanced profile for Dashboard Synthesizer")
        
        # Extract anonymized patient info from Agent 1
        agent1_patient_info = agent1_output.get("patient_info", {})
        
        # FIXED: Create mapped patient info without age calculation - use age_group only
        mapped_patient_info = {
            # REMOVED: "name" field (PII) - use generic identifier
            "display_name": "Friend",  # Generic, non-identifying name for UI
            "cultural_heritage": agent1_patient_info.get("cultural_heritage", "American"),
            "age_group": agent1_patient_info.get("age_group", "senior")
            # REMOVED: "age" field calculation that was causing the error
        }
        
        # Extract theme info and map correctly
        theme_info = agent1_output.get("theme_info", {})
        daily_theme = theme_info.get("name", "Universal")
        
        # Extract and map content from each agent
        music_data = agent4a_output.get("music_content", {})
        recipe_data = agent4b_output.get("recipe_content", {})
        
        # Map photo content fields correctly with theme filename priority
        agent4c_photo_data = agent4c_output.get("photo_content", {})
        
        # Ensure theme photo filename is preserved for UI
        theme_photo_filename = theme_info.get("photo_filename", "")
        agent_photo_filename = agent4c_photo_data.get("image_name", agent4c_photo_data.get("filename", ""))
        
        # Priority: Theme photo filename (for UI consistency) > Agent photo filename
        correct_filename = theme_photo_filename if theme_photo_filename else agent_photo_filename
        
        photo_data = {
            "filename": correct_filename,
            "description": agent4c_photo_data.get("description", ""),
            "cultural_context": agent4c_photo_data.get("cultural_context", agent4c_photo_data.get("heritage_connection", "")),
            "conversation_starters": agent4c_photo_data.get("conversation_starters", [])
        }
        
        # Debug logging for photo filename (no PII)
        logger.info(f"📷 Photo filename mapping:")
        logger.info(f"   Theme photo: {theme_photo_filename}")
        logger.info(f"   Agent photo: {agent_photo_filename}")
        logger.info(f"   Final photo: {correct_filename}")
        
        # Final fallback if still empty
        if not photo_data["filename"]:
            photo_data["filename"] = f"{daily_theme.lower().replace(' ', '_')}.png"
            logger.warning(f"⚠️ Using theme-based fallback filename: {photo_data['filename']}")
        
        # Extract nostalgia news data structure (PASS THROUGH SECTIONS)
        agent5_nostalgia_raw = agent5_output.get("nostalgia_news", {})
        nostalgia_data = agent5_nostalgia_raw if agent5_nostalgia_raw else self._create_empty_nostalgia_sections()
        
        # Create the final enhanced profile with correct structure - PII COMPLIANT
        final_profile = {
            # FIXED: Use mapped patient_info with anonymized fields only (no age field)
            "patient_info": mapped_patient_info,
            
            # Theme information
            "daily_theme": daily_theme,
            "theme_info": theme_info,
            
            # Content from agents 4A/4B/4C/5
            "music_content": music_data,
            "recipe_content": recipe_data,
            "photo_content": photo_data,
            "nostalgia_news": nostalgia_data,
            
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
                "all_content_available": True,
                "pii_compliant": True
            }
        }
        
        # Safe fallbacks: ensure required keys exist for Agent 6
        safe_fallbacks = {
            "music_content": {},
            "recipe_content": {},
            "photo_content": {"filename": "", "description": "", "conversation_starters": []},
            "nostalgia_news": self._create_empty_nostalgia_sections(),
            "patient_info": {"display_name": "Friend", "cultural_heritage": "American", "age_group": "senior"},
            "qloo_intelligence": {}
        }
        
        for key, fallback_value in safe_fallbacks.items():
            if key not in final_profile or not final_profile[key]:
                final_profile[key] = fallback_value
                logger.warning(f"⚠️ Added safe fallback for {key}")
        
        # Log the mapping for debugging (no PII)
        logger.info("✅ PII-compliant final enhanced profile created successfully")
        logger.info(f"   Display: {mapped_patient_info['display_name']} (age group: {mapped_patient_info['age_group']})")
        logger.info(f"   Heritage: {mapped_patient_info['cultural_heritage']}")
        logger.info(f"   Theme: {daily_theme}")
        logger.info(f"   Music: {music_data.get('artist', 'N/A')}")
        logger.info(f"   Recipe: {recipe_data.get('name', 'N/A')}")
        logger.info(f"   Photo: {photo_data.get('filename', 'N/A')}")
        logger.info(f"   News: {nostalgia_data.get('title', 'N/A')}")
        
        return final_profile

    
    def _create_empty_nostalgia_sections(self) -> Dict[str, Any]:
        """Create empty nostalgia news with sections structure - PII COMPLIANT"""
        
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
        """Create fallback music content - PII COMPLIANT"""
        
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
                "agent": "4A_fallback",
                "pii_compliant": True
            }
        }
    
    def _create_fallback_recipe(self) -> Dict[str, Any]:
        """Create fallback recipe content - PII COMPLIANT"""
        
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
                "agent": "4B_fallback",
                "pii_compliant": True
            }
        }
    
    def _create_fallback_photo_description(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback photo description - PII COMPLIANT"""
        
        theme_info = agent1_output.get("theme_info", {})
        theme_name = theme_info.get("name", "Memory")
        theme_id = theme_info.get("id", "memory_lane")
        
        # Use theme-based photo filename
        photo_filename = theme_info.get("photo_filename", f"{theme_id.lower()}.png")
        
        logger.info(f"🔄 Creating PII-compliant fallback photo description for theme: {theme_name}")
        logger.info(f"📷 Using photo filename: {photo_filename}")
        
        return {
            "photo_content": {
                "image_name": photo_filename,
                "filename": photo_filename,
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
                "filename_source": "theme_based",
                "pii_compliant": True
            }
        }
    
    def _create_fallback_nostalgia_news(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create fallback nostalgia news with new sections structure - PII COMPLIANT
        """
        
        patient_info = agent1_output.get("patient_info", {})
        theme_info = agent1_output.get("theme_info", {})
        
        # FIXED: No longer use patient names - use generic approach
        theme_name = theme_info.get("name", "Memory Lane")
        cultural_heritage = patient_info.get("cultural_heritage", "American")
        age_group = patient_info.get("age_group", "senior")
        
        logger.info(f"🔄 Creating PII-compliant fallback nostalgia news with sections structure")
        logger.info(f"   Theme: {theme_name}, Heritage: {cultural_heritage}, Age group: {age_group}")
        
        # Create newsletter-style content based on theme (no personal references)
        if "holiday" in theme_name.lower():
            memory_content = "Remember those wonderful holiday celebrations when families gathered together? The warmth of the season brought everyone closer, creating memories filled with joy, laughter, and cherished traditions."
            era_content = "Back in the 1940s and 50s, holiday seasons were magical times filled with homemade decorations, family recipes, and the gentle sounds of holiday music playing in the background."
            heritage_content = f"Holiday traditions have always brought families together, and {cultural_heritage} families created their own special ways of celebrating that honored both old customs and new traditions."
            themes = ["holidays", "family", "traditions", "celebrations"]
        elif "travel" in theme_name.lower():
            memory_content = "Remember those exciting family trips and adventures? Travel has always opened hearts to new experiences, creating lasting memories of discovery and the joy of exploring new places together."
            era_content = "In past decades, family travel was a grand adventure filled with scenic drives, roadside diners, and the excitement of seeing new places. Every journey was an opportunity to create stories that would be shared for years to come."
            heritage_content = f"Travel traditions often reflected cultural heritage, with {cultural_heritage} families bringing their own perspectives to exploration and creating unique travel experiences that honored their roots."
            themes = ["travel", "adventure", "discovery", "family"]
        else:
            memory_content = f"Remember those beautiful moments celebrating {theme_name.lower()}? Life's most precious memories come from the simple joys shared together, creating connections that warm the heart for years to come."
            era_content = f"In those wonderful days, {theme_name.lower()} was celebrated with family gatherings, community events, and traditions that brought people together in joy and celebration."
            heritage_content = f"Every family brought their own special traditions to {theme_name.lower()}, and {cultural_heritage} families created unique cultural experiences that honored their heritage while embracing new traditions."
            themes = ["memories", "joy", "family", "traditions"]
        
        # Create the new sections structure - NO PERSONAL INFORMATION
        nostalgia_news = {
            "title": f"Nostalgia News – {datetime.now().strftime('%B %d')}",
            "subtitle": f"{theme_name} Edition", 
            "date": datetime.now().strftime("%B %d, %Y"),
            # REMOVED: "personalized_for" field (PII)
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
                "age_group": age_group,
                "safety_level": "dementia_friendly",
                "structure_verified": True,
                "sections_count": 4,
                "newsletter_tone": True,
                "pii_compliant": True,
                "anonymized": True
            }
        }
        
        logger.info("✅ PII-compliant fallback nostalgia news with sections structure created")
        logger.info(f"   Sections: {list(nostalgia_news['sections'].keys())}")
        
        return {
            "nostalgia_news": nostalgia_news
        }

# Export the main class
__all__ = ["SequentialAgent"]