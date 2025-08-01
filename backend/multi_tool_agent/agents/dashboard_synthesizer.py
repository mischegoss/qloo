"""
Agent 8: Dashboard Synthesizer

 PII COMPLIANCE:
1. Works with anonymized profile data (no names, no location)
2. Receives exact structure from Agent 5 without modification
3. NO name field anywhere - completely removed
4. Proper validation and logging without PII
5. Safe fallbacks for missing data
6. Compatible with Sequential Agent's final enhanced profile
7. FIXED: Removed age calculation to prevent PII exposure
8. FIXED: Removed all name references
"""

import logging
import json
import os
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class DashboardSynthesizer:
    """
    Agent 6: PII-COMPLIANT Dashboard Synthesizer - Perfect Data Flow from Agent 5 (NO NAMES)
    """
    
    def __init__(self):
        self.recent_music_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "recent_music.json"
        )
        logger.info("🎨 Agent 6: PII-Compliant Dashboard Synthesizer initialized")
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        UPDATED: Final dashboard synthesis with anonymized profile support (NO NAMES)
        """
        
        try:
            logger.info("🎨 Agent 6: Synthesizing final dashboard (PII-compliant, no names)")
            
            # FIXED: Extract anonymized info only (NO NAMES)
            patient_info = enhanced_profile.get("patient_info", {})
            cultural_heritage = patient_info.get("cultural_heritage", "American")
            age_group = patient_info.get("age_group", "senior")
            theme = enhanced_profile.get("daily_theme", "Universal")
            
            # PII VALIDATION: Ensure no personal information is present
            pii_detected = self._detect_pii_in_profile(patient_info)
            if pii_detected:
                logger.warning(f"🚨 PII detected in patient_info: {pii_detected} - using safe fallbacks")
                cultural_heritage = "American"
            
            logger.info(f"🎯 Synthesizing dashboard - Theme: {theme}, Heritage: {cultural_heritage}, Age: {age_group}")
            
            # Extract content
            music_content = enhanced_profile.get("music_content", {})
            recipe_content = enhanced_profile.get("recipe_content", {})
            photo_content = enhanced_profile.get("photo_content", {})
            nostalgia_news_raw = enhanced_profile.get("nostalgia_news", {})
            
            # VALIDATE nostalgia news structure (no PII logging)
            logger.info(f"🔍 Nostalgia news validation:")
            if nostalgia_news_raw:
                logger.info(f"   Structure type: {type(nostalgia_news_raw)}")
                logger.info(f"   Top-level keys: {list(nostalgia_news_raw.keys())}")
                
                if "sections" in nostalgia_news_raw:
                    sections = nostalgia_news_raw["sections"]
                    logger.info(f"   Sections type: {type(sections)}")
                    if isinstance(sections, dict):
                        logger.info(f"   Section names: {list(sections.keys())}")
                        
                        # Log each section content length (no PII)
                        for section_name, section_data in sections.items():
                            if section_name == "conversation_starters":
                                questions = section_data.get("questions", []) if isinstance(section_data, dict) else []
                                logger.info(f"   {section_name}: {len(questions)} questions")
                            elif isinstance(section_data, dict):
                                content = section_data.get("content", "")
                                logger.info(f"   {section_name}: {len(content)} characters")
                else:
                    logger.warning("   No 'sections' key found in nostalgia news")
            else:
                logger.warning("   No nostalgia news data received")
            
            # Save recent music (no PII)
            self._save_recent_music(music_content)
            
            # FIXED: Use nostalgia news exactly as received from Agent 5
            final_nostalgia_news = nostalgia_news_raw if nostalgia_news_raw else self._create_emergency_nostalgia()
            
            # FIXED: Create final dashboard with anonymized patient info - NO NAME FIELD
            final_dashboard = {
                "patient_info": {
                    # FIXED: NO name field at all - completely removed
                    "cultural_heritage": cultural_heritage,
                    "age_group": age_group,  # FIXED: Only age_group, no specific age
                    "daily_theme": theme,
                    # Metadata for PII compliance
                    "anonymized": True,
                    "pii_compliant": True
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
                    # CRITICAL: Direct passthrough from Agent 5 (no modification)
                    "nostalgia_news": final_nostalgia_news
                },
                "metadata": {
                    "quality_score": self._assess_quality(enhanced_profile),
                    "personalization_level": self._assess_personalization(enhanced_profile),
                    "generation_timestamp": datetime.now().isoformat(),
                    "theme": theme,
                    "agent_pipeline": "6_agent_enhanced_pii_compliant",
                    "pii_compliant": True,
                    "anonymized_profile": True,
                    "cultural_heritage_used": cultural_heritage,
                    "age_group_used": age_group
                }
            }
            
            # Enhanced logging (no PII)
            sections_count = 0
            nostalgia_title = "No title"
            
            if final_nostalgia_news:
                nostalgia_title = final_nostalgia_news.get("title", "No title")
                if "sections" in final_nostalgia_news:
                    sections = final_nostalgia_news["sections"]
                    if isinstance(sections, dict):
                        sections_count = len(sections)
            
            logger.info("✅ Agent 6: PII-compliant final dashboard synthesized successfully")
            logger.info("📊 Dashboard Summary (anonymized):")
            logger.info(f"   👤 Profile: Heritage: {cultural_heritage}, Age group: {age_group}")
            logger.info(f"   🎯 Theme: {theme}")
            logger.info(f"   🎵 Music: {music_content.get('artist', 'N/A')} - {music_content.get('piece_title', 'N/A')}")
            logger.info(f"   🍽️ Recipe: {recipe_content.get('name', 'N/A')}")
            logger.info(f"   📷 Photo: {photo_content.get('filename', 'N/A')}")
            logger.info(f"   📰 Nostalgia News: {nostalgia_title} with {sections_count} sections")
            
            # Validate final structure for frontend
            if sections_count >= 4:
                logger.info("✅ Complete nostalgia news structure confirmed for frontend")
            else:
                logger.warning(f"⚠️ Incomplete nostalgia news: only {sections_count} sections")
            
            # Final PII validation of output
            if self._validate_output_pii_compliance(final_dashboard):
                logger.info("✅ Final dashboard PII compliance validated")
            else:
                logger.error("🚨 Final dashboard contains PII - applying emergency cleanup")
                final_dashboard = self._clean_pii_from_dashboard(final_dashboard)
            
            return final_dashboard
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self._emergency_fallback(enhanced_profile)
    
    def _detect_pii_in_profile(self, patient_info: Dict[str, Any]) -> List[str]:
        """
        Detect PII fields in patient info
        """
        
        pii_fields = ["first_name", "last_name", "full_name", "name", "email", "phone", 
                     "address", "city", "state", "zip_code", "ssn"]
        
        detected = [field for field in pii_fields if patient_info.get(field)]
        return detected
    
    def _validate_output_pii_compliance(self, dashboard: Dict[str, Any]) -> bool:
        """
        Validate that final dashboard output contains no PII
        """
        
        # Check patient_info section
        patient_info = dashboard.get("patient_info", {})
        
        # Allowed fields in patient_info - REMOVED "name" from allowed fields
        allowed_fields = ["cultural_heritage", "age_group", "daily_theme", 
                         "anonymized", "pii_compliant"]
        
        # Check for unexpected fields that might contain PII
        unexpected_fields = [field for field in patient_info.keys() 
                           if field not in allowed_fields]
        
        if unexpected_fields:
            logger.warning(f"⚠️ Unexpected fields in patient_info: {unexpected_fields}")
            return False
        
        # FIXED: Check that no name fields are present
        name_fields = ["name", "first_name", "last_name", "full_name"]
        for name_field in name_fields:
            if name_field in patient_info:
                logger.warning(f"⚠️ Name field detected in output: {name_field}")
                return False
        
        # FIXED: Check that no specific age is present
        if "age" in patient_info:
            logger.warning(f"⚠️ Specific age detected in output: {patient_info['age']}")
            return False
        
        return True
    
    def _clean_pii_from_dashboard(self, dashboard: Dict[str, Any]) -> Dict[str, Any]:
        """
        Emergency PII cleanup for dashboard
        """
        
        logger.info("🧹 Applying emergency PII cleanup")
        
        # Clean patient_info - REMOVE ALL NAME FIELDS
        if "patient_info" in dashboard:
            # Remove any unexpected PII fields - FIXED: Remove ALL name and age fields
            safe_patient_info = {
                "cultural_heritage": dashboard["patient_info"].get("cultural_heritage", "American"),
                "age_group": dashboard["patient_info"].get("age_group", "senior"),  # FIXED: Only age_group
                "daily_theme": dashboard["patient_info"].get("daily_theme", "Universal"),
                "anonymized": True,
                "pii_compliant": True
            }
            dashboard["patient_info"] = safe_patient_info
        
        return dashboard
    
    def _create_emergency_nostalgia(self) -> Dict[str, Any]:
        """Create emergency nostalgia news when none received - PII COMPLIANT"""
        
        logger.warning("🚨 Creating emergency PII-compliant nostalgia news")
        
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
                "full_sections": True,
                "pii_compliant": True,
                "anonymized": True
            }
        }
    
    def _save_recent_music(self, music_content: Dict[str, Any]) -> None:
        """Save recent music selection (no PII)"""
        
        try:
            if not music_content or not music_content.get("artist"):
                return
            
            os.makedirs(os.path.dirname(self.recent_music_file), exist_ok=True)
            
            recent_music_data = {
                "artist": music_content.get("artist", ""),
                "piece_title": music_content.get("piece_title", ""),
                "timestamp": datetime.now().isoformat(),
                "pii_compliant": True
            }
            
            with open(self.recent_music_file, 'w', encoding='utf-8') as f:
                json.dump(recent_music_data, f, indent=2)
                
            logger.info(f"💾 Saved recent music (PII-compliant): {recent_music_data['artist']} - {recent_music_data['piece_title']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save recent music: {e}")
    
    def _assess_quality(self, enhanced_profile: Dict[str, Any]) -> str:
        """Assess content quality"""
        
        score = 0
        if enhanced_profile.get("music_content", {}).get("artist"): 
            score += 1
        if enhanced_profile.get("recipe_content", {}).get("name"): 
            score += 1
        if enhanced_profile.get("photo_content", {}).get("filename"): 
            score += 1
        if enhanced_profile.get("nostalgia_news", {}).get("sections"): 
            score += 1
        
        # Bonus for cultural heritage integration
        if enhanced_profile.get("patient_info", {}).get("cultural_heritage"):
            score += 0.5
            
        return "high" if score >= 3.5 else "medium" if score >= 2 else "low"
    
    def _assess_personalization(self, enhanced_profile: Dict[str, Any]) -> str:
        """Assess personalization level (using anonymized data only)"""
        
        patient_info = enhanced_profile.get("patient_info", {})
        heritage = patient_info.get("cultural_heritage")
        age_group = patient_info.get("age_group")
        theme = enhanced_profile.get("daily_theme")
        
        personalization_factors = 0
        if heritage and heritage != "American":
            personalization_factors += 1
        if age_group and age_group != "senior":
            personalization_factors += 1
        if theme and theme != "Universal":
            personalization_factors += 1
        
        if personalization_factors >= 2:
            return "highly_personalized"
        elif personalization_factors >= 1:
            return "moderately_personalized"
        else:
            return "basic_personalized"
    
    def _emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback dashboard - PII COMPLIANT (NO NAMES)"""
        
        logger.warning("🔄 Using PII-compliant emergency fallback dashboard")
        
        # Extract safe anonymized info
        patient_info = enhanced_profile.get("patient_info", {})
        cultural_heritage = patient_info.get("cultural_heritage", "American")
        age_group = patient_info.get("age_group", "senior")
        theme = enhanced_profile.get("daily_theme", "Universal")
        
        return {
            "patient_info": {
                # FIXED: NO name field - completely removed
                "cultural_heritage": cultural_heritage,
                "age_group": age_group,  # FIXED: Only age_group, no specific age
                "daily_theme": theme,
                "anonymized": True,
                "pii_compliant": True
            },
            "content": {
                "music": {
                    "artist": "Classical Music", 
                    "piece_title": "Beautiful Melodies",
                    "conversation_starters": ["What music brings you joy?"]
                },
                "recipe": {
                    "name": "Comfort Food",
                    "ingredients": ["Simple ingredients"],
                    "instructions": ["Prepare with love"],
                    "conversation_starters": ["What's your favorite comfort food?"]
                },
                "photo": {
                    "filename": f"{theme.lower().replace(' ', '_')}.png", 
                    "description": "A peaceful scene",
                    "conversation_starters": ["What does this remind you of?"]
                },
                "nostalgia_news": self._create_emergency_nostalgia()
            },
            "metadata": {
                "quality_score": "low",
                "personalization_level": "basic",
                "agent_pipeline": "emergency_fallback_pii_compliant",
                "pii_compliant": True,
                "anonymized_profile": True,
                "generation_timestamp": datetime.now().isoformat()
            }
        }

# Export the main class
__all__ = ["DashboardSynthesizer"]