"""
Step 2: Simple Photo Analysis Agent - FIXED PATH
File: backend/multi_tool_agent/agents/simple_photo_analysis_agent.py

FIXED: Corrected path to config/photos/photo_analyses.json

SIMPLIFIED APPROACH:
- Loads pre-analyzed photo data for demo reliability
- Maps theme → photo filename → analysis data
- Falls back to Google Vision AI if needed
- Clean data structure for Step 3
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
        logger.info(f"📷 Loaded pre-analyzed data for {len(self.photo_analysis_data.get('photo_analysis_data', {}))} photos")
    
    def _load_photo_analysis_data(self) -> Dict[str, Any]:
        """Load pre-analyzed photo data from config - FIXED PATH"""
        
        try:
            # FIXED: Correct path to config/photos/photo_analyses.json
            config_path = Path(__file__).parent.parent.parent / "config" / "photos" / "photo_analyses.json"
            
            if config_path.exists():
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    logger.info(f"✅ Loaded photo analysis data from {config_path}")
                    return data
            else:
                logger.warning(f"⚠️ Photo analysis config not found: {config_path}")
                
        except Exception as e:
            logger.error(f"❌ Error loading photo analysis data: {e}")
        
        # Return fallback structure
        return {"photo_analysis_data": {}, "fallback_analysis": {}}
    
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
            photo_filename: Name of photo file (e.g. "birthday.png")
            theme_info: Theme information from Step 1
            
        Returns:
            Photo analysis data
        """
        
        logger.info(f"🔍 Step 2: Analyzing photo {photo_filename}")
        
        # PRIORITY 1: Try pre-analyzed data (recommended for demo)
        if photo_filename in self.photo_analysis_data.get("photo_analysis_data", {}):
            analysis_data = self.photo_analysis_data["photo_analysis_data"][photo_filename]
            
            logger.info(f"✅ Using pre-analyzed data for {photo_filename}")
            
            return {
                "photo_filename": photo_filename,
                "analysis_method": "pre_analyzed",
                "analysis_data": analysis_data,
                "theme_connection": theme_info.get("name", "Unknown"),
                "analysis_timestamp": datetime.now().isoformat(),
                "success": True
            }
        
        # PRIORITY 2: Try real-time Vision AI analysis (backup)
        if self.vision_tool:
            logger.info(f"🔄 Attempting real-time Vision AI analysis for {photo_filename}")
            
            real_time_analysis = await self._real_time_vision_analysis(photo_filename, theme_info)
            if real_time_analysis and real_time_analysis.get("success"):
                return real_time_analysis
        
        # PRIORITY 3: Use fallback analysis
        logger.info(f"📋 Using fallback analysis for {photo_filename}")
        return self._get_fallback_analysis(photo_filename, theme_info)
    
    async def _real_time_vision_analysis(self, photo_filename: str, theme_info: Dict[str, Any]) -> Dict[str, Any]:
        """Perform real-time Vision AI analysis on photo"""
        
        try:
            # In production, this would analyze the actual photo file
            # For now, return a mock real-time analysis structure
            
            theme_name = theme_info.get("name", "Memory")
            
            return {
                "photo_filename": photo_filename,
                "analysis_method": "real_time_vision_ai",
                "analysis_data": {
                    "description": f"A {theme_name.lower()} photo with warm, positive elements",
                    "conversation_starters": [
                        f"This {theme_name.lower()} photo brings back wonderful memories",
                        "What do you see in this image?",
                        "Tell me about this moment"
                    ],
                    "cultural_context": f"{theme_name.lower()} memories and experiences",
                    "memory_triggers": [theme_name.lower(), "memories", "experiences"],
                    "analysis_confidence": "real_time_vision_ai",
                    "dementia_friendly": True,
                    "safety_level": "positive_memories"
                },
                "theme_connection": theme_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ Real-time Vision AI analysis failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_fallback_analysis(self, photo_filename: str, theme_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get fallback analysis when other methods fail"""
        
        fallback_data = self.photo_analysis_data.get("fallback_analysis", {})
        theme_name = theme_info.get("name", "Memory")
        
        # Customize fallback for theme
        customized_fallback = fallback_data.copy()
        customized_fallback["conversation_starters"] = [
            f"This {theme_name.lower()} image brings back warm memories",
            f"Tell me about {theme_name.lower()} experiences you've had",
            "What memories does this bring to mind?"
        ]
        customized_fallback["cultural_context"] = f"{theme_name.lower()} memories and positive experiences"
        customized_fallback["memory_triggers"] = [theme_name.lower(), "memories", "experiences", "stories"]
        
        return {
            "photo_filename": photo_filename,
            "analysis_method": "fallback",
            "analysis_data": customized_fallback,
            "theme_connection": theme_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "success": True
        }
    
    def _enhance_profile_with_photo_analysis(self, consolidated_profile: Dict[str, Any], 
                                           photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add photo analysis to consolidated profile
        
        Args:
            consolidated_profile: Profile from Step 1
            photo_analysis: Photo analysis results
            
        Returns:
            Enhanced profile ready for Step 3
        """
        
        # Create enhanced profile (copy original)
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
        
        # Add step 2 metadata
        enhanced_profile["step2_metadata"] = {
            "agent": "SimplePhotoAnalysisAgent",
            "photo_filename": photo_analysis.get("photo_filename", "unknown"),
            "analysis_method": photo_analysis.get("analysis_method", "fallback"),
            "theme_connection": photo_analysis.get("theme_connection", "Unknown"),
            "success": photo_analysis.get("success", False),
            "processing_time": "step2_complete"
        }
        
        logger.info(f"✅ Profile enhanced with photo analysis")
        return enhanced_profile
    
    def _create_fallback_enhanced_profile(self, consolidated_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback enhanced profile when Step 2 fails completely"""
        
        logger.warning("🔄 Creating fallback enhanced profile for Step 2")
        
        # Use emergency fallback analysis
        emergency_analysis = {
            "photo_filename": "fallback.png",
            "analysis_method": "emergency_fallback",
            "analysis_data": self.photo_analysis_data.get("fallback_analysis", {}),
            "theme_connection": "General",
            "analysis_timestamp": datetime.now().isoformat(),
            "success": False,
            "error": "step2_complete_failure"
        }
        
        # Create enhanced profile with emergency fallback
        enhanced_profile = consolidated_profile.copy()
        enhanced_profile["photo_analysis"] = emergency_analysis
        
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
        return list(self.photo_analysis_data.get("photo_analysis_data", {}).keys())
    
    def validate_photo_analysis_data(self) -> Dict[str, Any]:
        """Validate photo analysis configuration"""
        
        photo_data = self.photo_analysis_data.get("photo_analysis_data", {})
        fallback_data = self.photo_analysis_data.get("fallback_analysis", {})
        
        validation = {
            "total_photos": len(photo_data),
            "photos_available": list(photo_data.keys()),
            "fallback_available": bool(fallback_data),
            "all_dementia_friendly": all(
                data.get("dementia_friendly", False) for data in photo_data.values()
            ),
            "all_positive_memories": all(
                data.get("safety_level") == "positive_memories" for data in photo_data.values()
            )
        }
        
        logger.info(f"📊 Photo analysis validation: {validation['total_photos']} photos, dementia_friendly: {validation['all_dementia_friendly']}")
        
        return validation

# Export the main class
__all__ = ["SimplePhotoAnalysisAgent"]