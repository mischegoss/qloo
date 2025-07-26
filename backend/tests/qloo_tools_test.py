"""
Qloo Tools Integration Test & Diagnostic
File: backend/tests/test_qloo_tools_integration.py

Tests the actual Qloo Tools integration and diagnoses API response issues.
Helps identify exactly what methods exist and what response formats are returned.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Setup paths
current_dir = Path(__file__).parent.absolute()
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_qloo_tool_methods():
    """Test what methods are actually available in QlooInsightsAPI"""
    
    logger.info("🔍 Testing Qloo Tool Methods Availability")
    logger.info("=" * 60)
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        # Get API key
        api_key = os.getenv("QLOO_API_KEY")
        if not api_key:
            logger.error("❌ No QLOO_API_KEY found in environment")
            return False
        
        # Initialize tool
        qloo = QlooInsightsAPI(api_key)
        
        # Test what methods exist
        methods_to_test = [
            "get_safe_classical_music",
            "get_tag_based_insights", 
            "location_only_insights",
            "simple_tag_insights",
            "get_insights",
            "test_connection"
        ]
        
        available_methods = []
        missing_methods = []
        
        for method_name in methods_to_test:
            if hasattr(qloo, method_name):
                available_methods.append(method_name)
                logger.info(f"✅ Method available: {method_name}")
            else:
                missing_methods.append(method_name)
                logger.info(f"❌ Method missing: {method_name}")
        
        logger.info(f"\n📊 Method Availability: {len(available_methods)}/{len(methods_to_test)}")
        
        return len(available_methods) > 0
        
    except ImportError as e:
        logger.error(f"❌ Failed to import QlooInsightsAPI: {e}")
        return False

async def test_qloo_classical_music_call():
    """Test the classical music API call and response format"""
    
    logger.info("🎵 Testing Classical Music API Call")
    logger.info("-" * 40)
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        api_key = os.getenv("QLOO_API_KEY")
        qloo = QlooInsightsAPI(api_key)
        
        # Test classical music call
        result = await qloo.get_safe_classical_music(
            cultural_heritage="universal",
            age_group="55_and_older", 
            take=3
        )
        
        logger.info(f"🔍 Response type: {type(result)}")
        logger.info(f"🔍 Response value: {result}")
        
        if isinstance(result, dict):
            logger.info("✅ Response is dict (expected)")
            
            # Check expected keys
            expected_keys = ["success", "entities", "results"]
            found_keys = [key for key in expected_keys if key in result]
            logger.info(f"📋 Found keys: {found_keys}")
            
            if "entities" in result:
                entities = result["entities"]
                logger.info(f"🎯 Entities count: {len(entities) if entities else 0}")
                if entities:
                    logger.info(f"🎯 Sample entity: {entities[0] if len(entities) > 0 else 'None'}")
            
            if "results" in result:
                results = result["results"]
                logger.info(f"🎯 Results count: {len(results) if results else 0}")
                if results:
                    logger.info(f"🎯 Sample result: {results[0] if len(results) > 0 else 'None'}")
        
        elif isinstance(result, str):
            logger.warning("⚠️ Response is string (unexpected)")
            logger.info(f"📝 String content: {result[:200]}...")
        
        else:
            logger.error(f"❌ Unexpected response type: {type(result)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Classical music test failed: {e}")
        return False

async def test_step3_with_real_qloo():
    """Test Step 3 agent with real Qloo tool"""
    
    logger.info("🚀 Testing Step 3 Agent with Real Qloo Tool")
    logger.info("-" * 40)
    
    try:
        from multi_tool_agent.agents.qloo_cultural_analysis_agent import QlooCulturalAnalysisAgent
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        api_key = os.getenv("QLOO_API_KEY")
        qloo = QlooInsightsAPI(api_key)
        agent = QlooCulturalAnalysisAgent(qloo)
        
        # Create test profile
        test_profile = {
            "patient_info": {
                "first_name": "Maria",
                "birth_year": 1945,
                "cultural_heritage": "Italian-American",
                "demo_dislikes": []
            },
            "theme_info": {
                "name": "Birthday",
                "photo_filename": "birthday.png"
            },
            "photo_analysis": {
                "success": True,
                "analysis_method": "pre_analyzed"
            },
            "pipeline_state": {
                "current_step": 2,
                "ready_for_step3": True
            }
        }
        
        # Run Step 3
        logger.info("🔄 Running Step 3 agent...")
        result = await agent.run(test_profile)
        
        # Analyze result
        if "cultural_intelligence" in result:
            cultural_intel = result["cultural_intelligence"]
            metadata = cultural_intel.get("metadata", {})
            
            logger.info("✅ Step 3 completed successfully")
            logger.info(f"📊 Successful calls: {metadata.get('successful_calls', 0)}")
            logger.info(f"📊 Total results: {metadata.get('total_results', 0)}")
            logger.info(f"📊 Qloo tool available: {metadata.get('qloo_tool_available', False)}")
            logger.info(f"📊 Fallback method: {metadata.get('fallback_method', 'unknown')}")
            
            # Check recommendations
            recommendations = cultural_intel.get("cultural_recommendations", {})
            
            artists = recommendations.get("artists", {})
            logger.info(f"🎵 Artists: {artists.get('entity_count', 0)} ({artists.get('method', 'unknown')})")
            
            places = recommendations.get("places", {})
            logger.info(f"🍽️ Places: {places.get('entity_count', 0)} ({places.get('method', 'unknown')})")
            
            return True
        else:
            logger.error("❌ No cultural intelligence in result")
            return False
            
    except Exception as e:
        logger.error(f"❌ Step 3 test failed: {e}")
        return False

async def diagnose_api_issues():
    """Diagnose specific API integration issues"""
    
    logger.info("🔬 Diagnosing API Integration Issues")
    logger.info("-" * 40)
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        api_key = os.getenv("QLOO_API_KEY")
        qloo = QlooInsightsAPI(api_key)
        
        # Test 1: Check method existence
        logger.info("🧪 Test 1: Method Existence")
        missing_methods = []
        
        if not hasattr(qloo, 'get_tag_based_insights'):
            missing_methods.append('get_tag_based_insights')
            logger.warning("⚠️ Missing: get_tag_based_insights")
        else:
            logger.info("✅ Found: get_tag_based_insights")
        
        if not hasattr(qloo, 'get_safe_classical_music'):
            missing_methods.append('get_safe_classical_music')
            logger.warning("⚠️ Missing: get_safe_classical_music")
        else:
            logger.info("✅ Found: get_safe_classical_music")
        
        # Test 2: Response format analysis
        logger.info("\n🧪 Test 2: Response Format Analysis")
        
        # Try a minimal call to see response format
        try:
            minimal_result = await qloo.get_safe_classical_music("universal", take=1)
            logger.info(f"📊 Minimal call response type: {type(minimal_result)}")
            
            if isinstance(minimal_result, dict):
                keys = list(minimal_result.keys())
                logger.info(f"📊 Response keys: {keys}")
            
        except Exception as e:
            logger.error(f"❌ Minimal call failed: {e}")
        
        # Test 3: Check for alternative methods
        logger.info("\n🧪 Test 3: Alternative Methods")
        all_methods = [method for method in dir(qloo) if not method.startswith('_')]
        logger.info(f"📋 All available methods: {all_methods}")
        
        return len(missing_methods) == 0
        
    except Exception as e:
        logger.error(f"❌ Diagnosis failed: {e}")
        return False

async def main():
    """Main diagnostic function"""
    
    logger.info("🚀 Qloo Tools Integration Diagnostic")
    logger.info("=" * 80)
    
    # Check environment
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        logger.error("❌ QLOO_API_KEY not found in environment")
        logger.info("💡 Set QLOO_API_KEY before running this test")
        return False
    
    logger.info(f"✅ API key found: {api_key[:8]}...")
    
    # Run tests
    tests = [
        ("Method Availability", test_qloo_tool_methods),
        ("Classical Music Call", test_qloo_classical_music_call),
        ("API Issues Diagnosis", diagnose_api_issues),
        ("Step 3 Integration", test_step3_with_real_qloo)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = await test_func()
            results.append(result)
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{status} {test_name}")
        except Exception as e:
            logger.error(f"❌ FAILED {test_name}: {e}")
            results.append(False)
    
    # Summary
    logger.info("=" * 80)
    passed = sum(results)
    total = len(results)
    
    logger.info(f"🎯 DIAGNOSTIC RESULTS: {passed}/{total} tests passed")
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        logger.info(f"   {test_name}: {status}")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED - Qloo integration working!")
    else:
        logger.warning("⚠️ Some tests failed - check specific issues above")
        
        # Provide recommendations
        logger.info("\n💡 RECOMMENDATIONS:")
        if not results[0]:  # Method availability
            logger.info("   - Update QlooInsightsAPI to include missing methods")
        if not results[1]:  # Classical music call
            logger.info("   - Fix response parsing in get_safe_classical_music")
        if not results[2]:  # API issues
            logger.info("   - Check Qloo API response format compatibility")
        if not results[3]:  # Step 3 integration
            logger.info("   - Update Step 3 agent to handle current API responses")
    
    return passed == total

if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.info("💡 python-dotenv not available, using existing environment")
    
    # Run diagnostic
    success = asyncio.run(main())
    exit(0 if success else 1)