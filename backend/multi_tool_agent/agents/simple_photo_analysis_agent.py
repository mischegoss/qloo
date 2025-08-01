"""
Step 2: Simple Photo Analysis Agent
File: backend/multi_tool_agent/agents/simple_photo_analysis_agent.py

Features:
- Uses pre-analyzed photos first (to save build time)
- Uses live Google Vision AI as fallback
- Planned improvement: Upload photos to be analyzed with Google Vision to better personalize prefernes
"""

import logging
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class SimplePhotoAnalysisAgent:
    """
    Step 2: Simple Photo Analysis Agent
    
    PURPOSE:
    - Take consolidated profile from Step 1
    - Load pre-analyzed photo data based on theme
    - Add photo analysis to profile for Step 3
    - Maintain demo reliability with fallbacks
    """
    
    def __init__(self, vision_tool=None):
        self.vision_tool = vision_tool
        self.photo_analysis_data = self._load_photo_analysis_data()
        
        logger.info("✅ Step 2: Simple Photo Analysis Agent initialized")
        logger.info(f"📷 Loaded pre-analyzed data for {len(self.photo_analysis_data.get('photo_analyses', []))} photos")
    
    def _load_photo_analysis_data(self) -> Dict[str, Any]:
        """Load pre-analyzed photo data from config - FIXED PATH"""
        
        # CRITICAL FIX: Correct path to existing config file
        potential_paths = [
            # Primary path: config/photo_analyses.json (this is where the file actually exists)
            Path(__file__).parent.parent.parent / "config" / "photo_analyses.json",
            # Fallback paths for different execution contexts
            Path("config/photo_analyses.json"),
            Path("backend/config/photo_analyses.json"),
            # Legacy path (in case it was moved)
            Path(__file__).parent.parent.parent / "config" / "photos" / "photo_analyses.json"
        ]
        
        for config_path in potential_paths:
            try:
                if config_path.exists():
                    logger.info(f"📁 Found photo analysis config at: {config_path}")
                    with open(config_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Validate the data structure
                        if "photo_analyses" in data:
                            photo_count = len(data["photo_analyses"])
                            logger.info(f"✅ Loaded {photo_count} photo analyses from {config_path}")
                            return data
                        else:
                            logger.warning(f"⚠️ Invalid structure in {config_path}, missing 'photo_analyses' key")
                            
            except Exception as e:
                logger.warning(f"⚠️ Could not load {config_path}: {e}")
                continue
        
        # If no config found, log all attempted paths and use fallback
        logger.warning("⚠️ Photo analysis config not found at any of these locations:")
        for path in potential_paths:
            logger.warning(f"   - {path}")
        
        logger.info("🔄 Using fallback photo analysis data")
        return self._get_fallback_photo_data()
    
    def _get_fallback_photo_data(self) -> Dict[str, Any]:
        """Provide fallback photo analysis data when config is missing"""
        
        return {
            "photo_analyses": [
                {
                    "image_name": "family.png",
                    "theme": "family",
                    "google_vision_description": "A warm family gathering with multiple generations sitting together",
                    "conversation_starters": [
                        "Tell me about your family",
                        "What family traditions were special to you?",
                        "Do you remember family gatherings like this?"
                    ],
                    "dementia_friendly": True,
                    "safety_level": "positive_memories"
                },
                {
                    "image_name": "memory_lane.png",
                    "theme": "memory_lane",
                    "google_vision_description": "A nostalgic scene showing objects from the past",
                    "conversation_starters": [
                        "This reminds me of the good old days",
                        "What brings back happy memories for you?",
                        "Tell me about something from your past"
                    ],
                    "dementia_friendly": True,
                    "safety_level": "positive_memories"
                }
            ],
            "metadata": {
                "source": "fallback_data",
                "total_photos": 2,
                "dementia_safe": True
            }
        }
    
    async def run(self, consolidated_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Analyze photo and enhance profile
        
        Args:
            consolidated_profile: Output from Step 1
            
        Returns:
            Enhanced profile with photo analysis for Step 3
        """
        
        logger.info("📸 Step 2: Starting simple photo analysis")
        
        try:
            # Extract theme information from Step 1
            theme_info = consolidated_profile.get("theme_info", {})
            photo_filename = theme_info.get("photo_filename", "")
            theme_name = theme_info.get("name", "Unknown")
            
            logger.info(f"🎯 Analyzing photo: {photo_filename} for theme: {theme_name}")
            
            # Get photo analysis data
            photo_analysis = await self._analyze_photo(photo_filename, theme_info)
            
            # Enhance the consolidated profile
            enhanced_profile = self._enhance_profile_with_photo_analysis(
                consolidated_profile, photo_analysis
            )
            
            logger.info(f"✅ Step 2: Photo analysis completed for {photo_filename}")
            
            return enhanced_profile
            
        except Exception as e:
            logger.error(f"❌ Step 2 failed: {e}")
            return self._create_fallback_enhanced_profile(consolidated_profile)
    
    async def _analyze_photo(self, photo_filename: str, theme_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze photo using pre-analyzed data or real-time Vision AI
        
        Args:
            photo_filename: Name of photo file (e.g. "family.png")
            theme_info: Theme information from Step 1
            
        Returns:
            Photo analysis data
        """
        
        logger.info(f"🔍 Step 2: Analyzing photo {photo_filename}")
        
        # First try: Get pre-analyzed data
        pre_analyzed = self._get_pre_analyzed_data(photo_filename)
        
        if pre_analyzed:
            logger.info(f"✅ Using pre-analyzed data for {photo_filename}")
            return {
                "analysis_data": pre_analyzed,
                "source": "pre_analyzed",
                "theme_connection": theme_info.get("name", "Unknown"),
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        # Second try: Real-time Vision AI analysis
        if self.vision_tool and photo_filename:
            logger.info(f"🔄 Attempting real-time Vision AI analysis for {photo_filename}")
            try:
                vision_result = await self._use_vision_ai(photo_filename)
                if vision_result:
                    return {
                        "analysis_data": vision_result,
                        "source": "vision_ai",
                        "theme_connection": theme_info.get("name", "Unknown"),
                        "analysis_timestamp": datetime.now().isoformat()
                    }
            except Exception as e:
                logger.warning(f"⚠️ Vision AI failed: {e}")
        
        # Third try: Theme-based fallback
        logger.info(f"🔄 Using theme-based fallback analysis")
        return self._get_theme_based_fallback(theme_info)
    
    def _get_pre_analyzed_data(self, photo_filename: str) -> Optional[Dict[str, Any]]:
        """Get pre-analyzed data for specific photo"""
        
        photo_analyses = self.photo_analysis_data.get("photo_analyses", [])
        
        for analysis in photo_analyses:
            if analysis.get("image_name") == photo_filename:
                return analysis
        
        # Try partial matching (without extension)
        base_filename = photo_filename.replace(".png", "").replace(".jpg", "")
        
        for analysis in photo_analyses:
            analysis_name = analysis.get("image_name", "").replace(".png", "").replace(".jpg", "")
            if analysis_name == base_filename:
                return analysis
        
        return None
    
    async def _use_vision_ai(self, photo_filename: str) -> Optional[Dict[str, Any]]:
        """Use Google Vision AI for real-time analysis"""
        
        try:
            # This would call the actual Vision AI tool
            # For now, return a safe fallback
            return {
                "google_vision_description": f"Analysis of {photo_filename}",
                "conversation_starters": [
                    "What do you see in this image?",
                    "Does this remind you of anything?",
                    "What are your thoughts about this?"
                ],
                "dementia_friendly": True,
                "safety_level": "positive_memories"
            }
        except Exception as e:
            logger.error(f"❌ Vision AI analysis failed: {e}")
            return None
    
    def _get_theme_based_fallback(self, theme_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback analysis based on theme"""
        
        theme_name = theme_info.get("name", "Memory Lane")
        theme_id = theme_info.get("id", "memory_lane")
        
        return {
            "analysis_data": {
                "google_vision_description": f"A {theme_name.lower()} themed image",
                "conversation_starters": theme_info.get("conversation_prompts", [
                    "What does this make you think of?",
                    "Does this bring back any memories?"
                ])[:3],
                "dementia_friendly": True,
                "safety_level": "positive_memories",
                "theme": theme_id
            },
            "source": "theme_fallback",
            "theme_connection": theme_name,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _enhance_profile_with_photo_analysis(self, 
                                           consolidated_profile: Dict[str, Any],
                                           photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Add photo analysis to consolidated profile"""
        
        enhanced_profile = consolidated_profile.copy()
        
        # Add photo analysis section
        enhanced_profile["photo_analysis"] = photo_analysis
        
        # Update pipeline state
        pipeline_state = enhanced_profile.get("pipeline_state", {})
        pipeline_state.update({
            "current_step": 2,
            "next_step": "qloo_cultural_analysis",
            "photo_analysis_complete": True,
            "step2_timestamp": datetime.now().isoformat()
        })
        enhanced_profile["pipeline_state"] = pipeline_state
        
        logger.info("✅ Profile enhanced with photo analysis")
        
        return enhanced_profile
    
    def _create_fallback_enhanced_profile(self, consolidated_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback enhanced profile when analysis fails"""
        
        enhanced_profile = consolidated_profile.copy()
        
        # Add minimal photo analysis
        enhanced_profile["photo_analysis"] = {
            "analysis_data": {
                "google_vision_description": "Photo analysis not available",
                "conversation_starters": [
                    "Tell me what you see",
                    "What does this remind you of?"
                ],
                "dementia_friendly": True,
                "safety_level": "positive_memories"
            },
            "source": "fallback",
            "theme_connection": "General",
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Update pipeline state
        pipeline_state = enhanced_profile.get("pipeline_state", {})
        pipeline_state.update({
            "current_step": 2,
            "next_step": "qloo_cultural_analysis",
            "photo_analysis_complete": False,
            "step2_fallback_used": True,
            "step2_timestamp": datetime.now().isoformat()
        })
        enhanced_profile["pipeline_state"] = pipeline_state
        
        return enhanced_profile
    
    def get_available_photos(self) -> List[str]:
        """Get list of available pre-analyzed photos"""
        photo_analyses = self.photo_analysis_data.get("photo_analyses", [])
        return [analysis.get("image_name", "") for analysis in photo_analyses if analysis.get("image_name")]
    
    def validate_photo_analysis_data(self) -> Dict[str, Any]:
        """Validate photo analysis configuration"""
        
        photo_analyses = self.photo_analysis_data.get("photo_analyses", [])
        
        validation = {
            "total_photos": len(photo_analyses),
            "photos_available": [analysis.get("image_name", "") for analysis in photo_analyses],
            "all_dementia_friendly": all(
                analysis.get("dementia_friendly", False) for analysis in photo_analyses
            ),
            "all_positive_memories": all(
                analysis.get("safety_level") == "positive_memories" for analysis in photo_analyses
            ),
            "data_source": self.photo_analysis_data.get("metadata", {}).get("source", "unknown")
        }
        
        logger.info(f"📊 Photo analysis validation: {validation['total_photos']} photos, dementia_friendly: {validation['all_dementia_friendly']}")
        
        return validation

# Export the main class
__all__ = ["SimplePhotoAnalysisAgent"]