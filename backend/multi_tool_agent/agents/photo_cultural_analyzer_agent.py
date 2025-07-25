"""
Photo Cultural Analyzer Agent - FIXED for Theme Photos ONLY in Automatic Pipeline
File: backend/multi_tool_agent/agents/photo_cultural_analyzer_agent.py

MAJOR CHANGES:
- THEME PHOTOS: Properly analyzed with VisionAI in automatic pipeline
- PERSONAL PHOTOS: Completely excluded from automatic pipeline (on-demand only)
- Enhanced error handling for VisionAI
- Simplified logic focused exclusively on theme photos
- All other functionality preserved
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
    Agent 5: Photo Cultural Analyzer - THEME PHOTOS ONLY in Automatic Pipeline
    
    AUTOMATIC PIPELINE: Theme photos only (analyzed with VisionAI)
    PERSONAL PHOTOS: Separate on-demand functionality (not through this agent)
    """
    
    def __init__(self, vision_ai_tool):
        self.vision_ai_tool = vision_ai_tool
        logger.info("Photo Cultural Analyzer initialized - THEME PHOTOS ONLY in automatic pipeline")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_of_the_day: Optional[str] = None,  # IGNORED in automatic pipeline
                  stored_photo_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:  # IGNORED in automatic pipeline
        """
        FIXED: Analyze THEME PHOTOS ONLY in automatic pipeline
        
        Args:
            consolidated_info: Information from Agent 1 (includes theme data)
            cultural_profile: Cultural profile from Agent 2
            qloo_intelligence: Cultural intelligence from Agent 3
            sensory_content: Sensory content from Agent 4
            photo_of_the_day: IGNORED - not used in automatic pipeline
            stored_photo_analysis: IGNORED - not used in automatic pipeline
            
        Returns:
            Theme photo analysis only
        """
        
        try:
            logger.info("🎯 Starting Theme Photo Analysis - AUTOMATIC PIPELINE ONLY")
            logger.info("📷 Personal photos: EXCLUDED from automatic pipeline")
            
            # Extract patient info
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            
            # Extract theme information
            daily_theme = consolidated_info.get("daily_theme", {})
            theme_of_the_day = daily_theme.get("theme_of_the_day", {})
            theme_image = daily_theme.get("theme_image", {})
            
            theme_name = theme_of_the_day.get("name", "Unknown")
            theme_id = theme_of_the_day.get("id", "unknown")
            
            logger.info(f"🎯 Processing theme: {theme_name} (ID: {theme_id})")
            logger.info(f"🖼️ Theme image: {theme_image.get('filename', 'Not found')}")
            logger.info(f"✅ Theme image exists: {theme_image.get('exists', False)}")
            
            # ONLY analyze theme image (no personal photos in automatic pipeline)
            theme_image_analysis = await self._analyze_theme_image_only(
                theme_image, theme_of_the_day, heritage, birth_year
            )
            
            # Generate conversation starters based on theme image analysis
            conversation_starters = theme_image_analysis.get("conversation_starters", [])
            memory_triggers = theme_image_analysis.get("memory_triggers", [])
            
            logger.info(f"✅ Theme photo analysis completed:")
            logger.info(f"   🎯 Theme: {theme_name}")
            logger.info(f"   🖼️ Image analyzed: {theme_image.get('filename', 'N/A')}")
            logger.info(f"   💬 Conversation starters: {len(conversation_starters)}")
            logger.info(f"   🧠 Memory triggers: {len(memory_triggers)}")
            
            return {
                "photo_analysis": {
                    "status": "success",
                    "analysis_type": "theme_photo_only",
                    "primary_source": "theme_image",
                    
                    # REMOVED: Personal photo analysis (not in automatic pipeline)
                    
                    # Theme image analysis (primary and only source)
                    "theme_image": {
                        "image_info": theme_image,
                        "vision_analysis": theme_image_analysis.get("vision_analysis", {}),
                        "conversation_starters": conversation_starters,
                        "memory_triggers": memory_triggers,
                        "theme_alignment": theme_image_analysis.get("theme_alignment", {}),
                        "status": theme_image_analysis.get("status", "analyzed")
                    },
                    
                    # Simplified analysis (theme-only)
                    "combined_analysis": {
                        "conversation_starters": conversation_starters,
                        "memory_triggers": memory_triggers,
                        "cultural_integration": self._analyze_theme_cultural_alignment(
                            theme_image_analysis, heritage, theme_of_the_day
                        ),
                        "visual_coherence": {"coherence_level": "theme_focused"}
                    },
                    
                    # Metadata
                    "processing_metadata": {
                        "agent": "photo_cultural_analyzer",
                        "analysis_sources": ["theme_image_only"],
                        "theme_context": {
                            "theme_name": theme_name,
                            "theme_id": theme_id,
                            "theme_image_found": theme_image.get("exists", False)
                        },
                        "conversation_count": len(conversation_starters),
                        "memory_trigger_count": len(memory_triggers),
                        "pipeline_mode": "automatic_theme_only",
                        "personal_photos_excluded": True
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Theme photo analysis failed: {e}")
            return self._create_theme_fallback_analysis(
                consolidated_info, theme_of_the_day
            )
    
    async def _analyze_theme_image_only(self, theme_image: Dict[str, Any], 
                                      theme: Dict[str, Any], heritage: str, 
                                      birth_year: Optional[int]) -> Dict[str, Any]:
        """
        FIXED: Analyze theme image with proper VisionAI handling
        Theme photos SHOULD be analyzed - personal photos are excluded from pipeline
        """
        
        theme_name = theme.get("name", "Unknown")
        theme_id = theme.get("id", "unknown")
        
        logger.info(f"🎯 Analyzing THEME image for '{theme_name}' (ID: {theme_id})")
        
        # Check if theme image exists
        if not theme_image.get("exists", False):
            logger.warning(f"⚠️ Theme image missing for theme '{theme_name}' - using fallback")
            return self._create_fallback_theme_analysis(theme, heritage)
        
        # Get image path
        image_path = theme_image.get("backend_path")
        if not image_path or not Path(image_path).exists():
            logger.warning(f"⚠️ Theme image file not found: {image_path} - using fallback")
            return self._create_fallback_theme_analysis(theme, heritage)
        
        try:
            # Check if VisionAI tool is available and properly initialized
            if not self.vision_ai_tool:
                logger.warning(f"⚠️ VisionAI tool not available - using theme-based fallback")
                return self._create_fallback_theme_analysis(theme, heritage)
            
            # Read and encode image for Vision AI
            logger.info(f"🔍 Running VisionAI analysis on THEME image: {theme_image.get('filename')}")
            
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Call VisionAI with proper error handling
            vision_result = await self.vision_ai_tool.analyze_with_google_vision(image_base64)
            
            if vision_result and vision_result.get("success"):
                logger.info(f"✅ VisionAI analysis successful for THEME image: {theme_image.get('filename')}")
                
                # Generate theme-specific conversation starters based on VisionAI results
                theme_conversation_starters = self._generate_theme_conversation_starters_from_vision(
                    vision_result, theme, heritage, birth_year
                )
                
                # Generate theme-specific memory triggers
                theme_memory_triggers = self._generate_theme_memory_triggers_from_vision(
                    vision_result, theme, heritage
                )
                
                # Assess theme alignment
                theme_alignment = self._assess_theme_alignment(vision_result, theme)
                
                return {
                    "vision_analysis": vision_result,
                    "conversation_starters": theme_conversation_starters,
                    "memory_triggers": theme_memory_triggers,
                    "theme_alignment": theme_alignment,
                    "status": "analyzed"
                }
            else:
                logger.warning(f"⚠️ VisionAI failed for THEME image: {theme_image.get('filename')} - using fallback")
                return self._create_fallback_theme_analysis(theme, heritage)
                
        except Exception as e:
            logger.error(f"❌ THEME image analysis failed: {e}")
            logger.info(f"🔄 Using fallback analysis for theme: {theme_name}")
            return self._create_fallback_theme_analysis(theme, heritage)
    
    def _generate_theme_conversation_starters_from_vision(self, 
                                                        vision_result: Dict[str, Any],
                                                        theme: Dict[str, Any], 
                                                        heritage: str,
                                                        birth_year: Optional[int]) -> List[Dict[str, Any]]:
        """
        Generate conversation starters for THEME photos based on VisionAI analysis
        """
        
        theme_name = theme.get("name", "Unknown")
        theme_prompts = theme.get("conversation_prompts", [])
        
        objects = vision_result.get("objects", [])
        labels = vision_result.get("labels", [])
        
        starters = []
        
        # Use theme's built-in prompts as high priority
        for i, prompt in enumerate(theme_prompts[:2]):  # Use first 2 theme prompts
            starters.append({
                "type": "theme_prompt",
                "starter": prompt,
                "follow_up": f"What do you remember about {theme_name.lower()}?",
                "theme_context": theme_name,
                "source": "theme_config",
                "priority": "high"
            })
        
        # Add VisionAI-based starters
        if "people" in objects or "family" in labels:
            starters.append({
                "type": "theme_people",
                "starter": f"This {theme_name.lower()} image shows people together.",
                "follow_up": f"What {theme_name.lower()} memories do you have with others?",
                "theme_context": theme_name,
                "source": "vision_ai",
                "priority": "high"
            })
        
        if "home" in labels or "house" in objects or "building" in objects:
            starters.append({
                "type": "theme_place",
                "starter": f"This reminds me of {theme_name.lower()} at home.",
                "follow_up": f"What was {theme_name.lower()} like in your home?",
                "theme_context": theme_name,
                "source": "vision_ai",
                "priority": "medium"
            })
        
        if "celebration" in labels or "gathering" in labels:
            starters.append({
                "type": "theme_celebration",
                "starter": f"This looks like a {theme_name.lower()} celebration.",
                "follow_up": f"What celebrations do you remember?",
                "theme_context": theme_name,
                "source": "vision_ai",
                "priority": "medium"
            })
        
        # Fallback if no specific starters generated
        if len(starters) < 3:
            starters.append({
                "type": "theme_general",
                "starter": f"What does this {theme_name.lower()} image remind you of?",
                "follow_up": "Tell me about those memories.",
                "theme_context": theme_name,
                "source": "theme_fallback",
                "priority": "medium"
            })
        
        # Sort by priority and limit
        starters.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 2))
        return starters[:5]  # Return top 5 theme starters
    
    def _generate_theme_memory_triggers_from_vision(self, 
                                                  vision_result: Dict[str, Any],
                                                  theme: Dict[str, Any], 
                                                  heritage: str) -> List[str]:
        """
        Generate memory triggers for THEME photos based on VisionAI analysis
        """
        
        theme_name = theme.get("name", "Unknown")
        labels = vision_result.get("labels", [])
        objects = vision_result.get("objects", [])
        
        triggers = []
        
        # Add theme-specific triggers
        triggers.append(f"{theme_name} memories")
        
        # Add VisionAI-based triggers
        for label in labels[:3]:  # Use top 3 labels
            triggers.append(f"{label} and {theme_name.lower()}")
        
        for obj in objects[:2]:  # Use top 2 objects
            triggers.append(f"{obj} memories")
        
        # Add heritage-specific trigger if relevant
        if heritage and heritage != "American":
            triggers.append(f"{heritage} {theme_name.lower()} traditions")
        
        return triggers[:5]  # Limit to 5 triggers
    
    def _assess_theme_alignment(self, vision_result: Dict[str, Any], 
                               theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess how well the theme image aligns with the theme
        """
        
        theme_name = theme.get("name", "Unknown").lower()
        theme_keywords = theme.get("conversation_prompts", [])
        
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
            if any(word.lower() in detected_labels or word.lower() in detected_objects 
                   for word in keyword.split()):
                alignment_score += 1
                matching_elements.append(keyword)
        
        return {
            "alignment_score": alignment_score,
            "max_possible_score": 2 + len(theme_keywords),
            "matching_elements": matching_elements,
            "alignment_quality": "high" if alignment_score >= 2 else "medium" if alignment_score >= 1 else "low"
        }
    
    def _analyze_theme_cultural_alignment(self, theme_analysis: Dict[str, Any],
                                        heritage: str, theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze cultural alignment for theme only
        """
        
        return {
            "heritage_context": heritage,
            "theme_context": theme.get("name", "Unknown"),
            "theme_image_available": bool(theme_analysis.get("vision_analysis")),
            "cultural_coherence": "theme_focused"
        }
    
    def _create_fallback_theme_analysis(self, theme: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """
        Create fallback analysis when theme image analysis fails
        """
        
        theme_name = theme.get("name", "Unknown")
        theme_prompts = theme.get("conversation_prompts", [])
        
        # Use theme conversation prompts as fallback
        fallback_starters = []
        if theme_prompts:
            for prompt in theme_prompts[:3]:
                fallback_starters.append({
                    "type": "theme_fallback",
                    "starter": prompt,
                    "follow_up": f"Tell me more about {theme_name.lower()}.",
                    "theme_context": theme_name,
                    "source": "theme_fallback",
                    "priority": "medium"
                })
        
        # Ensure at least one fallback starter
        if not fallback_starters:
            fallback_starters.append({
                "type": "theme_general",
                "starter": f"What does {theme_name.lower()} remind you of?",
                "follow_up": "Tell me about those memories.",
                "theme_context": theme_name,
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
    
    def _create_theme_fallback_analysis(self, consolidated_info: Dict[str, Any],
                                      theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create fallback analysis when entire theme analysis fails
        """
        
        theme_name = theme.get("name", "Unknown")
        
        return {
            "photo_analysis": {
                "status": "fallback",
                "analysis_type": "theme_fallback",
                "primary_source": "fallback",
                
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
                    "pipeline_mode": "automatic_theme_only",
                    "personal_photos_excluded": True,
                    "fallback_reason": "theme_analysis_failure"
                }
            }
        }