"""
Step 2: Integration Test for Simple Photo Analysis - FIXED PYTHON PATH
File: backend/tests/step_2_test.py

CRITICAL FIX:
- Added Python path configuration for direct script execution
- Now correctly imports multi_tool_agent module
- Maintains all existing test functionality
- Safe fallbacks and error handling preserved
"""

import sys
import os
from pathlib import Path

# CRITICAL FIX: Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_step2_photo_analysis():
    """Comprehensive test of Step 2 Photo Analysis"""
    
    logger.info("🧪 Testing Step 2: Simple Photo Analysis Integration")
    logger.info("=" * 60)
    
    test_results = {
        "photo_analysis_agent": False,
        "pre_analyzed_data": False,
        "step1_to_step2_flow": False,
        "enhanced_profile_structure": False,
        "fallback_mechanisms": False
    }
    
    try:
        # Test 1: Photo Analysis Agent Initialization
        logger.info("🔧 Test 1: Photo Analysis Agent Initialization")
        
        from multi_tool_agent.agents.simple_photo_analysis_agent import SimplePhotoAnalysisAgent
        
        photo_agent = SimplePhotoAnalysisAgent()
        
        # Validate initialization
        if hasattr(photo_agent, 'photo_analysis_data'):
            test_results["photo_analysis_agent"] = True
            logger.info("✅ Photo Analysis Agent initialized successfully")
            
            # Check available photos
            available_photos = photo_agent.get_available_photos()
            logger.info(f"📷 Available photos: {len(available_photos)}")
            for photo in available_photos[:3]:  # Show first 3
                logger.info(f"   - {photo}")
        else:
            logger.error("❌ Photo Analysis Agent initialization failed")
        
        logger.info("-" * 40)
        
        # Test 2: Pre-analyzed Data Loading
        logger.info("🔧 Test 2: Pre-analyzed Data Loading")
        
        validation = photo_agent.validate_photo_analysis_data()
        
        if validation["total_photos"] > 0 and validation["fallback_available"]:
            test_results["pre_analyzed_data"] = True
            logger.info("✅ Pre-analyzed data loaded successfully")
            logger.info(f"📊 Total photos: {validation['total_photos']}")
            logger.info(f"📊 Dementia friendly: {validation['all_dementia_friendly']}")
            logger.info(f"📊 Positive memories: {validation['all_positive_memories']}")
        else:
            logger.error("❌ Pre-analyzed data validation failed")
        
        logger.info("-" * 40)
        
        # Test 3: Step 1 → Step 2 Data Flow
        logger.info("🔧 Test 3: Step 1 → Step 2 Data Flow")
        
        # Create mock consolidated profile from Step 1
        mock_consolidated_profile = {
            "patient_info": {
                "name": "Test Patient",
                "age": 75,
                "care_preferences": ["family", "comfort"]
            },
            "theme_info": {
                "name": "Birthday Celebration",
                "photo_filename": "birthday.png",
                "description": "Special birthday memories"
            },
            "pipeline_state": {
                "current_step": 1,
                "step1_complete": True
            }
        }
        
        # Run Step 2 with mock data
        enhanced_profile = await photo_agent.run(mock_consolidated_profile)
        
        if ("photo_analysis" in enhanced_profile and 
            enhanced_profile["pipeline_state"]["current_step"] == 2):
            
            test_results["step1_to_step2_flow"] = True
            logger.info("✅ Step 1 → Step 2 data flow working correctly")
            
            photo_analysis = enhanced_profile["photo_analysis"]
            logger.info(f"🔍 Photo analyzed: {photo_analysis.get('photo_filename')}")
            logger.info(f"🔍 Analysis method: {photo_analysis.get('analysis_method')}")
            logger.info(f"🔍 Theme connection: {photo_analysis.get('theme_connection')}")
        else:
            logger.error("❌ Step 1 → Step 2 data flow failed")
        
        logger.info("-" * 40)
        
        # Test 4: Enhanced Profile Structure
        logger.info("🔧 Test 4: Enhanced Profile Structure")
        
        # Check enhanced profile structure
        required_sections = ["patient_info", "theme_info", "photo_analysis", "pipeline_state"]
        
        if all(section in enhanced_profile for section in required_sections):
            test_results["enhanced_profile_structure"] = True
            logger.info("✅ Enhanced profile structure is correct")
            
            # Validate photo analysis section
            photo_analysis = enhanced_profile["photo_analysis"]
            analysis_data = photo_analysis.get("analysis_data", {})
            
            logger.info(f"📋 Conversation starters: {len(analysis_data.get('conversation_starters', []))}")
            logger.info(f"📋 Cultural context: {analysis_data.get('cultural_context', 'N/A')}")
            logger.info(f"📋 Memory triggers: {len(analysis_data.get('memory_triggers', []))}")
            logger.info(f"📋 Safety level: {analysis_data.get('safety_level', 'N/A')}")
            
        else:
            missing_sections = [s for s in required_sections if s not in enhanced_profile]
            logger.error(f"❌ Enhanced profile missing sections: {missing_sections}")
        
        logger.info("-" * 40)
        
        # Test 5: Fallback Mechanisms
        logger.info("🔧 Test 5: Fallback Mechanisms")
        
        # Test with invalid photo filename
        mock_invalid_profile = mock_consolidated_profile.copy()
        mock_invalid_profile["theme_info"]["photo_filename"] = "nonexistent.png"
        
        fallback_profile = await photo_agent.run(mock_invalid_profile)
        
        if ("photo_analysis" in fallback_profile and 
            fallback_profile["photo_analysis"].get("analysis_method") in ["fallback", "emergency_fallback"]):
            
            test_results["fallback_mechanisms"] = True
            logger.info("✅ Fallback mechanisms working correctly")
            
            fallback_analysis = fallback_profile["photo_analysis"]
            logger.info(f"🔄 Fallback method: {fallback_analysis.get('analysis_method')}")
            logger.info(f"🔄 Fallback success: {fallback_analysis.get('success')}")
        else:
            logger.error("❌ Fallback mechanisms failed")
        
        logger.info("=" * 60)
        
        # Final Results Summary
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        logger.info(f"🎯 STEP 2 TEST RESULTS: {passed_tests}/{total_tests} tests passed")
        
        for test_name, passed in test_results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            logger.info(f"   {test_name}: {status}")
        
        if passed_tests == total_tests:
            logger.info("🎉 ALL STEP 2 TESTS PASSED!")
            logger.info("✅ Step 2: Photo Analysis is working correctly")
            logger.info("🚀 Ready to proceed to Step 3: Qloo Cultural Analysis")
            
            # Show data ready for Step 3
            logger.info("\n📋 Data Ready for Step 3:")
            logger.info(f"   Patient info: ✅ {bool(enhanced_profile.get('patient_info'))}")
            logger.info(f"   Theme info: ✅ {bool(enhanced_profile.get('theme_info'))}")
            logger.info(f"   Photo analysis: ✅ {bool(enhanced_profile.get('photo_analysis'))}")
            logger.info(f"   Pipeline state: ✅ {enhanced_profile.get('pipeline_state', {}).get('current_step') == 2}")
            
        else:
            logger.warning(f"⚠️ {total_tests - passed_tests} tests failed")
            logger.warning("🔧 Check failed components before proceeding to Step 3")
        
        return passed_tests == total_tests
        
    except Exception as e:
        logger.error(f"❌ Step 2 integration test failed: {e}")
        return False

