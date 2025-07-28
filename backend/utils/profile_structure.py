"""
Step 1: Clean Profile Structure Definition (Anonymized)
File: backend/utils/profile_structure.py

CLEAN PIPELINE DATA STRUCTURE:
- Anonymized profile format matching frontend data flow
- No PII transmission to backend
- Clear data contracts between steps
- Type hints and validation
- Easy to extend and debug
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class AnonymizedPatientInfo:
    """Anonymized patient information - NO PII"""
    birth_year: Optional[int] = None
    current_age: Optional[int] = None
    age_group: str = "senior"  # senior, oldest_senior, adult
    cultural_heritage: str = "American"
    interests: List[str] = None
    profile_complete: bool = False
    
    def __post_init__(self):
        """Calculate derived fields and set defaults"""
        if self.interests is None:
            self.interests = ["music", "family", "cooking"]
        
        # Calculate current_age from birth_year if available
        if self.birth_year and not self.current_age:
            self.current_age = datetime.now().year - self.birth_year
        
        # Ensure age_group matches current_age
        if self.current_age:
            if self.current_age >= 80:
                self.age_group = "oldest_senior"
            elif self.current_age >= 65:
                self.age_group = "senior"
            else:
                self.age_group = "adult"

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
    
    def __post_init__(self):
        """Set defaults and calculate derived fields"""
        if self.preferred_types is None:
            self.preferred_types = []
        if self.avoided_types is None:
            self.avoided_types = []
        
        # Recalculate total_feedback
        self.total_feedback = len(self.likes) + len(self.dislikes)
        self.feedback_available = self.total_feedback > 0

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
    
    def __post_init__(self):
        """Set defaults"""
        if self.errors is None:
            self.errors = []

class ProfileStructure:
    """
    Clean Profile Structure for Pipeline Steps (Anonymized)
    
    PURPOSE:
    - Anonymized data format matching frontend transmission
    - Type-safe profile management with no PII
    - Easy validation and debugging
    - Clear data contracts between agents
    """
    
    def __init__(self):
        self.version = "1.0"
        
    def create_from_frontend_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Step 1 profile from frontend request
        
        Args:
            request_data: Request from frontend API call
            
        Returns:
            Clean anonymized profile for Step 2
        """
        
        # Extract anonymized patient profile from frontend
        patient_profile = request_data.get("patient_profile", {})
        
        # Create anonymized patient info (NO PII)
        patient_info = AnonymizedPatientInfo(
            birth_year=patient_profile.get("birth_year"),
            age_group=patient_profile.get("age_group", "senior"),
            cultural_heritage=patient_profile.get("cultural_heritage", "American"),
            interests=patient_profile.get("interests", ["music", "family", "cooking"]),
            profile_complete=patient_profile.get("profile_complete", False)
        )
        
        # Create theme info (will be populated by theme selection logic)
        theme_info = ThemeInfo(
            id="default_theme",
            name="Memory Lane",
            description="A journey through cherished memories and familiar experiences",
            conversation_prompts=[
                "What brings back your happiest memories?",
                "Tell me about a special tradition from your past.",
                "What music always makes you smile?"
            ],
            photo_filename="travel.png"
        )
        
        # Create feedback info from request
        feedback_data = request_data.get("feedback_data", {"likes": [], "dislikes": []})
        feedback_info = FeedbackInfo(
            likes=feedback_data.get("likes", []),
            dislikes=feedback_data.get("dislikes", [])
        )
        
        # Create session metadata
        session_metadata = SessionMetadata(
            session_id=request_data.get("session_id", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            request_type="dashboard",
            timestamp=datetime.now().isoformat(),
            step="information_consolidation"
        )
        
        # Create pipeline state
        pipeline_state = PipelineState(
            current_step=1,
            next_step="photo_analysis",
            profile_ready=True,
            fallback_used=False
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
            "content_generation": {  # Added by Step 4 (4A/B/C)
                "music": {},
                "recipe": {},
                "photo_description": {}
            },
            "nostalgia_news": {},  # Added by Step 5
            "dashboard_synthesis": {}  # Added by Step 6
        }
        
        return profile
    
    def validate_anonymized_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate anonymized profile structure (NO PII CHECK)
        
        Args:
            profile: Profile to validate
            
        Returns:
            Validation results
        """
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "completeness": {},
            "anonymization_verified": True
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
        
        # Check anonymized patient info completeness
        patient_info = profile.get("patient_info", {})
        
        # CRITICAL: Verify NO PII is present
        pii_fields = ["first_name", "last_name", "name", "city", "state", "address", "phone", "email"]
        for pii_field in pii_fields:
            if pii_field in patient_info:
                validation["errors"].append(f"PII DETECTED: {pii_field} must not be present in backend")
                validation["valid"] = False
                validation["anonymization_verified"] = False
        
        # Check required anonymized fields
        anonymized_required = ["cultural_heritage", "age_group", "interests"]
        for field in anonymized_required:
            if not patient_info.get(field):
                validation["warnings"].append(f"Missing anonymized field: {field}")
        
        # Check theme info
        theme_info = profile.get("theme_info", {})
        theme_required = ["id", "name", "description"]
        
        for field in theme_required:
            if not theme_info.get(field):
                validation["errors"].append(f"Missing theme field: {field}")
                validation["valid"] = False
        
        # Calculate completeness
        validation["completeness"] = {
            "patient_anonymized": validation["anonymization_verified"],
            "profile_complete": patient_info.get("profile_complete", False),
            "theme_selected": bool(theme_info.get("name")),
            "feedback_available": profile.get("feedback_info", {}).get("feedback_available", False),
            "ready_for_step2": validation["valid"] and validation["anonymization_verified"]
        }
        
        return validation
    
    def get_anonymized_summary(self, profile: Dict[str, Any]) -> str:
        """Get human-readable anonymized summary (NO PII)"""
        
        patient_info = profile.get("patient_info", {})
        theme_info = profile.get("theme_info", {})
        feedback_info = profile.get("feedback_info", {})
        
        age_group = patient_info.get("age_group", "unknown")
        heritage = patient_info.get("cultural_heritage", "unknown")
        interests = patient_info.get("interests", [])
        theme = theme_info.get("name", "unknown")
        feedback_count = feedback_info.get("total_feedback", 0)
        
        interests_str = ", ".join(interests[:3]) if interests else "none"
        
        return f"Patient: {age_group} ({heritage}) - Interests: {interests_str} - Theme: {theme}, Feedback: {feedback_count} items"
    
    def get_step_summary(self, profile: Dict[str, Any]) -> str:
        """Get pipeline step summary"""
        
        pipeline_state = profile.get("pipeline_state", {})
        current_step = pipeline_state.get("current_step", 0)
        next_step = pipeline_state.get("next_step", "unknown")
        ready = pipeline_state.get("profile_ready", False)
        fallback = pipeline_state.get("fallback_used", False)
        
        status = "FALLBACK" if fallback else "READY" if ready else "NOT READY"
        
        return f"Step {current_step} → {next_step} ({status})"
    
    def extract_for_next_step(self, profile: Dict[str, Any], 
                             next_step: str) -> Dict[str, Any]:
        """
        Extract relevant anonymized data for next pipeline step
        
        Args:
            profile: Current profile
            next_step: Name of next step
            
        Returns:
            Relevant anonymized data for next step
        """
        
        if next_step == "photo_analysis":
            return {
                "patient_info": profile.get("patient_info", {}),
                "theme_info": profile.get("theme_info", {}),
                "feedback_info": profile.get("feedback_info", {}),
                "pipeline_state": profile.get("pipeline_state", {})
            }
        
        # For other steps, return full anonymized profile
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
            "content_generation": 4,
            "nostalgia_news": 5,
            "dashboard_synthesis": 6
        }
        
        if step_name in step_mapping:
            pipeline_state = profile.get("pipeline_state", {})
            pipeline_state["current_step"] = step_mapping[step_name]
            
            # Determine next step
            step_order = ["photo_analysis", "qloo_intelligence", "content_generation", 
                         "nostalgia_news", "dashboard_synthesis"]
            
            current_index = step_order.index(step_name) if step_name in step_order else -1
            if current_index >= 0 and current_index < len(step_order) - 1:
                pipeline_state["next_step"] = step_order[current_index + 1]
            else:
                pipeline_state["next_step"] = "complete"
        
        return profile

# Global instance
profile_structure = ProfileStructure()

# Convenience functions for anonymized data
def create_anonymized_patient_info(birth_year: int = None, 
                                  cultural_heritage: str = "American",
                                  interests: List[str] = None,
                                  **kwargs) -> AnonymizedPatientInfo:
    """Create AnonymizedPatientInfo instance with defaults (NO PII)"""
    
    if interests is None:
        interests = ["music", "family", "cooking"]
    
    return AnonymizedPatientInfo(
        birth_year=birth_year,
        cultural_heritage=cultural_heritage,
        interests=interests,
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
        **kwargs
    )

def create_session_metadata(session_id: str = None, 
                           request_type: str = "dashboard",
                           step: str = "information_consolidation") -> SessionMetadata:
    """Create SessionMetadata instance"""
    
    if session_id is None:
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return SessionMetadata(
        session_id=session_id,
        request_type=request_type,
        timestamp=datetime.now().isoformat(),
        step=step
    )

# Safe fallback functions
def safe_get_patient_heritage(profile: Dict[str, Any]) -> str:
    """Safely get patient heritage with fallback"""
    try:
        return profile.get("patient_info", {}).get("cultural_heritage", "American")
    except:
        return "American"

def safe_get_patient_age_group(profile: Dict[str, Any]) -> str:
    """Safely get patient age group with fallback"""
    try:
        return profile.get("patient_info", {}).get("age_group", "senior")
    except:
        return "senior"

def safe_get_patient_interests(profile: Dict[str, Any]) -> List[str]:
    """Safely get patient interests with fallback"""
    try:
        interests = profile.get("patient_info", {}).get("interests", [])
        return interests if interests else ["music", "family", "cooking"]
    except:
        return ["music", "family", "cooking"]

# Export
__all__ = [
    "ProfileStructure", "profile_structure",
    "AnonymizedPatientInfo", "ThemeInfo", "FeedbackInfo", "SessionMetadata", "PipelineState",
    "create_anonymized_patient_info", "create_theme_info", "create_feedback_info", "create_session_metadata",
    "safe_get_patient_heritage", "safe_get_patient_age_group", "safe_get_patient_interests"
]