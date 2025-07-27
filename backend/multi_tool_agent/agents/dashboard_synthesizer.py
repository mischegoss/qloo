"""
Agent 6: Dashboard Synthesizer - WITH RECENT MUSIC TRACKING
File: backend/multi_tool_agent/agents/dashboard_synthesizer.py

NEW FEATURE:
- Saves current music selection to recent_music.json
- Enables Music Agent to avoid repetition on next run
"""

import logging
import json
import os
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DashboardSynthesizer:
    """
    Agent 6: Final Dashboard Assembly with Recent Music Tracking
    """
    
    def __init__(self):
        # Path to recent music tracking file
        self.recent_music_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "recent_music.json"
        )
        
        logger.info("🎨 Agent 6: Dashboard Synthesizer initialized")
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Final dashboard synthesis with music tracking
        """
        
        try:
            logger.info("🎨 Agent 6: Synthesizing final dashboard")
            
            patient_name = enhanced_profile.get("patient_info", {}).get("name", "Unknown")
            theme = enhanced_profile.get("daily_theme", "Universal")
            
            logger.info(f"🎯 Synthesizing dashboard for: {patient_name} - {theme}")
            
            # Extract all agent results
            music_content = enhanced_profile.get("music_content", {})
            recipe_content = enhanced_profile.get("recipe_content", {})
            photo_content = enhanced_profile.get("photo_content", {})
            nostalgia_news = enhanced_profile.get("nostalgia_news", {})
            
            # Save current music selection for next time
            self._save_recent_music(music_content)
            
            # Assess quality and personalization
            quality_score = self._assess_quality(enhanced_profile)
            personalization_level = self._assess_personalization(enhanced_profile)
            
            # Create final dashboard
            final_dashboard = {
                "patient_info": {
                    "name": patient_name,
                    "cultural_heritage": enhanced_profile.get("patient_info", {}).get("cultural_heritage", ""),
                    "age": enhanced_profile.get("patient_info", {}).get("age", 0),
                    "daily_theme": theme
                },
                "content": {
                    "music": {
                        "artist": music_content.get("artist", ""),
                        "piece_title": music_content.get("piece_title", ""),
                        "youtube_url": music_content.get("youtube_url"),
                        "youtube_embed": music_content.get("youtube_embed"),
                        "conversation_starters": music_content.get("conversation_starters", []),
                        "fun_fact": music_content.get("fun_fact", "")
                    },
                    "recipe": {
                        "name": recipe_content.get("name", ""),
                        "description": recipe_content.get("description", ""),
                        "ingredients": recipe_content.get("ingredients", []),
                        "instructions": recipe_content.get("instructions", []),
                        "conversation_starters": recipe_content.get("conversation_starters", [])
                    },
                    "photo": {
                        "filename": photo_content.get("filename", ""),
                        "description": photo_content.get("description", ""),
                        "cultural_context": photo_content.get("cultural_context", ""),
                        "conversation_starters": photo_content.get("conversation_starters", [])
                    },
                    "nostalgia_news": {
                        "headline": nostalgia_news.get("headline", ""),
                        "content": nostalgia_news.get("content", ""),
                        "themes": nostalgia_news.get("themes", []),
                        "conversation_starters": nostalgia_news.get("conversation_starters", [])
                    }
                },
                "metadata": {
                    "quality_score": quality_score,
                    "personalization_level": personalization_level,
                    "generation_timestamp": datetime.now().isoformat(),
                    "theme": theme,
                    "agent_pipeline": "6_agent_enhanced"
                }
            }
            
            # Log summary
            logger.info("✅ Agent 6: Final dashboard synthesized successfully")
            logger.info("📊 Dashboard Summary:")
            logger.info(f"   👤 Patient: {patient_name} ({enhanced_profile.get('patient_info', {}).get('cultural_heritage', '')})")
            logger.info(f"   🎯 Theme: {theme}")
            logger.info(f"   🎵 Music: {music_content.get('artist', '')} - {music_content.get('piece_title', '')}")
            logger.info(f"   🍽️ Recipe: {recipe_content.get('name', '')}")
            logger.info(f"   📷 Photo: {photo_content.get('filename', '')}")
            logger.info(f"   📰 Nostalgia News: {nostalgia_news.get('headline', '')}")
            logger.info(f"   📈 Quality: {quality_score}")
            logger.info(f"   🎨 Personalization: {personalization_level}")
            
            return final_dashboard
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self._emergency_fallback(enhanced_profile)
    
    def _save_recent_music(self, music_content: Dict[str, Any]) -> None:
        """
        Save current music selection to avoid repetition next time
        """
        
        try:
            if not music_content or not music_content.get("artist"):
                logger.warning("⚠️ No music content to save")
                return
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.recent_music_file), exist_ok=True)
            
            # Prepare recent music data
            recent_music_data = {
                "artist": music_content.get("artist", ""),
                "piece_title": music_content.get("piece_title", ""),
                "youtube_url": music_content.get("youtube_url"),
                "search_query": music_content.get("search_query", ""),
                "timestamp": datetime.now().isoformat(),
                "selection_method": music_content.get("metadata", {}).get("selection_method", "unknown")
            }
            
            # Write to file
            with open(self.recent_music_file, 'w', encoding='utf-8') as f:
                json.dump(recent_music_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved recent music: {recent_music_data['artist']} - {recent_music_data['piece_title']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save recent music: {e}")
            # Don't let this failure break the whole pipeline
            pass
    
    def _assess_quality(self, enhanced_profile: Dict[str, Any]) -> str:
        """Assess overall content quality"""
        
        score = 0
        max_score = 6
        
        # Check each content type
        if enhanced_profile.get("music_content", {}).get("artist"):
            score += 1
        if enhanced_profile.get("recipe_content", {}).get("name"):
            score += 1
        if enhanced_profile.get("photo_content", {}).get("filename"):
            score += 1
        if enhanced_profile.get("nostalgia_news", {}).get("headline"):
            score += 1
        if enhanced_profile.get("qloo_intelligence", {}).get("cultural_recommendations"):
            score += 1
        if enhanced_profile.get("music_content", {}).get("youtube_url"):
            score += 1
        
        if score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
    
    def _assess_personalization(self, enhanced_profile: Dict[str, Any]) -> str:
        """Assess personalization level"""
        
        heritage = enhanced_profile.get("patient_info", {}).get("cultural_heritage", "")
        qloo_data = enhanced_profile.get("qloo_intelligence", {})
        theme_match = enhanced_profile.get("daily_theme", "")
        
        if heritage and qloo_data and theme_match:
            return "highly_personalized"
        elif heritage and (qloo_data or theme_match):
            return "moderately_personalized"
        else:
            return "basic_personalized"
    
    def _emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback dashboard"""
        
        logger.warning("🔄 Using emergency fallback dashboard")
        
        patient_name = enhanced_profile.get("patient_info", {}).get("name", "Unknown")
        
        return {
            "patient_info": {
                "name": patient_name,
                "cultural_heritage": "",
                "age": 0,
                "daily_theme": "Universal"
            },
            "content": {
                "music": {
                    "artist": "Johann Sebastian Bach",
                    "piece_title": "Air on the G String",
                    "youtube_url": None,
                    "youtube_embed": None,
                    "conversation_starters": ["Classical music is so timeless"],
                    "fun_fact": "Bach composed beautiful music for all to enjoy"
                },
                "recipe": {
                    "name": "Simple Tea and Cookies",
                    "description": "A comforting classic",
                    "ingredients": ["Tea", "Cookies"],
                    "instructions": ["Brew tea", "Enjoy with cookies"],
                    "conversation_starters": ["Nothing beats a good cup of tea"]
                },
                "photo": {
                    "filename": "default.png",
                    "description": "A peaceful scene",
                    "cultural_context": "",
                    "conversation_starters": ["This is a lovely picture"]
                },
                "nostalgia_news": {
                    "headline": "Beautiful Day Ahead",
                    "content": "Today is a wonderful day to enjoy simple pleasures.",
                    "themes": ["positivity"],
                    "conversation_starters": ["Every day has something special"]
                }
            },
            "metadata": {
                "quality_score": "low",
                "personalization_level": "basic_personalized",
                "generation_timestamp": datetime.now().isoformat(),
                "theme": "Universal",
                "agent_pipeline": "emergency_fallback"
            }
        }

# Export the main class
__all__ = ["DashboardSynthesizer"]