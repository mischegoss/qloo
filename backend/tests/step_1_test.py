"""
Step 1: Test Script and Validation
File: backend/tests/test_step1_pipeline.py

PURPOSE:
- Test all Step 1 components together
- Validate data flow and structure
- Ensure clean handoff to Step 2
- Debug any integration issues
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Mock imports (replace with actual imports in real environment)
class MockThemeManager:
    """Mock theme manager for testing"""
    def get_daily_theme(self, session_id=None):
        return {
            "theme_of_the_day": {
                "id": "birthday",
                "name": "Birthday",
                "description": "Celebrating special occasions and milestones",
                "conversation_prompts": [
                    "How did you celebrate birthdays when you were young?",
                    "What was your favorite kind of birthday cake?",
                    "Do you remember a special birthday gift?"
                ]
            },
            "photo_filename": "birthday.png",
            "selection_metadata": {
                "date": "2024-01-26",
                "selection_method": "daily_consistent"
            }
        }

async def test_step1_complete_pipeline():
    """Test complete Step 1 pipeline"""
    
    logger.info("🧪 Testing Step 1: Information Consolidation Pipeline")
    logger.info("=" * 60)
    
    # Test input data (simulating UI input)
    test_patient_profile = {
        "first_name": "Maria",
        "birth_year": 1945,
        "cultural_heritage": "Italian-American",
        "city": "Brooklyn",
        "state": "New York",
        "additional_context": "Loves music and cooking"
    }
    
    test_feedback_data = {
        "likes": [
            {
                "type": "music",
                "name": "Frank Sinatra - My Way",
                "session_id": "test_session"
            },
            {
                "type": "recipe",
                "name": "Spaghetti with Marinara",
                "session_id": "test_session"
            }
        ],
        "dislikes": [
            {
                "type": "tv_show",
                "name": "Reality TV Show",
                "reason": "too_loud",
                "session_id": "test_session"
            }
        ]
    }
    
    try:
        # Step 1: Test Information Consolidator
        logger.info("📋 Testing Information Consolidator Agent...")
        
        # Initialize components
        mock_theme_manager = MockThemeManager()
        
        # Simulate the Information Consolidator logic
        consolidated_result = await simulate_information_consolidator(
            patient_profile=test_patient_profile,
            feedback_data=test_feedback_data,
            theme_manager=mock_theme_manager,
            session_id="test_session_123"
        )
        
        # Validate results
        logger.info("✅ Information Consolidator completed")
        logger.info("🔍 Validating Step 1 output...")
        
        validation_results = validate_step1_output(consolidated_result)
        
        if validation_results["valid"]:
            logger.info("✅ Step 1 validation: PASSED")
            
            # Display summary
            display_step1_summary(consolidated_result)
            
            # Test data extraction for Step 2
            step2_data = extract_for_step2(consolidated_result)
            logger.info("✅ Step 2 data extraction: SUCCESS")
            logger.info(f"📦 Step 2 will receive: {list(step2_data.keys())}")
            
            return True
            
        else:
            logger.error("❌ Step 1 validation: FAILED")
            for error in validation_results["errors"]:
                logger.error(f"   - {error}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Step 1 test failed: {e}")
        return False

async def simulate_information_consolidator(patient_profile: Dict[str, Any],
                                           feedback_data: Dict[str, Any],
                                           theme_manager,
                                           session_id: str) -> Dict[str, Any]:
    """Simulate the Information Consolidator Agent logic"""
    
    # Extract basic profile information
    basic_info = extract_basic_profile(patient_profile)
    
    # Process feedback
    feedback_summary = process_feedback(feedback_data)
    
    # Select theme
    theme_data = theme_manager.get_daily_theme(session_id)
    selected_theme = theme_data["theme_of_the_day"]
    photo_filename = theme_data["photo_filename"]
    
    # Create consolidated profile
    consolidated_profile = {
        "patient_info": basic_info,
        "theme_info": {
            **selected_theme,
            "photo_filename": photo_filename
        },
        "feedback_info": feedback_summary,
        "session_metadata": {
            "session_id": session_id,
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
    
    return consolidated_profile

def extract_basic_profile(patient_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and clean basic profile information"""
    
    first_name = patient_profile.get("first_name", "Friend")
    birth_year = patient_profile.get("birth_year")
    cultural_heritage = patient_profile.get("cultural_heritage", "American")
    
    current_age = None
    age_group = "senior"
    
    if birth_year:
        current_age = datetime.now().year - birth_year
        if current_age >= 80:
            age_group = "oldest_senior"
        elif current_age >= 65:
            age_group = "senior"
        else:
            age_group = "adult"
    
    return {
        "first_name": first_name,
        "birth_year": birth_year,
        "current_age": current_age,
        "age_group": age_group,
        "cultural_heritage": cultural_heritage,
        "location": f"{patient_profile.get('city', '')}, {patient_profile.get('state', '')}",
        "additional_context": patient_profile.get("additional_context", ""),
        "profile_complete": bool(first_name and birth_year and cultural_heritage)
    }

