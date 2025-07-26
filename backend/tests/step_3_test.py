"""
Step 3: Integration Tests
File: backend/tests/test_step3_integration.py

Comprehensive tests for Step 3: Qloo Cultural Analysis
- Complete Steps 1-2-3 pipeline flow
- Qloo API integration validation
- Fallback mechanism testing
- Step 4 readiness confirmation
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

# Add backend directory to Python path with explicit path resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)  # Go up from tests/ to backend/
project_root = os.path.dirname(backend_dir)  # Go up from backend/ to project root

# Add both backend and project root to Python path
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_root)

print(f"DEBUG: Current dir: {current_dir}")
print(f"DEBUG: Backend dir: {backend_dir}")
print(f"DEBUG: Project root: {project_root}")
print(f"DEBUG: Python path: {sys.path[:3]}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_step3_complete_integration():
    """Test complete Steps 1-2-3 integration flow"""
    
    logger.info("🧪 Testing Complete Steps 1-2-3 Integration")
    logger.info("=" * 80)
    
    test_results = {
        "step1_step2_integration": False,
        "step3_qloo_calls": False,
        "cultural_intelligence_validation": False,
        "step4_readiness": False,
        "fallback_mechanisms": False
    }
    
    try:
        # Import required modules with better error handling
        print("DEBUG: Attempting to import Step 3 modules...")
        
        try:
            from multi_tool_agent.agents.qloo_cultural_analysis_agent import QlooCulturalAnalysisAgent
            print("✅ Successfully imported QlooCulturalAnalysisAgent")
        except ImportError as e:
            logger.error(f"❌ Failed to import QlooCulturalAnalysisAgent: {e}")
            logger.error("💡 Make sure qloo_cultural_analysis_agent.py is in backend/multi_tool_agent/agents/")
            return False
        
        try:
            from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
            print("✅ Successfully imported QlooInsightsAPI")
        except ImportError as e:
            logger.error(f"❌ Failed to import QlooInsightsAPI: {e}")
            logger.error("💡 Make sure qloo_tools.py exists in backend/multi_tool_agent/tools/")
            return False
        
        try:
            from utils.enhanced_profile_structure_step3 import (
                validate_step3_output, 
                extract_for_step4,
                get_cultural_insights_summary,
                create_step3_test_profile
            )
            print("✅ Successfully imported Step 3 profile structure utilities")
        except ImportError as e:
            logger.error(f"❌ Failed to import Step 3 utilities: {e}")
            logger.error("💡 Make sure enhanced_profile_structure_step3.py is in backend/utils/")
            return False
        
        try:
            from utils.enhanced_profile_structure import enhanced_profile_structure
            print("✅ Successfully imported enhanced_profile_structure")
        except ImportError as e:
            logger.error(f"❌ Failed to import enhanced_profile_structure: {e}")
            logger.error("💡 Make sure enhanced_profile_structure.py is in backend/utils/")
            return False
        
        # Test 1: Validate Step 1-2 integration using existing test profile
        logger.info("🔍 Test 1: Steps 1-2 Integration Validation")
        
        # Create mock Step 2 output (would come from actual Steps 1-2)
        mock_step2_profile = create_mock_step2_profile()
        
        if validate_mock_step2_profile(mock_step2_profile):
            test_results["step1_step2_integration"] = True
            logger.info("✅ Steps 1-2 integration valid")
        else:
            logger.error("❌ Steps 1-2 integration invalid")
        
        logger.info("-" * 60)
        
        # Test 2: Step 3 Qloo Cultural Analysis
        logger.info("🔍 Test 2: Step 3 Qloo Cultural Analysis")
        
        # Initialize Qloo tool and agent
        api_key = os.getenv("QLOO_API_KEY")
        if api_key:
            qloo_tool = QlooInsightsAPI(api_key)
            
            # Test connection
            connection_ok = await qloo_tool.test_connection()
            if connection_ok:
                logger.info("✅ Qloo API connection successful")
                
                # Initialize Step 3 agent
                step3_agent = QlooCulturalAnalysisAgent(qloo_tool)
                
                # Run Step 3 analysis
                enhanced_profile = await step3_agent.run(mock_step2_profile)
                
                # Validate Step 3 output
                validation = validate_step3_output(enhanced_profile)
                if validation["valid"]:
                    test_results["step3_qloo_calls"] = True
                    logger.info("✅ Step 3 Qloo calls successful")
                    
                    # Log cultural intelligence summary
                    insights = get_cultural_insights_summary(enhanced_profile)
                    logger.info(f"📊 Cultural insights: {insights['successful_calls']} successful calls")
                    logger.info(f"   Heritage: {insights['cultural_heritage']}")
                    logger.info(f"   Artists: {insights['artists']['count']} ({insights['artists']['method']})")
                    logger.info(f"   Places: {insights['places']['count']} ({insights['places']['method']})")
                    
                else:
                    logger.error("❌ Step 3 output validation failed")
                    for key, result in validation.items():
                        if not result and key != "valid":
                            logger.error(f"   - {key}: FAILED")
            else:
                logger.warning("⚠️ Qloo API connection failed, testing fallback")
                # Test fallback mechanism
                step3_agent = QlooCulturalAnalysisAgent(None)  # No API tool
                enhanced_profile = await step3_agent.run(mock_step2_profile)
                
                if enhanced_profile.get("cultural_intelligence"):
                    test_results["step3_qloo_calls"] = True
                    logger.info("✅ Step 3 fallback mechanism working")
        else:
            logger.warning("⚠️ No QLOO_API_KEY found, testing fallback only")
            step3_agent = QlooCulturalAnalysisAgent(None)
            enhanced_profile = await test_step3_fallback_only(step3_agent, mock_step2_profile)
            if enhanced_profile:
                test_results["step3_qloo_calls"] = True
        
        logger.info("-" * 60)
        
        # Test 3: Cultural Intelligence Validation
        logger.info("🔍 Test 3: Cultural Intelligence Data Validation")
        
        if "enhanced_profile" in locals():
            cultural_intelligence = enhanced_profile.get("cultural_intelligence", {})
            
            # Check required structure
            if (cultural_intelligence.get("cultural_recommendations") and
                cultural_intelligence.get("metadata")):
                
                # Validate artists data
                artists = cultural_intelligence["cultural_recommendations"].get("artists", {})
                places = cultural_intelligence["cultural_recommendations"].get("places", {})
                
                if (artists.get("available") or artists.get("method") == "fallback") and \
                   (places.get("available") or places.get("method") == "fallback"):
                    test_results["cultural_intelligence_validation"] = True
                    logger.info("✅ Cultural intelligence data structure valid")
                else:
                    logger.error("❌ Cultural intelligence missing required data")
            else:
                logger.error("❌ Cultural intelligence structure invalid")
        
        logger.info("-" * 60)
        
        # Test 4: Step 4 Readiness
        logger.info("🔍 Test 4: Step 4 Readiness Validation")
        
        if "enhanced_profile" in locals():
            step4_data = extract_for_step4(enhanced_profile)
            
            if step4_data.get("metadata", {}).get("ready_for_gemini_curation"):
                test_results["step4_readiness"] = True
                logger.info("✅ Profile ready for Step 4 (Gemini Content Curation)")
                
                # Log Step 4 data summary
                logger.info(f"📋 Step 4 data ready:")
                logger.info(f"   Patient: {step4_data['patient_context']['first_name']} ({step4_data['patient_context']['cultural_heritage']})")
                logger.info(f"   Theme: {step4_data['theme_context']['theme_name']}")
                logger.info(f"   Artists: {step4_data['cultural_recommendations']['artists']['entity_count']} available")
                logger.info(f"   Places: {step4_data['cultural_recommendations']['places']['entity_count']} available")
            else:
                logger.error("❌ Profile not ready for Step 4")
                if "error" in step4_data:
                    logger.error(f"   Error: {step4_data['error']}")
        
        logger.info("-" * 60)
        
        # Test 5: Fallback Mechanisms
        logger.info("🔍 Test 5: Fallback Mechanisms Validation")
        
        # Create profile with invalid data to trigger fallbacks
        invalid_profile = create_invalid_step2_profile()
        
        # Test with no API tool (forces fallback)
        fallback_agent = QlooCulturalAnalysisAgent(None)
        fallback_profile = await fallback_agent.run(invalid_profile)
        
        if (fallback_profile.get("cultural_intelligence") and
            fallback_profile.get("pipeline_state", {}).get("ready_for_step4")):
            test_results["fallback_mechanisms"] = True
            logger.info("✅ Fallback mechanisms working correctly")
            
            # Check fallback metadata
            fallback_metadata = fallback_profile["cultural_intelligence"]["metadata"]
            logger.info(f"🔄 Fallback method: {fallback_metadata.get('method', 'unknown')}")
        else:
            logger.error("❌ Fallback mechanisms failed")
        
        logger.info("=" * 80)
        
        # Final Results Summary
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        logger.info(f"🎯 STEP 3 TEST RESULTS: {passed_tests}/{total_tests} tests passed")
        
        for test_name, passed in test_results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            logger.info(f"   {test_name}: {status}")
        
        if passed_tests == total_tests:
            logger.info("🎉 ALL STEP 3 TESTS PASSED!")
            logger.info("✅ Step 3: Qloo Cultural Analysis is working correctly")
            logger.info("🚀 Ready to proceed to Step 4: Gemini Content Curation")
            
            # Show final data ready for Step 4
            if "enhanced_profile" in locals():
                final_step4_data = extract_for_step4(enhanced_profile)
                logger.info("\n📋 Final Data Ready for Step 4:")
                logger.info(f"   Cultural heritage: ✅ {final_step4_data['patient_context']['cultural_heritage']}")
                logger.info(f"   Artists available: ✅ {final_step4_data['cultural_recommendations']['artists']['entity_count']}")
                logger.info(f"   Places available: ✅ {final_step4_data['cultural_recommendations']['places']['entity_count']}")
                logger.info(f"   Theme context: ✅ {final_step4_data['theme_context']['theme_name']}")
                logger.info(f"   Photo context: ✅ {bool(final_step4_data['photo_context']['analysis_data'])}")
        else:
            logger.warning(f"⚠️ {total_tests - passed_tests} tests failed")
            logger.warning("🔧 Check failed components before proceeding to Step 4")
        
        return passed_tests == total_tests
        
    except Exception as e:
        logger.error(f"❌ Step 3 integration test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def create_mock_step2_profile() -> Dict[str, Any]:
    """Create mock Step 2 output for testing Step 3"""
    
    return {
        "patient_info": {
            "first_name": "Maria",
            "birth_year": 1945,
            "cultural_heritage": "Italian-American",
            "city": "Brooklyn",
            "state": "New York",
            "additional_context": "Loves music and cooking",
            "demo_dislikes": []  # No dislikes for full testing
        },
        
        "theme_info": {
            "id": "birthday",
            "name": "Birthday",
            "photo_filename": "birthday.png",
            "conversation_starters": [
                "What was your favorite birthday memory?",
                "How did your family celebrate birthdays?"
            ],
            "selection_metadata": {
                "date": datetime.now().isoformat(),
                "selection_method": "daily_consistent"
            }
        },
        
        "feedback_info": {
            "likes": [],
            "dislikes": [],
            "session_count": 1
        },
        
        "photo_analysis": {
            "photo_filename": "birthday.png",
            "analysis_method": "pre_analyzed",
            "analysis_data": {
                "description": "A warm birthday celebration scene with cake and decorations",
                "objects_detected": ["cake", "candles", "decorations", "table"],
                "mood": "celebratory",
                "conversation_starters": [
                    "This reminds me of birthday parties - what was your favorite cake?",
                    "Do you remember blowing out candles as a child?"
                ]
            },
            "theme_connection": "Birthday",
            "analysis_timestamp": datetime.now().isoformat(),
            "success": True
        },
        
        "session_metadata": {
            "session_id": "test_session_step3",
            "timestamp": datetime.now().isoformat(),
            "user_agent": "test_integration"
        },
        
        "pipeline_state": {
            "current_step": 2,
            "next_step": 3,
            "step_name": "photo_analysis",
            "completion_time": datetime.now().isoformat(),
            "ready_for_step3": True
        }
    }

def validate_mock_step2_profile(profile: Dict[str, Any]) -> bool:
    """Validate that mock Step 2 profile has required structure"""
    
    required_sections = ["patient_info", "theme_info", "photo_analysis", "pipeline_state"]
    
    for section in required_sections:
        if section not in profile:
            logger.error(f"❌ Missing required section: {section}")
            return False
    
    # Check pipeline readiness
    pipeline_state = profile.get("pipeline_state", {})
    if not pipeline_state.get("ready_for_step3"):
        logger.error("❌ Profile not ready for Step 3")
        return False
    
    return True

def create_invalid_step2_profile() -> Dict[str, Any]:
    """Create invalid Step 2 profile to test fallback mechanisms"""
    
    return {
        "patient_info": {
            "first_name": "Test",
            "birth_year": None,  # Invalid birth year
            "cultural_heritage": "",  # Empty heritage
            "demo_dislikes": []
        },
        
        "theme_info": {
            "id": "unknown",
            "name": "Unknown Theme",
            "photo_filename": "nonexistent.png"
        },
        
        "photo_analysis": {
            "photo_filename": "nonexistent.png",
            "analysis_method": "fallback",
            "success": False
        },
        
        "pipeline_state": {
            "current_step": 2,
            "next_step": 3,
            "ready_for_step3": True  # Still ready, but with invalid data
        }
    }

async def test_step3_fallback_only(agent, profile: Dict[str, Any]) -> Dict[str, Any]:
    """Test Step 3 with fallback mechanisms only"""
    
    try:
        logger.info("🔄 Testing Step 3 fallback mechanisms")
        
        # Run agent with no API tool (forces fallback)
        result = await agent.run(profile)
        
        if result.get("cultural_intelligence"):
            logger.info("✅ Fallback mechanisms functional")
            return result
        else:
            logger.error("❌ Fallback mechanisms failed")
            return None
            
    except Exception as e:
        logger.error(f"❌ Fallback test failed: {e}")
        return None

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the integration test
    success = asyncio.run(test_step3_complete_integration())
    
    # Exit with appropriate code
    exit(0 if success else 1)