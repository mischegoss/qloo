"""
Agent 4A: Simplified Music Curation + YouTube Agent
File: backend/multi_tool_agent/agents/music_curation_agent.py

SIMPLIFIED STEP 4A: Focus on what matters
- Simple heritage-based classical music selection
- Direct YouTube API integration 
- No age calculations (irrelevant for classical)
- Comprehensive fallbacks ensure it always works
"""

import logging
import random
from typing import Dict, Any, List, Optional

# CRITICAL: Define logger BEFORE using it in imports
logger = logging.getLogger(__name__)

# Import the actual tools using fixed approach
try:
    # Try importing through the fixed __init__.py
    from ..tools import YouTubeAPI, SimpleGeminiTool
    logger.debug("✅ Imported tools via __init__.py")
except ImportError as e1:
    # Fallback to direct imports
    try:
        from ..tools.youtube_tools import YouTubeAPI
        from ..tools.simple_gemini_tools import SimpleGeminiTool
        logger.debug("✅ Imported tools directly")
    except ImportError as e2:
        # Try absolute imports (for when running tests)
        try:
            from multi_tool_agent.tools.youtube_tools import YouTubeAPI
            from multi_tool_agent.tools.simple_gemini_tools import SimpleGeminiTool
            logger.debug("✅ Imported tools via absolute imports")
        except ImportError as e3:
            # Final fallback - no tools available
            YouTubeAPI = None
            SimpleGeminiTool = None
            logger.warning(f"⚠️ Could not import tools: {e1}, {e2}, {e3} - running in fallback mode")

