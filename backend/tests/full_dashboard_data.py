#!/usr/bin/env python3
"""
Comprehensive Test for Agents 4A, 4B, 4C with Real API Testing
File: backend/tests/test_agents_4abc_complete.py

TESTS:
- Agent 4A: Music Curation + YouTube integration (fallback + real APIs)
- Agent 4B: Recipe Selection with theme-first filtering  
- Agent 4C: Photo Description with cultural enhancement (fallback + real Gemini)
- Dashboard output format validation
- Italian demo patient scenario
- Debugging and error reporting

REQUIREMENTS:
- API keys in project_root/.env file:
  YOUTUBE_API_KEY=your_youtube_key
  GEMINI_API_KEY=your_gemini_key
  QLOO_API_KEY=your_qloo_key (optional for this test)
- python-dotenv package: pip install python-dotenv

Run from backend/tests/ directory:
python test_agents_4abc_complete.py
"""

import asyncio
import logging
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configure logging with detailed debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CRITICAL: Set up Python path correctly for imports
# Handle different execution contexts (tests/, backend/, project root)
current_file = Path(__file__).resolve()
tests_dir = current_file.parent
backend_dir = tests_dir.parent
project_root = backend_dir.parent

# Add all possible paths to ensure imports work
paths_to_add = [str(backend_dir), str(project_root), str(project_root / "backend")]
for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

logger.info(f"📁 Test file: {current_file}")
logger.info(f"📁 Backend dir: {backend_dir}")
logger.info(f"📁 Python paths: {sys.path[:3]}...")

# Change to backend directory for consistent file access
if os.getcwd() != str(backend_dir):
    os.chdir(backend_dir)
    logger.info(f"📁 Changed working directory to: {os.getcwd()}")

# Load environment variables from project root/.env
try:
    from dotenv import load_dotenv
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        logger.info(f"✅ Loaded environment variables from {env_file}")
    else:
        logger.warning(f"⚠️ No .env file found at {env_file}")
except ImportError:
    logger.warning("⚠️ python-dotenv not available, environment variables may not load")

# Check for API keys
api_keys = {
    "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    "QLOO_API_KEY": os.getenv("QLOO_API_KEY")
}

logger.info("🔑 API Key Status:")
for key_name, key_value in api_keys.items():
    if key_value:
        logger.info(f"   {key_name}: ✅ Found ({len(key_value)} chars)")
    else:
        logger.info(f"   {key_name}: ❌ Missing")

real_apis_available = any(api_keys.values())

# Import agents with comprehensive error handling
agents_imported = {"4A": False, "4B": False, "4C": False}
import_errors = {}

def safe_import(module_path: str, class_name: str, agent_id: str):
    """Safely import an agent class with detailed error reporting"""
    try:
        # Try multiple import strategies
        import_strategies = [
            lambda: __import__(module_path, fromlist=[class_name]),
            lambda: __import__(f"backend.{module_path}", fromlist=[class_name]),
            lambda: __import__(f"multi_tool_agent.{module_path.split('.')[-2]}.{module_path.split('.')[-1]}", fromlist=[class_name])
        ]
        
        for i, strategy in enumerate(import_strategies):
            try:
                module = strategy()
                agent_class = getattr(module, class_name)
                agents_imported[agent_id] = True
                logger.info(f"✅ Agent {agent_id} imported successfully (strategy {i+1})")
                return agent_class
            except (ImportError, AttributeError) as e:
                continue
        
        # If all strategies fail
        raise ImportError(f"All import strategies failed for {class_name}")
        
    except Exception as e:
        import_errors[agent_id] = str(e)
        logger.error(f"❌ Failed to import Agent {agent_id} ({class_name}): {e}")
        return None

# Import all agents
logger.info("📦 Importing agents...")
MusicCurationAgent = safe_import("multi_tool_agent.agents.music_curation_agent", "MusicCurationAgent", "4A")
RecipeSelectionAgent = safe_import("multi_tool_agent.agents.recipe_selection_agent", "RecipeSelectionAgent", "4B") 
PhotoDescriptionAgent = safe_import("multi_tool_agent.agents.photo_description_agent", "PhotoDescriptionAgent", "4C")

# Import tools for optional testing with real APIs
try:
    from multi_tool_agent.tools.simple_gemini_tools import SimpleGeminiTool
    from multi_tool_agent.tools.youtube_tools import YouTubeAPI
    tools_available = True
    logger.info("✅ Tools imported successfully")