def process_feedback(feedback_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process feedback data"""
    
    if not feedback_data:
        return {
            "likes": [],
            "dislikes": [],
            "total_feedback": 0,
            "feedback_available": False,
            "insights": {"preferred_types": [], "avoided_types": []}
        }
    
    likes = feedback_data.get("likes", [])
    dislikes = feedback_data.get("dislikes", [])
    
    # Generate simple insights
    preferred_types = list(set([like.get("type", "unknown") for like in likes]))
    avoided_types = list(set([dislike.get("type", "unknown") for dislike in dislikes]))
    
    return {
        "likes": likes,
        "dislikes": dislikes,
        "total_feedback": len(likes) + len(dislikes),
        "feedback_available": len(likes) + len(dislikes) > 0,
        "insights": {
            "preferred_types": preferred_types,
            "avoided_types": avoided_types,
            "engagement_level": "engaged" if len(likes) + len(dislikes) > 2 else "exploring"
        }
    }

def validate_step1_output(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Step 1 output structure"""
    
    validation = {
        "valid": True,
        "errors": [],
        "warnings": []
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
    
    # Check patient info
    patient_info = profile.get("patient_info", {})
    if not patient_info.get("first_name"):
        validation["warnings"].append("Missing patient first name")
    if not patient_info.get("cultural_heritage"):
        validation["warnings"].append("Missing cultural heritage")
    
    # Check theme info
    theme_info = profile.get("theme_info", {})
    required_theme_fields = ["id", "name", "description", "conversation_prompts"]
    for field in required_theme_fields:
        if not theme_info.get(field):
            validation["errors"].append(f"Missing theme field: {field}")
            validation["valid"] = False
    
    # Check photo filename
    if not theme_info.get("photo_filename"):
        validation["warnings"].append("Missing photo filename for UI")
    
    # Check pipeline state
    pipeline_state = profile.get("pipeline_state", {})
    if pipeline_state.get("current_step") != 1:
        validation["errors"].append("Incorrect pipeline step")
        validation["valid"] = False
    
    if pipeline_state.get("next_step") != "photo_analysis":
        validation["errors"].append("Incorrect next step")
        validation["valid"] = False
    
    return validation

def display_step1_summary(profile: Dict[str, Any]):
    """Display human-readable summary of Step 1 results"""
    
    logger.info("📊 Step 1 Results Summary:")
    logger.info("-" * 40)
    
    # Patient info
    patient_info = profile.get("patient_info", {})
    logger.info(f"👤 Patient: {patient_info.get('first_name', 'Unknown')}")
    logger.info(f"📅 Age: {patient_info.get('current_age', 'Unknown')} ({patient_info.get('age_group', 'Unknown')})")
    logger.info(f"🌍 Heritage: {patient_info.get('cultural_heritage', 'Unknown')}")
    logger.info(f"📍 Location: {patient_info.get('location', 'Unknown')}")
    
    # Theme info
    theme_info = profile.get("theme_info", {})
    logger.info(f"🎯 Theme: {theme_info.get('name', 'Unknown')}")
    logger.info(f"📷 Photo: {theme_info.get('photo_filename', 'None')}")
    logger.info(f"📝 Description: {theme_info.get('description', 'None')}")
    
    # Feedback info
    feedback_info = profile.get("feedback_info", {})
    logger.info(f"👍 Feedback: {feedback_info.get('total_feedback', 0)} items")
    if feedback_info.get("feedback_available"):
        insights = feedback_info.get("insights", {})
        logger.info(f"   Preferred: {insights.get('preferred_types', [])}")
        logger.info(f"   Avoided: {insights.get('avoided_types', [])}")
    
    # Pipeline state
    pipeline_state = profile.get("pipeline_state", {})
    logger.info(f"🔧 Pipeline: Step {pipeline_state.get('current_step')} → {pipeline_state.get('next_step')}")

def extract_for_step2(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Extract data needed for Step 2 (Photo Analysis)"""
    
    return {
        "patient_info": profile.get("patient_info", {}),
        "theme_info": profile.get("theme_info", {}),
        "feedback_info": profile.get("feedback_info", {}),
        "session_metadata": profile.get("session_metadata", {}),
        "pipeline_state": profile.get("pipeline_state", {})
    }

async def test_theme_to_photo_mapping():
    """Test theme to photo filename mapping"""
    
    logger.info("🧪 Testing Theme → Photo Mapping")
    logger.info("-" * 40)
    
    test_themes = [
        {"id": "birthday", "name": "Birthday"},
        {"id": "memory_lane", "name": "Memory Lane"},
        {"id": "family", "name": "Family"},
        {"id": "music", "name": "Music"},
        {"id": "food", "name": "Food"}
    ]
    
    for theme in test_themes:
        # Simple mapping logic
        theme_id = theme.get("id", "")
        if theme_id:
            photo_filename = f"{theme_id.lower()}.png"
        else:
            clean_name = theme.get("name", "").lower().replace(" ", "_")
            photo_filename = f"{clean_name}.png"
        
        logger.info(f"🎯 {theme['name']} → {photo_filename}")
    
    logger.info("✅ Theme mapping test completed")

async def run_all_step1_tests():
    """Run all Step 1 tests"""
    
    logger.info("🚀 Running Complete Step 1 Test Suite")
    logger.info("=" * 60)
    
    # Test 1: Theme to photo mapping
    await test_theme_to_photo_mapping()
    logger.info("")
    
    # Test 2: Complete pipeline
    pipeline_success = await test_step1_complete_pipeline()
    
    logger.info("")
    logger.info("=" * 60)
    
    if pipeline_success:
        logger.info("🎉 Step 1 Test Suite: ALL TESTS PASSED")
        logger.info("✅ Ready to proceed to Step 2: Photo Analysis")
    else:
        logger.error("❌ Step 1 Test Suite: SOME TESTS FAILED")
        logger.error("🔧 Fix issues before proceeding to Step 2")
    
    return pipeline_success

if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(run_all_step1_tests())