class MusicCurationAgent:
    """
    Agent 4A: Simplified Music Curation + YouTube
    
    Takes Qloo artists and selects appropriate classical music with YouTube integration.
    Much simpler approach focused on heritage matching only.
    """
    
    def __init__(self, youtube_tool=None, gemini_tool=None):
        self.youtube_tool = youtube_tool
        self.gemini_tool = gemini_tool
        
        # Simple classical music database with heritage mapping
        self.classical_database = self._load_classical_database()
        
        logger.info("🎵 Agent 4A: Simplified Music Curation initialized with fixed tools")
    
    def _load_classical_database(self) -> List[Dict[str, Any]]:
        """Simple classical music database with heritage tags"""
        
        return [
            {
                "artist": "Johann Sebastian Bach",
                "search_name": "bach",
                "pieces": ["Air on the G String", "Brandenburg Concerto No. 3", "Jesu Joy of Man's Desiring"],
                "heritage_tags": ["german", "european"],
                "conversation_starters": [
                    "Do you remember hearing this beautiful music?",
                    "This reminds me of peaceful Sunday mornings"
                ],
                "fun_fact": "Bach wrote over 1000 pieces of music in his lifetime"
            },
            {
                "artist": "Wolfgang Amadeus Mozart", 
                "search_name": "mozart",
                "pieces": ["Eine kleine Nachtmusik", "Piano Sonata No. 11", "Symphony No. 40"],
                "heritage_tags": ["austrian", "european"],
                "conversation_starters": [
                    "Mozart's music always sounds so cheerful",
                    "Do you have a favorite classical composer?"
                ],
                "fun_fact": "Mozart started composing music when he was just 5 years old"
            },
            {
                "artist": "Antonio Vivaldi",
                "search_name": "vivaldi", 
                "pieces": ["Spring from Four Seasons", "Winter from Four Seasons", "Summer from Four Seasons"],
                "heritage_tags": ["italian", "european"],
                "conversation_starters": [
                    "This music makes me think of beautiful seasons",
                    "Can you hear the birds singing in this music?"
                ],
                "fun_fact": "Vivaldi's Four Seasons music describes different times of the year"
            },
            {
                "artist": "Frederic Chopin",
                "search_name": "chopin",
                "pieces": ["Minute Waltz", "Nocturne in E-flat major", "Raindrop Prelude"],
                "heritage_tags": ["polish", "european"],
                "conversation_starters": [
                    "Chopin's piano music sounds like dancing",
                    "Do you enjoy piano music?"
                ],
                "fun_fact": "Chopin wrote most of his music for solo piano"
            },
            {
                "artist": "Ludwig van Beethoven",
                "search_name": "beethoven",
                "pieces": ["Ode to Joy", "Moonlight Sonata", "Symphony No. 5"],
                "heritage_tags": ["german", "european"],
                "conversation_starters": [
                    "This music feels so powerful and moving",
                    "Beethoven's music tells such beautiful stories"
                ],
                "fun_fact": "Beethoven continued composing even after he lost his hearing"
            }
        ]
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Simple music curation using heritage + Qloo data
        """
        try:
            logger.info("🎵 Agent 4A: Starting simplified music curation")
            
            # Extract simple context
            heritage = self._extract_heritage(enhanced_profile)
            qloo_artists = self._extract_qloo_artists(enhanced_profile)
            
            logger.info(f"👤 Heritage: {heritage}")
            logger.info(f"🎼 Qloo artists available: {len(qloo_artists)}")
            
            # Try Gemini-powered curation first, fall back to simple logic
            curated_selection = await self._try_gemini_curation(heritage, qloo_artists)
            
            if curated_selection:
                # Use Gemini's smart selection
                selected_composer = self._find_composer_by_name(curated_selection["selected_artist"])
                selected_piece = curated_selection["piece_suggestions"][0] if curated_selection["piece_suggestions"] else "classical piece"
                conversation_starters = curated_selection["conversation_starters"]
                fun_fact = curated_selection["fun_fact"]
                curation_method = "gemini_powered"
            else:
                # Fall back to simple selection
                selected_composer = self._select_best_composer(heritage, qloo_artists)
                selected_piece = random.choice(selected_composer["pieces"])
                conversation_starters = selected_composer["conversation_starters"]
                fun_fact = selected_composer["fun_fact"]
                curation_method = "simple_fallback"
            
            # Create YouTube search query using fixed format
            search_query = f"{selected_composer['search_name']} {selected_piece.lower()}"
            
            # Search YouTube using FIXED API
            youtube_result = await self._search_youtube(search_query)
            
            # Return simple result
            return {
                "music_content": {
                    "artist": selected_composer["artist"],
                    "piece_title": selected_piece,
                    "search_query": search_query,
                    "youtube_url": youtube_result.get("url") if youtube_result else None,
                    "youtube_title": youtube_result.get("title") if youtube_result else None,
                    "youtube_embed": youtube_result.get("embedUrl") if youtube_result else None,
                    "conversation_starters": conversation_starters,
                    "fun_fact": fun_fact
                },
                "metadata": {
                    "heritage_match": self._heritage_matches(heritage, selected_composer),
                    "selection_method": curation_method,
                    "agent": "music_curation_agent_4a"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4A failed: {e}")
            return self._emergency_fallback()
    
    def _extract_heritage(self, enhanced_profile: Dict[str, Any]) -> str:
        """Extract heritage from enhanced profile"""
        
        patient_info = enhanced_profile.get("patient_info", {})
        heritage = patient_info.get("cultural_heritage", "Universal")
        
        return heritage.lower()
    
    def _extract_qloo_artists(self, enhanced_profile: Dict[str, Any]) -> List[str]:
        """Extract Qloo artist names"""
        
        try:
            # Handle potential double-wrapping
            qloo_data = enhanced_profile.get("qloo_intelligence", {})
            if "qloo_intelligence" in qloo_data:
                qloo_data = qloo_data["qloo_intelligence"]
            
            artists_data = qloo_data.get("cultural_recommendations", {}).get("artists", {})
            
            if artists_data.get("success") and artists_data.get("entities"):
                artist_names = [artist.get("name", "").lower() for artist in artists_data["entities"]]
                return [name for name in artist_names if name]  # Remove empty strings
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Error extracting Qloo artists: {e}")
            return []
    
    def _select_best_composer(self, heritage: str, qloo_artists: List[str]) -> Dict[str, Any]:
        """Select best classical composer based on heritage and Qloo data"""
        
        # First try: Match BOTH heritage AND Qloo artists (best match)
        for composer in self.classical_database:
            composer_name = composer["search_name"]
            heritage_match = any(tag in heritage for tag in composer["heritage_tags"])
            qloo_match = any(composer_name in qloo_artist for qloo_artist in qloo_artists)
            
            if heritage_match and qloo_match:
                logger.info(f"✅ Perfect match (heritage + Qloo): {composer['artist']}")
                return composer
        
        # Second try: Heritage match (prioritize cultural connection)
        heritage_matches = []
        for composer in self.classical_database:
            if any(tag in heritage for tag in composer["heritage_tags"]):
                heritage_matches.append(composer)
        
        if heritage_matches:
            selected = random.choice(heritage_matches)
            logger.info(f"✅ Heritage match: {selected['artist']} for {heritage}")
            return selected
        
        # Third try: Any Qloo match
        for composer in self.classical_database:
            composer_name = composer["search_name"]
            if any(composer_name in qloo_artist for qloo_artist in qloo_artists):
                logger.info(f"✅ Qloo match found: {composer['artist']}")
                return composer
        
        # Fourth try: Default to Bach (most universally known)
        default_composer = self.classical_database[0]  # Bach
        logger.info(f"✅ Default selection: {default_composer['artist']}")
        return default_composer
    
    async def _try_gemini_curation(self, heritage: str, qloo_artists: List[str]) -> Optional[Dict[str, Any]]:
        """Try to use Gemini for intelligent music curation"""
        
        if not self.gemini_tool:
            logger.info("💡 Gemini tool not available, using simple selection")
            return None
        
        try:
            logger.info("🤖 Trying Gemini-powered music curation")
            
            # Use SimpleGeminiTool's specialized method
            result = await self.gemini_tool.curate_music_selection(
                heritage=heritage,
                available_artists=qloo_artists,
                theme="classical music"  # Could be enhanced with actual theme
            )
            
            if result and result.get("selected_artist"):
                logger.info(f"✅ Gemini selected: {result['selected_artist']}")
                return result
            else:
                logger.warning("⚠️ Gemini returned invalid result")
                return None
                
        except Exception as e:
            logger.error(f"❌ Gemini curation failed: {e}")
            return None
    
    def _find_composer_by_name(self, artist_name: str) -> Dict[str, Any]:
        """Find composer in database by name"""
        
        artist_lower = artist_name.lower()
        
        for composer in self.classical_database:
            if (artist_lower in composer["artist"].lower() or 
                artist_lower in composer["search_name"].lower()):
                return composer
        
        # Default to Bach if not found
        return self.classical_database[0]
    
    def _heritage_matches(self, heritage: str, composer: Dict[str, Any]) -> bool:
        """Check if heritage matches composer"""
        return any(tag in heritage for tag in composer["heritage_tags"])
    
    async def _search_youtube(self, search_query: str) -> Optional[Dict[str, Any]]:
        """Search YouTube using the FIXED Creative Commons API"""
        
        if not self.youtube_tool:
            logger.warning("⚠️ YouTube tool not available")
            return self._youtube_fallback()
        
        try:
            logger.info(f"🔍 YouTube search (Creative Commons): {search_query}")
            
            # Use the FIXED YouTubeAPI.search_videos method
            results = await self.youtube_tool.search_videos(
                query=search_query,
                max_results=1,
                audio_only=True  # Prioritize audio-only content
            )
            
            if results and len(results) > 0:
                video = results[0]
                return {
                    "url": video.get("url"),
                    "title": video.get("title"),
                    "channel": video.get("channelTitle"),
                    "embedUrl": video.get("embedUrl"),  # Proper embed URL
                    "success": True
                }
            else:
                logger.warning("⚠️ No Creative Commons results found")
                return self._youtube_fallback()
                
        except Exception as e:
            logger.error(f"❌ YouTube search failed: {e}")
            return self._youtube_fallback()
    
    def _youtube_fallback(self) -> Dict[str, Any]:
        """Simple YouTube fallback with Creative Commons URLs"""
        
        fallback_videos = [
            {
                "url": "https://www.youtube.com/watch?v=GMkmQlfOJDk",
                "title": "Bach - Air on the G String (Public Domain)", 
                "channel": "Classical Archive",
                "embedUrl": "https://www.youtube.com/embed/GMkmQlfOJDk"
            },
            {
                "url": "https://www.youtube.com/watch?v=o1dBg__wsuo",
                "title": "Mozart - Eine kleine Nachtmusik (Creative Commons)",
                "channel": "Public Domain Music",
                "embedUrl": "https://www.youtube.com/embed/o1dBg__wsuo"
            }
        ]
        
        import random
        selected = random.choice(fallback_videos)
        selected.update({"success": False, "fallback": True})
        
        return selected
    
    def _emergency_fallback(self) -> Dict[str, Any]:
        """Emergency fallback when everything fails"""
        
        return {
            "music_content": {
                "artist": "Johann Sebastian Bach",
                "piece_title": "Air on the G String", 
                "search_query": "bach air g string",
                "youtube_url": "https://www.youtube.com/watch?v=GMkmQlfOJDk",
                "youtube_title": "Bach - Air on the G String",
                "youtube_embed": "https://www.youtube.com/embed/GMkmQlfOJDk",
                "conversation_starters": [
                    "This is such beautiful, peaceful music",
                    "Do you enjoy classical music?"
                ],
                "fun_fact": "Bach is one of the most famous classical composers"
            },
            "metadata": {
                "heritage_match": False,
                "selection_method": "emergency_fallback", 
                "agent": "music_curation_agent_4a"
            }
        }


# Simple test function
async def test_agent_with_fixed_tools():
    """Test the simplified agent with fixed YouTube and Gemini tools"""
    
    # Import the fixed tools (you would do this in real usage)
    # from .youtube_tools_fixed import YouTubeAPI
    # from .simple_gemini_tool import SimpleGeminiTool
    
    # Mock enhanced profile from Step 3
    mock_profile = {
        "patient_info": {
            "cultural_heritage": "Italian-American"
        },
        "qloo_intelligence": {
            "cultural_recommendations": {
                "artists": {
                    "success": True,
                    "entities": [
                        {"name": "Vivaldi"},
                        {"name": "Bach"}
                    ]
                }
            }
        }
    }
    
    # Test with no tools (pure fallback)
    logger.info("🧪 Testing Agent 4A with fallbacks only...")
    agent_fallback = MusicCurationAgent()
    result_fallback = await agent_fallback.run(mock_profile)
    print(f"✅ Fallback Result: {result_fallback['music_content']['artist']} - {result_fallback['music_content']['piece_title']}")
    
    # Test with tools (in real usage, you'd initialize them with API keys)
    # youtube_tool = YouTubeAPI("YOUR_YOUTUBE_API_KEY")
    # gemini_tool = SimpleGeminiTool("YOUR_GEMINI_API_KEY") 
    # agent_with_tools = MusicCurationAgent(youtube_tool, gemini_tool)
    # result_with_tools = await agent_with_tools.run(mock_profile)
    
    return result_fallback


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_with_fixed_tools())