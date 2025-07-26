"""
Step 2: Integration Test for Simple Photo Analysis
File: backend/tests/test_step2_integration.py

COMPREHENSIVE TESTING:
- Tests Step 1 → Step 2 data flow
- Validates photo analysis functionality
- Tests pre-analyzed data loading
- Validates enhanced profile structure
- Tests fallback mechanisms
"""

import asyncio
import logging
import json
from pathlib import Path
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
            logger.error("❌ Pre-analyzed data loading failed")
            
        logger.info("-" * 40)
        
        # Test 3: Step 1 to Step 2 Data Flow
        logger.info("🔧 Test 3: Step 1 → Step 2 Data Flow")
        
        # Create mock Step 1 profile (simulate Step 1 output)
        mock_step1_profile = {
            "version": "1.0",
            "patient_info": {
                "first_name": "Maria",
                "birth_year": 1945,
                "current_age": 79,
                "age_group": "senior",
                "cultural_heritage": "Italian-American",
                "location": "Brooklyn, New York",
                "profile_complete": True
            },
            "theme_info": {
                "id": "birthday",
                "name": "Birthday",
                "description": "Celebrating special occasions and joyful milestones",
                "conversation_prompts": [
                    "How did you celebrate birthdays when you were young?",
                    "What was your favorite kind of birthday cake?"
                ],
                "photo_filename": "birthday.png",
                "source": "theme_manager"
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
                "profile_ready": True
            }
        }
        
        # Run Step 2 analysis
        enhanced_profile = await photo_agent.run(mock_step1_profile)
        
        # Validate enhanced profile
        if ("photo_analysis" in enhanced_profile and 
            enhanced_profile.get("pipeline_state", {}).get("current_step") == 2):
            
            test_results["step1_to_step2_flow"] = True
            logger.info("✅ Step 1 → Step 2 data flow successful")
            
            # Show photo analysis results
            photo_analysis = enhanced_profile["photo_analysis"]
            logger.info(f"📷 Photo analyzed: {photo_analysis.get('photo_filename')}")
            logger.info(f"🔍 Analysis method: {photo_analysis.get('analysis_method')}")
            logger.info(f"🎯 Theme connection: {photo_analysis.get('theme_connection')}")
            logger.info(f"✅ Success: {photo_analysis.get('success')}")
            
            # Show conversation starters
            analysis_data = photo_analysis.get("analysis_data", {})
            conversation_starters = analysis_data.get("conversation_starters", [])
            if conversation_starters:
                logger.info(f"💬 Conversation starters: {len(conversation_starters)}")
                for i, starter in enumerate(conversation_starters[:2], 1):
                    logger.info(f"   {i}. {starter}")
        else:
            logger.error("❌ Step 1 → Step 2 data flow failed")
            logger.error(f"   Enhanced profile keys: {list(enhanced_profile.keys())}")
        
        logger.info("-" * 40)
        
        # Test 4: Enhanced Profile Structure
        logger.info("🔧 Test 4: Enhanced Profile Structure")
        
        try:
            from utils.enhanced_profile_structure import enhanced_profile_structure
            
            # Validate enhanced profile
            validation = enhanced_profile_structure.validate_step2_profile(enhanced_profile)
            
            if validation["valid"] and validation["ready_for_step3"]:
                test_results["enhanced_profile_structure"] = True
                logger.info("✅ Enhanced profile structure validation passed")
                logger.info(f"📊 Step 1 valid: {validation['step1_valid']}")
                logger.info(f"📊 Step 2 valid: {validation['step2_valid']}")
                logger.info(f"📊 Ready for Step 3: {validation['ready_for_step3']}")
                
                # Show Step 2 summary
                step2_summary = enhanced_profile_structure.get_step2_summary(enhanced_profile)
                logger.info(f"📋 Step 2 Summary: {step2_summary}")
                
                # Show combined insights for Step 3
                combined_insights = enhanced_profile_structure.combine_step1_step2_insights(enhanced_profile)
                logger.info(f"🎯 Combined insights for Step 3:")
                logger.info(f"   Cultural heritage: {combined_insights['cultural_heritage']}")
                logger.info(f"   Theme context: {combined_insights['theme_context']}")
                logger.info(f"   Visual context: {combined_insights['visual_context'][:3]}...")
                logger.info(f"   Memory triggers: {combined_insights['memory_triggers'][:3]}...")
                
            else:
                logger.error("❌ Enhanced profile structure validation failed")
                logger.error(f"   Errors: {validation['errors']}")
                logger.error(f"   Warnings: {validation['warnings']}")
        
        except ImportError as e:
            logger.error(f"❌ Enhanced profile structure import failed: {e}")
        
        logger.info("-" * 40)
        
        # Test 5: Fallback Mechanisms
        logger.info("🔧 Test 5: Fallback Mechanisms")
        
        # Test with invalid photo filename
        mock_invalid_profile = mock_step1_profile.copy()
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
            step3_data = enhanced_profile_structure.extract_for_step3(enhanced_profile)
            logger.info(f"   Patient info: ✅ {bool(step3_data.get('patient_info'))}")
            logger.info(f"   Theme info: ✅ {bool(step3_data.get('theme_info'))}")
            logger.info(f"   Photo analysis: ✅ {bool(step3_data.get('photo_analysis'))}")
            logger.info(f"   Ready for Qloo: ✅ {step3_data.get('ready_for_qloo')}")
            
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
        from config.theme_config import simplified_theme_manager
        
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