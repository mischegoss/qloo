#!/usr/bin/env python3
"""
Quick Step 3 Integration Test
File: backend/tests/quick_step3_integration_test.py

VERIFICATION: Test simplified qloo_tools.py + Cultural Analysis Agent
- Verify missing methods are now present
- Test API calls work with simple tags
- Test Agent 3 can call the methods successfully
- Test both API and fallback scenarios
"""

import os
import sys
import logging
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent  # Go up to project root (not just backend)
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))  # Also add backend path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

async def test_qloo_tools_methods():
    """Test 1: Verify qloo_tools has all required methods"""
    
    logger.info("🧪 Test 1: Qloo Tools Method Verification")
    logger.info("-" * 50)
    
    try:
        from backend.multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        api_key = os.getenv("QLOO_API_KEY", "test_key")
        qloo = QlooInsightsAPI(api_key)
        
        # Check required methods exist
        required_methods = [
            'get_safe_classical_music',
            'get_tag_based_insights', 
            'make_cultural_calls',
            'test_connection'
        ]
        
        for method in required_methods:
            if hasattr(qloo, method):
                logger.info(f"✅ Method found: {method}")
            else:
                logger.error(f"❌ Method missing: {method}")
                return False
        
        logger.info("✅ All required methods present in qloo_tools")
        return True
        
    except Exception as e:
        logger.error(f"❌ Qloo tools test failed: {e}")
        return False

