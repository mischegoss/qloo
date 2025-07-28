"""
Enhanced Profile Structure for Steps 1-2-3 (Anonymized)
File: backend/utils/enhanced_profile_structure.py

Handles the complete anonymized data flow and validation for:
- Step 1 (Information Consolidation) → Step 2 (Photo Analysis)
- Step 2 (Photo Analysis) → Step 3 (Qloo Cultural Analysis)

FIXED TO MATCH ANONYMIZED DATA FLOW - NO PII IN BACKEND
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnhancedProfileStructure:
    """
    Enhanced Profile Structure Manager (Anonymized)
    
    Handles anonymized data flow and validation between Steps 1-2-3:
    - Validates Step 1 → Step 2 transition (NO PII)
    - Validates Step 2 → Step 3 transition (NO PII)
    - Provides clean data extraction for each step
    - Ensures strict anonymization throughout pipeline
    """
    
    def __init__(self):
        self.version = "2.0.0"
        logger.info("✅ Enhanced Profile Structure initialized - Anonymized Pipeline")
    
    def validate_step1_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 1 anonymized profile is ready for Step 2
        
        Args:
            profile: Anonymized profile from Step 1 (Information Consolidation)
            
        Returns:
            Validation results with PII detection
        """
        
        validation = {
            "valid": False,
            "step1_valid": False,
            "ready_for_step2": False,
            "anonymization_verified": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Check required Step 1 sections
            required_sections = ["patient_info", "theme_info", "feedback_info", "session_metadata", "pipeline_state"]
            
            for section in required_sections:
                if section not in profile:
                    validation["errors"].append(f"Missing required section: {section}")
            
            # CRITICAL: Check for PII in patient_info - MUST NOT BE PRESENT
            patient_info = profile.get("patient_info", {})
            pii_fields = ["first_name", "last_name", "name", "city", "state", "address", "phone", "email"]
            
            for pii_field in pii_fields:
                if pii_field in patient_info:
                    validation["errors"].append(f"PII DETECTED: {pii_field} must not be present in backend")
                    validation["anonymization_verified"] = False
            
            # Check required anonymized fields
            if not patient_info.get("cultural_heritage"):
                validation["warnings"].append("Missing cultural_heritage")
            if not patient_info.get("age_group"):
                validation["warnings"].append("Missing age_group")
            if not patient_info.get("interests"):
                validation["warnings"].append("Missing interests")
            
            # Check theme info
            theme_info = profile.get("theme_info", {})
            if not theme_info.get("name"):
                validation["errors"].append("Missing theme name")
            if not theme_info.get("photo_filename"):
                validation["warnings"].append("Missing photo_filename")
            
            # Check pipeline state
            pipeline_state = profile.get("pipeline_state", {})
            if pipeline_state.get("current_step") != 1:
                validation["errors"].append("Profile not at Step 1")
            if not pipeline_state.get("profile_ready"):
                validation["errors"].append("Profile not marked as ready")
            
            # Set validation results - ONLY valid if anonymized AND no errors
            validation["step1_valid"] = len(validation["errors"]) == 0 and validation["anonymization_verified"]
            validation["ready_for_step2"] = validation["step1_valid"]
            validation["valid"] = validation["step1_valid"]
            
            if validation["anonymization_verified"]:
                logger.info("✅ Step 1 profile anonymization verified")
            else:
                logger.error("❌ PII detected in Step 1 profile")
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Step 1 validation failed: {e}")
            validation["errors"].append(f"Validation exception: {str(e)}")
            return validation
    
    def validate_step2_profile(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 2 enhanced anonymized profile is ready for Step 3
        
        Args:
            enhanced_profile: Enhanced anonymized profile from Step 2 (Photo Analysis)
            
        Returns:
            Validation results with PII detection
        """
        
        validation = {
            "valid": False,
            "step1_valid": False,
            "step2_valid": False,
            "ready_for_step3": False,
            "anonymization_verified": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            # First validate Step 1 sections are still present and anonymized
            step1_validation = self.validate_step1_profile(enhanced_profile)
            validation["step1_valid"] = step1_validation["valid"]
            validation["anonymization_verified"] = step1_validation["anonymization_verified"]
            
            if not step1_validation["valid"]:
                validation["errors"].extend([f"Step 1: {error}" for error in step1_validation["errors"]])
            
            # Check Step 2 additions
            photo_analysis = enhanced_profile.get("photo_analysis", {})
            if not photo_analysis:
                validation["errors"].append("Missing photo_analysis section")
            else:
                # Validate photo analysis structure
                if not photo_analysis.get("photo_filename"):
                    validation["errors"].append("Missing photo_filename in analysis")
                if not photo_analysis.get("analysis_method"):
                    validation["errors"].append("Missing analysis_method in analysis")
                if "success" not in photo_analysis:
                    validation["errors"].append("Missing success flag in analysis")
                
                # Check analysis data
                analysis_data = photo_analysis.get("analysis_data", {})
                if not analysis_data:
                    validation["warnings"].append("Empty analysis_data")
            
            # Check pipeline state update
            pipeline_state = enhanced_profile.get("pipeline_state", {})
            if pipeline_state.get("current_step") != 2:
                validation["errors"].append("Pipeline not updated to Step 2")
            if pipeline_state.get("next_step") != "qloo_intelligence":
                validation["warnings"].append("Next step not set to qloo_intelligence")
            
            # Set validation results - ONLY valid if anonymized AND no errors
            step2_errors = [e for e in validation["errors"] if not e.startswith("Step 1:")]
            validation["step2_valid"] = len(step2_errors) == 0
            validation["ready_for_step3"] = (validation["step1_valid"] and 
                                           validation["step2_valid"] and 
                                           validation["anonymization_verified"])
            validation["valid"] = validation["ready_for_step3"]
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Step 2 validation failed: {e}")
            validation["errors"].append(f"Validation exception: {str(e)}")
            return validation
    
    def extract_for_step2(self, step1_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract anonymized data needed for Step 2 (Photo Analysis)
        
        Args:
            step1_profile: Anonymized profile from Step 1
            
        Returns:
            Clean anonymized data package for Step 2
        """
        
        try:
            # Validate anonymization first
            validation = self.validate_step1_profile(step1_profile)
            if not validation["anonymization_verified"]:
                logger.error("❌ PII detected in Step 1 profile - cannot proceed to Step 2")
                return {
                    "error": "PII detected in profile",
                    "validation_errors": validation["errors"],
                    "ready_for_photo_analysis": False
                }
            
            return {
                "patient_info": step1_profile.get("patient_info", {}),  # Anonymized only
                "theme_info": step1_profile.get("theme_info", {}),
                "feedback_info": step1_profile.get("feedback_info", {}),
                "session_metadata": step1_profile.get("session_metadata", {}),
                "pipeline_state": step1_profile.get("pipeline_state", {}),
                "ready_for_photo_analysis": True,
                "anonymization_verified": True
            }
            
        except Exception as e:
            logger.error(f"❌ Step 2 data extraction failed: {e}")
            return {"error": str(e), "ready_for_photo_analysis": False}
    
    def extract_for_step3(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract anonymized data needed for Step 3 (Qloo Cultural Analysis)
        
        Args:
            enhanced_profile: Enhanced anonymized profile from Step 2
            
        Returns:
            Clean anonymized data package for Step 3 Qloo Agent
        """
        
        try:
            # Validate anonymization first
            validation = self.validate_step2_profile(enhanced_profile)
            
            if not validation["anonymization_verified"]:
                logger.error("❌ PII detected in Step 2 profile - cannot proceed to Step 3")
                return {
                    "error": "PII detected in profile",
                    "validation_errors": validation["errors"],
                    "ready_for_qloo": False
                }
            
            if not validation["valid"]:
                return {
                    "error": "Step 2 validation failed",
                    "validation_errors": validation["errors"],
                    "ready_for_qloo": False
                }
            
            # Extract anonymized patient info
            patient_info = enhanced_profile.get("patient_info", {})
            
            # Create anonymized patient profile for Qloo Agent
            anonymized_patient_profile = {
                "cultural_heritage": patient_info.get("cultural_heritage", "American"),
                "birth_year": patient_info.get("birth_year", 1942),
                "current_age": patient_info.get("current_age", 80),
                "age_group": patient_info.get("age_group", "senior"),
                "interests": patient_info.get("interests", ["music", "family", "cooking"]),
                "profile_complete": patient_info.get("profile_complete", False)
            }
            
            return {
                # PRIMARY DATA FOR QLOO AGENT (anonymized format)
                "patient_profile": anonymized_patient_profile,
                
                # SUPPORTING ANONYMIZED DATA
                "patient_info": patient_info,  # Keep for backward compatibility
                "theme_info": enhanced_profile.get("theme_info", {}),
                "feedback_info": enhanced_profile.get("feedback_info", {}),
                "photo_analysis": enhanced_profile.get("photo_analysis", {}),
                "session_metadata": enhanced_profile.get("session_metadata", {}),
                "pipeline_state": enhanced_profile.get("pipeline_state", {}),
                
                # STEP 3 METADATA
                "ready_for_qloo": True,
                "anonymization_verified": True,
                "extraction_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Step 3 data extraction failed: {e}")
            return {"error": str(e), "ready_for_qloo": False}
    
    def get_step1_summary(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get Step 1 anonymized summary for logging/debugging (NO PII)"""
        
        try:
            patient_info = profile.get("patient_info", {})
            theme_info = profile.get("theme_info", {})
            feedback_info = profile.get("feedback_info", {})
            
            return {
                "cultural_heritage": patient_info.get("cultural_heritage", "Unknown"),
                "age_group": patient_info.get("age_group", "Unknown"),
                "birth_year": patient_info.get("birth_year", "Unknown"),
                "interests_count": len(patient_info.get("interests", [])),
                "theme_selected": theme_info.get("name", "Unknown"),
                "photo_filename": theme_info.get("photo_filename", "Unknown"),
                "feedback_count": feedback_info.get("total_feedback", 0),
                "step": 1,
                "pii_removed": True  # Confirmation that no PII is present
            }
            
        except Exception as e:
            logger.error(f"❌ Step 1 summary failed: {e}")
            return {"error": str(e)}
    
    def get_step2_summary(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get Step 2 anonymized summary for logging/debugging (NO PII)"""
        
        try:
            step1_summary = self.get_step1_summary(enhanced_profile)
            photo_analysis = enhanced_profile.get("photo_analysis", {})
            
            return {
                **step1_summary,
                "photo_analyzed": photo_analysis.get("photo_filename", "Unknown"),
                "analysis_method": photo_analysis.get("analysis_method", "Unknown"),
                "analysis_success": photo_analysis.get("success", False),
                "theme_connection": photo_analysis.get("theme_connection", "Unknown"),
                "conversation_starters_count": len(photo_analysis.get("analysis_data", {}).get("conversation_starters", [])),
                "step": 2
            }
            
        except Exception as e:
            logger.error(f"❌ Step 2 summary failed: {e}")
            return {"error": str(e)}
    
    def combine_step1_step2_insights(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine anonymized insights from Steps 1-2 for Step 3 preparation
        
        Args:
            enhanced_profile: Enhanced anonymized profile from Step 2
            
        Returns:
            Combined anonymized insights for Step 3
        """
        
        try:
            patient_info = enhanced_profile.get("patient_info", {})
            theme_info = enhanced_profile.get("theme_info", {})
            photo_analysis = enhanced_profile.get("photo_analysis", {})
            analysis_data = photo_analysis.get("analysis_data", {})
            
            # Extract cultural context (ANONYMIZED ONLY)
            cultural_heritage = patient_info.get("cultural_heritage", "American")
            birth_year = patient_info.get("birth_year", 1942)
            age_group = patient_info.get("age_group", "senior")
            interests = patient_info.get("interests", ["music", "family", "cooking"])
            
            # Extract theme context
            theme_name = theme_info.get("name", "Unknown")
            theme_conversation_starters = theme_info.get("conversation_prompts", [])
            
            # Extract visual context
            photo_conversation_starters = analysis_data.get("conversation_starters", [])
            memory_triggers = analysis_data.get("memory_triggers", [])
            cultural_context = analysis_data.get("cultural_context", "")
            
            return {
                # ANONYMIZED CULTURAL CONTEXT
                "cultural_heritage": cultural_heritage,
                "birth_year": birth_year,
                "age_group": age_group,
                "interests": interests,
                "age_demographic": self._get_age_demographic(birth_year),
                
                # THEME AND VISUAL CONTEXT
                "theme_context": theme_name,
                "photo_context": photo_analysis.get("photo_filename", ""),
                "visual_context": analysis_data.get("description", ""),
                "memory_triggers": memory_triggers,
                "cultural_context": cultural_context,
                "conversation_starters": theme_conversation_starters + photo_conversation_starters,
                
                # STEP 3 PREPARATION (ANONYMIZED)
                "qloo_ready_data": {
                    "heritage_for_qloo": cultural_heritage,
                    "age_group_for_qloo": age_group,
                    "interests_for_qloo": interests,
                    "theme_for_context": theme_name
                },
                
                "combined_insights_ready": True,
                "anonymization_verified": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Combined insights failed: {e}")
            return {"error": str(e), "combined_insights_ready": False}
    
    def _get_age_demographic(self, birth_year: int) -> str:
        """Get age demographic for cultural analysis"""
        
        if not birth_year:
            return "55_and_older"
        
        current_year = datetime.now().year
        age = current_year - birth_year
        
        if age >= 55:
            return "55_and_older"
        elif age >= 36:
            return "36_to_55"
        else:
            return "18_to_35"
    
    def create_test_step1_profile(self) -> Dict[str, Any]:
        """Create test Step 1 anonymized profile for testing (NO PII)"""
        
        return {
            "patient_info": {
                # NO PII FIELDS - only anonymized data
                "birth_year": 1942,
                "current_age": 81,
                "age_group": "oldest_senior",
                "cultural_heritage": "Italian-American",
                "interests": ["music", "cooking", "family"],
                "profile_complete": True
            },
            "theme_info": {
                "id": "travel",
                "name": "Travel",
                "description": "Exploring places and memories of journeys",
                "photo_filename": "travel.png",
                "conversation_prompts": [
                    "What was your favorite place to visit?",
                    "Tell me about a memorable trip you took."
                ]
            },
            "feedback_info": {
                "likes": [],
                "dislikes": [],
                "total_feedback": 0,
                "feedback_available": False
            },
            "session_metadata": {
                "session_id": "test_session_anonymized",
                "request_type": "dashboard",
                "timestamp": datetime.now().isoformat(),
                "step": "information_consolidation"
            },
            "pipeline_state": {
                "current_step": 1,
                "next_step": "photo_analysis",
                "profile_ready": True,
                "fallback_used": False
            }
        }
    
    def create_test_step2_profile(self) -> Dict[str, Any]:
        """Create test Step 2 enhanced anonymized profile for testing (NO PII)"""
        
        step1_profile = self.create_test_step1_profile()
        
        # Add Step 2 photo analysis
        step1_profile["photo_analysis"] = {
            "photo_filename": "travel.png",
            "analysis_method": "pre_analyzed",
            "analysis_data": {
                "description": "A scenic coastal view with blue water and peaceful atmosphere",
                "objects_detected": ["ocean", "coastline", "sky", "peaceful scene"],
                "mood": "peaceful",
                "conversation_starters": [
                    "This reminds me of beautiful coastal trips - have you been to the ocean?",
                    "What's your favorite place by the water?"
                ],
                "memory_triggers": ["travel", "ocean", "peaceful", "scenic"],
                "cultural_context": "travel memories and beautiful places"
            },
            "theme_connection": "Travel",
            "analysis_timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        # Update pipeline state
        step1_profile["pipeline_state"] = {
            "current_step": 2,
            "next_step": "qloo_intelligence",
            "photo_analysis_complete": True,
            "profile_ready": True,
            "step2_timestamp": datetime.now().isoformat()
        }
        
        return step1_profile
    
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

# Create singleton instance for import
enhanced_profile_structure = EnhancedProfileStructure()