async def test_all_themes():
    """Test photo analysis for all available themes"""
    
    logger.info("\n🎭 Testing All Available Themes")
    logger.info("-" * 40)
    
    try:
        from multi_tool_agent.agents.simple_photo_analysis_agent import SimplePhotoAnalysisAgent
        
        photo_agent = SimplePhotoAnalysisAgent()
        available_photos = photo_agent.get_available_photos()
        
        logger.info(f"📷 Testing {len(available_photos)} photos")
        
        for photo_filename in available_photos:
            # Extract theme name from filename
            theme_name = photo_filename.replace(".png", "").replace("_", " ").title()
            
            # Create mock profile for this theme
            mock_profile = {
                "theme_info": {
                    "name": theme_name,
                    "photo_filename": photo_filename
                },
                "pipeline_state": {"current_step": 1}
            }
            
            # Analyze photo
            result = await photo_agent._analyze_photo(photo_filename, mock_profile["theme_info"])
            
            if result.get("success"):
                analysis_data = result.get("analysis_data", {})
                starters = analysis_data.get("conversation_starters", [])
                logger.info(f"✅ {photo_filename}: {len(starters)} conversation starters")
            else:
                logger.warning(f"⚠️ {photo_filename}: Analysis failed")
        
        logger.info("✅ All theme photos tested")
        
    except Exception as e:
        logger.error(f"❌ Theme testing failed: {e}")

if __name__ == "__main__":
    async def run_all_tests():
        """Run all Step 2 tests"""
        
        # Main integration test
        main_test_success = await test_step2_photo_analysis()
        
        # Test all themes
        await test_all_themes()
        
        return main_test_success
    
    # Run tests
    success = asyncio.run(run_all_tests())
    
    if success:
        logger.info("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        logger.info("✅ Step 2 is ready for integration")
    else:
        logger.error("\n❌ Some tests failed - check logs above")
        sys.exit(1)