async def test_qloo_api_calls():
    """Test 2: Test simplified API calls"""
    
    logger.info("\n🧪 Test 2: Simplified API Calls")
    logger.info("-" * 50)
    
    try:
        from backend.multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        api_key = os.getenv("QLOO_API_KEY")
        if not api_key:
            logger.info("⚠️ No API key - testing fallbacks only")
            api_key = "test_key"
        
        qloo = QlooInsightsAPI(api_key)
        
        # Test 1: Classical music call
        logger.info("\n🎵 Testing classical music call...")
        classical_result = await qloo.get_safe_classical_music("Italian-American", take=3)
        
        logger.info(f"   Success: {classical_result.get('success')}")
        logger.info(f"   Entities: {classical_result.get('entity_count', 0)}")
        logger.info(f"   Content type: {classical_result.get('content_type')}")
        
        # Test 2: Cuisine places call
        logger.info("\n🍽️ Testing cuisine places call...")
        places_result = await qloo.get_tag_based_insights("urn:entity:place", "italian", take=3)
        
        logger.info(f"   Success: {places_result.get('success')}")
        logger.info(f"   Entities: {places_result.get('entity_count', 0)}")
        logger.info(f"   Tag: {places_result.get('tag')}")
        
        # Test 3: Combined cultural calls
        logger.info("\n🎯 Testing combined cultural calls...")
        combined_result = await qloo.make_cultural_calls("Italian-American")
        
        successful_calls = combined_result.get('successful_calls', 0)
        total_results = combined_result.get('total_results', 0)
        
        logger.info(f"   Successful calls: {successful_calls}/2")
        logger.info(f"   Total results: {total_results}")
        
        # Verify structure
        cultural_recs = combined_result.get("cultural_recommendations", {})
        has_artists = "artists" in cultural_recs
        has_places = "places" in cultural_recs
        
        logger.info(f"   Has artists: {has_artists}")
        logger.info(f"   Has places: {has_places}")
        
        logger.info("✅ API calls completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ API calls test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cultural_analysis_agent():
    """Test 3: Test simplified Cultural Analysis Agent"""
    
    logger.info("\n🧪 Test 3: Cultural Analysis Agent Integration")
    logger.info("-" * 50)
    
    try:
        from backend.multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        from backend.multi_tool_agent.agents.qloo_cultural_analysis_agent import QlooCulturalAnalysisAgent
        
        # Initialize tools
        api_key = os.getenv("QLOO_API_KEY", "test_key")
        qloo_tool = QlooInsightsAPI(api_key)
        agent = QlooCulturalAnalysisAgent(qloo_tool)
        
        # Test data
        consolidated_info = {
            "patient_profile": {
                "cultural_heritage": "Italian-American",
                "birth_year": 1945,
                "name": "Maria"
            }
        }
        
        cultural_profile = {
            "cultural_profile": {
                "cultural_elements": {
                    "heritage": "Italian-American"
                }
            }
        }
        
        # Run the agent
        logger.info("🚀 Running Cultural Analysis Agent...")
        result = await agent.run(consolidated_info, cultural_profile)
        
        # Verify result structure
        qloo_intel = result.get("qloo_intelligence", {})
        metadata = qloo_intel.get("metadata", {})
        cultural_recs = qloo_intel.get("cultural_recommendations", {})
        
        logger.info(f"✅ Agent completed successfully")
        logger.info(f"   Agent: {metadata.get('agent')}")
        logger.info(f"   Version: {metadata.get('version')}")
        logger.info(f"   Heritage: {metadata.get('heritage')}")
        logger.info(f"   Successful calls: {metadata.get('successful_calls', 0)}")
        logger.info(f"   Total results: {metadata.get('total_results', 0)}")
        
        # Check cultural recommendations
        if "artists" in cultural_recs:
            artists_count = cultural_recs["artists"].get("entity_count", 0)
            logger.info(f"   Artists: {artists_count}")
        
        if "places" in cultural_recs:
            places_count = cultural_recs["places"].get("entity_count", 0)
            logger.info(f"   Places: {places_count}")
        
        # Verify ready for Step 4
        has_artists = "artists" in cultural_recs
        has_places = "places" in cultural_recs
        has_metadata = bool(metadata)
        
        step4_ready = has_artists and has_places and has_metadata
        logger.info(f"✅ Step 4 ready: {step4_ready}")
        
        return step4_ready
        
    except Exception as e:
        logger.error(f"❌ Cultural Analysis Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_fallback_scenarios():
    """Test 4: Test fallback scenarios"""
    
    logger.info("\n🧪 Test 4: Fallback Scenarios")
    logger.info("-" * 50)
    
    try:
        from backend.multi_tool_agent.agents.qloo_cultural_analysis_agent import QlooCulturalAnalysisAgent
        
        # Test with no Qloo tool
        agent = QlooCulturalAnalysisAgent(qloo_tool=None)
        
        consolidated_info = {
            "patient_profile": {
                "cultural_heritage": "Irish",
                "birth_year": 1950,
                "name": "Patrick"
            }
        }
        
        cultural_profile = {}
        
        logger.info("🔄 Testing fallback scenario (no Qloo tool)...")
        result = await agent.run(consolidated_info, cultural_profile)
        
        qloo_intel = result.get("qloo_intelligence", {})
        metadata = qloo_intel.get("metadata", {})
        cultural_recs = qloo_intel.get("cultural_recommendations", {})
        
        logger.info(f"✅ Fallback completed")
        logger.info(f"   Approach: {metadata.get('approach')}")
        logger.info(f"   Heritage: {metadata.get('heritage')}")
        logger.info(f"   Fallback reason: {metadata.get('fallback_reason')}")
        
        # Verify fallback data exists
        has_fallback_artists = "artists" in cultural_recs
        has_fallback_places = "places" in cultural_recs
        
        logger.info(f"   Fallback artists: {has_fallback_artists}")
        logger.info(f"   Fallback places: {has_fallback_places}")
        
        return has_fallback_artists and has_fallback_places
        
    except Exception as e:
        logger.error(f"❌ Fallback test failed: {e}")
        return False

async def test_different_heritages():
    """Test 5: Test different heritage mappings"""
    
    logger.info("\n🧪 Test 5: Different Heritage Mappings")
    logger.info("-" * 50)
    
    try:
        from backend.multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        qloo = QlooInsightsAPI("test_key")
        
        test_heritages = [
            "Italian-American",
            "Irish", 
            "German",
            "Chinese",
            "Mexican",
            "Jewish",
            "Polish"
        ]
        
        for heritage in test_heritages:
            music_tag = qloo._get_heritage_music_tag(heritage)
            cuisine_tag = qloo._get_heritage_cuisine_tag(heritage)
            
            logger.info(f"   {heritage}:")
            logger.info(f"     Music → {music_tag}")
            logger.info(f"     Cuisine → {cuisine_tag}")
        
        logger.info("✅ Heritage mapping test completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Heritage mapping test failed: {e}")
        return False

async def main():
    """Run all integration tests"""
    
    logger.info("🚀 Quick Step 3 Integration Test")
    logger.info("=" * 60)
    
    tests = [
        ("Qloo Tools Methods", test_qloo_tools_methods),
        ("API Calls", test_qloo_api_calls),
        ("Cultural Analysis Agent", test_cultural_analysis_agent),
        ("Fallback Scenarios", test_fallback_scenarios),
        ("Heritage Mappings", test_different_heritages)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("🎯 INTEGRATION TEST RESULTS")
    logger.info("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("✅ Step 3 is ready to go!")
        logger.info("🚀 Ready for Step 4: Gemini Content Curation")
    else:
        logger.warning(f"⚠️ {total - passed} tests failed")
        logger.warning("🔧 Check failed components before proceeding")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)