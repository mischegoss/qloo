"""
Enhanced Profile Structure - Complete File with Step 3 Integration Fix
File: backend/utils/enhanced_profile_structure.py

COMPLETE INTEGRATION FIX:
- Updated extract_for_step3() to map patient_info → patient_profile
- Maintains all existing functionality and backward compatibility
- Ready for simplified Cultural Analysis Agent
- Includes all validation and summary methods
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnhancedProfileStructure:
    """
    Enhanced Profile Structure with complete Step 3 integration fix.
    Handles data flow between all pipeline steps with proper format mapping.
    """
    
    def __init__(self):
        self.version = "2.0"
        logger.info("✅ Enhanced Profile Structure initialized - Step 3 compatible")
    
    def extract_for_step3(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data needed for Step 3 (Cultural Analysis).
        CRITICAL FIX: Maps patient_info → patient_profile for simplified Cultural Analysis Agent.
        
        Args:
            enhanced_profile: Profile after Step 2
            
        Returns:
            Data formatted for simplified Cultural Analysis Agent
        """
        
        logger.info("🔧 Extracting Step 3 data - simplified agent compatible format")
        
        # Get original data sections
        patient_info = enhanced_profile.get("patient_info", {})
        theme_info = enhanced_profile.get("theme_info", {})
        photo_analysis = enhanced_profile.get("photo_analysis", {})
        pipeline_state = enhanced_profile.get("pipeline_state", {})
        feedback_info = enhanced_profile.get("feedback_info", {})
        
        # CRITICAL FIX: Map patient_info → patient_profile for simplified Cultural Analysis Agent
        step3_data = {
            # Main data for simplified Cultural Analysis Agent (NEW FORMAT)
            "patient_profile": {
                "cultural_heritage": patient_info.get("cultural_heritage", "American"),
                "birth_year": patient_info.get("birth_year", 1945),
                "first_name": patient_info.get("first_name", "Friend"),
                "current_age": patient_info.get("current_age", 80),
                "age_group": patient_info.get("age_group", "senior"),
                "location": patient_info.get("location", ""),
                "additional_context": patient_info.get("additional_context", ""),
                "demo_dislikes": patient_info.get("demo_dislikes", [])
            },
            
            # Keep original sections for backward compatibility
            "patient_info": patient_info,
            "theme_info": theme_info,
            "photo_analysis": photo_analysis,
            "feedback_info": feedback_info,
            "pipeline_state": pipeline_state,
            
            # Step 3 readiness indicators
            "ready_for_qloo": self._check_step3_readiness(enhanced_profile),
            "step3_metadata": {
                "extracted_at": datetime.now().isoformat(),
                "heritage_extracted": bool(patient_info.get("cultural_heritage")),
                "theme_available": bool(theme_info.get("name")),
                "photo_analyzed": photo_analysis.get("success", False),
                "simplified_agent_compatible": True,
                "data_format": "patient_profile_mapped"
            }
        }
        
        heritage = step3_data['patient_profile']['cultural_heritage']
        ready = step3_data['ready_for_qloo']
        logger.info(f"✅ Step 3 data extracted - Heritage: {heritage}, Ready: {ready}")
        
        return step3_data
    
    def _check_step3_readiness(self, profile: Dict[str, Any]) -> bool:
        """Check if profile is ready for Step 3 Cultural Analysis"""
        
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        photo_analysis = profile.get("photo_analysis", {})
        
        # Check essential data for Cultural Analysis
        has_heritage = bool(patient_info.get("cultural_heritage"))
        has_theme = bool(theme_info.get("name"))
        has_photo = bool(photo_analysis.get("photo_filename"))
        
        ready = has_heritage and has_theme and has_photo
        
        logger.info(f"🎯 Step 3 readiness: {ready} (heritage: {has_heritage}, theme: {has_theme}, photo: {has_photo})")
        return ready
    
    def validate_step2_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 2 profile for Step 3 readiness.
        Checks both Step 1 and Step 2 data completeness.
        """
        
        validation = {
            "valid": True,
            "step1_valid": True,
            "step2_valid": True,
            "ready_for_step3": False,
            "errors": [],
            "warnings": []
        }
        
        # Check Step 1 data (patient and theme)
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        
        if not patient_info.get("cultural_heritage"):
            validation["errors"].append("Missing cultural heritage")
            validation["step1_valid"] = False
            validation["valid"] = False
        
        if not patient_info.get("first_name"):
            validation["warnings"].append("Missing patient first name")
        
        if not theme_info.get("name"):
            validation["errors"].append("Missing theme name")
            validation["step1_valid"] = False
            validation["valid"] = False
        
        if not theme_info.get("photo_filename"):
            validation["warnings"].append("Missing photo filename")
        
        # Check Step 2 data (photo analysis)
        photo_analysis = profile.get("photo_analysis", {})
        
        if not photo_analysis:
            validation["errors"].append("Missing photo analysis")
            validation["step2_valid"] = False
            validation["valid"] = False
        else:
            if not photo_analysis.get("photo_filename"):
                validation["warnings"].append("No photo filename in analysis")
            
            if not photo_analysis.get("success"):
                validation["warnings"].append("Photo analysis was not successful")
                
            if not photo_analysis.get("analysis_method"):
                validation["warnings"].append("No analysis method specified")
        
        # Check pipeline state
        pipeline_state = profile.get("pipeline_state", {})
        if pipeline_state.get("current_step") != 2:
            validation["warnings"].append("Pipeline not at Step 2")
        
        # Overall readiness for Step 3
        validation["ready_for_step3"] = validation["valid"] and self._check_step3_readiness(profile)
        
        return validation
    
    def get_step2_summary(self, profile: Dict[str, Any]) -> str:
        """Get human-readable Step 2 summary"""
        
        photo_analysis = profile.get("photo_analysis", {})
        method = photo_analysis.get("analysis_method", "unknown")
        success = photo_analysis.get("success", False)
        filename = photo_analysis.get("photo_filename", "none")
        theme_connection = photo_analysis.get("theme_connection", "unknown")
        
        return f"Photo: {filename}, Method: {method}, Success: {success}, Theme: {theme_connection}"
    
    def combine_step1_step2_insights(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine insights from Steps 1-2 for Step 3 context.
        Creates comprehensive context for Cultural Analysis.
        """
        
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        photo_analysis = profile.get("photo_analysis", {})
        feedback_info = profile.get("feedback_info", {})
        
        # Extract comprehensive insights
        combined_insights = {
            # Core cultural context
            "cultural_heritage": patient_info.get("cultural_heritage", "American"),
            "theme_context": theme_info.get("name", "Unknown"),
            "photo_connection": photo_analysis.get("theme_connection", "Unknown"),
            
            # Visual and memory context
            "visual_context": self._extract_visual_context(photo_analysis),
            "memory_triggers": theme_info.get("conversation_prompts", ["No memory triggers"]),
            "conversation_starters": self._extract_conversation_starters(photo_analysis),
            
            # Patient context
            "patient_context": {
                "name": patient_info.get("first_name", "Friend"),
                "age": patient_info.get("current_age", "Unknown"),
                "birth_year": patient_info.get("birth_year", "Unknown"),
                "location": patient_info.get("location", "Unknown"),
                "additional_context": patient_info.get("additional_context", "")
            },
            
            # Feedback insights
            "feedback_insights": {
                "available": feedback_info.get("feedback_available", False),
                "preferred_types": feedback_info.get("insights", {}).get("preferred_types", []),
                "avoided_types": feedback_info.get("insights", {}).get("avoided_types", []),
                "engagement_level": feedback_info.get("insights", {}).get("engagement_level", "new_user")
            },
            
            # Step 3 preparation
            "step3_context": {
                "heritage_for_qloo": patient_info.get("cultural_heritage", "American"),
                "theme_for_context": theme_info.get("name", "Unknown"),
                "photo_analyzed": photo_analysis.get("success", False),
                "ready_for_cultural_analysis": self._check_step3_readiness(profile)
            }
        }
        
        heritage = combined_insights['cultural_heritage']
        theme = combined_insights['theme_context']
        logger.info(f"🎯 Combined insights for Step 3: Heritage={heritage}, Theme={theme}")
        
        return combined_insights
    
    def _extract_visual_context(self, photo_analysis: Dict[str, Any]) -> List[str]:
        """Extract visual context from photo analysis"""
        
        analysis_data = photo_analysis.get("analysis_data", {})
        
        # Try multiple possible keys for visual description
        visual_context = []
        
        if "description" in analysis_data:
            desc = analysis_data["description"]
            if isinstance(desc, list):
                visual_context.extend(desc)
            elif isinstance(desc, str):
                visual_context.append(desc)
        
        if "visual_elements" in analysis_data:
            elements = analysis_data["visual_elements"]
            if isinstance(elements, list):
                visual_context.extend(elements)
        
        if "key_objects" in analysis_data:
            objects = analysis_data["key_objects"]
            if isinstance(objects, list):
                visual_context.extend(objects)
        
        # Fallback if no visual context found
        if not visual_context:
            visual_context = ["Photo analyzed", "Visual content available"]
        
        return visual_context[:5]  # Limit to 5 elements
    
    def _extract_conversation_starters(self, photo_analysis: Dict[str, Any]) -> List[str]:
        """Extract conversation starters from photo analysis"""
        
        analysis_data = photo_analysis.get("analysis_data", {})
        
        conversation_starters = analysis_data.get("conversation_starters", [])
        
        # Fallback if none found
        if not conversation_starters:
            theme_connection = photo_analysis.get("theme_connection", "this image")
            conversation_starters = [
                f"What do you think about {theme_connection}?",
                "Does this bring back any memories?",
                "What's your favorite part of this?"
            ]
        
        return conversation_starters[:3]  # Limit to 3 starters
    
    def get_pipeline_summary(self, profile: Dict[str, Any]) -> str:
        """Get overall pipeline summary"""
        
        pipeline_state = profile.get("pipeline_state", {})
        patient_info = profile.get("patient_info", {})
        
        current_step = pipeline_state.get("current_step", 0)
        next_step = pipeline_state.get("next_step", "unknown")
        patient_name = patient_info.get("first_name", "Unknown")
        heritage = patient_info.get("cultural_heritage", "Unknown")
        
        return f"Step {current_step} → {next_step} | Patient: {patient_name} ({heritage})"
    
    def extract_for_step4(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data for Step 4 (placeholder for future use)"""
        
        # For now, just pass through the full profile
        # This can be enhanced later when Step 4 requirements are defined
        return profile
    
    def add_qloo_intelligence(self, profile: Dict[str, Any], 
                            qloo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add Qloo intelligence data to profile (Step 3 → Step 4)"""
        
        profile["qloo_intelligence"] = qloo_data
        
        # Update pipeline state
        pipeline_state = profile.get("pipeline_state", {})
        pipeline_state.update({
            "current_step": 3,
            "next_step": "content_curation",
            "qloo_analysis_complete": True,
            "step3_timestamp": datetime.now().isoformat()
        })
        profile["pipeline_state"] = pipeline_state
        
        # Add Step 3 metadata
        qloo_metadata = qloo_data.get("qloo_intelligence", {}).get("metadata", {})
        successful_calls = qloo_metadata.get("successful_calls", 0)
        heritage = qloo_metadata.get("heritage", "Unknown")
        
        logger.info(f"✅ Qloo intelligence added: {successful_calls} successful calls for {heritage}")
        
        return profile

# Create singleton instance for easy importing
enhanced_profile_structure = EnhancedProfileStructure()

# Export for imports
__all__ = ["enhanced_profile_structure", "EnhancedProfileStructure"]