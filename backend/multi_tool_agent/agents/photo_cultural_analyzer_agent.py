"""
Photo Cultural Analyzer Agent - FIXED for Theme Image Priority
File: backend/multi_tool_agent/agents/photo_cultural_analyzer_agent.py

FIXES:
- PRIORITIZES theme images over personal photos (theme images first!)
- FIXED theme data extraction to properly get theme from consolidated_info
- ALWAYS finds theme images when valid theme provided (from JSON file)
- Enhanced debugging for theme data flow
- Simplified approach focused on theme images primarily
"""

import logging
import random
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Configure logger
logger = logging.getLogger(__name__)

class PhotoCulturalAnalyzerAgent:
    """
    Agent 5: Photo Cultural Analyzer - FIXED for Theme Image Priority
    
    PRIORITY ORDER:
    1. Theme images (ALWAYS available from JSON - prioritized!)
    2. Personal uploaded photos (secondary)
    3. Combined analysis only if both available
    """
    
    def __init__(self, vision_ai_tool):
        self.vision_ai_tool = vision_ai_tool
        logger.info("Photo Cultural Analyzer initialized - FIXED with theme image priority")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_of_the_day: str,
                  stored_photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Analyze theme images FIRST, then personal photos
        
        Args:
            consolidated_info: Information from Agent 1 (includes theme data)
            cultural_profile: Cultural profile from Agent 2
            qloo_intelligence: Cultural intelligence from Agent 3
            sensory_content: Sensory content from Agent 4
            photo_of_the_day: Personal photo path (secondary)
            stored_photo_analysis: Pre-stored analysis of personal photo (secondary)
            
        Returns:
            Theme-prioritized photo analysis
        """
        
        try:
            logger.info("🔍 Starting ENHANCED photo cultural analysis - Personal + Theme Images")
            
            # Extract patient info
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            
            # FIXED: Extract theme information with better debugging
            logger.info("🔧 DEBUG: Extracting theme data from consolidated_info")
            daily_theme = consolidated_info.get("daily_theme", {})
            logger.info(f"🔧 DEBUG: daily_theme keys: {list(daily_theme.keys())}")
            
            # Check both possible theme structures (for compatibility)
            theme_of_the_day = daily_theme.get("theme_of_the_day", {})
            if not theme_of_the_day:
                # Fallback to original Agent 1 structure if transformation didn't work
                theme_of_the_day = daily_theme.get("theme", {})
                logger.info("🔧 DEBUG: Using fallback theme structure from Agent 1")
            
            theme_image = daily_theme.get("theme_image", {})
            
            theme_name = theme_of_the_day.get("name", "Unknown")
            theme_id = theme_of_the_day.get("id", "unknown")
            
            logger.info(f"📷 Processing personal photo: {photo_of_the_day}")
            logger.info(f"🎯 Processing theme: {theme_name} (ID: {theme_id})")
            logger.info(f"🖼️ Theme image: {theme_image.get('filename', 'Not found')}")
            logger.info(f"🔧 DEBUG: Theme image exists: {theme_image.get('exists', False)}")
            logger.info(f"🔧 DEBUG: Full theme_image data: {theme_image}")
            
            # PRIORITY 1: Analyze theme image FIRST (should always be available)
            theme_image_analysis = await self._analyze_theme_image_priority(
                theme_image, theme_of_the_day, heritage, birth_year
            )
            
            # PRIORITY 2: Analyze personal photo (secondary)
            personal_photo_analysis = self._process_personal_photo_analysis(
                stored_photo_analysis, photo_of_the_day, heritage, birth_year
            )
            
            # PRIORITY 3: Combine if both available, otherwise prioritize theme
            if theme_image_analysis.get("status") == "analyzed":
                logger.info("✅ Theme image found and analyzed - using as primary source")
                primary_source = "theme_image"
                conversation_starters = theme_image_analysis.get("conversation_starters", [])
                
                # Add personal photo starters as secondary if available
                if personal_photo_analysis.get("status") == "analyzed":
                    personal_starters = personal_photo_analysis.get("conversation_starters", [])
                    conversation_starters.extend(personal_starters[:2])  # Add max 2 personal
                    logger.info("✅ Added personal photo starters as secondary")
                
            else:
                logger.warning("⚠️ Theme image not available, falling back to personal photo")
                primary_source = "personal_photo"
                conversation_starters = personal_photo_analysis.get("conversation_starters", [])
            
            # Generate combined memory triggers
            combined_memory_triggers = self._generate_combined_memory_triggers(
                personal_photo_analysis, theme_image_analysis, theme_of_the_day
            )
            
            # Cultural integration
            cultural_integration = self._analyze_combined_cultural_alignment(
                personal_photo_analysis, theme_image_analysis, heritage, theme_of_the_day
            )
            
            logger.info(f"✅ ENHANCED photo analysis completed:")
            logger.info(f"   🎯 Primary source: {primary_source}")
            logger.info(f"   📷 Personal photo conversation starters: {len(personal_photo_analysis.get('conversation_starters', []))}")
            logger.info(f"   🎯 Theme image conversation starters: {len(theme_image_analysis.get('conversation_starters', []))}")
            logger.info(f"   🔗 Combined conversation starters: {len(conversation_starters)}")
            
            return {
                "photo_analysis": {
                    "status": "success",
                    "analysis_type": "theme_prioritized",
                    "primary_source": primary_source,
                    
                    # Personal photo analysis (secondary)
                    "personal_photo": {
                        "photo_path": photo_of_the_day,
                        "vision_analysis": personal_photo_analysis.get("vision_analysis", {}),
                        "conversation_starters": personal_photo_analysis.get("conversation_starters", []),
                        "memory_triggers": personal_photo_analysis.get("memory_triggers", []),
                        "status": personal_photo_analysis.get("status", "not_available")
                    },
                    
                    # Theme image analysis (priority)
                    "theme_image": {
                        "image_info": theme_image,
                        "vision_analysis": theme_image_analysis.get("vision_analysis", {}),
                        "conversation_starters": theme_image_analysis.get("conversation_starters", []),
                        "memory_triggers": theme_image_analysis.get("memory_triggers", []),
                        "theme_alignment": theme_image_analysis.get("theme_alignment", {}),
                        "status": theme_image_analysis.get("status", "not_available")
                    },
                    
                    # Combined insights (theme-prioritized)
                    "combined_analysis": {
                        "conversation_starters": conversation_starters,
                        "memory_triggers": combined_memory_triggers,
                        "cultural_integration": cultural_integration,
                        "visual_coherence": self._assess_visual_coherence(
                            personal_photo_analysis, theme_image_analysis
                        )
                    },
                    
                    # Metadata
                    "processing_metadata": {
                        "agent": "photo_cultural_analyzer",
                        "analysis_sources": [
                            "personal_photo_stored" if personal_photo_analysis.get("status") == "analyzed" else "no_personal_photo",
                            "theme_image_analyzed" if theme_image_analysis.get("status") == "analyzed" else "no_theme_image"
                        ],
                        "theme_context": {
                            "theme_name": theme_name,
                            "theme_id": theme_id,
                            "theme_image_found": theme_image.get("exists", False)
                        },
                        "conversation_count": len(conversation_starters),
                        "memory_trigger_count": len(combined_memory_triggers),
                        "enhanced_approach": True,
                        "primary_source": primary_source
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ ENHANCED photo cultural analysis failed: {e}")
            return self._create_enhanced_fallback_analysis(
                photo_of_the_day, consolidated_info, theme_of_the_day
            )
    
    async def _analyze_theme_image_priority(self, theme_image: Dict[str, Any], 
                                          theme: Dict[str, Any], heritage: str, 
                                          birth_year: Optional[int]) -> Dict[str, Any]:
        """
        FIXED: Prioritized theme image analysis with better error handling
        
        Theme images should ALWAYS be available from JSON file when valid theme provided
        """
        
        theme_name = theme.get("name", "Unknown")
        theme_id = theme.get("id", "unknown")
        
        logger.info(f"🎯 PRIORITY: Analyzing theme image for '{theme_name}' (ID: {theme_id})")
        
        # Check if theme is valid (not Unknown)
        if theme_id == "unknown" or theme_name == "Unknown":
            logger.warning("⚠️ Invalid theme provided - cannot find theme image")
            return self._create_fallback_theme_analysis(theme, heritage)
        
        # Theme images should exist for all valid themes
        if not theme_image.get("exists", False):
            logger.error(f"❌ Theme image missing for valid theme '{theme_name}' - this should not happen!")
            logger.error(f"🔧 DEBUG: Expected theme image data: {theme_image}")
            return self._create_fallback_theme_analysis(theme, heritage)
        
        try:
            # Read theme image file
            image_path = Path(theme_image["backend_path"])
            
            if not image_path.exists():
                logger.error(f"❌ Theme image file not found at {image_path}")
                return self._create_fallback_theme_analysis(theme, heritage)
            
            # Convert image to base64 for Vision AI
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            logger.info(f"🔍 Analyzing theme image: {theme_image['filename']}")
            
            # Use Vision AI to analyze theme image
            if self.vision_ai_tool:
                vision_result = await self.vision_ai_tool.analyze_with_google_vision(image_base64)
                
                if vision_result and vision_result.get("success"):
                    logger.info(f"✅ Theme image analysis successful: {theme_image['filename']}")
                    
                    # Generate conversation starters based on theme image
                    theme_conversation_starters = self._generate_theme_priority_conversation_starters(
                        vision_result, theme, heritage, birth_year
                    )
                    
                    # Generate theme-specific memory triggers
                    theme_memory_triggers = self._generate_theme_memory_triggers(
                        vision_result, theme, heritage
                    )
                    
                    # Assess theme alignment
                    theme_alignment = self._assess_theme_alignment(vision_result, theme)
                    
                    return {
                        "vision_analysis": {
                            "objects": vision_result.get("objects", []),
                            "labels": vision_result.get("labels", []),
                            "colors": vision_result.get("colors", []),
                            "text_content": vision_result.get("text", [])
                        },
                        "conversation_starters": theme_conversation_starters,
                        "memory_triggers": theme_memory_triggers,
                        "theme_alignment": theme_alignment,
                        "status": "analyzed"
                    }
                else:
                    logger.warning(f"🎯 Vision AI failed for theme image: {theme_image['filename']}")
                    
            return self._create_fallback_theme_analysis(theme, heritage)
            
        except Exception as e:
            logger.error(f"❌ Error analyzing theme image: {e}")
            return self._create_fallback_theme_analysis(theme, heritage)
    
    def _generate_theme_priority_conversation_starters(self, 
                                                     vision_result: Dict[str, Any], 
                                                     theme: Dict[str, Any],
                                                     heritage: str, 
                                                     birth_year: Optional[int]) -> List[Dict[str, Any]]:
        """
        ENHANCED: Generate theme-prioritized conversation starters
        """
        
        theme_name = theme.get("name", "Unknown")
        theme_id = theme.get("id", "unknown")
        theme_prompts = theme.get("conversation_prompts", [])
        
        objects = vision_result.get("objects", [])
        labels = vision_result.get("labels", [])
        
        theme_starters = []
        
        # PRIORITY: Use theme-specific conversation prompts (from JSON)
        if theme_prompts:
            for prompt in theme_prompts[:3]:  # Take first 3 theme prompts
                theme_starters.append({
                    "type": "theme_specific",
                    "starter": prompt,
                    "follow_up": f"Tell me more about {theme_name.lower()}.",
                    "theme_context": theme_name,
                    "source": "theme_image",
                    "priority": "high"
                })
        
        # Add image-specific questions based on detected content
        if "celebration" in labels or "party" in objects:
            theme_starters.append({
                "type": "celebration",
                "starter": "Do you remember celebrations like this?",
                "follow_up": "What made them special?",
                "theme_context": theme_name,
                "source": "theme_image",
                "priority": "medium"
            })
        
        # Food-specific questions (if food theme)
        if theme_id == "food" or any(word in labels for word in ["food", "cooking", "kitchen"]):
            theme_starters.append({
                "type": "food",
                "starter": "What foods do you see here?",
                "follow_up": "Did you like to cook these?",
                "theme_context": theme_name,
                "source": "theme_image",
                "priority": "high"
            })
        
        # Season-specific questions
        if any(word in labels for word in ["spring", "summer", "fall", "winter", "seasonal"]):
            theme_starters.append({
                "type": "seasonal",
                "starter": "What season do you see here?",
                "follow_up": "What did you do in this season?",
                "theme_context": theme_name,
                "source": "theme_image",
                "priority": "medium"
            })
        
        # Simple fallback using theme name
        if not theme_starters:
            theme_starters.append({
                "type": "theme_general",
                "starter": f"What does {theme_name.lower()} remind you of?",
                "follow_up": "Tell me about those memories.",
                "theme_context": theme_name,
                "source": "theme_image",
                "priority": "medium"
            })
        
        # Sort by priority and limit
        theme_starters.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 2))
        return theme_starters[:4]  # Return top 4 theme starters
    
    def _process_personal_photo_analysis(self, stored_photo_analysis: Dict[str, Any], 
                                       photo_path: str, heritage: str, 
                                       birth_year: Optional[int]) -> Dict[str, Any]:
        """
        Process existing personal photo analysis (SECONDARY to theme images)
        """
        
        if not stored_photo_analysis or not photo_path:
            logger.info("📷 No personal photo available for analysis")
            return {
                "vision_analysis": {},
                "conversation_starters": [],
                "memory_triggers": [],
                "status": "no_personal_photo"
            }
        
        # Use stored vision analysis data
        vision_analysis = stored_photo_analysis.get("vision_analysis", {})
        logger.info(f"📷 Processing personal photo: {len(vision_analysis.get('objects', []))} objects, {len(vision_analysis.get('labels', []))} labels")
        
        # Generate simple conversation starters for personal photo
        personal_conversation_starters = self._generate_simple_conversation_starters_for_personal_photo(
            vision_analysis, heritage, birth_year
        )
        
        # Generate memory triggers for personal photo
        personal_memory_triggers = self._generate_simple_memory_triggers(vision_analysis, heritage)
        
        return {
            "vision_analysis": vision_analysis,
            "conversation_starters": personal_conversation_starters,
            "memory_triggers": personal_memory_triggers,
            "status": "analyzed"
        }
    
    def _generate_simple_conversation_starters_for_personal_photo(self, 
                                                                vision_analysis: Dict[str, Any], 
                                                                heritage: str, 
                                                                birth_year: Optional[int]) -> List[Dict[str, Any]]:
        """
        Generate simple conversation starters for personal photos (SECONDARY)
        """
        
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        people = vision_analysis.get("people", [])
        activities = vision_analysis.get("activities", [])
        
        simple_starters = []
        
        # People questions (if people detected)
        if people or "people" in objects:
            simple_starters.append({
                "type": "people",
                "starter": "Who do you see here?",
                "follow_up": "Tell me about them.",
                "source": "personal_photo",
                "priority": "medium"
            })
        
        # Family questions
        if any(word in labels for word in ["family", "gathering", "home"]):
            simple_starters.append({
                "type": "family",
                "starter": "What was happening here?",
                "follow_up": "Was this a special day?",
                "source": "personal_photo",
                "priority": "medium"
            })
        
        # Food/cooking questions  
        if any(word in objects + labels for word in ["food", "kitchen", "cooking", "table"]):
            simple_starters.append({
                "type": "food",
                "starter": "What food do you see?",
                "follow_up": "Did you like to cook?",
                "source": "personal_photo",
                "priority": "medium"
            })
        
        # Simple fallback if nothing specific detected
        if not simple_starters:
            simple_starters.append({
                "type": "general",
                "starter": "Tell me about this photo.",
                "follow_up": "What do you remember?",
                "source": "personal_photo",
                "priority": "low"
            })
        
        # Limit to 2 for personal photos (since theme is priority)
        return simple_starters[:2]
    
    def _generate_combined_memory_triggers(self, personal_analysis: Dict[str, Any],
                                         theme_analysis: Dict[str, Any],
                                         theme: Dict[str, Any]) -> List[str]:
        """Generate combined memory triggers (theme-prioritized)"""
        
        theme_triggers = theme_analysis.get("memory_triggers", [])
        personal_triggers = personal_analysis.get("memory_triggers", [])
        
        # Prioritize theme triggers
        all_triggers = theme_triggers.copy()
        
        # Add unique personal triggers
        for trigger in personal_triggers:
            if trigger not in all_triggers:
                all_triggers.append(trigger)
        
        # Add theme-specific trigger if not already present
        theme_name = theme.get("name", "")
        if theme_name and f"{theme_name} memories" not in all_triggers:
            all_triggers.append(f"{theme_name} memories")
        
        return all_triggers[:5]
    
    def _generate_theme_memory_triggers(self, vision_result: Dict[str, Any], 
                                      theme: Dict[str, Any], heritage: str) -> List[str]:
        """Generate memory triggers specific to theme images"""
        
        triggers = []
        theme_name = theme.get("name", "")
        labels = vision_result.get("labels", [])
        
        # Theme-specific triggers
        if theme_name:
            triggers.append(f"{theme_name} experiences")
        
        # Visual content triggers
        if "celebration" in labels:
            triggers.append("Celebrations and parties")
        if "nature" in labels or "outdoor" in labels:
            triggers.append("Time outdoors")
        if "traditional" in labels:
            triggers.append("Family traditions")
        if "food" in labels or "cooking" in labels:
            triggers.append("Cooking and meals")
        
        return triggers[:3]
    
    def _generate_simple_memory_triggers(self, vision_analysis: Dict[str, Any], heritage: str) -> List[str]:
        """Generate simple memory triggers from personal photos"""
        
        triggers = []
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        
        if "family" in labels:
            triggers.append("Family gatherings")
        if "food" in objects or "kitchen" in objects:
            triggers.append("Cooking together")
        if "celebration" in labels:
            triggers.append("Special occasions")
        
        return triggers[:2]  # Limit for personal photos since theme is priority
    
    def _assess_theme_alignment(self, vision_result: Dict[str, Any], theme: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how well the theme image aligns with theme expectations"""
        
        theme_keywords = theme.get("recipe_keywords", [])
        theme_name = theme.get("name", "").lower()
        
        detected_labels = [label.lower() for label in vision_result.get("labels", [])]
        detected_objects = [obj.lower() for obj in vision_result.get("objects", [])]
        
        alignment_score = 0
        matching_elements = []
        
        # Check theme name alignment
        if theme_name in detected_labels:
            alignment_score += 2
            matching_elements.append(theme_name)
        
        # Check keyword alignment
        for keyword in theme_keywords:
            if keyword.lower() in detected_labels or keyword.lower() in detected_objects:
                alignment_score += 1
                matching_elements.append(keyword)
        
        return {
            "alignment_score": alignment_score,
            "max_possible_score": 2 + len(theme_keywords),
            "matching_elements": matching_elements,
            "alignment_quality": "high" if alignment_score >= 2 else "medium" if alignment_score >= 1 else "low"
        }
    
    def _analyze_combined_cultural_alignment(self, personal_analysis: Dict[str, Any],
                                           theme_analysis: Dict[str, Any], 
                                           heritage: str, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cultural alignment (theme-prioritized)"""
        
        return {
            "heritage_context": heritage,
            "theme_context": theme.get("name", "Unknown"),
            "personal_photo_available": bool(personal_analysis.get("vision_analysis")),
            "theme_image_available": bool(theme_analysis.get("vision_analysis")),
            "cultural_coherence": "theme_prioritized" if theme_analysis.get("vision_analysis") else "personal_only"
        }
    
    def _assess_visual_coherence(self, personal_analysis: Dict[str, Any], 
                                theme_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess visual coherence between personal photos and theme images"""
        
        personal_labels = set(personal_analysis.get("vision_analysis", {}).get("labels", []))
        theme_labels = set(theme_analysis.get("vision_analysis", {}).get("labels", []))
        
        common_elements = personal_labels.intersection(theme_labels)
        coherence_score = len(common_elements)
        
        return {
            "common_visual_elements": list(common_elements),
            "coherence_score": coherence_score,
            "coherence_level": "high" if coherence_score >= 3 else "medium" if coherence_score >= 1 else "low"
        }
    
    def _create_fallback_theme_analysis(self, theme: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Create fallback theme analysis when image not available"""
        
        theme_name = theme.get("name", "Unknown")
        theme_prompts = theme.get("conversation_prompts", [])
        
        # Use theme conversation prompts as fallback
        fallback_starters = []
        if theme_prompts:
            for prompt in theme_prompts[:2]:
                fallback_starters.append({
                    "type": "theme_fallback",
                    "starter": prompt,
                    "follow_up": f"Tell me more about {theme_name.lower()}.",
                    "source": "theme_fallback",
                    "priority": "medium"
                })
        
        return {
            "vision_analysis": {},
            "conversation_starters": fallback_starters,
            "memory_triggers": [f"{theme_name} memories"],
            "theme_alignment": {"alignment_quality": "fallback"},
            "status": "fallback"
        }
    
    def _create_enhanced_fallback_analysis(self, photo_path: str, 
                                         consolidated_info: Dict[str, Any],
                                         theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback analysis with theme priority"""
        
        theme_name = theme.get("name", "Unknown")
        
        return {
            "photo_analysis": {
                "status": "fallback",
                "analysis_type": "theme_prioritized_fallback",
                "primary_source": "fallback",
                "personal_photo": {
                    "photo_path": photo_path or "Not available",
                    "vision_analysis": {},
                    "conversation_starters": [],
                    "memory_triggers": []
                },
                "theme_image": {
                    "image_info": {"filename": "Not found", "exists": False},
                    "vision_analysis": {},
                    "conversation_starters": [],
                    "memory_triggers": [],
                    "theme_alignment": {"alignment_quality": "fallback"}
                },
                "combined_analysis": {
                    "conversation_starters": [
                        {
                            "type": "general",
                            "starter": "What brings back good memories for you?",
                            "follow_up": f"Tell me about {theme_name.lower()}.",
                            "source": "fallback",
                            "priority": "medium"
                        }
                    ],
                    "memory_triggers": [f"{theme_name} memories"],
                    "cultural_integration": {"cultural_coherence": "fallback"},
                    "visual_coherence": {"coherence_level": "fallback"}
                },
                "processing_metadata": {
                    "agent": "photo_cultural_analyzer",
                    "analysis_sources": ["fallback"],
                    "theme_context": {"theme_name": theme_name},
                    "enhanced_approach": True,
                    "primary_source": "fallback",
                    "fallback_reason": "Analysis failure"
                }
            }
        }