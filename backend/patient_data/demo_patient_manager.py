"""
Demo Patient Manager - Missing Module Implementation
File: backend/patient_data/demo_patient_manager.py

Simple implementation of the missing DemoPatientManager class
that provides demo patient profiles for testing the pipeline.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DemoPatientManager:
    """
    Demo Patient Manager
    
    Provides demo patient profiles for testing the 6-agent pipeline.
    Simple implementation with hardcoded demo patients.
    """
    
    def __init__(self):
        self.data_dir = "demo_data"
        self.demo_patients = self._load_demo_patients()
        logger.info("✅ Demo Patient Manager initialized")
        logger.info(f"📊 Loaded {len(self.demo_patients)} demo patients")
    
    def _load_demo_patients(self) -> Dict[str, Dict[str, Any]]:
        """Load demo patient profiles"""
        
        return {
            "demo_patient": {
                "patient_id": "demo_patient",
                "first_name": "Maria",
                "birth_year": 1945,
                "cultural_heritage": "Italian-American",
                "city": "Brooklyn",
                "state": "New York",
                "additional_context": "Loves music and cooking, enjoys family stories",
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat()
            },
            "maria_rossi": {
                "patient_id": "maria_rossi",
                "first_name": "Maria",
                "birth_year": 1945,
                "cultural_heritage": "Italian-American",
                "city": "Brooklyn",
                "state": "New York",
                "additional_context": "Loves classical music and Italian cooking",
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat()
            },
            "john_smith": {
                "patient_id": "john_smith",
                "first_name": "John",
                "birth_year": 1940,
                "cultural_heritage": "Irish-American",
                "city": "Boston",
                "state": "Massachusetts",
                "additional_context": "Enjoys folk music and storytelling",
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat()
            },
            "anna_wagner": {
                "patient_id": "anna_wagner",
                "first_name": "Anna",
                "birth_year": 1950,
                "cultural_heritage": "German-American",
                "city": "Milwaukee",
                "state": "Wisconsin",
                "additional_context": "Loves classical music and baking",
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def get_patient_profile(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get patient profile by ID"""
        
        profile = self.demo_patients.get(patient_id)
        if profile:
            logger.info(f"📋 Retrieved profile for: {profile['first_name']} ({patient_id})")
            return profile.copy()
        else:
            logger.warning(f"⚠️ Patient not found: {patient_id}")
            return None
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Get all demo patients"""
        
        patients = list(self.demo_patients.values())
        logger.info(f"📋 Retrieved {len(patients)} patient profiles")
        return patients
    
    def update_patient_feedback(self, patient_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update patient feedback data"""
        
        if patient_id not in self.demo_patients:
            raise ValueError(f"Patient {patient_id} not found")
        
        patient = self.demo_patients[patient_id]
        
        # Extract feedback information
        likes = feedback_data.get("likes", [])
        dislikes = feedback_data.get("dislikes", [])
        
        # Update patient record
        patient["demo_dislikes"].extend(dislikes)
        patient["feedback_points"] += len(likes) + len(dislikes)
        patient["last_updated"] = datetime.now().isoformat()
        
        # Create feedback summary
        feedback_summary = {
            "patient_id": patient_id,
            "total_likes": len(likes),
            "total_dislikes": len(dislikes),
            "total_feedback_points": patient["feedback_points"],
            "updated_timestamp": patient["last_updated"]
        }
        
        logger.info(f"💡 Updated feedback for {patient['first_name']}: {len(likes)} likes, {len(dislikes)} dislikes")
        
        return feedback_summary
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get_patient_profile for backward compatibility"""
        return self.get_patient_profile(patient_id)
    
    def create_demo_session(self, patient_id: str = "demo_patient") -> Dict[str, Any]:
        """Create a demo session for testing"""
        
        patient = self.get_patient_profile(patient_id)
        if not patient:
            # Return default demo patient
            patient = self.demo_patients["demo_patient"]
        
        session = {
            "session_id": f"demo_session_{int(datetime.now().timestamp())}",
            "patient_profile": patient,
            "request_type": "dashboard",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"🧪 Created demo session for {patient['first_name']}")
        return session
    
    def get_status(self) -> Dict[str, Any]:
        """Get manager status"""
        
        return {
            "manager_type": "demo_patient_manager",
            "total_patients": len(self.demo_patients),
            "available_patients": list(self.demo_patients.keys()),
            "data_directory": self.data_dir,
            "last_loaded": datetime.now().isoformat()
        }

# Export for imports
__all__ = ["DemoPatientManager"]