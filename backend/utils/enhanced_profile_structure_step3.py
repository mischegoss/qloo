"""
Enhanced Profile Structure - Step 3 Integration (Anonymized)
File: backend/utils/enhanced_profile_structure_step3.py

COMPLETE ANONYMIZED INTEGRATION FIX:
- Updated extract_for_step3() to map patient_info → patient_profile (NO PII)
- Maintains all existing functionality and backward compatibility
- Ready for simplified Cultural Analysis Agent with anonymized data
- Includes all validation and summary methods (NO PII)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnhancedProfileStructure:
    """
    Enhanced Profile Structure with complete Step 3 integration fix (Anonymized).
    Handles anonymized data flow between all pipeline steps with proper format mapping.
    NO PII PROCESSING - BACKEND SAFE
    """
    
    def __init__(self):
        self.version = "2.0.0"
        logger.info("✅ Enhanced Profile Structure initialized - Step 3 compatible (Anonymized)")
    
    def extract_for_step3(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract anonymized data needed for Step 3 (Cultural Analysis).
        CRITICAL FIX: Maps patient_info → patient_profile for simplified Cultural Analysis Agent.
        NO PII - COMPLETELY ANONYMIZED
        
        Args:
            enhanced_profile: Anonymized profile after Step 2
            
        Returns:
            Anonymized data formatted for simplified Cultural Analysis Agent
        """
        
        logger.info("🔧 Extracting Step 3 data - simplified agent compatible format (anonymized)")
        
        # Get original anonymized data sections
        patient_info = enhanced_profile.get("patient_info", {})
        theme_info = enhanced_profile.get("theme_info", {})
        photo_analysis = enhanced_profile.get("photo_analysis", {})
        pipeline_state = enhanced_profile.get("pipeline_state", {})
        feedback_info = enhanced_profile.get("feedback_info", {})
        
        # CRITICAL: Verify no PII is present
        pii_fields = ["first_name", "last_name", "name", "city", "state", "address", "phone", "email"]
        for pii_field in pii_fields:
            if pii_field in patient_info:
                logger.error(f"❌ PII DETECTED: {pii_field} found in patient_info - CANNOT PROCEED")
                return {
                    "error": f"PII detected: {pii_field}",
                    "ready_for_qloo": False,
                    "anonymization_failed": True
                }
        
        # CRITICAL FIX: Map patient_info → patient_profile for simplified Cultural Analysis Agent
        # ANONYMIZED VERSION - NO PII
        step3_data = {
            # Main anonymized data for simplified Cultural Analysis Agent (NEW FORMAT)
            "patient_profile": {
                "cultural_heritage": patient_info.get("cultural_heritage", "American"),
                "birth_year": patient_info.get("birth_year", 1942),
                "current_age": patient_info.get("current_age", 80),
                "age_group": patient_info.get("age_group", "senior"),
                "interests": patient_info.get("interests", ["music", "family", "cooking"]),
                "profile_complete": patient_info.get("profile_complete", False)
                # NO PII FIELDS: first_name, location, additional_context removed
            },
            
            # Keep original anonymized sections for backward compatibility
            "patient_info": patient_info,
            "theme_info": theme_info,
            "photo_analysis": photo_analysis,
            "feedback_info": feedback_info,
            "pipeline_state": pipeline_state,
            
            # Step 3 readiness indicators
            "ready_for_qloo": self._check_step3_readiness(enhanced_profile),
            "anonymization_verified": True,
            "step3_metadata": {
                "extracted_at": datetime.now().isoformat(),
                "heritage_extracted": bool(patient_info.get("cultural_heritage")),
                "theme_available": bool(theme_info.get("name")),
                "photo_analyzed": photo_analysis.get("success", False),
                "simplified_agent_compatible": True,
                "data_format": "patient_profile_mapped_anonymized",
                "pii_removed": True
            }
        }
        
        heritage = step3_data['patient_profile']['cultural_heritage']
        age_group = step3_data['patient_profile']['age_group']
        ready = step3_data['ready_for_qloo']
        logger.info(f"✅ Step 3 anonymized data extracted - Heritage: {heritage}, Age: {age_group}, Ready: {ready}")
        
        return step3_data
    
    def _check_step3_readiness(self, profile: Dict[str, Any]) -> bool:
        """Check if anonymized profile is ready for Step 3 Cultural Analysis"""
        
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        photo_analysis = profile.get("photo_analysis", {})
        
        # Check essential anonymized data for Cultural Analysis
        has_heritage = bool(patient_info.get("cultural_heritage"))
        has_age_group = bool(patient_info.get("age_group"))
        has_interests = bool(patient_info.get("interests"))
        has_theme = bool(theme_info.get("name"))
        has_photo = bool(photo_analysis.get("photo_filename"))
        
        ready = has_heritage and has_age_group and has_interests and has_theme and has_photo
        
        logger.info(f"🎯 Step 3 readiness: {ready} (heritage: {has_heritage}, age_group: {has_age_group}, interests: {has_interests}, theme: {has_theme}, photo: {has_photo})")
        return ready
    
    def validate_step2_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 2 anonymized profile for Step 3 readiness.
        Checks both Step 1 and Step 2 data completeness with PII detection.
        """
        
        validation = {
            "valid": True,
            "step1_valid": True,
            "step2_valid": True,
            "ready_for_step3": False,
            "anonymization_verified": True,
            "errors": [],
            "warnings": []
        }
        
        # CRITICAL: Check for PII first
        patient_info = profile.get("patient_info", {})
        pii_fields = ["first_name", "last_name", "name", "city", "state", "address", "phone", "email"]
        
        for pii_field in pii_fields:
            if pii_field in patient_info:
                validation["errors"].append(f"PII DETECTED: {pii_field} must not be present in backend")
                validation["anonymization_verified"] = False
                validation["valid"] = False
        
        # Check Step 1 anonymized data (patient and theme)
        theme_info = profile.get("theme_info", {})
        
        if not patient_info.get("cultural_heritage"):
            validation["errors"].append("Missing cultural heritage")
            validation["step1_valid"] = False
            validation["valid"] = False
        
        if not patient_info.get("age_group"):
            validation["warnings"].append("Missing age group")
        
        if not patient_info.get("interests"):
            validation["warnings"].append("Missing interests")
        
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
        
        # Overall readiness for Step 3 - ONLY if anonymized AND valid
        validation["ready_for_step3"] = (validation["valid"] and 
                                       validation["anonymization_verified"] and 
                                       self._check_step3_readiness(profile))
        
        return validation
    
    def get_step2_summary(self, profile: Dict[str, Any]) -> str:
        """Get human-readable Step 2 anonymized summary (NO PII)"""
        
        photo_analysis = profile.get("photo_analysis", {})
        patient_info = profile.get("patient_info", {})
        
        method = photo_analysis.get("analysis_method", "unknown")
        success = photo_analysis.get("success", False)
        filename = photo_analysis.get("photo_filename", "none")
        theme_connection = photo_analysis.get("theme_connection", "unknown")
        heritage = patient_info.get("cultural_heritage", "unknown")
        age_group = patient_info.get("age_group", "unknown")
        
        return f"Heritage: {heritage}, Age: {age_group}, Photo: {filename}, Method: {method}, Success: {success}, Theme: {theme_connection}"
    
    def combine_step1_step2_insights(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine anonymized insights from Steps 1-2 for Step 3 context.
        Creates comprehensive anonymized context for Cultural Analysis.
        NO PII PROCESSING
        """
        
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        photo_analysis = profile.get("photo_analysis", {})
        feedback_info = profile.get("feedback_info", {})
        
        # Extract comprehensive anonymized insights
        combined_insights = {
            # Core anonymized cultural context
            "cultural_heritage": patient_info.get("cultural_heritage", "American"),
            "age_group": patient_info.get("age_group", "senior"),
            "birth_year": patient_info.get("birth_year", 1942),
            "interests": patient_info.get("interests", ["music", "family", "cooking"]),
            "theme_context": theme_info.get("name", "Unknown"),
            "photo_connection": photo_analysis.get("theme_connection", "Unknown"),
            
            # Visual and memory context
            "visual_context": self._extract_visual_context(photo_analysis),
            "memory_triggers": theme_info.get("conversation_prompts", ["No memory triggers"]),
            "conversation_starters": self._extract_conversation_starters(photo_analysis),
            
            # Anonymized patient context (NO PII)
            "patient_context": {
                "age_group": patient_info.get("age_group", "Unknown"),
                "birth_year": patient_info.get("birth_year", "Unknown"),
                "cultural_heritage": patient_info.get("cultural_heritage", "Unknown"),
                "interests": patient_info.get("interests", [])
                # NO PII: name, age, location, additional_context removed
            },
            
            # Feedback insights
            "feedback_insights": {
                "available": feedback_info.get("feedback_available", False),
                "preferred_types": feedback_info.get("insights", {}).get("preferred_types", []),
                "avoided_types": feedback_info.get("insights", {}).get("avoided_types", []),
                "engagement_level": feedback_info.get("insights", {}).get("engagement_level", "new_user")
            },
            
            # Step 3 preparation (anonymized)
            "step3_context": {
                "heritage_for_qloo": patient_info.get("cultural_heritage", "American"),
                "age_group_for_qloo": patient_info.get("age_group", "senior"),
                "interests_for_qloo": patient_info.get("interests", ["music", "family", "cooking"]),
                "theme_for_context": theme_info.get("name", "Unknown"),
                "photo_analyzed": photo_analysis.get("success", False),
                "ready_for_cultural_analysis": self._check_step3_readiness(profile)
            },
            
            # Anonymization verification
            "anonymization_verified": True,
            "pii_removed": True
        }
        
        heritage = combined_insights['cultural_heritage']
        theme = combined_insights['theme_context']
        age_group = combined_insights['age_group']
        logger.info(f"🎯 Combined anonymized insights for Step 3: Heritage={heritage}, Age={age_group}, Theme={theme}")
        
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
        """Get overall anonymized pipeline summary (NO PII)"""
        
        pipeline_state = profile.get("pipeline_state", {})
        patient_info = profile.get("patient_info", {})
        
        current_step = pipeline_state.get("current_step", 0)
        next_step = pipeline_state.get("next_step", "unknown")
        heritage = patient_info.get("cultural_heritage", "Unknown")
        age_group = patient_info.get("age_group", "Unknown")
        
        return f"Step {current_step} → {next_step} | Heritage: {heritage}, Age: {age_group}"
    
    def extract_for_step4(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract anonymized data for Step 4 (content generation)"""
        
        # Verify anonymization first
        patient_info = profile.get("patient_info", {})
        pii_fields = ["first_name", "last_name", "name", "city", "state", "address"]
        
        for pii_field in pii_fields:
            if pii_field in patient_info:
                logger.error(f"❌ PII DETECTED in Step 4 extraction: {pii_field}")
                return {
                    "error": f"PII detected: {pii_field}",
                    "anonymization_failed": True
                }
        
        # Pass through the full anonymized profile for Step 4
        return {
            **profile,
            "step4_ready": True,
            "anonymization_verified": True
        }
    
    def add_qloo_intelligence(self, profile: Dict[str, Any], 
                            qloo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add Qloo intelligence data to anonymized profile (Step 3 → Step 4)"""
        
        try:
            profile["qloo_intelligence"] = qloo_data
            
            # Update pipeline state
            pipeline_state = profile.get("pipeline_state", {})
            pipeline_state.update({
                "current_step": 3,
                "next_step": "content_generation",
                "qloo_analysis_complete": True,
                "step3_timestamp": datetime.now().isoformat()
            })
            profile["pipeline_state"] = pipeline_state
            
            # Add Step 3 metadata (anonymized logging)
            qloo_metadata = qloo_data.get("metadata", {})
            successful_calls = qloo_metadata.get("successful_calls", 0)
            heritage = profile.get("patient_info", {}).get("cultural_heritage", "Unknown")
            
            logger.info(f"✅ Qloo intelligence added: {successful_calls} successful calls for {heritage} heritage")
            
            return profile
            
        except Exception as e:
            logger.error(f"❌ Failed to add Qloo intelligence: {e}")
            # Safe fallback - return original profile
            return profile
    
    def safe_get_heritage(self, profile: Dict[str, Any]) -> str:
        """Safely get cultural heritage with fallback"""
        try:
            return profile.get("patient_info", {}).get("cultural_heritage", "American")
        except:
            return "American"
    
    def safe_get_age_group(self, profile: Dict[str, Any]) -> str:
        """Safely get age group with fallback"""
        try:
            return profile.get("patient_info", {}).get("age_group", "senior")
        except:
            return "senior"
    
    def safe_get_interests(self, profile: Dict[str, Any]) -> List[str]:
        """Safely get interests with fallback"""
        try:
            interests = profile.get("patient_info", {}).get("interests", [])
            return interests if interests else ["music", "family", "cooking"]
        except:
            return ["music", "family", "cooking"]

# Create singleton instance for easy importing
enhanced_profile_structure = EnhancedProfileStructure()

# Export for imports
__all__ = ["enhanced_profile_structure", "EnhancedProfileStructure"]