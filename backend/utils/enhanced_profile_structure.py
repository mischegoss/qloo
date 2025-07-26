"""
Enhanced Profile Structure for Steps 1-2-3
File: backend/utils/enhanced_profile_structure.py

Handles the complete data flow and validation for:
- Step 1 (Information Consolidation) → Step 2 (Photo Analysis)
- Step 2 (Photo Analysis) → Step 3 (Qloo Cultural Analysis)

This is the missing piece that the tests expect!
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnhancedProfileStructure:
    """
    Enhanced Profile Structure Manager
    
    Handles data flow and validation between Steps 1-2-3:
    - Validates Step 1 → Step 2 transition
    - Validates Step 2 → Step 3 transition
    - Provides data extraction for each step
    - Ensures clean data contracts
    """
    
    def __init__(self):
        self.version = "1.0.0"
        logger.info("✅ Enhanced Profile Structure initialized")
    
    def validate_step1_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 1 profile is ready for Step 2
        
        Args:
            profile: Profile from Step 1 (Information Consolidation)
            
        Returns:
            Validation results
        """
        
        validation = {
            "valid": False,
            "step1_valid": False,
            "ready_for_step2": False,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Check required Step 1 sections
            required_sections = ["patient_info", "theme_info", "feedback_info", "session_metadata", "pipeline_state"]
            
            for section in required_sections:
                if section not in profile:
                    validation["errors"].append(f"Missing required section: {section}")
            
            # Check patient info completeness
            patient_info = profile.get("patient_info", {})
            if not patient_info.get("first_name"):
                validation["warnings"].append("Missing patient first_name")
            if not patient_info.get("cultural_heritage"):
                validation["warnings"].append("Missing cultural_heritage")
            
            # Check theme info
            theme_info = profile.get("theme_info", {})
            if not theme_info.get("name"):
                validation["errors"].append("Missing theme name")
            if not theme_info.get("photo_filename"):
                validation["errors"].append("Missing photo_filename")
            
            # Check pipeline state
            pipeline_state = profile.get("pipeline_state", {})
            if pipeline_state.get("current_step") != 1:
                validation["errors"].append("Profile not at Step 1")
            if not pipeline_state.get("profile_ready"):
                validation["errors"].append("Profile not marked as ready")
            
            # Set validation results
            validation["step1_valid"] = len(validation["errors"]) == 0
            validation["ready_for_step2"] = validation["step1_valid"]
            validation["valid"] = validation["step1_valid"]
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Step 1 validation failed: {e}")
            validation["errors"].append(f"Validation exception: {str(e)}")
            return validation
    
    def validate_step2_profile(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 2 enhanced profile is ready for Step 3
        
        Args:
            enhanced_profile: Enhanced profile from Step 2 (Photo Analysis)
            
        Returns:
            Validation results
        """
        
        validation = {
            "valid": False,
            "step1_valid": False,
            "step2_valid": False,
            "ready_for_step3": False,
            "errors": [],
            "warnings": []
        }
        
        try:
            # First validate Step 1 sections are still present
            step1_validation = self.validate_step1_profile(enhanced_profile)
            validation["step1_valid"] = step1_validation["valid"]
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
            if pipeline_state.get("next_step") != "qloo_cultural_analysis":
                validation["warnings"].append("Next step not set to qloo_cultural_analysis")
            
            # Set validation results
            validation["step2_valid"] = len([e for e in validation["errors"] if not e.startswith("Step 1:")]) == 0
            validation["ready_for_step3"] = validation["step1_valid"] and validation["step2_valid"]
            validation["valid"] = validation["ready_for_step3"]
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Step 2 validation failed: {e}")
            validation["errors"].append(f"Validation exception: {str(e)}")
            return validation
    
    def extract_for_step2(self, step1_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data needed for Step 2 (Photo Analysis)
        
        Args:
            step1_profile: Profile from Step 1
            
        Returns:
            Clean data package for Step 2
        """
        
        try:
            return {
                "patient_info": step1_profile.get("patient_info", {}),
                "theme_info": step1_profile.get("theme_info", {}),
                "feedback_info": step1_profile.get("feedback_info", {}),
                "session_metadata": step1_profile.get("session_metadata", {}),
                "pipeline_state": step1_profile.get("pipeline_state", {}),
                "ready_for_photo_analysis": True
            }
            
        except Exception as e:
            logger.error(f"❌ Step 2 data extraction failed: {e}")
            return {"error": str(e), "ready_for_photo_analysis": False}
    
    def extract_for_step3(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data needed for Step 3 (Qloo Cultural Analysis)
        
        Args:
            enhanced_profile: Enhanced profile from Step 2
            
        Returns:
            Clean data package for Step 3
        """
        
        try:
            # Validate first
            validation = self.validate_step2_profile(enhanced_profile)
            
            if not validation["valid"]:
                return {
                    "error": "Step 2 validation failed",
                    "validation_errors": validation["errors"],
                    "ready_for_qloo": False
                }
            
            return {
                "patient_info": enhanced_profile.get("patient_info", {}),
                "theme_info": enhanced_profile.get("theme_info", {}),
                "feedback_info": enhanced_profile.get("feedback_info", {}),
                "photo_analysis": enhanced_profile.get("photo_analysis", {}),
                "session_metadata": enhanced_profile.get("session_metadata", {}),
                "pipeline_state": enhanced_profile.get("pipeline_state", {}),
                "ready_for_qloo": True,
                "extraction_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Step 3 data extraction failed: {e}")
            return {"error": str(e), "ready_for_qloo": False}
    
    def get_step1_summary(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get Step 1 summary for logging/debugging"""
        
        try:
            patient_info = profile.get("patient_info", {})
            theme_info = profile.get("theme_info", {})
            feedback_info = profile.get("feedback_info", {})
            
            return {
                "patient_name": patient_info.get("first_name", "Unknown"),
                "cultural_heritage": patient_info.get("cultural_heritage", "Unknown"),
                "birth_year": patient_info.get("birth_year", "Unknown"),
                "theme_selected": theme_info.get("name", "Unknown"),
                "photo_filename": theme_info.get("photo_filename", "Unknown"),
                "feedback_count": feedback_info.get("total_feedback", 0),
                "step": 1
            }
            
        except Exception as e:
            logger.error(f"❌ Step 1 summary failed: {e}")
            return {"error": str(e)}
    
    def get_step2_summary(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get Step 2 summary for logging/debugging"""
        
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
        Combine insights from Steps 1-2 for Step 3 preparation
        
        Args:
            enhanced_profile: Enhanced profile from Step 2
            
        Returns:
            Combined insights for Step 3
        """
        
        try:
            patient_info = enhanced_profile.get("patient_info", {})
            theme_info = enhanced_profile.get("theme_info", {})
            photo_analysis = enhanced_profile.get("photo_analysis", {})
            analysis_data = photo_analysis.get("analysis_data", {})
            
            # Extract cultural context
            cultural_heritage = patient_info.get("cultural_heritage", "American")
            birth_year = patient_info.get("birth_year", 1945)
            
            # Extract theme context
            theme_name = theme_info.get("name", "Unknown")
            theme_conversation_starters = theme_info.get("conversation_starters", [])
            
            # Extract visual context
            photo_conversation_starters = analysis_data.get("conversation_starters", [])
            memory_triggers = analysis_data.get("memory_triggers", [])
            cultural_context = analysis_data.get("cultural_context", "")
            
            return {
                "cultural_heritage": cultural_heritage,
                "birth_year": birth_year,
                "age_demographic": self._get_age_demographic(birth_year),
                "theme_context": theme_name,
                "photo_context": photo_analysis.get("photo_filename", ""),
                "visual_context": analysis_data.get("description", ""),
                "memory_triggers": memory_triggers,
                "cultural_context": cultural_context,
                "conversation_starters": theme_conversation_starters + photo_conversation_starters,
                "combined_insights_ready": True,
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
        """Create test Step 1 profile for testing"""
        
        return {
            "patient_info": {
                "first_name": "Maria",
                "birth_year": 1945,
                "cultural_heritage": "Italian-American",
                "city": "Brooklyn",
                "state": "New York",
                "additional_context": "Loves music and cooking"
            },
            "theme_info": {
                "id": "birthday",
                "name": "Birthday",
                "description": "Celebrating special moments and memories",
                "photo_filename": "birthday.png",
                "conversation_starters": [
                    "What was your favorite birthday memory?",
                    "How did your family celebrate birthdays?"
                ]
            },
            "feedback_info": {
                "likes": [],
                "dislikes": [],
                "total_feedback": 0,
                "feedback_available": False
            },
            "session_metadata": {
                "session_id": "test_session",
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
        """Create test Step 2 enhanced profile for testing"""
        
        step1_profile = self.create_test_step1_profile()
        
        # Add Step 2 photo analysis
        step1_profile["photo_analysis"] = {
            "photo_filename": "birthday.png",
            "analysis_method": "pre_analyzed",
            "analysis_data": {
                "description": "A warm birthday celebration scene with cake and decorations",
                "objects_detected": ["cake", "candles", "decorations", "table"],
                "mood": "celebratory",
                "conversation_starters": [
                    "This reminds me of birthday parties - what was your favorite cake?",
                    "Do you remember blowing out candles as a child?"
                ],
                "memory_triggers": ["birthday", "celebration", "cake", "family"],
                "cultural_context": "birthday memories and celebrations"
            },
            "theme_connection": "Birthday",
            "analysis_timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        # Update pipeline state
        step1_profile["pipeline_state"] = {
            "current_step": 2,
            "next_step": "qloo_cultural_analysis",
            "photo_analysis_complete": True,
            "profile_ready": True,
            "step2_timestamp": datetime.now().isoformat()
        }
        
        return step1_profile

# Create singleton instance for import
enhanced_profile_structure = EnhancedProfileStructure()