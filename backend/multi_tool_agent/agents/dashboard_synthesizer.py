"""
Agent 6: Dashboard Synthesizer - FIXED DATA FLOW  
File: backend/multi_tool_agent/agents/dashboard_synthesizer.py

CRITICAL FIXES:
1. Receives EXACT structure from Agent 5
2. Passes it through without modification
3. Proper validation and logging
4. Safe fallbacks for missing data
"""

import logging
import json
import os
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DashboardSynthesizer:
    """
    Agent 6: FIXED Dashboard Synthesizer - Perfect Data Flow from Agent 5
    """
    
    def __init__(self):
        self.recent_music_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "recent_music.json"
        )
        logger.info("🎨 Agent 6: Dashboard Synthesizer initialized")
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Final dashboard synthesis with perfect nostalgia news handling
        """
        
        try:
            logger.info("🎨 Agent 6: Synthesizing final dashboard")
            
            # Extract basic info
            patient_name = enhanced_profile.get("patient_info", {}).get("name", "Unknown")
            theme = enhanced_profile.get("daily_theme", "Universal")
            
            logger.info(f"🎯 Synthesizing dashboard for: {patient_name} - {theme}")
            
            # Extract content
            music_content = enhanced_profile.get("music_content", {})
            recipe_content = enhanced_profile.get("recipe_content", {})
            photo_content = enhanced_profile.get("photo_content", {})
            nostalgia_news_raw = enhanced_profile.get("nostalgia_news", {})
            
            # CRITICAL: Validate nostalgia news structure
            logger.info(f"🔍 Raw nostalgia news type: {type(nostalgia_news_raw)}")
            if nostalgia_news_raw:
                logger.info(f"🔍 Nostalgia keys: {list(nostalgia_news_raw.keys())}")
                if "sections" in nostalgia_news_raw:
                    sections = nostalgia_news_raw["sections"]
                    logger.info(f"🔍 Sections found: {list(sections.keys()) if isinstance(sections, dict) else 'Not a dict'}")
                    
                    # Log each section content length
                    if isinstance(sections, dict):
                        for section_name, section_data in sections.items():
                            if section_name == "conversation_starters":
                                questions = section_data.get("questions", [])
                                logger.info(f"   {section_name}: {len(questions)} questions")
                            else:
                                content = section_data.get("content", "")
                                logger.info(f"   {section_name}: {len(content)} characters")
            
            # Save recent music
            self._save_recent_music(music_content)
            
            # FIXED: Use nostalgia news exactly as received from Agent 5
            final_nostalgia_news = nostalgia_news_raw if nostalgia_news_raw else self._create_emergency_nostalgia()
            
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
                    # CRITICAL: Direct passthrough from Agent 5
                    "nostalgia_news": final_nostalgia_news
                },
                "metadata": {
                    "quality_score": self._assess_quality(enhanced_profile),
                    "personalization_level": self._assess_personalization(enhanced_profile),
                    "generation_timestamp": datetime.now().isoformat(),
                    "theme": theme,
                    "agent_pipeline": "6_agent_enhanced"
                }
            }
            
            # Enhanced logging
            sections_count = 0
            nostalgia_title = "No title"
            
            if final_nostalgia_news:
                nostalgia_title = final_nostalgia_news.get("title", "No title")
                if "sections" in final_nostalgia_news:
                    sections_count = len(final_nostalgia_news["sections"])
            
            logger.info("✅ Agent 6: Final dashboard synthesized successfully")
            logger.info("📊 Dashboard Summary:")
            logger.info(f"   👤 Patient: {patient_name} ({enhanced_profile.get('patient_info', {}).get('cultural_heritage', '')})")
            logger.info(f"   🎯 Theme: {theme}")
            logger.info(f"   🎵 Music: {music_content.get('artist', '')} - {music_content.get('piece_title', '')}")
            logger.info(f"   🍽️ Recipe: {recipe_content.get('name', '')}")
            logger.info(f"   📷 Photo: {photo_content.get('filename', '')}")
            logger.info(f"   📰 Nostalgia News: {nostalgia_title} with {sections_count} sections")
            
            # Validate final structure for frontend
            if sections_count >= 4:
                logger.info("✅ Complete nostalgia news structure confirmed for frontend")
            else:
                logger.warning(f"⚠️ Incomplete nostalgia news: only {sections_count} sections")
            
            return final_dashboard
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self._emergency_fallback(enhanced_profile)
    
    def _create_emergency_nostalgia(self) -> Dict[str, Any]:
        """Create emergency nostalgia news when none received"""
        
        logger.warning("🚨 Creating emergency nostalgia news")
        
        return {
            "title": f"Today's Special News",
            "subtitle": "Daily Edition",
            "date": datetime.now().strftime("%B %d, %Y"),
            "sections": {
                "memory_spotlight": {
                    "headline": "📚 Memory Spotlight",
                    "content": "Today is filled with opportunities for meaningful moments and beautiful memories that enrich our lives.",
                    "fun_fact": "Every day brings new possibilities for joy and connection."
                },
                "era_highlights": {
                    "headline": "🎵 Era Highlights",
                    "content": "Throughout history, music and traditions have brought people together in celebration and joy.",
                    "fun_fact": "Music is a universal language that speaks to every heart."
                },
                "heritage_traditions": {
                    "headline": "🏛️ Heritage Traditions",
                    "content": "Cultural traditions connect us to our roots and enrich our lives with meaning and purpose.",
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
            "themes": ["Connection", "Joy", "Memories"],
            "metadata": {
                "generated_by": "agent6_emergency",
                "full_sections": True
            }
        }
    
    def _save_recent_music(self, music_content: Dict[str, Any]) -> None:
        """Save recent music selection"""
        
        try:
            if not music_content or not music_content.get("artist"):
                return
            
            os.makedirs(os.path.dirname(self.recent_music_file), exist_ok=True)
            
            recent_music_data = {
                "artist": music_content.get("artist", ""),
                "piece_title": music_content.get("piece_title", ""),
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.recent_music_file, 'w', encoding='utf-8') as f:
                json.dump(recent_music_data, f, indent=2)
                
            logger.info(f"💾 Saved recent music: {recent_music_data['artist']} - {recent_music_data['piece_title']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save recent music: {e}")
    
    def _assess_quality(self, enhanced_profile: Dict[str, Any]) -> str:
        """Assess content quality"""
        
        score = 0
        if enhanced_profile.get("music_content", {}).get("artist"): score += 1
        if enhanced_profile.get("recipe_content", {}).get("name"): score += 1
        if enhanced_profile.get("photo_content", {}).get("filename"): score += 1
        if enhanced_profile.get("nostalgia_news", {}).get("sections"): score += 1
        
        return "high" if score >= 3 else "medium" if score >= 2 else "low"
    
    def _assess_personalization(self, enhanced_profile: Dict[str, Any]) -> str:
        """Assess personalization level"""
        
        heritage = enhanced_profile.get("patient_info", {}).get("cultural_heritage")
        theme = enhanced_profile.get("daily_theme")
        
        if heritage and theme:
            return "highly_personalized"
        elif heritage or theme:
            return "moderately_personalized"
        else:
            return "basic_personalized"
    
    def _emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback dashboard"""
        
        logger.warning("🔄 Using emergency fallback dashboard")
        
        return {
            "patient_info": {
                "name": enhanced_profile.get("patient_info", {}).get("name", "Unknown"),
                "cultural_heritage": "",
                "age": 0,
                "daily_theme": "Universal"
            },
            "content": {
                "music": {"artist": "Classical Music", "piece_title": "Beautiful Melodies"},
                "recipe": {"name": "Comfort Food"},
                "photo": {"filename": "default.png", "description": "A peaceful scene"},
                "nostalgia_news": self._create_emergency_nostalgia()
            },
            "metadata": {
                "quality_score": "low",
                "personalization_level": "basic",
                "agent_pipeline": "emergency_fallback"
            }
        }

# Export the main class
__all__ = ["DashboardSynthesizer"]