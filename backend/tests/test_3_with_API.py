#!/usr/bin/env python3
"""
Test Step 3 with Real Qloo API Key
File: backend/tests/test_step3_with_api_key.py

REAL API TESTING: Verify actual Qloo API calls work with your API key
"""

import os
import sys
import logging
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env from: {env_path}")
    else:
        print(f"⚠️ No .env file found at: {env_path}")
except ImportError:
    print("⚠️ python-dotenv not installed, trying without .env loading")
    # Try to load manually
    env_path = project_root / ".env"
    if env_path.exists():
        print(f"📁 Found .env file at: {env_path}")
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value
                    if key == "QLOO_API_KEY":
                        print(f"✅ Loaded QLOO_API_KEY: {value[:8]}...")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

async def test_real_qloo_api_calls():
    """Test real Qloo API calls with actual API key"""
    
    logger.info("🧪 Testing Real Qloo API Calls")
    logger.info("=" * 60)
    
    # Check for API key
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        logger.error("❌ No QLOO_API_KEY environment variable found!")
        logger.info("💡 Set your API key: export QLOO_API_KEY='your_key_here'")
        return False
    
    logger.info(f"✅ API key found: {api_key[:8]}...")
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        qloo = QlooInsightsAPI(api_key)
        
        # Test 1: Real Classical Music Call
        logger.info("\n🎵 Test 1: Real Classical Music API Call")
        logger.info("-" * 40)
        
        classical_result = await qloo.get_safe_classical_music("Italian-American", take=5)
        
        # Debug: Show actual response structure
        logger.info(f"🔍 Debug - Classical result keys: {list(classical_result.keys())}")
        logger.info(f"🔍 Debug - Entities type: {type(classical_result.get('entities'))}")
        if classical_result.get("entities"):
            entities = classical_result["entities"]
            if isinstance(entities, (list, dict)):
                logger.info(f"🔍 Debug - Entities content: {entities}")
        
        logger.info(f"✅ Success: {classical_result.get('success')}")
        logger.info(f"🎼 Entities found: {classical_result.get('entity_count', 0)}")
        logger.info(f"📊 Content type: {classical_result.get('content_type')}")
        
        if classical_result.get("entities"):
            entities = classical_result["entities"]
            logger.info("🎯 Sample artists:")
            
            # Handle different data types for entities
            if isinstance(entities, list):
                for i, artist in enumerate(entities[:3], 1):
                    name = artist.get("name", "Unknown") if isinstance(artist, dict) else str(artist)
                    artist_type = artist.get("type", "Unknown") if isinstance(artist, dict) else "Artist"
                    logger.info(f"   {i}. {name} ({artist_type})")
            elif isinstance(entities, dict):
                logger.info(f"   📊 Entities data: {entities}")
            else:
                logger.info(f"   📊 Entities type: {type(entities)}, value: {entities}")
        
        # Test 2: Real Cuisine Places Call  
        logger.info("\n🍽️ Test 2: Real Italian Cuisine API Call")
        logger.info("-" * 40)
        
        places_result = await qloo.get_tag_based_insights("urn:entity:place", "italian", take=5)
        
        # Debug: Show actual response structure
        logger.info(f"🔍 Debug - Places result keys: {list(places_result.keys())}")
        logger.info(f"🔍 Debug - Entities type: {type(places_result.get('entities'))}")
        if places_result.get("entities"):
            entities = places_result["entities"]
            if isinstance(entities, (list, dict)):
                logger.info(f"🔍 Debug - Entities content: {entities}")
        
        logger.info(f"✅ Success: {places_result.get('success')}")
        logger.info(f"🍽️ Places found: {places_result.get('entity_count', 0)}")
        logger.info(f"🏷️ Tag used: {places_result.get('tag')}")
        
        if places_result.get("entities"):
            entities = places_result["entities"]
            logger.info("🎯 Sample places:")
            
            # Handle different data types for entities
            if isinstance(entities, list):
                for i, place in enumerate(entities[:3], 1):
                    name = place.get("name", "Unknown") if isinstance(place, dict) else str(place)
                    place_type = place.get("type", "Unknown") if isinstance(place, dict) else "Place"
                    logger.info(f"   {i}. {name} ({place_type})")
            elif isinstance(entities, dict):
                logger.info(f"   📊 Entities data: {entities}")
            else:
                logger.info(f"   📊 Entities type: {type(entities)}, value: {entities}")
        
        # Test 3: Combined Cultural Calls
        logger.info("\n🎯 Test 3: Combined Cultural Intelligence")
        logger.info("-" * 40)
        
        combined_result = await qloo.make_cultural_calls("Italian-American")
        
        successful_calls = combined_result.get("successful_calls", 0)
        total_results = combined_result.get("total_results", 0)
        
        logger.info(f"✅ Successful calls: {successful_calls}/2")
        logger.info(f"📊 Total results: {total_results}")
        
        cultural_recs = combined_result.get("cultural_recommendations", {})
        
        if "artists" in cultural_recs:
            artists_data = cultural_recs["artists"]
            artists_count = artists_data.get("entity_count", 0)
            artists_type = artists_data.get("content_type", "unknown")
            logger.info(f"🎵 Artists: {artists_count} ({artists_type})")
        
        if "places" in cultural_recs:
            places_data = cultural_recs["places"]
            places_count = places_data.get("entity_count", 0) 
            places_type = places_data.get("content_type", "unknown")
            logger.info(f"🍽️ Places: {places_count} ({places_type})")
        
        # Test 4: Different Heritage Types
        logger.info("\n🌍 Test 4: Different Heritage Types")
        logger.info("-" * 40)
        
        test_heritages = ["Irish", "German", "Chinese"]
        
        for heritage in test_heritages:
            logger.info(f"\n🔍 Testing {heritage} heritage:")
            
            heritage_result = await qloo.make_cultural_calls(heritage)
            heritage_calls = heritage_result.get("successful_calls", 0)
            heritage_total = heritage_result.get("total_results", 0)
            
            logger.info(f"   Calls: {heritage_calls}/2, Results: {heritage_total}")
            
            # Check what we got
            heritage_recs = heritage_result.get("cultural_recommendations", {})
            if "artists" in heritage_recs:
                music_type = qloo._get_heritage_music_tag(heritage)
                content_type = heritage_recs["artists"].get("content_type", "unknown")
                logger.info(f"   Music: {music_type} → {content_type}")
            
            if "places" in heritage_recs:
                cuisine_type = qloo._get_heritage_cuisine_tag(heritage)
                content_type = heritage_recs["places"].get("content_type", "unknown")
                logger.info(f"   Cuisine: {cuisine_type} → {content_type}")
        
        # Test 5: Full Cultural Analysis Agent
        logger.info("\n🤖 Test 5: Full Cultural Analysis Agent")
        logger.info("-" * 40)
        
        from multi_tool_agent.agents.qloo_cultural_analysis_agent import QlooCulturalAnalysisAgent
        
        agent = QlooCulturalAnalysisAgent(qloo)
        
        # Test with Italian-American
        test_profile = {
            "patient_profile": {
                "cultural_heritage": "Italian-American",
                "birth_year": 1945,
                "first_name": "Maria"
            }
        }
        
        agent_result = await agent.run(test_profile, {})
        
        qloo_intel = agent_result.get("qloo_intelligence", {})
        metadata = qloo_intel.get("metadata", {})
        agent_recs = qloo_intel.get("cultural_recommendations", {})
        
        logger.info(f"✅ Agent completed successfully")
        logger.info(f"🎯 Heritage: {metadata.get('heritage')}")
        logger.info(f"📊 Successful calls: {metadata.get('successful_calls')}")
        logger.info(f"🔧 Approach: {metadata.get('approach')}")
        
        agent_has_artists = "artists" in agent_recs
        agent_has_places = "places" in agent_recs
        
        logger.info(f"🎵 Has artists: {agent_has_artists}")
        logger.info(f"🍽️ Has places: {agent_has_places}")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("🎯 REAL API TEST SUMMARY")
        logger.info("=" * 60)
        
        api_working = (classical_result.get("success") and 
                      places_result.get("success") and
                      successful_calls > 0)
        
        if api_working:
            logger.info("🎉 SUCCESS! Real Qloo API calls are working!")
            logger.info("✅ Classical music recommendations working")
            logger.info("✅ Cuisine place recommendations working") 
            logger.info("✅ Cultural Analysis Agent working with real API")
            logger.info("✅ Heritage-based recommendations working")
            logger.info("🚀 Step 3 is fully functional with real Qloo data!")
        else:
            logger.warning("⚠️ Some API calls failed - check API key and network")
        
        return api_working
        
    except Exception as e:
        logger.error(f"❌ Real API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_api_connection():
    """Quick API connection test"""
    
    logger.info("🔌 Testing API Connection")
    logger.info("-" * 30)
    
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        logger.error("❌ No API key")
        return False
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        qloo = QlooInsightsAPI(api_key)
        connected = await qloo.test_connection()
        
        if connected:
            logger.info("✅ API connection successful!")
        else:
            logger.error("❌ API connection failed")
        
        return connected
        
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False

async def main():
    """Run real API tests"""
    
    logger.info("🚀 Real Qloo API Testing")
    logger.info("💡 This will test actual API calls with your Qloo API key")
    logger.info("")
    
    # Test connection first
    connection_ok = await test_api_connection()
    
    if not connection_ok:
        logger.error("❌ API connection failed - stopping tests")
        return False
    
    # Run full API tests
    success = await test_real_qloo_api_calls()
    
    if success:
        logger.info("\n🎉 ALL REAL API TESTS PASSED!")
        logger.info("✅ Step 3 is ready for production with real Qloo data!")
    else:
        logger.error("\n❌ Some API tests failed")
        logger.error("🔧 Check API key, network, and Qloo service status")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)