except ImportError as e:
    tools_available = False
    logger.warning(f"⚠️ Tools not available: {e}")

class AgentTestSuite:
    """Comprehensive test suite for Agents 4A, 4B, 4C with real API testing"""
    
    def __init__(self):
        self.results = {}
        self.debug_info = {}
        self.real_apis_available = real_apis_available
        
        # Initialize tools if API keys available
        self.youtube_tool = None
        self.gemini_tool = None
        
        if api_keys["YOUTUBE_API_KEY"]:
            try:
                self.youtube_tool = YouTubeAPI(api_keys["YOUTUBE_API_KEY"])
                logger.info("✅ YouTube tool initialized with real API key")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize YouTube tool: {e}")
        
        if api_keys["GEMINI_API_KEY"]:
            try:
                self.gemini_tool = SimpleGeminiTool(api_keys["GEMINI_API_KEY"])
                logger.info("✅ Gemini tool initialized with real API key")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Gemini tool: {e}")
        
        # Demo patient data - Italian for hackathon demo
        self.demo_profile = {
            "patient_info": {
                "first_name": "Maria",
                "cultural_heritage": "Italian-American", 
                "birth_year": 1945,
                "current_age": 79,
                "city": "Brooklyn",
                "state": "New York"
            },
            "theme_info": {
                "id": "family",
                "name": "Family",
                "description": "Cherishing family bonds and togetherness"
            },
            "qloo_intelligence": {
                "cultural_recommendations": {
                    "artists": {
                        "success": True,
                        "entities": [
                            {"name": "Vivaldi", "type": "classical"},
                            {"name": "Puccini", "type": "opera"},
                            {"name": "Bach", "type": "classical"}
                        ]
                    }
                }
            }
        }
        
        # Alternative test scenarios
        self.test_scenarios = [
            {
                "name": "Italian Family Theme",
                "profile": self.demo_profile
            },
            {
                "name": "Irish Birthday Theme", 
                "profile": {
                    **self.demo_profile,
                    "patient_info": {
                        **self.demo_profile["patient_info"],
                        "first_name": "Patrick",
                        "cultural_heritage": "Irish-American"
                    },
                    "theme_info": {
                        "id": "birthday",
                        "name": "Birthday", 
                        "description": "Celebrating special occasions"
                    }
                }
            },
            {
                "name": "German Music Theme",
                "profile": {
                    **self.demo_profile,
                    "patient_info": {
                        **self.demo_profile["patient_info"],
                        "first_name": "Hans",
                        "cultural_heritage": "German-American"
                    },
                    "theme_info": {
                        "id": "music",
                        "name": "Music",
                        "description": "Musical memories and melodies"
                    }
                }
            }
        ]
        
        logger.info(f"🧪 Test suite initialized with {len(self.test_scenarios)} scenarios")
    
    async def test_agent_4a_music(self) -> bool:
        """Test Agent 4A: Music Curation with both fallback and real APIs"""
        
        logger.info("\n🎵 Testing Agent 4A: Music Curation")
        logger.info("=" * 50)
        
        if not MusicCurationAgent:
            logger.error("❌ Agent 4A not available for testing")
            return False
        
        try:
            # Test 1: Fallback mode (no real APIs)
            logger.info("🧪 Testing fallback mode (no APIs)...")
            agent_fallback = MusicCurationAgent()
            
            result_fallback = await agent_fallback.run(self.demo_profile)
            
            # Validate fallback result
            if not self._validate_music_output(result_fallback, "fallback"):
                return False
            
            music_content = result_fallback["music_content"]
            metadata = result_fallback["metadata"]
            
            logger.info(f"   🎼 Fallback: {music_content['artist']} - {music_content['piece_title']}")
            logger.info(f"   🔧 Method: {metadata['selection_method']}")
            
            self.results["4A_fallback"] = result_fallback
            
            # Test 2: Real APIs mode (if available)
            if self.youtube_tool or self.gemini_tool:
                logger.info("🧪 Testing with real APIs...")
                agent_real = MusicCurationAgent(
                    youtube_tool=self.youtube_tool, 
                    gemini_tool=self.gemini_tool
                )
                
                result_real = await agent_real.run(self.demo_profile)
                
                if not self._validate_music_output(result_real, "real_apis"):
                    return False
                
                music_content_real = result_real["music_content"]
                metadata_real = result_real["metadata"]
                
                logger.info(f"   🎼 Real APIs: {music_content_real['artist']} - {music_content_real['piece_title']}")
                logger.info(f"   🔧 Method: {metadata_real['selection_method']}")
                
                # Test API connections
                if self.youtube_tool:
                    try:
                        yt_test = await self.youtube_tool.test_connection()
                        logger.info(f"   📺 YouTube API: {'✅ Working' if yt_test else '❌ Failed'}")
                    except Exception as e:
                        logger.warning(f"   📺 YouTube API test failed: {e}")
                
                if self.gemini_tool:
                    try:
                        gemini_test = await self.gemini_tool.test_connection()
                        logger.info(f"   🤖 Gemini API: {'✅ Working' if gemini_test else '❌ Failed'}")
                    except Exception as e:
                        logger.warning(f"   🤖 Gemini API test failed: {e}")
                
                # Compare results
                if metadata["selection_method"] != metadata_real["selection_method"]:
                    logger.info("   ✅ Real APIs produce different results than fallback!")
                else:
                    logger.info("   ⚠️ Real APIs and fallback produced same results")
                
                self.results["4A_real_apis"] = result_real
            else:
                logger.info("   ⚠️ No real API keys available, skipping real API test")
            
            # Test additional scenarios
            for scenario in self.test_scenarios[1:]:  # Skip first (already tested)
                scenario_name = scenario["name"]
                profile = scenario["profile"]
                
                logger.info(f"🧪 Testing scenario: {scenario_name}")
                
                # Test with best available agent (real APIs if available)
                if self.youtube_tool or self.gemini_tool:
                    agent = MusicCurationAgent(youtube_tool=self.youtube_tool, gemini_tool=self.gemini_tool)
                else:
                    agent = MusicCurationAgent()
                
                result = await agent.run(profile)
                
                if not self._validate_music_output(result, scenario_name):
                    return False
                
                music_content = result["music_content"]
                metadata = result["metadata"]
                
                logger.info(f"   🎼 Selected: {music_content['artist']} - {music_content['piece_title']}")
                logger.info(f"   🌍 Heritage match: {metadata['heritage_match']}")
                
                self.results[f"4A_{scenario_name}"] = result
                
            logger.info("✅ Agent 4A tests completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Agent 4A test failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _validate_music_output(self, result: Dict[str, Any], test_type: str) -> bool:
        """Validate music agent output structure"""
        
        required_fields = ["music_content", "metadata"]
        music_fields = ["artist", "piece_title", "youtube_url", "conversation_starters"]
        metadata_fields = ["heritage_match", "selection_method", "agent"]
        
        # Check main structure
        for field in required_fields:
            if field not in result:
                logger.error(f"❌ {test_type}: Missing required field: {field}")
                return False
        
        # Check music content
        for field in music_fields:
            if field not in result["music_content"]:
                logger.error(f"❌ {test_type}: Missing music field: {field}")
                return False
        
        # Check metadata
        for field in metadata_fields:
            if field not in result["metadata"]:
                logger.error(f"❌ {test_type}: Missing metadata field: {field}")
                return False
        
        return True
    
    async def test_agent_4b_recipes(self) -> bool:
        """Test Agent 4B: Recipe Selection"""
        
        logger.info("\n🍽️ Testing Agent 4B: Recipe Selection") 
        logger.info("=" * 50)
        
        if not RecipeSelectionAgent:
            logger.error("❌ Agent 4B not available for testing")
            return False
        
        try:
            # Test with pure JSON mode (no Gemini)
            agent = RecipeSelectionAgent()
            
            for scenario in self.test_scenarios:
                scenario_name = scenario["name"]
                profile = scenario["profile"]
                
                logger.info(f"🧪 Testing scenario: {scenario_name}")
                
                # Run agent
                result = await agent.run(profile)
                
                # Validate output structure
                if not self._validate_recipe_output(result, scenario_name):
                    return False
                
                # Log results
                recipe_content = result["recipe_content"]
                metadata = result["metadata"]
                
                logger.info(f"   🍽️ Selected: {recipe_content['name']}")
                logger.info(f"   🌍 Heritage match: {metadata['heritage_match']}")
                logger.info(f"   🎯 Theme match: {metadata['theme_match']}")
                logger.info(f"   🔧 Method: {metadata['selection_method']}")
                logger.info(f"   🥘 Ingredients: {len(recipe_content['ingredients'])}")
                logger.info(f"   💬 Conversation starters: {len(recipe_content['conversation_starters'])}")
                
                # Validate safety (microwave-only)
                if not metadata.get("microwave_only", False):
                    logger.warning("⚠️ Recipe safety flag not set")
                
                # Store for dashboard validation
                self.results[f"4B_{scenario_name}"] = result
                
            logger.info("✅ Agent 4B tests completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Agent 4B test failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _validate_recipe_output(self, result: Dict[str, Any], test_type: str) -> bool:
        """Validate recipe agent output structure"""
        
        required_fields = ["recipe_content", "metadata"]
        recipe_fields = ["name", "ingredients", "instructions", "conversation_starters", "heritage_connection"]
        metadata_fields = ["heritage_match", "theme_match", "selection_method", "agent"]
        
        # Check main structure
        for field in required_fields:
            if field not in result:
                logger.error(f"❌ {test_type}: Missing required field: {field}")
                return False
        
        # Check recipe content
        for field in recipe_fields:
            if field not in result["recipe_content"]:
                logger.error(f"❌ {test_type}: Missing recipe field: {field}")
                return False
        
        # Check metadata
        for field in metadata_fields:
            if field not in result["metadata"]:
                logger.error(f"❌ {test_type}: Missing metadata field: {field}")
                return False
        
        return True
    
    async def test_agent_4c_photos(self) -> bool:
        """Test Agent 4C: Photo Description with cultural enhancement"""
        
        logger.info("\n📷 Testing Agent 4C: Photo Description")
        logger.info("=" * 50)
        
        if not PhotoDescriptionAgent:
            logger.error("❌ Agent 4C not available for testing")
            return False
        
        try:
            # Test 1: Fallback mode (no Gemini)
            logger.info("🧪 Testing fallback mode (no Gemini)...")
            agent_fallback = PhotoDescriptionAgent()
            
            result_fallback = await agent_fallback.run(self.demo_profile)
            
            if not self._validate_photo_output(result_fallback, "fallback"):
                return False
            
            photo_content = result_fallback["photo_content"]
            metadata = result_fallback["metadata"]
            
            logger.info(f"   📷 Fallback: {photo_content['image_name']}")
            logger.info(f"   🤖 Enhanced: {metadata['cultural_enhancement']}")
            logger.info(f"   💬 Starters: {photo_content['conversation_starters'][:1]}")
            
            self.results["4C_fallback"] = result_fallback
            
            # Test 2: Real Gemini API mode (if available)
            if self.gemini_tool:
                logger.info("🧪 Testing with real Gemini API...")
                agent_real = PhotoDescriptionAgent(gemini_tool=self.gemini_tool)
                
                result_real = await agent_real.run(self.demo_profile)
                
                if not self._validate_photo_output(result_real, "real_gemini"):
                    return False
                
                photo_content_real = result_real["photo_content"]
                metadata_real = result_real["metadata"]
                
                logger.info(f"   📷 Enhanced: {photo_content_real['image_name']}")
                logger.info(f"   🤖 Enhanced: {metadata_real['cultural_enhancement']}")
                logger.info(f"   💬 Enhanced starters: {photo_content_real['conversation_starters'][:1]}")
                
                # Test Gemini API connection
                try:
                    gemini_test = await self.gemini_tool.test_connection()
                    logger.info(f"   🤖 Gemini API: {'✅ Working' if gemini_test else '❌ Failed'}")
                except Exception as e:
                    logger.warning(f"   🤖 Gemini API test failed: {e}")
                
                # Compare enhancement results
                if metadata_real["cultural_enhancement"] and not metadata["cultural_enhancement"]:
                    logger.info("   ✅ Gemini API successfully enhanced photo description!")
                    
                    # Show before/after comparison
                    logger.info("   📊 Enhancement Comparison:")
                    logger.info(f"      Before: {result_fallback['photo_content']['conversation_starters'][0]}")
                    logger.info(f"      After:  {result_real['photo_content']['conversation_starters'][0]}")
                    
                    # Check for cultural context
                    if photo_content_real.get("cultural_connection_summary"):
                        logger.info(f"      Cultural Context: {photo_content_real['cultural_connection_summary']}")
                
                self.results["4C_real_gemini"] = result_real
            else:
                logger.info("   ⚠️ No Gemini API key available, skipping enhancement test")
            
            # Test additional scenarios
            for scenario in self.test_scenarios[1:]:  # Skip first (already tested)
                scenario_name = scenario["name"]
                profile = scenario["profile"]
                
                logger.info(f"🧪 Testing scenario: {scenario_name}")
                
                # Use best available agent (with Gemini if available)
                if self.gemini_tool:
                    agent = PhotoDescriptionAgent(gemini_tool=self.gemini_tool)
                else:
                    agent = PhotoDescriptionAgent()
                
                result = await agent.run(profile)
                
                if not self._validate_photo_output(result, scenario_name):
                    return False
                
                photo_content = result["photo_content"]
                metadata = result["metadata"]
                
                logger.info(f"   📷 Image: {photo_content['image_name']}")
                logger.info(f"   🎯 Theme: {photo_content['theme']}")
                logger.info(f"   🤖 Enhanced: {metadata['cultural_enhancement']}")
                
                # Check that image name matches theme
                expected_image = f"{profile['theme_info']['id']}.png"
                actual_image = photo_content['image_name']
                if expected_image != actual_image:
                    logger.warning(f"   ⚠️ Image mismatch: expected {expected_image}, got {actual_image}")
                
                self.results[f"4C_{scenario_name}"] = result
                
            logger.info("✅ Agent 4C tests completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Agent 4C test failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _validate_photo_output(self, result: Dict[str, Any], test_type: str) -> bool:
        """Validate photo agent output structure"""
        
        required_fields = ["photo_content", "metadata"]
        photo_fields = ["image_name", "theme", "description", "conversation_starters", "heritage_connection"]
        metadata_fields = ["theme_match", "cultural_enhancement", "selection_method", "agent"]
        
        # Check main structure
        for field in required_fields:
            if field not in result:
                logger.error(f"❌ {test_type}: Missing required field: {field}")
                return False
        
        # Check photo content
        for field in photo_fields:
            if field not in result["photo_content"]:
                logger.error(f"❌ {test_type}: Missing photo field: {field}")
                return False
        
        # Check metadata
        for field in metadata_fields:
            if field not in result["metadata"]:
                logger.error(f"❌ {test_type}: Missing metadata field: {field}")
                return False
        
        return True
    
    def validate_dashboard_format(self) -> bool:
        """Validate that all agent outputs can be assembled into dashboard format"""
        
        logger.info("\n📊 Validating Dashboard Format")
        logger.info("=" * 50)
        
        try:
            # Use the best available results (prefer real APIs over fallback)
            agent_results = {}
            
            # For Agent 4A (Music)
            if "4A_real_apis" in self.results:
                agent_results["4A"] = self.results["4A_real_apis"]
                logger.info("   🎵 Using real API results for music")
            elif "4A_fallback" in self.results:
                agent_results["4A"] = self.results["4A_fallback"]
                logger.info("   🎵 Using fallback results for music")
            else:
                logger.error("❌ No Agent 4A results available")
                return False
            
            # For Agent 4B (Recipe) - always uses JSON
            demo_scenario = "Italian Family Theme"
            if f"4B_{demo_scenario}" in self.results:
                agent_results["4B"] = self.results[f"4B_{demo_scenario}"]
                logger.info("   🍽️ Using recipe results")
            else:
                logger.error("❌ No Agent 4B results available")
                return False
            
            # For Agent 4C (Photo)
            if "4C_real_gemini" in self.results:
                agent_results["4C"] = self.results["4C_real_gemini"]
                logger.info("   📷 Using Gemini-enhanced photo results")
            elif "4C_fallback" in self.results:
                agent_results["4C"] = self.results["4C_fallback"]
                logger.info("   📷 Using fallback photo results")
            else:
                logger.error("❌ No Agent 4C results available")
                return False
            
            # Simulate dashboard assembly
            dashboard_data = {
                "music_tile": {
                    "artist": agent_results["4A"]["music_content"]["artist"],
                    "piece": agent_results["4A"]["music_content"]["piece_title"],
                    "youtube_url": agent_results["4A"]["music_content"]["youtube_url"],
                    "conversation_starters": agent_results["4A"]["music_content"]["conversation_starters"]
                },
                "recipe_tile": {
                    "name": agent_results["4B"]["recipe_content"]["name"],
                    "ingredients": agent_results["4B"]["recipe_content"]["ingredients"],
                    "instructions": agent_results["4B"]["recipe_content"]["instructions"],
                    "conversation_starters": agent_results["4B"]["recipe_content"]["conversation_starters"]
                },
                "photo_tile": {
                    "image_name": agent_results["4C"]["photo_content"]["image_name"],
                    "description": agent_results["4C"]["photo_content"]["description"],
                    "conversation_starters": agent_results["4C"]["photo_content"]["conversation_starters"]
                },
                "metadata": {
                    "heritage_matches": {
                        "music": agent_results["4A"]["metadata"]["heritage_match"],
                        "recipe": agent_results["4B"]["metadata"]["heritage_match"],
                        "photo": agent_results["4C"]["metadata"]["cultural_enhancement"]
                    },
                    "theme_matches": {
                        "recipe": agent_results["4B"]["metadata"]["theme_match"],
                        "photo": agent_results["4C"]["metadata"]["theme_match"]
                    },
                    "api_usage": {
                        "music_real_apis": "4A_real_apis" in self.results,
                        "photo_enhanced": "4C_real_gemini" in self.results,
                        "apis_available": self.real_apis_available
                    }
                }
            }
            
            # Validate dashboard data
            logger.info("📊 Dashboard tiles assembled:")
            logger.info(f"   🎵 Music: {dashboard_data['music_tile']['artist']} - {dashboard_data['music_tile']['piece']}")
            logger.info(f"   🍽️ Recipe: {dashboard_data['recipe_tile']['name']}")
            logger.info(f"   📷 Photo: {dashboard_data['photo_tile']['image_name']}")
            
            # Show API enhancement status
            api_usage = dashboard_data["metadata"]["api_usage"]
            logger.info(f"   🚀 API Enhancement Status:")
            logger.info(f"      Music APIs: {'✅ Used' if api_usage['music_real_apis'] else '❌ Fallback'}")
            logger.info(f"      Photo Enhancement: {'✅ Used' if api_usage['photo_enhanced'] else '❌ Fallback'}")
            logger.info(f"      APIs Available: {'✅ Yes' if api_usage['apis_available'] else '❌ No'}")
            
            # Check all tiles have conversation starters
            for tile_name, tile_data in dashboard_data.items():
                if tile_name == "metadata":
                    continue
                starters = tile_data.get("conversation_starters", [])
                if len(starters) < 2:
                    logger.error(f"❌ {tile_name} has insufficient conversation starters: {len(starters)}")
                    return False
            
            # Store assembled dashboard
            self.results["dashboard"] = dashboard_data
            
            logger.info("✅ Dashboard format validation successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dashboard validation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        logger.info("\n📋 Generating Test Report")
        logger.info("=" * 50)
        
        # Count results by type
        agent_tests = {"4A": 0, "4B": 0, "4C": 0}
        api_tests = {"fallback": 0, "real_apis": 0, "enhanced": 0}
        
        for key in self.results.keys():
            if key.startswith("4A"):
                agent_tests["4A"] += 1
                if "real_apis" in key:
                    api_tests["real_apis"] += 1
                elif "fallback" in key:
                    api_tests["fallback"] += 1
            elif key.startswith("4B"):
                agent_tests["4B"] += 1
            elif key.startswith("4C"):
                agent_tests["4C"] += 1
                if "real_gemini" in key:
                    api_tests["enhanced"] += 1
                elif "fallback" in key:
                    api_tests["fallback"] += 1
        
        # Generate report
        report = {
            "test_summary": {
                "total_scenarios": len(self.test_scenarios),
                "agents_tested": len([a for a in agents_imported.values() if a]),
                "agents_imported": agents_imported,
                "import_errors": import_errors,
                "tools_available": tools_available,
                "results_generated": len(self.results)
            },
            "api_status": {
                "real_apis_available": self.real_apis_available,
                "api_keys_found": {k: v is not None for k, v in api_keys.items()},
                "youtube_tool_ready": self.youtube_tool is not None,
                "gemini_tool_ready": self.gemini_tool is not None
            },
            "agent_results": {
                "4A_music": agent_tests["4A"],
                "4B_recipes": agent_tests["4B"], 
                "4C_photos": agent_tests["4C"]
            },
            "api_tests": {
                "fallback_tests": api_tests["fallback"],
                "real_api_tests": api_tests["real_apis"],
                "enhanced_tests": api_tests["enhanced"]
            },
            "dashboard_ready": "dashboard" in self.results,
            "demo_scenario": {
                "patient": self.demo_profile["patient_info"]["first_name"],
                "heritage": self.demo_profile["patient_info"]["cultural_heritage"],
                "theme": self.demo_profile["theme_info"]["name"]
            }
        }
        
        # Log summary
        logger.info(f"📊 Test Results Summary:")
        logger.info(f"   Agents imported: {sum(agents_imported.values())}/3")
        logger.info(f"   Scenarios tested: {len(self.test_scenarios)}")
        logger.info(f"   Results generated: {len(self.results)}")
        logger.info(f"   Dashboard ready: {report['dashboard_ready']}")
        
        # Log API status
        logger.info(f"🔑 API Status:")
        logger.info(f"   Real APIs available: {self.real_apis_available}")
        logger.info(f"   YouTube tool: {'✅ Ready' if self.youtube_tool else '❌ Not available'}")
        logger.info(f"   Gemini tool: {'✅ Ready' if self.gemini_tool else '❌ Not available'}")
        
        # Log test types
        logger.info(f"🧪 Test Coverage:")
        logger.info(f"   Fallback tests: {api_tests['fallback']}")
        logger.info(f"   Real API tests: {api_tests['real_apis']}")
        logger.info(f"   Enhanced tests: {api_tests['enhanced']}")
        
        if import_errors:
            logger.warning(f"   Import errors: {list(import_errors.keys())}")
        
        return report

async def run_comprehensive_test():
    """Run the complete test suite"""
    
    logger.info("🚀 Starting Comprehensive Agent Test Suite")
    logger.info("=" * 80)
    
    # Initialize test suite
    suite = AgentTestSuite()
    
    # Track test results
    test_results = {}
    
    # Test each agent
    test_results["4A"] = await suite.test_agent_4a_music()
    test_results["4B"] = await suite.test_agent_4b_recipes() 
    test_results["4C"] = await suite.test_agent_4c_photos()
    
    # Validate dashboard format
    test_results["dashboard"] = suite.validate_dashboard_format()
    
    # Generate report
    report = suite.generate_test_report()
    
    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("🎯 FINAL TEST RESULTS")
    logger.info("=" * 80)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, passed in test_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"   Agent {test_name}: {status}")
    
    logger.info(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed")
    
    # Success criteria
    if passed_tests == total_tests:
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("✅ Agents 4A, 4B, 4C are working correctly!")
        logger.info("🚀 Ready for dashboard integration!")
        
        # Show demo data
        if "dashboard" in suite.results:
            dashboard = suite.results["dashboard"]
            logger.info("\n🎪 Demo Dashboard Data:")
            logger.info(f"   🎵 Music: {dashboard['music_tile']['artist']}")
            logger.info(f"   🍽️ Recipe: {dashboard['recipe_tile']['name']}")
            logger.info(f"   📷 Photo: {dashboard['photo_tile']['image_name']}")
            
            # Show API enhancement status
            api_usage = dashboard["metadata"]["api_usage"]
            logger.info(f"\n🚀 API Enhancement Status:")
            logger.info(f"   YouTube API: {'✅ Enhanced' if api_usage['music_real_apis'] else '❌ Fallback'}")
            logger.info(f"   Gemini Enhancement: {'✅ Active' if api_usage['photo_enhanced'] else '❌ Fallback'}")
            
            if api_usage["apis_available"]:
                logger.info("🎊 Real API integration working - Demo will show enhanced cultural personalization!")
            else:
                logger.info("📝 Fallback mode working - Demo will be reliable but without API enhancements")
    else:
        logger.error(f"❌ {total_tests - passed_tests} tests failed")
        logger.error("🔧 Fix issues before proceeding")
    
    # Return for external validation
    return {
        "success": passed_tests == total_tests,
        "results": test_results,
        "report": report,
        "dashboard_data": suite.results.get("dashboard")
    }

if __name__ == "__main__":
    # Run the comprehensive test
    logger.info("Starting test from command line...")
    
    try:
        final_results = asyncio.run(run_comprehensive_test())
        exit_code = 0 if final_results["success"] else 1
        
        logger.info(f"Test completed with exit code: {exit_code}")
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        logger.warning("Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test suite crashed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)