"""
Updated Sequential Agent - 6 Agent Pipeline with Nostalgia News
File: backend/multi_tool_agent/sequential_agent.py

UPDATED PIPELINE:
Agent 1: Information Consolidator (profile, theme, feedback)
Agent 2: Simple Photo Analysis (theme → photo analysis)
Agent 3: Qloo Cultural Intelligence (heritage → artists, preferences)
Agents 4A/4B/4C: Content Generation (music, recipe, photo description) [parallel]
Agent 5: Nostalgia News Generator (Gemini cultural storytelling)
Agent 6: Dashboard Synthesizer (final assembly)
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SequentialAgent:
    """
    Updated Sequential Agent with 6-agent pipeline including Nostalgia News.
    
    PIPELINE FLOW:
    1. Information Consolidator → 2. Photo Analysis → 3. Qloo Intelligence 
    → 4A/4B/4C (parallel) → 5. Nostalgia News → 6. Dashboard Synthesizer
    """
    
    def __init__(self, 
                 agent1=None,  # Information Consolidator
                 agent2=None,  # Simple Photo Analysis  
                 agent3=None,  # Qloo Cultural Intelligence
                 agent4a=None, # Music Curation
                 agent4b=None, # Recipe Selection
                 agent4c=None, # Photo Description
                 agent5=None,  # Nostalgia News Generator
                 agent6=None): # Dashboard Synthesizer
        
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent3 = agent3
        self.agent4a = agent4a
        self.agent4b = agent4b
        self.agent4c = agent4c
        self.agent5 = agent5
        self.agent6 = agent6
        
        self.agents_available = [
            f"Agent {i}" for i, agent in enumerate([agent1, agent2, agent3, agent4a, agent4b, agent4c, agent5, agent6], 1)
            if agent is not None
        ]
        
        logger.info(f"Sequential Agent initialized with: {', '.join(self.agents_available)}")
        logger.info("🌟 NEW: Features Nostalgia News Generator with Gemini AI")
        logger.info("📰 Star Feature: Personalized cultural storytelling")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: str = "default",
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete 6-agent pipeline with Nostalgia News generation.
        
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
            final_dashboard = await self.agent6.run(
                agent1_output=agent1_output,
                agent2_output=agent2_output,
                agent3_output=agent3_output,
                agent4a_output=agent4a_output,
                agent4b_output=agent4b_output,
                agent4c_output=agent4c_output,
                agent5_output=agent5_output
            )
            
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
        """Create enhanced profile for content agents (4A/4B/4C)"""
        
        # Start with Agent 1 output
        enhanced_profile = agent1_output.copy()
        
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
                    "Tell me about a special memory"
                ]
            },
            "metadata": {
                "theme_match": True,
                "cultural_enhancement": False,
                "selection_method": "emergency_fallback",
                "agent": "4C_fallback"
            }
        }
    
    def _create_fallback_nostalgia_news(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback nostalgia news"""
        
        patient_info = agent1_output.get("patient_info", {})
        first_name = patient_info.get("first_name", "Friend")
        current_date = datetime.now().strftime("%B %d")
        
        return {
            "nostalgia_news": {
                "title": f"{first_name}'s Nostalgia News for {current_date}",
                "subtitle": "Special Edition",
                "date": datetime.now().strftime("%B %d, %Y"),
                "personalized_for": first_name,
                "sections": {
                    "message": {
                        "headline": "✨ Today's Special Message",
                        "content": f"Every day brings new opportunities for joy and connection, {first_name}. Your stories and memories are treasured."
                    },
                    "conversation_corner": {
                        "headline": "💭 Let's Talk",
                        "questions": [
                            f"What made you smile today, {first_name}?",
                            "What's a happy memory you'd like to share?",
                            "What are you grateful for today?"
                        ]
                    }
                },
                "metadata": {
                    "generated_by": "emergency_fallback",
                    "generation_timestamp": datetime.now().isoformat(),
                    "safety_level": "dementia_friendly"
                }
            }
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents in the pipeline"""
        
        agent_status = {
            "agent1_information_consolidator": self.agent1 is not None,
            "agent2_simple_photo_analysis": self.agent2 is not None,
            "agent3_qloo_cultural_intelligence": self.agent3 is not None,
            "agent4a_music_curation": self.agent4a is not None,
            "agent4b_recipe_selection": self.agent4b is not None,
            "agent4c_photo_description": self.agent4c is not None,
            "agent5_nostalgia_news_generator": self.agent5 is not None,
            "agent6_dashboard_synthesizer": self.agent6 is not None
        }
        
        total_agents = len([agent for agent in agent_status.values() if agent])
        
        return {
            "total_agents_available": total_agents,
            "all_agents_ready": total_agents == 8,
            "agents": agent_status,
            "pipeline_mode": "6_agent_nostalgia_news",
            "star_feature": "nostalgia_news_generator",
            "ready_for_execution": total_agents >= 6,  # Minimum viable pipeline
            "pipeline_description": "Info → Photo → Qloo → Content(4A/4B/4C) → Nostalgia News → Dashboard"
        }

# Export the main class
__all__ = ["SequentialAgent"]