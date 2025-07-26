"""
Step 1: Clean Profile Structure Definition
File: backend/utils/profile_structure.py

CLEAN PIPELINE DATA STRUCTURE:
- Standardized profile format for all pipeline steps
- Clear data contracts between steps
- Type hints and validation
- Easy to extend and debug
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class PatientInfo:
    """Basic patient information"""
    first_name: str
    birth_year: Optional[int] = None
    current_age: Optional[int] = None
    age_group: str = "senior"
    cultural_heritage: str = "American"
    location: str = ""
    additional_context: str = ""
    profile_complete: bool = False

@dataclass
class ThemeInfo:
    """Selected theme information"""
    id: str
    name: str
    description: str
    conversation_prompts: List[str]
    photo_filename: str = ""
    source: str = "theme_manager"

@dataclass
class FeedbackInfo:
    """Feedback summary"""
    likes: List[Dict[str, Any]]
    dislikes: List[Dict[str, Any]]
    total_feedback: int = 0
    feedback_available: bool = False
    preferred_types: List[str] = None
    avoided_types: List[str] = None
    engagement_level: str = "new_user"

@dataclass
class SessionMetadata:
    """Session tracking information"""
    session_id: str
    request_type: str
    timestamp: str
    step: str
    
@dataclass
class PipelineState:
    """Pipeline state tracking"""
    current_step: int
    next_step: str
    profile_ready: bool
    fallback_used: bool = False
    errors: List[str] = None

class ProfileStructure:
    """
    Clean Profile Structure for Pipeline Steps
    
    PURPOSE:
    - Standardized data format between all pipeline steps
    - Type-safe profile management
    - Easy validation and debugging
    - Clear data contracts
    """
    
    def __init__(self):
        self.version = "1.0"
        
    def create_step1_profile(self,
                            patient_info: PatientInfo,
                            theme_info: ThemeInfo,
                            feedback_info: FeedbackInfo,
                            session_metadata: SessionMetadata) -> Dict[str, Any]:
        """
        Create Step 1 profile structure
        
        Args:
            patient_info: Basic patient information
            theme_info: Selected theme
            feedback_info: Feedback summary
            session_metadata: Session tracking
            
        Returns:
            Clean profile for Step 2
        """
        
        pipeline_state = PipelineState(
            current_step=1,
            next_step="photo_analysis",
            profile_ready=True,
            fallback_used=False,
            errors=[]
        )
        
        profile = {
            "version": self.version,
            "patient_info": asdict(patient_info),
            "theme_info": asdict(theme_info),
            "feedback_info": asdict(feedback_info),
            "session_metadata": asdict(session_metadata),
            "pipeline_state": asdict(pipeline_state),
            
            # Step-specific data (will be added by subsequent steps)
            "photo_analysis": {},  # Added by Step 2
            "qloo_intelligence": {},  # Added by Step 3
            "content_curation": {},  # Added by Step 4
            "youtube_content": {},  # Added by Step 5
            "recipe_content": {},  # Added by Step 6
            "dashboard_content": {}  # Added by Step 7
        }
        
        return profile
    
    def validate_step1_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Step 1 profile structure
        
        Args:
            profile: Profile to validate
            
        Returns:
            Validation results
        """
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "completeness": {}
        }
        
        # Check required sections
        required_sections = [
            "patient_info", "theme_info", "feedback_info",
            "session_metadata", "pipeline_state"
        ]
        
        for section in required_sections:
            if section not in profile:
                validation["errors"].append(f"Missing required section: {section}")
                validation["valid"] = False
        
        # Check patient info completeness
        patient_info = profile.get("patient_info", {})
        patient_required = ["first_name", "cultural_heritage"]
        
        for field in patient_required:
            if not patient_info.get(field):
                validation["warnings"].append(f"Missing patient field: {field}")
        
        # Check theme info
        theme_info = profile.get("theme_info", {})
        theme_required = ["id", "name", "description"]
        
        for field in theme_required:
            if not theme_info.get(field):
                validation["errors"].append(f"Missing theme field: {field}")
                validation["valid"] = False
        
        # Calculate completeness
        validation["completeness"] = {
            "patient_complete": patient_info.get("profile_complete", False),
            "theme_selected": bool(theme_info.get("name")),
            "feedback_available": profile.get("feedback_info", {}).get("feedback_available", False),
            "ready_for_step2": validation["valid"]
        }
        
        return validation
    
    def get_patient_summary(self, profile: Dict[str, Any]) -> str:
        """Get human-readable patient summary"""
        
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        feedback_info = profile.get("feedback_info", {})
        
        name = patient_info.get("first_name", "Unknown")
        age = patient_info.get("current_age", "Unknown")
        heritage = patient_info.get("cultural_heritage", "Unknown")
        theme = theme_info.get("name", "Unknown")
        feedback_count = feedback_info.get("total_feedback", 0)
        
        return f"{name} (age {age}, {heritage}) - Theme: {theme}, Feedback: {feedback_count} items"
    
    def get_step_summary(self, profile: Dict[str, Any]) -> str:
        """Get pipeline step summary"""
        
        pipeline_state = profile.get("pipeline_state", {})
        current_step = pipeline_state.get("current_step", 0)
        next_step = pipeline_state.get("next_step", "unknown")
        ready = pipeline_state.get("profile_ready", False)
        
        return f"Step {current_step} → {next_step} (Ready: {ready})"
    
    def extract_for_next_step(self, profile: Dict[str, Any], 
                             next_step: str) -> Dict[str, Any]:
        """
        Extract relevant data for next pipeline step
        
        Args:
            profile: Current profile
            next_step: Name of next step
            
        Returns:
            Relevant data for next step
        """
        
        if next_step == "photo_analysis":
            return {
                "patient_info": profile.get("patient_info", {}),
                "theme_info": profile.get("theme_info", {}),
                "feedback_info": profile.get("feedback_info", {}),
                "pipeline_state": profile.get("pipeline_state", {})
            }
        
        # For other steps, return full profile
        return profile
    
    def add_step_data(self, profile: Dict[str, Any], 
                     step_name: str, 
                     step_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add data from a pipeline step to profile
        
        Args:
            profile: Current profile
            step_name: Name of the step
            step_data: Data from the step
            
        Returns:
            Updated profile
        """
        
        profile[step_name] = step_data
        
        # Update pipeline state
        step_mapping = {
            "photo_analysis": 2,
            "qloo_intelligence": 3,
            "content_curation": 4,
            "youtube_content": 5,
            "recipe_content": 6,
            "dashboard_content": 7
        }
        
        if step_name in step_mapping:
            pipeline_state = profile.get("pipeline_state", {})
            pipeline_state["current_step"] = step_mapping[step_name]
            
            # Determine next step
            step_order = ["photo_analysis", "qloo_intelligence", "content_curation", 
                         "youtube_content", "recipe_content", "dashboard_content"]
            
            current_index = step_order.index(step_name) if step_name in step_order else -1
            if current_index >= 0 and current_index < len(step_order) - 1:
                pipeline_state["next_step"] = step_order[current_index + 1]
            else:
                pipeline_state["next_step"] = "complete"
        
        return profile

# Global instance
profile_structure = ProfileStructure()

# Convenience functions
def create_patient_info(first_name: str, birth_year: int = None, 
                       cultural_heritage: str = "American", **kwargs) -> PatientInfo:
    """Create PatientInfo instance with defaults"""
    current_age = (datetime.now().year - birth_year) if birth_year else None
    age_group = "senior" if current_age and current_age >= 65 else "adult"
    
    return PatientInfo(
        first_name=first_name,
        birth_year=birth_year,
        current_age=current_age,
        age_group=age_group,
        cultural_heritage=cultural_heritage,
        **kwargs
    )

def create_theme_info(theme_id: str, name: str, description: str, 
                     conversation_prompts: List[str], **kwargs) -> ThemeInfo:
    """Create ThemeInfo instance"""
    return ThemeInfo(
        id=theme_id,
        name=name,
        description=description,
        conversation_prompts=conversation_prompts,
        **kwargs
    )

def create_feedback_info(likes: List[Dict] = None, dislikes: List[Dict] = None, 
                        **kwargs) -> FeedbackInfo:
    """Create FeedbackInfo instance with defaults"""
    likes = likes or []
    dislikes = dislikes or []
    
    return FeedbackInfo(
        likes=likes,
        dislikes=dislikes,
        total_feedback=len(likes) + len(dislikes),
        feedback_available=len(likes) + len(dislikes) > 0,
        **kwargs
    )

def create_session_metadata(session_id: str = "default", 
                           request_type: str = "dashboard",
                           step: str = "information_consolidation") -> SessionMetadata:
    """Create SessionMetadata instance"""
    return SessionMetadata(
        session_id=session_id,
        request_type=request_type,
        timestamp=datetime.now().isoformat(),
        step=step
    )

# Export
__all__ = [
    "ProfileStructure", "profile_structure",
    "PatientInfo", "ThemeInfo", "FeedbackInfo", "SessionMetadata", "PipelineState",
    "create_patient_info", "create_theme_info", "create_feedback_info", "create_session_metadata"
]