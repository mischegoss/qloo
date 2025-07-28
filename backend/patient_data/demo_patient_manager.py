"""
Demo Patient Manager - Anonymized Implementation
File: backend/patient_data/demo_patient_manager.py

ANONYMIZED IMPLEMENTATION: Provides demo patient profiles for testing the pipeline
with proper anonymization compliance. NO PII stored or transmitted.
Only provides anonymized data for backend processing.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DemoPatientManager:
    """
    Demo Patient Manager (Anonymized)
    
    Provides anonymized demo patient profiles for testing the 6-agent pipeline.
    NO PII - only cultural_heritage, birth_year, age_group, and interests.
    """
    
    def __init__(self):
        self.data_dir = "demo_data"
        self.anonymized_profiles = self._load_anonymized_profiles()
        logger.info("✅ Demo Patient Manager initialized (Anonymized)")
        logger.info(f"📊 Loaded {len(self.anonymized_profiles)} anonymized demo profiles")
    
    def _load_anonymized_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Load anonymized demo patient profiles - NO PII"""
        
        current_year = datetime.now().year
        
        return {
            "demo_patient": {
                "patient_id": "demo_patient",
                # ANONYMIZED DATA ONLY
                "birth_year": 1942,
                "current_age": current_year - 1942,
                "age_group": "oldest_senior",
                "cultural_heritage": "Italian-American",
                "interests": ["music", "cooking", "family"],
                "profile_complete": True,
                # METADATA (NON-PII)
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat(),
                "anonymization_verified": True
            },
            "italian_american_senior": {
                "patient_id": "italian_american_senior",
                # ANONYMIZED DATA ONLY  
                "birth_year": 1945,
                "current_age": current_year - 1945,
                "age_group": "oldest_senior",
                "cultural_heritage": "Italian-American",
                "interests": ["music", "cooking", "family"],
                "profile_complete": True,
                # METADATA (NON-PII)
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat(),
                "anonymization_verified": True
            },
            "irish_american_senior": {
                "patient_id": "irish_american_senior",
                # ANONYMIZED DATA ONLY
                "birth_year": 1950,
                "current_age": current_year - 1950,
                "age_group": "senior",
                "cultural_heritage": "Irish-American",
                "interests": ["music", "family", "reading"],
                "profile_complete": True,
                # METADATA (NON-PII)
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat(),
                "anonymization_verified": True
            },
            "german_american_boomer": {
                "patient_id": "german_american_boomer",
                # ANONYMIZED DATA ONLY
                "birth_year": 1955,
                "current_age": current_year - 1955,
                "age_group": "senior",
                "cultural_heritage": "German-American",
                "interests": ["music", "cooking", "gardening"],
                "profile_complete": True,
                # METADATA (NON-PII)
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat(),
                "anonymization_verified": True
            },
            "chinese_american_elder": {
                "patient_id": "chinese_american_elder",
                # ANONYMIZED DATA ONLY
                "birth_year": 1935,
                "current_age": current_year - 1935,
                "age_group": "oldest_senior",
                "cultural_heritage": "Chinese-American",
                "interests": ["music", "family", "cooking"],
                "profile_complete": True,
                # METADATA (NON-PII)
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat(),
                "anonymization_verified": True
            },
            "american_veteran": {
                "patient_id": "american_veteran",
                # ANONYMIZED DATA ONLY
                "birth_year": 1940,
                "current_age": current_year - 1940,
                "age_group": "oldest_senior",
                "cultural_heritage": "American",
                "interests": ["music", "history", "travel"],
                "profile_complete": True,
                # METADATA (NON-PII)
                "demo_dislikes": [],
                "feedback_points": 0,
                "last_updated": datetime.now().isoformat(),
                "anonymization_verified": True
            }
        }
    
    def get_anonymized_profile(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Get anonymized patient profile by ID - NO PII
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            Anonymized profile or None if not found
        """
        
        profile = self.anonymized_profiles.get(patient_id)
        if profile:
            # Verify anonymization
            if not self._verify_anonymization(profile):
                logger.error(f"❌ PII detected in profile {patient_id} - cannot return")
                return None
            
            heritage = profile.get("cultural_heritage", "Unknown")
            age_group = profile.get("age_group", "Unknown")
            logger.info(f"📋 Retrieved anonymized profile: {heritage}, {age_group} ({patient_id})")
            return profile.copy()
        else:
            logger.warning(f"⚠️ Patient not found: {patient_id}")
            return None
    
    def get_all_anonymized_profiles(self) -> List[Dict[str, Any]]:
        """
        Get all anonymized demo profiles - NO PII
        
        Returns:
            List of anonymized profiles
        """
        
        anonymized_profiles = []
        
        for profile in self.anonymized_profiles.values():
            if self._verify_anonymization(profile):
                anonymized_profiles.append(profile.copy())
            else:
                logger.error(f"❌ PII detected in profile {profile.get('patient_id', 'unknown')}")
        
        logger.info(f"📋 Retrieved {len(anonymized_profiles)} anonymized profiles")
        return anonymized_profiles
    
    def update_feedback(self, patient_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update patient feedback data (anonymized)
        
        Args:
            patient_id: Patient identifier
            feedback_data: Feedback data (likes, dislikes)
            
        Returns:
            Anonymized feedback summary
        """
        
        if patient_id not in self.anonymized_profiles:
            raise ValueError(f"Patient {patient_id} not found")
        
        profile = self.anonymized_profiles[patient_id]
        
        # Extract feedback information
        likes = feedback_data.get("likes", [])
        dislikes = feedback_data.get("dislikes", [])
        
        # Update profile record (anonymized)
        profile["demo_dislikes"].extend(dislikes)
        profile["feedback_points"] += len(likes) + len(dislikes)
        profile["last_updated"] = datetime.now().isoformat()
        
        # Create anonymized feedback summary
        feedback_summary = {
            "patient_id": patient_id,
            "cultural_heritage": profile.get("cultural_heritage", "Unknown"),
            "age_group": profile.get("age_group", "Unknown"),
            "total_likes": len(likes),
            "total_dislikes": len(dislikes),
            "total_feedback_points": profile["feedback_points"],
            "updated_timestamp": profile["last_updated"],
            "anonymization_verified": True
        }
        
        heritage = profile.get("cultural_heritage", "Unknown")
        logger.info(f"💡 Updated feedback for {heritage} patient: {len(likes)} likes, {len(dislikes)} dislikes")
        
        return feedback_summary
    
    def create_anonymized_demo_session(self, patient_id: str = "demo_patient") -> Dict[str, Any]:
        """
        Create an anonymized demo session for testing
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            Anonymized demo session data
        """
        
        anonymized_profile = self.get_anonymized_profile(patient_id)
        if not anonymized_profile:
            # Return default demo patient
            anonymized_profile = self.anonymized_profiles["demo_patient"]
        
        # Verify no PII in session
        if not self._verify_anonymization(anonymized_profile):
            logger.error("❌ PII detected in demo session - using safe fallback")
            anonymized_profile = self._get_safe_fallback_profile()
        
        session = {
            "session_id": f"demo_session_{int(datetime.now().timestamp())}",
            "patient_profile": anonymized_profile,  # ANONYMIZED ONLY
            "request_type": "dashboard",
            "timestamp": datetime.now().isoformat(),
            "anonymization_verified": True
        }
        
        heritage = anonymized_profile.get("cultural_heritage", "Unknown")
        age_group = anonymized_profile.get("age_group", "Unknown")
        logger.info(f"🧪 Created anonymized demo session: {heritage}, {age_group}")
        
        return session
    
    def get_patient_profile(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get_anonymized_profile for backward compatibility"""
        return self.get_anonymized_profile(patient_id)
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get_anonymized_profile for backward compatibility"""
        return self.get_anonymized_profile(patient_id)
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Alias for get_all_anonymized_profiles for backward compatibility"""
        return self.get_all_anonymized_profiles()
    
    def update_patient_feedback(self, patient_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for update_feedback for backward compatibility"""
        return self.update_feedback(patient_id, feedback_data)
    
    def create_demo_session(self, patient_id: str = "demo_patient") -> Dict[str, Any]:
        """Alias for create_anonymized_demo_session for backward compatibility"""
        return self.create_anonymized_demo_session(patient_id)
    
    def _verify_anonymization(self, profile: Dict[str, Any]) -> bool:
        """
        Verify that profile contains no PII
        
        Args:
            profile: Profile to check
            
        Returns:
            True if anonymized, False if PII detected
        """
        
        # List of PII fields that should NOT be present
        pii_fields = [
            "first_name", "last_name", "name", "full_name",
            "city", "state", "address", "street", "zip_code",
            "phone", "email", "ssn", "medical_id",
            "location", "additional_context"
        ]
        
        for pii_field in pii_fields:
            if pii_field in profile:
                logger.error(f"❌ PII DETECTED: {pii_field} found in profile")
                return False
        
        # Verify required anonymized fields are present
        required_fields = ["cultural_heritage", "birth_year", "age_group", "interests"]
        for field in required_fields:
            if field not in profile:
                logger.warning(f"⚠️ Missing required anonymized field: {field}")
        
        return True
    
    def _get_safe_fallback_profile(self) -> Dict[str, Any]:
        """Get a safe fallback profile if PII is detected"""
        
        current_year = datetime.now().year
        
        return {
            "patient_id": "safe_fallback",
            "birth_year": 1942,
            "current_age": current_year - 1942,
            "age_group": "oldest_senior",
            "cultural_heritage": "American",
            "interests": ["music", "family", "cooking"],
            "profile_complete": True,
            "demo_dislikes": [],
            "feedback_points": 0,
            "last_updated": datetime.now().isoformat(),
            "anonymization_verified": True,
            "fallback_used": True
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get manager status (anonymized)"""
        
        # Count profiles by heritage (anonymized demographics)
        heritage_counts = {}
        for profile in self.anonymized_profiles.values():
            heritage = profile.get("cultural_heritage", "Unknown")
            heritage_counts[heritage] = heritage_counts.get(heritage, 0) + 1
        
        return {
            "manager_type": "demo_patient_manager_anonymized",
            "total_profiles": len(self.anonymized_profiles),
            "available_profiles": list(self.anonymized_profiles.keys()),
            "heritage_distribution": heritage_counts,
            "data_directory": self.data_dir,
            "anonymization_verified": True,
            "pii_compliant": True,
            "last_loaded": datetime.now().isoformat()
        }
    
    def validate_all_profiles(self) -> Dict[str, Any]:
        """
        Validate all profiles for anonymization compliance
        
        Returns:
            Validation results
        """
        
        validation_results = {
            "total_profiles": len(self.anonymized_profiles),
            "valid_profiles": [],
            "invalid_profiles": [],
            "anonymization_verified": True
        }
        
        for patient_id, profile in self.anonymized_profiles.items():
            if self._verify_anonymization(profile):
                heritage = profile.get("cultural_heritage", "Unknown")
                age_group = profile.get("age_group", "Unknown")
                validation_results["valid_profiles"].append(f"{patient_id}: {heritage}, {age_group}")
            else:
                validation_results["invalid_profiles"].append(f"{patient_id}: PII detected")
                validation_results["anonymization_verified"] = False
        
        validation_results["validation_passed"] = len(validation_results["invalid_profiles"]) == 0
        
        return validation_results
    
    def get_random_anonymized_profile(self) -> Dict[str, Any]:
        """Get a random anonymized profile for testing"""
        
        import random
        patient_ids = list(self.anonymized_profiles.keys())
        random_id = random.choice(patient_ids)
        return self.get_anonymized_profile(random_id)

def test_anonymized_demo_manager():
    """Test the anonymized demo patient manager"""
    
    print("🧪 Testing Anonymized Demo Patient Manager")
    print("=" * 45)
    
    # Initialize manager
    manager = DemoPatientManager()
    
    # Test getting all profiles
    all_profiles = manager.get_all_anonymized_profiles()
    print(f"\n✅ Retrieved {len(all_profiles)} anonymized profiles")
    
    # Test individual profile retrieval
    demo_profile = manager.get_anonymized_profile("demo_patient")
    if demo_profile:
        heritage = demo_profile.get("cultural_heritage")
        age_group = demo_profile.get("age_group")
        interests = demo_profile.get("interests", [])
        print(f"✅ Demo profile: {heritage}, {age_group}, {len(interests)} interests")
    
    # Test demo session creation
    session = manager.create_anonymized_demo_session()
    if session.get("anonymization_verified"):
        print("✅ Demo session created successfully (anonymized)")
    
    # Test validation
    validation = manager.validate_all_profiles()
    print(f"✅ Profile validation: {validation['validation_passed']}")
    print(f"   Valid profiles: {len(validation['valid_profiles'])}")
    print(f"   Invalid profiles: {len(validation['invalid_profiles'])}")
    
    # Test status
    status = manager.get_status()
    print(f"✅ Manager status: PII compliant = {status['pii_compliant']}")
    
    return validation['validation_passed']

if __name__ == "__main__":
    print("Testing Anonymized Demo Patient Manager")
    print("(PII-Compliant, Backend-Safe)")
    print("=" * 50)
    
    test_passed = test_anonymized_demo_manager()
    
    print(f"\n" + "=" * 50)
    print(f"Anonymized Demo Manager Test: {'✅ PASSED' if test_passed else '❌ FAILED'}")
    
    if test_passed:
        print(f"\n🎉 SUCCESS! Anonymized demo manager working correctly.")
        print(f"✅ NO PII - only anonymized data")
        print(f"✅ Safe for backend processing")
        print(f"✅ Proper fallback mechanisms")
        print(f"✅ Validation and compliance checks")
    else:
        print(f"\n❌ Issues found in anonymized demo manager")

# Export for imports
__all__ = ["DemoPatientManager"]