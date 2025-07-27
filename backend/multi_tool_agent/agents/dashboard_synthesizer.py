"""
Agent 6: Dashboard Synthesizer - Final Assembly Agent
File: backend/multi_tool_agent/agents/dashboard_synthesizer.py

PURPOSE:
- Takes outputs from all 5 previous agents
- Assembles final dashboard structure for UI
- Ensures clean data flow and proper formatting
- Adds final metadata and quality checks
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DashboardSynthesizer:
    """
    Agent 6: Dashboard Synthesizer
    
    Final agent that assembles outputs from Agents 1-5 into the complete 
    dashboard structure for the UI, including the Nostalgia News section.
    """
    
    def __init__(self):
        logger.info("🎨 Agent 6: Dashboard Synthesizer initialized")
    
    async def run(self,
                  agent1_output: Dict[str, Any],
                  agent2_output: Dict[str, Any],
                  agent3_output: Dict[str, Any], 
                  agent4a_output: Dict[str, Any],
                  agent4b_output: Dict[str, Any],
                  agent4c_output: Dict[str, Any],
                  agent5_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize final dashboard from all agent outputs
        
        Args:
            agent1_output: Information consolidator results
            agent2_output: Photo analysis results
            agent3_output: Qloo cultural intelligence
            agent4a_output: Music curation results
            agent4b_output: Recipe selection results
            agent4c_output: Photo description results
            agent5_output: Nostalgia news results
            
        Returns:
            Complete dashboard for UI
        """
        
        logger.info("🎨 Agent 6: Synthesizing final dashboard")
        
        try:
            # Extract theme and profile information
            theme_data = self._extract_theme_data(agent1_output)
            profile_data = self._extract_profile_data(agent1_output)
            
            logger.info(f"🎯 Synthesizing dashboard for: {profile_data['first_name']} - {theme_data['name']}")
            
            # Assemble the three main content tiles
            music_tile = self._create_music_tile(agent4a_output)
            recipe_tile = self._create_recipe_tile(agent4b_output)
            photo_tile = self._create_photo_tile(agent4c_output, agent2_output)
            
            # Get the nostalgia news (star feature)
            nostalgia_news = agent5_output.get("nostalgia_news", {})
            
            # Create final dashboard structure
            dashboard = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                
                # Theme and profile context
                "theme": theme_data,
                "profile": profile_data,
                
                # Main content tiles
                "content_tiles": {
                    "music": music_tile,
                    "recipe": recipe_tile, 
                    "photo": photo_tile
                },
                
                # Star feature - Nostalgia News
                "nostalgia_news": nostalgia_news,
                
                # Dashboard metadata
                "dashboard_metadata": {
                    "agents_executed": 6,
                    "generation_timestamp": datetime.now().isoformat(),
                    "pipeline_version": "5_agent_nostalgia_news",
                    "content_quality": self._assess_content_quality(music_tile, recipe_tile, photo_tile, nostalgia_news),
                    "personalization_level": self._assess_personalization_level(profile_data, nostalgia_news),
                    "cultural_intelligence_used": self._assess_cultural_usage(agent3_output),
                    "safety_level": "dementia_friendly"
                }
            }
            
            # Quality validation
            validation_result = self._validate_dashboard(dashboard)
            dashboard["validation"] = validation_result
            
            logger.info("✅ Agent 6: Final dashboard synthesized successfully")
            self._log_dashboard_summary(dashboard)
            
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            return self._create_emergency_dashboard(agent1_output)
    
    def _extract_theme_data(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Extract clean theme data for dashboard"""
        
        theme_info = agent1_output.get("theme_info", {})
        
        return {
            "id": theme_info.get("id", "unknown"),
            "name": theme_info.get("name", "Memory"), 
            "description": theme_info.get("description", "A special theme for today"),
            "photo_filename": theme_info.get("photo_filename", "default.png")
        }
    
    def _extract_profile_data(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Extract clean profile data for dashboard"""
        
        patient_info = agent1_output.get("patient_info", {})
        
        return {
            "first_name": patient_info.get("first_name", "Friend"),
            "cultural_heritage": patient_info.get("cultural_heritage", "American"),
            "birth_year": patient_info.get("birth_year"),
            "age_group": patient_info.get("age_group", "senior")
        }
    
    def _create_music_tile(self, agent4a_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create music tile from Agent 4A output"""
        
        music_content = agent4a_output.get("music_content", {})
        metadata = agent4a_output.get("metadata", {})
        
        return {
            "type": "music",
            "title": "🎵 Musical Memories",
            "artist": music_content.get("artist", "Classical Artist"),
            "piece": music_content.get("piece_title", "Beautiful Music"),
            "youtube_url": music_content.get("youtube_url", ""),
            "fun_fact": music_content.get("fun_fact", ""),
            "conversation_starters": music_content.get("conversation_starters", [
                "Do you enjoy this type of music?",
                "What music did you listen to when you were younger?"
            ]),
            "metadata": {
                "heritage_match": metadata.get("heritage_match", False),
                "source": metadata.get("selection_method", "fallback"),
                "cultural_connection": metadata.get("cultural_connection", "general")
            }
        }
    
    def _create_recipe_tile(self, agent4b_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create recipe tile from Agent 4B output"""
        
        recipe_content = agent4b_output.get("recipe_content", {})
        metadata = agent4b_output.get("metadata", {})
        
        return {
            "type": "recipe",
            "title": "🍽️ Comfort Kitchen",
            "name": recipe_content.get("name", "Comfort Food"),
            "ingredients": recipe_content.get("ingredients", []),
            "instructions": recipe_content.get("instructions", []),
            "heritage_tags": recipe_content.get("heritage_tags", []),
            "theme_tags": recipe_content.get("theme_tags", []),
            "fun_fact": recipe_content.get("fun_fact", ""),
            "conversation_starters": recipe_content.get("conversation_starters", [
                "Have you made something like this before?",
                "What's your favorite comfort food?"
            ]),
            "metadata": {
                "heritage_match": metadata.get("heritage_match", False),
                "theme_match": metadata.get("theme_match", False),
                "safety_level": "microwave_safe"
            }
        }
    
    def _create_photo_tile(self, agent4c_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create photo tile from Agent 4C and Agent 2 outputs"""
        
        photo_content = agent4c_output.get("photo_content", {})
        photo_analysis = agent2_output.get("photo_analysis", {})
        metadata = agent4c_output.get("metadata", {})
        
        return {
            "type": "photo",
            "title": "📷 Photo of the Day",
            "image_name": photo_content.get("image_name", "default.png"),  # Critical for UI
            "theme": photo_content.get("theme", "Memory"),
            "description": photo_content.get("description", "A special moment in time"),
            "heritage_connection": photo_content.get("heritage_connection", ""),
            "era_context": photo_content.get("era_context", ""),
            "conversation_starters": photo_content.get("conversation_starters", [
                "What does this photo remind you of?",
                "Have you experienced something similar?"
            ]),
            "metadata": {
                "analysis_method": photo_analysis.get("analysis_method", "fallback"),
                "cultural_enhancement": metadata.get("cultural_enhancement", False),
                "theme_match": metadata.get("theme_match", True)
            }
        }
    
    def _assess_content_quality(self, music_tile: Dict[str, Any], 
                               recipe_tile: Dict[str, Any],
                               photo_tile: Dict[str, Any],
                               nostalgia_news: Dict[str, Any]) -> str:
        """Assess overall content quality"""
        
        quality_scores = []
        
        # Check music quality
        music_source = music_tile.get("metadata", {}).get("source", "fallback")
        quality_scores.append("high" if music_source != "fallback" else "medium")
        
        # Check recipe quality  
        recipe_heritage = recipe_tile.get("metadata", {}).get("heritage_match", False)
        quality_scores.append("high" if recipe_heritage else "medium")
        
        # Check photo quality
        photo_analysis = photo_tile.get("metadata", {}).get("analysis_method", "fallback")
        quality_scores.append("high" if photo_analysis != "fallback" else "medium")
        
        # Check nostalgia news quality
        news_source = nostalgia_news.get("metadata", {}).get("generated_by", "fallback")
        quality_scores.append("high" if news_source == "gemini" else "medium")
        
        # Overall assessment
        high_count = quality_scores.count("high")
        
        if high_count >= 3:
            return "high"
        elif high_count >= 2:
            return "medium"
        else:
            return "basic"
    
    def _assess_personalization_level(self, profile_data: Dict[str, Any], 
                                     nostalgia_news: Dict[str, Any]) -> str:
        """Assess level of personalization achieved"""
        
        personalization_factors = []
        
        # Check if name is used
        if profile_data.get("first_name") != "Friend":
            personalization_factors.append("name")
        
        # Check if heritage is utilized
        if profile_data.get("cultural_heritage") != "American":
            personalization_factors.append("heritage")
        
        # Check if nostalgia news is personalized
        if nostalgia_news.get("personalized_for"):
            personalization_factors.append("nostalgia_news")
        
        # Check if birth year/era is used
        if profile_data.get("birth_year"):
            personalization_factors.append("era")
        
        # Assessment
        factor_count = len(personalization_factors)
        
        if factor_count >= 4:
            return "highly_personalized"
        elif factor_count >= 2:
            return "moderately_personalized"
        else:
            return "basic_personalization"
    
    def _assess_cultural_usage(self, agent3_output: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how well Qloo cultural intelligence was utilized"""
        
        qloo_data = agent3_output.get("qloo_intelligence", {})
        cultural_recs = qloo_data.get("cultural_recommendations", {})
        metadata = qloo_data.get("metadata", {})
        
        return {
            "qloo_calls_successful": metadata.get("successful_calls", 0),
            "total_qloo_results": metadata.get("total_results", 0),
            "artists_available": len(cultural_recs.get("artists", {}).get("entities", [])),
            "cultural_intelligence_level": "high" if metadata.get("successful_calls", 0) > 0 else "fallback"
        }
    
    def _validate_dashboard(self, dashboard: Dict[str, Any]) -> Dict[str, Any]:
        """Validate final dashboard structure"""
        
        validation = {
            "structure_valid": True,
            "content_complete": True,
            "ui_ready": True,
            "issues": []
        }
        
        # Check required sections
        required_sections = ["content_tiles", "nostalgia_news", "theme", "profile"]
        for section in required_sections:
            if section not in dashboard:
                validation["structure_valid"] = False
                validation["issues"].append(f"Missing section: {section}")
        
        # Check content tiles
        required_tiles = ["music", "recipe", "photo"]
        content_tiles = dashboard.get("content_tiles", {})
        for tile in required_tiles:
            if tile not in content_tiles:
                validation["content_complete"] = False
                validation["issues"].append(f"Missing tile: {tile}")
        
        # Check UI requirements
        photo_tile = content_tiles.get("photo", {})
        if not photo_tile.get("image_name", "").endswith(".png"):
            validation["ui_ready"] = False
            validation["issues"].append("Photo tile missing proper image_name for UI")
        
        # Check nostalgia news
        nostalgia_news = dashboard.get("nostalgia_news", {})
        if not nostalgia_news.get("title"):
            validation["content_complete"] = False
            validation["issues"].append("Nostalgia news missing title")
        
        return validation
    
    def _log_dashboard_summary(self, dashboard: Dict[str, Any]) -> None:
        """Log summary of generated dashboard"""
        
        profile = dashboard.get("profile", {})
        theme = dashboard.get("theme", {})
        metadata = dashboard.get("dashboard_metadata", {})
        content_tiles = dashboard.get("content_tiles", {})
        nostalgia_news = dashboard.get("nostalgia_news", {})
        
        logger.info("📊 Dashboard Summary:")
        logger.info(f"   👤 Patient: {profile.get('first_name')} ({profile.get('cultural_heritage')})")
        logger.info(f"   🎯 Theme: {theme.get('name')}")
        logger.info(f"   🎵 Music: {content_tiles.get('music', {}).get('artist')} - {content_tiles.get('music', {}).get('piece')}")
        logger.info(f"   🍽️ Recipe: {content_tiles.get('recipe', {}).get('name')}")
        logger.info(f"   📷 Photo: {content_tiles.get('photo', {}).get('image_name')}")
        logger.info(f"   📰 Nostalgia News: {nostalgia_news.get('title', 'Generated')}")
        logger.info(f"   📈 Quality: {metadata.get('content_quality', 'unknown')}")
        logger.info(f"   🎨 Personalization: {metadata.get('personalization_level', 'unknown')}")
    
    def _create_emergency_dashboard(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Create emergency dashboard when synthesis fails"""
        
        logger.warning("🚨 Creating emergency dashboard")
        
        profile_data = self._extract_profile_data(agent1_output)
        theme_data = self._extract_theme_data(agent1_output)
        
        return {
            "success": False,
            "error": "dashboard_synthesis_failed",
            "timestamp": datetime.now().isoformat(),
            
            "theme": theme_data,
            "profile": profile_data,
            
            "content_tiles": {
                "music": {
                    "type": "music",
                    "title": "🎵 Musical Memories",
                    "artist": "Classical Music",
                    "piece": "Beautiful Melodies",
                    "conversation_starters": ["What music do you enjoy?"]
                },
                "recipe": {
                    "type": "recipe", 
                    "title": "🍽️ Comfort Kitchen",
                    "name": "Comfort Food",
                    "ingredients": ["Simple ingredients"],
                    "conversation_starters": ["What's your favorite comfort food?"]
                },
                "photo": {
                    "type": "photo",
                    "title": "📷 Photo of the Day", 
                    "image_name": "default.png",
                    "description": "A special moment",
                    "conversation_starters": ["Tell me about this photo"]
                }
            },
            
            "nostalgia_news": {
                "title": f"{profile_data['first_name']}'s News",
                "sections": {
                    "message": {
                        "headline": "✨ Today's Message",
                        "content": f"Every day is special, {profile_data['first_name']}! Let's enjoy the moment together."
                    }
                }
            },
            
            "dashboard_metadata": {
                "agents_executed": 1,
                "generation_timestamp": datetime.now().isoformat(),
                "pipeline_version": "emergency_fallback",
                "safety_level": "dementia_friendly"
            }
        }

# Export the main class
__all__ = ["DashboardSynthesizer"]