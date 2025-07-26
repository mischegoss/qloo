"""
Simple Debug Test - Step by Step
File: backend/tests/simple_debug_test.py

Minimal test to debug exactly where things are failing.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any

# Set up path
backend_dir = Path(__file__).parent.parent
project_root = backend_dir.parent  # Go up one more level to find .env
sys.path.insert(0, str(backend_dir))
os.chdir(backend_dir)

print("🚀 Simple Debug Test - With .env Loading")
print("=" * 50)

# Step 0: Load .env file
print("\n📋 Step 0: Loading .env file...")
try:
    # Try to load python-dotenv
    try:
        from dotenv import load_dotenv
        print("   ✅ python-dotenv available")
    except ImportError:
        print("   ⚠️ python-dotenv not installed, trying manual .env loading")
        load_dotenv = None
    
    # Look for .env file in project root
    env_file = project_root / ".env"
    print(f"   📁 Looking for .env in: {env_file}")
    
    if env_file.exists():
        print("   ✅ .env file found")
        
        if load_dotenv:
            # Use python-dotenv if available
            load_dotenv(env_file)
            print("   ✅ .env loaded with python-dotenv")
        else:
            # Manual .env loading
            print("   🔧 Loading .env manually...")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip().strip('"').strip("'")
                        os.environ[key.strip()] = value
                        print(f"   📝 Loaded: {key.strip()}")
            print("   ✅ .env loaded manually")
    else:
        print(f"   ❌ .env file not found at: {env_file}")
        print("   💡 Make sure .env file exists in project root")
    
    # Check if API keys are now available
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    print(f"   🔑 YouTube API key after loading: {'✅ Found' if youtube_key else '❌ Missing'}")
    print(f"   🔑 Gemini API key after loading: {'✅ Found' if gemini_key else '❌ Missing'}")
    
    if youtube_key:
        print(f"   📏 YouTube key length: {len(youtube_key)} chars")
    if gemini_key:
        print(f"   📏 Gemini key length: {len(gemini_key)} chars")
    
    print("   ✅ Step 0 complete")
    
except Exception as e:
    print(f"   ❌ .env loading failed: {e}")
    print("   💡 Continuing without .env file...")
    import traceback
    traceback.print_exc()

# Step 1: Test basic imports
print("\n📦 Step 1: Testing basic imports...")
try:
    print("   Importing logging...")
    import logging
    print("   ✅ logging imported")
    
    print("   Importing asyncio...")
    import asyncio
    print("   ✅ asyncio imported")
    
    print("   ✅ Step 1 complete")
except Exception as e:
    print(f"   ❌ Step 1 failed: {e}")
    sys.exit(1)

# Step 2: Test MusicCurationAgent import
print("\n📦 Step 2: Testing MusicCurationAgent import...")
try:
    print("   Importing MusicCurationAgent...")
    from multi_tool_agent.agents.music_curation_agent import MusicCurationAgent
    print("   ✅ MusicCurationAgent imported successfully")
    print("   ✅ Step 2 complete")
except Exception as e:
    print(f"   ❌ Step 2 failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test tool imports
print("\n📦 Step 3: Testing tool imports...")
try:
    print("   Importing YouTubeAPI...")
    from multi_tool_agent.tools.youtube_tools import YouTubeAPI
    print("   ✅ YouTubeAPI imported")
    
    print("   Importing SimpleGeminiTool...")
    from multi_tool_agent.tools.simple_gemini_tools import SimpleGeminiTool
    print("   ✅ SimpleGeminiTool imported")
    
    print("   ✅ Step 3 complete")
except Exception as e:
    print(f"   ❌ Step 3 failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test agent creation
print("\n🔧 Step 4: Testing agent creation...")
try:
    print("   Creating agent without tools...")
    agent = MusicCurationAgent()
    print("   ✅ Agent created successfully")
    
    print(f"   📊 Agent has {len(agent.classical_database)} composers")
    print("   ✅ Step 4 complete")
except Exception as e:
    print(f"   ❌ Step 4 failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Test tool creation with REAL API keys
print("\n🔧 Step 5: Testing tool creation with REAL API keys...")

# Get real API keys from environment
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

print(f"   📋 YouTube API key: {'✅ Found' if youtube_api_key else '❌ Missing'}")
print(f"   📋 Gemini API key: {'✅ Found' if gemini_api_key else '❌ Missing'}")

youtube_tool = None
gemini_tool = None

if youtube_api_key:
    try:
        print("   Creating YouTube tool with REAL API key...")
        youtube_tool = YouTubeAPI(youtube_api_key)
        print("   ✅ YouTube tool created with real key")
    except Exception as e:
        print(f"   ❌ YouTube tool creation failed: {e}")
else:
    print("   ⚠️ Skipping YouTube tool (no API key)")

if gemini_api_key:
    try:
        print("   Creating Gemini tool with REAL API key...")
        gemini_tool = SimpleGeminiTool(gemini_api_key)
        print("   ✅ Gemini tool created with real key")
    except Exception as e:
        print(f"   ❌ Gemini tool creation failed: {e}")
else:
    print("   ⚠️ Skipping Gemini tool (no API key)")

if youtube_tool or gemini_tool:
    print("   ✅ Step 5 complete - some tools available")
else:
    print("   ⚠️ Step 5 complete - no real API keys available (will test fallback mode)")

# Step 5b: Test actual API connections
print("\n🌐 Step 5b: Testing real API connections...")

if youtube_tool:
    try:
        print("   Testing YouTube API connection...")
        youtube_connection = asyncio.run(youtube_tool.test_connection())
        print(f"   📺 YouTube connection: {'✅ Working' if youtube_connection else '❌ Failed'}")
    except Exception as e:
        print(f"   ❌ YouTube connection test failed: {e}")

if gemini_tool:
    try:
        print("   Testing Gemini API connection...")
        gemini_connection = asyncio.run(gemini_tool.test_connection())
        print(f"   🤖 Gemini connection: {'✅ Working' if gemini_connection else '❌ Failed'}")
    except Exception as e:
        print(f"   ❌ Gemini connection test failed: {e}")

print("   ✅ Step 5b complete")

# Step 6: Test agent with tools
print("\n🔧 Step 6: Testing agent with real tools...")
try:
    print("   Creating agent with real tools...")
    agent_with_tools = MusicCurationAgent(youtube_tool=youtube_tool, gemini_tool=gemini_tool)
    print("   ✅ Agent with real tools created")
    
    # Check if tools are actually attached
    has_youtube = agent_with_tools.youtube_tool is not None
    has_gemini = agent_with_tools.gemini_tool is not None
    
    print(f"   📊 YouTube tool attached: {has_youtube}")
    print(f"   📊 Gemini tool attached: {has_gemini}")
    
    # Test what happens with real vs no tools
    if has_youtube or has_gemini:
        print("   🎯 Agent will use REAL APIs!")
    else:
        print("   🎯 Agent will use fallback mode")
    
    print("   ✅ Step 6 complete")
except Exception as e:
    print(f"   ❌ Step 6 failed: {e}")
    import traceback
    traceback.print_exc()

# Step 7: Test agent runs with comparison
print("\n🚀 Step 7: Testing agent runs (fallback vs real APIs)...")

def create_test_profile() -> Dict[str, Any]:
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

async def test_agent_runs():
    try:
        profile = create_test_profile()
        
        # Test 1: Fallback mode (no tools)
        print("\n   🔧 Test 7a: Fallback mode (no tools)...")
        agent_fallback = MusicCurationAgent()
        result_fallback = await agent_fallback.run(profile)
        
        if "music_content" in result_fallback:
            music = result_fallback["music_content"]
            method = result_fallback["metadata"].get("selection_method", "unknown")
            print(f"   🎵 Fallback result: {music.get('artist')} - {music.get('piece_title')}")
            print(f"   🔧 Fallback method: {method}")
            print(f"   📺 Fallback YouTube: {music.get('youtube_url', 'No URL')[:50]}...")
        
        # Test 2: With real tools (if available)
        if youtube_tool or gemini_tool:
            print("\n   🔧 Test 7b: With REAL APIs...")
            result_real = await agent_with_tools.run(profile)
            
            if "music_content" in result_real:
                music = result_real["music_content"]
                method = result_real["metadata"].get("selection_method", "unknown")
                print(f"   🎵 Real API result: {music.get('artist')} - {music.get('piece_title')}")
                print(f"   🔧 Real API method: {method}")
                
                # Check if we got real YouTube results
                youtube_url = music.get('youtube_url')
                if youtube_url and youtube_url != result_fallback['music_content'].get('youtube_url'):
                    print(f"   📺 ✅ Real YouTube URL: {youtube_url[:50]}...")
                    print("   🎉 YouTube API is working!")
                else:
                    print("   📺 ⚠️ YouTube API may not be working (same as fallback)")
                
                # Check if Gemini was used
                if method == "gemini_powered":
                    print("   🤖 ✅ Gemini API is working!")
                else:
                    print("   🤖 ⚠️ Gemini API not used (using fallback)")
                
                # Compare results
                if method != result_fallback["metadata"].get("selection_method"):
                    print("   ✅ Real APIs produce different results than fallback!")
                else:
                    print("   ⚠️ Real APIs and fallback produced same results")
        else:
            print("\n   ⚠️ Test 7b: Skipped (no real API keys)")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Agent run failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the async test
try:
    print("   Starting async agent tests...")
    success = asyncio.run(test_agent_runs())
    
    if success:
        print("   ✅ Step 7 complete")
    else:
        print("   ❌ Step 7 failed")
        
except Exception as e:
    print(f"   ❌ Step 7 crashed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🎯 REAL API DEBUG TEST COMPLETE")
print("=" * 50)

if youtube_api_key and gemini_api_key:
    print("🔑 Both API keys found - tested real functionality")
    print("🎉 If you see '✅ YouTube API is working!' and '✅ Gemini API is working!' above,")
    print("    then Agent 4A is fully functional with real APIs!")
elif youtube_api_key or gemini_api_key:
    print("🔑 Some API keys found - partial real testing")
    print("💡 Add missing API keys to test full functionality")
else:
    print("🔑 No API keys found - tested fallback mode only")
    print("💡 To test with real APIs, set environment variables:")
    print("    export YOUTUBE_API_KEY='your_youtube_key'")
    print("    export GEMINI_API_KEY='your_gemini_key'")

print("\n🚀 Next Steps:")
print("1. If all tests passed → Agent 4A is working!")
print("2. If real APIs work → Ready for Agent 4B (Recipe Selection)")
print("3. If only fallbacks work → Need to debug API integration")