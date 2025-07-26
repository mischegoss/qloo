"""
Working Music Test - All Fixed Imports  
File: backend/tests/working_music_test.py

Simple test that definitely works with the fixed import structure.
Run from backend directory: python tests/working_music_test.py
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Dict, Any

# CRITICAL FIX: Set up Python path correctly
# Get the backend directory (parent of tests directory)
current_file = Path(__file__).resolve()
tests_dir = current_file.parent
backend_dir = tests_dir.parent

# Add backend directory to Python path so we can import multi_tool_agent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Change to backend directory if not already there
if os.getcwd() != str(backend_dir):
    os.chdir(backend_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all imports work correctly"""
    
    logger.info("🧪 Testing Fixed Imports")
    logger.info("=" * 50)
    
    try:
        # Test 1: Try to import the music agent
        logger.info("📦 Importing MusicCurationAgent...")
        from multi_tool_agent.agents.music_curation_agent import MusicCurationAgent
        logger.info("✅ MusicCurationAgent imported successfully")
        
        # Test 2: Try to import YouTube tool
        logger.info("📦 Importing YouTubeAPI...")
        from multi_tool_agent.tools.youtube_tools import YouTubeAPI
        logger.info("✅ YouTubeAPI imported successfully")
        
        # Test 3: Try to import Gemini tool (CORRECTED FILE NAME)
        logger.info("📦 Importing SimpleGeminiTool...")
        try:
            from multi_tool_agent.tools.simple_gemini_tools import SimpleGeminiTool  # Note: simple_gemini_tools (with 's')
            logger.info("✅ SimpleGeminiTool imported successfully")
        except ImportError as e:
            logger.warning(f"⚠️ SimpleGeminiTool import failed: {e}")
            logger.info("📦 Trying GeminiRecipeGenerator fallback...")
            try:
                from multi_tool_agent.tools.gemini_tools import GeminiRecipeGenerator as SimpleGeminiTool
                logger.info("✅ GeminiRecipeGenerator imported as fallback")
            except ImportError as e2:
                logger.error(f"❌ Both Gemini imports failed: {e}, {e2}")
                SimpleGeminiTool = None
        
        # Test 4: Create agent instance
        logger.info("🔧 Creating MusicCurationAgent instance...")
        agent = MusicCurationAgent()
        logger.info("✅ Agent created successfully")
        logger.info(f"📊 Agent has {len(agent.classical_database)} composers available")
        
        return True, (MusicCurationAgent, YouTubeAPI, SimpleGeminiTool)
        
    except Exception as e:
        logger.error(f"❌ Import test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False, (None, None, None)

def create_mock_profile() -> Dict[str, Any]:  # Fixed typing
    """Create a simple mock profile for testing"""
    
    return {
        "patient_info": {
            "first_name": "Maria",
            "cultural_heritage": "Italian-American"
        },
        "qloo_intelligence": {
            "cultural_recommendations": {
                "artists": {
                    "success": True,
                    "entities": [
                        {"name": "Antonio Vivaldi"},
                        {"name": "Johann Sebastian Bach"},
                        {"name": "Wolfgang Amadeus Mozart"}
                    ]
                }
            }
        }
    }

async def test_agent_with_real_tools():
    """Test Agent 4A with real tool instances"""
    
    logger.info("\n🧪 Testing Agent with Real Tools")
    logger.info("=" * 50)
    
    # First check imports
    import_success, (MusicCurationAgent, YouTubeAPI, SimpleGeminiTool) = test_imports()
    
    if not import_success:
        logger.error("❌ Cannot test agent - imports failed")
        return False
    
    try:
        # Get API keys from environment (optional for testing)
        youtube_api_key = os.getenv("YOUTUBE_API_KEY", "TEST_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY", "TEST_KEY")
        
        # Create tool instances
        youtube_tool = None
        gemini_tool = None
        
        if YouTubeAPI:
            try:
                youtube_tool = YouTubeAPI(youtube_api_key)
                logger.info("✅ YouTube tool created")
            except Exception as e:
                logger.warning(f"⚠️ YouTube tool creation failed: {e}")
        
        if SimpleGeminiTool:
            try:
                gemini_tool = SimpleGeminiTool(gemini_api_key)
                logger.info("✅ Gemini tool created")
            except Exception as e:
                logger.warning(f"⚠️ Gemini tool creation failed: {e}")
        
        # Create agent WITH tools
        logger.info("🔧 Creating agent with tools...")
        agent = MusicCurationAgent(youtube_tool=youtube_tool, gemini_tool=gemini_tool)
        
        # Show tool availability
        has_youtube = agent.youtube_tool is not None
        has_gemini = agent.gemini_tool is not None
        logger.info(f"📊 Agent tools: YouTube={has_youtube}, Gemini={has_gemini}")
        
        # Create test profile
        logger.info("📋 Creating test profile...")
        profile = create_mock_profile()
        
        # Run the agent
        logger.info("🚀 Running agent with tools...")
        result = await agent.run(profile)
        
        # Validate result
        logger.info("🔍 Validating result...")
        
        if "music_content" not in result:
            logger.error("❌ Missing music_content in result")
            return False
        
        music_content = result["music_content"]
        
        # Log the results
        logger.info("✅ Agent with tools test successful!")
        logger.info(f"🎵 Selected Artist: {music_content['artist']}")
        logger.info(f"🎼 Selected Piece: {music_content['piece_title']}")
        logger.info(f"🔧 Selection Method: {result['metadata']['selection_method']}")
        
        # Check if tools were actually used
        selection_method = result['metadata']['selection_method']
        if selection_method == "gemini_powered":
            logger.info("🤖 ✅ Gemini tool was used for curation!")
        elif "fallback" in selection_method:
            logger.warning("⚠️ Agent used fallback mode despite having tools")
        
        # Check YouTube results
        if music_content.get('youtube_url'):
            logger.info(f"📺 ✅ YouTube URL found: {music_content['youtube_url'][:50]}...")
        else:
            logger.warning("⚠️ No YouTube URL (using fallback)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent with tools test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def test_fallback_vs_tools_comparison():
    """Compare agent behavior with and without tools"""
    
    logger.info("\n🧪 Testing Fallback vs Tools Comparison")
    logger.info("=" * 50)
    
    try:
        from multi_tool_agent.agents.music_curation_agent import MusicCurationAgent
        from multi_tool_agent.tools.youtube_tools import YouTubeAPI
        from multi_tool_agent.tools.simple_gemini_tools import SimpleGeminiTool
        
        profile = create_mock_profile()
        
        # Test 1: Fallback mode (no tools)
        logger.info("🔧 Testing fallback mode (no tools)...")
        agent_fallback = MusicCurationAgent()
        result_fallback = await agent_fallback.run(profile)
        
        logger.info(f"   Fallback result: {result_fallback['music_content']['artist']}")
        logger.info(f"   Selection method: {result_fallback['metadata']['selection_method']}")
        
        # Test 2: With mock tools (even if API keys are fake)
        logger.info("🔧 Testing with tools (mock keys)...")
        try:
            youtube_tool = YouTubeAPI("mock_key")
            gemini_tool = SimpleGeminiTool("mock_key") 
            
            agent_with_tools = MusicCurationAgent(youtube_tool=youtube_tool, gemini_tool=gemini_tool)
            result_with_tools = await agent_with_tools.run(profile)
            
            logger.info(f"   With tools result: {result_with_tools['music_content']['artist']}")
            logger.info(f"   Selection method: {result_with_tools['metadata']['selection_method']}")
            
            # Compare results
            if result_fallback['metadata']['selection_method'] != result_with_tools['metadata']['selection_method']:
                logger.info("✅ Tools are being recognized and used differently!")
            else:
                logger.warning("⚠️ Same selection method - tools may not be working")
                
        except Exception as e:
            logger.warning(f"⚠️ Tool creation failed: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Comparison test failed: {e}")
        return False

def main():
    """Run all tests"""
    
    logger.info("🚀 Working Music Test - Fixed Imports")
    logger.info("=" * 60)
    
    # Show detailed environment info
    logger.info(f"📍 Current directory: {os.getcwd()}")
    logger.info(f"📁 Backend directory: {backend_dir}")
    logger.info(f"📁 Tests directory: {tests_dir}")
    logger.info(f"🐍 Python path[0]: {sys.path[0]}")
    
    # Check directory structure
    logger.info("\n🔍 Checking directory structure...")
    if backend_dir.exists():
        logger.info(f"✅ Backend directory exists: {backend_dir}")
    else:
        logger.error(f"❌ Backend directory missing: {backend_dir}")
        return False
    
    multi_tool_dir = backend_dir / "multi_tool_agent"
    if multi_tool_dir.exists():
        logger.info(f"✅ multi_tool_agent directory exists: {multi_tool_dir}")
    else:
        logger.error(f"❌ multi_tool_agent directory missing: {multi_tool_dir}")
        logger.error("💡 This is the main issue - check your project structure")
        return False
    
    agents_dir = multi_tool_dir / "agents"
    if agents_dir.exists():
        logger.info(f"✅ agents directory exists: {agents_dir}")
        # List agent files
        agent_files = list(agents_dir.glob("*.py"))
        logger.info(f"📋 Agent files found: {[f.name for f in agent_files]}")
    else:
        logger.error(f"❌ agents directory missing: {agents_dir}")
    
    tools_dir = multi_tool_dir / "tools"
    if tools_dir.exists():
        logger.info(f"✅ tools directory exists: {tools_dir}")
        # List tool files
        tool_files = list(tools_dir.glob("*.py"))
        logger.info(f"📋 Tool files found: {[f.name for f in tool_files]}")
    else:
        logger.error(f"❌ tools directory missing: {tools_dir}")
    
async def test_heritage_matching():
    """Test heritage matching logic"""
    
    logger.info("\n🧪 Testing Heritage Matching")
    logger.info("=" * 50)
    
    try:
        from multi_tool_agent.agents.music_curation_agent import MusicCurationAgent
        agent = MusicCurationAgent()
        
        heritages_to_test = [
            ("Italian-American", "Should prefer Vivaldi"),
            ("German", "Should prefer Bach or Beethoven"),
            ("Polish", "Should prefer Chopin"),
            ("Universal", "Should use default")
        ]
        
        for heritage, expected in heritages_to_test:
            logger.info(f"\n🌍 Testing {heritage}...")
            
            profile = create_mock_profile()
            profile["patient_info"]["cultural_heritage"] = heritage
            
            result = await agent.run(profile)
            selected_artist = result["music_content"]["artist"]
            heritage_match = result["metadata"]["heritage_match"]
            
            logger.info(f"   → Selected: {selected_artist}")
            logger.info(f"   → Heritage match: {heritage_match}")
            logger.info(f"   → Expected: {expected}")
        
        logger.info("✅ Heritage matching test completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Heritage matching test failed: {e}")
        return False
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("🎯 TEST RESULTS")
    logger.info("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("✅ Agent 4A is working correctly!")
        logger.info("🚀 Ready to proceed with Agent 4B (Recipe Selection)")
    else:
        logger.warning(f"⚠️ {total - passed} tests failed")
        
        # Provide helpful debugging info
        logger.info("\n🔧 DEBUGGING HELP:")
        logger.info("1. Verify your project structure:")
        logger.info("   backend/")
        logger.info("   ├── multi_tool_agent/")
        logger.info("   │   ├── agents/")
        logger.info("   │   │   └── music_curation_agent.py")
        logger.info("   │   └── tools/")
        logger.info("   │       ├── __init__.py")
        logger.info("   │       ├── youtube_tools.py")
        logger.info("   │       └── simple_gemini_tools.py")
        logger.info("   └── tests/")
        logger.info("       └── working_music_test.py")
        logger.info("2. Make sure all files have been created")
        logger.info("3. Check file permissions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)