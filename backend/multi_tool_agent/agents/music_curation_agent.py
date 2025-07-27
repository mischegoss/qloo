"""
Agent 4A: Music Curation Agent - FIXED QLOO DATA EXTRACTION
File: backend/multi_tool_agent/agents/music_curation_agent.py

CRITICAL FIXES:
- Fixed Qloo artist data extraction ('str' object has no attribute 'get')
- Added safe data type checking for all Qloo responses
- Improved error handling with detailed logging
- Maintained fallback functionality
"""

import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MusicCurationAgent:
    """
    Agent 4A: Simplified Music Curation Agent - FIXED VERSION
    
    CRITICAL FIXES APPLIED:
    - Safe Qloo data extraction with type checking
    - Proper handling of string vs dict responses
    - Enhanced error logging for debugging
    - Maintained all fallback mechanisms
    """
    
    def __init__(self, youtube_tool=None, gemini_tool=None):
        self.youtube_tool = youtube_tool
        self.gemini_tool = gemini_tool
        
        # Classical composers database with heritage mapping
        self.classical_database = [
            {
                "artist": "Johann Sebastian Bach",
                "search_name": "bach",
                "pieces": ["Air on the G String", "Brandenburg Concerto", "Well-Tempered Clavier"],
                "heritage_tags": ["german", "european", "universal"],
                "conversation_starters": [
                    "Bach's music is so mathematical and beautiful",
                    "This music has such intricate harmonies"
                ],
                "fun_fact": "Bach had 20 children and taught many of them music"
            },
            {
                "artist": "Wolfgang Amadeus Mozart",
                "search_name": "mozart",
                "pieces": ["Eine kleine Nachtmusik", "Piano Sonata No. 11", "Requiem"],
                "heritage_tags": ["austrian", "german", "european", "universal"],
                "conversation_starters": [
                    "Mozart wrote this when he was so young",
                    "This music feels so elegant and graceful"
                ],
                "fun_fact": "Mozart composed over 600 pieces in his short 35-year life"
            },
            {
                "artist": "Antonio Vivaldi", 
                "search_name": "vivaldi",
                "pieces": ["The Four Seasons", "Gloria in D major", "Concerto for Two Violins"],
                "heritage_tags": ["italian", "european"],
                "conversation_starters": [
                    "You can hear the seasons in this music",
                    "Vivaldi really captured the sounds of nature"
                ],
                "fun_fact": "Vivaldi was known as 'The Red Priest' due to his red hair"
            },
            {
                "artist": "Frédéric Chopin",
                "search_name": "chopin", 
                "pieces": ["Nocturne in E-flat major", "Minute Waltz", "Prelude in D-flat major"],
                "heritage_tags": ["polish", "french", "european"],
                "conversation_starters": [
                    "Chopin's piano music is so romantic",
                    "This brings back memories of elegant ballrooms"
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
        
        logger.info("🎵 Agent 4A: Simplified Music Curation initialized with fixed tools")
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Simple music curation using heritage + Qloo data
        """
        try:
            logger.info("🎵 Agent 4A: Starting simplified music curation")
            
            # Extract simple context with safe data handling
            heritage = self._extract_heritage(enhanced_profile)
            qloo_artists = self._extract_qloo_artists_safe(enhanced_profile)
            
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
            import traceback
            logger.error(traceback.format_exc())
            return self._emergency_fallback()
    
    def _extract_heritage(self, enhanced_profile: Dict[str, Any]) -> str:
        """Extract heritage from enhanced profile"""
        
        patient_info = enhanced_profile.get("patient_info", {})
        heritage = patient_info.get("cultural_heritage", "Universal")
        
        return heritage.lower()
    
    def _extract_qloo_artists_safe(self, enhanced_profile: Dict[str, Any]) -> List[str]:
        """
        CRITICAL FIX: Safe extraction of Qloo artist names with type checking
        """
        
        try:
            # Navigate to Qloo data safely
            qloo_data = enhanced_profile.get("qloo_intelligence", {})
            
            # Handle potential double-wrapping
            if "qloo_intelligence" in qloo_data and isinstance(qloo_data["qloo_intelligence"], dict):
                qloo_data = qloo_data["qloo_intelligence"]
            
            cultural_recs = qloo_data.get("cultural_recommendations", {})
            artists_data = cultural_recs.get("artists", {})
            
            logger.debug(f"🔍 Qloo artists_data type: {type(artists_data)}")
            logger.debug(f"🔍 Qloo artists_data content: {artists_data}")
            
            # CRITICAL FIX: Check if artists_data is a dict and has expected structure
            if not isinstance(artists_data, dict):
                logger.warning(f"⚠️ artists_data is not a dict: {type(artists_data)}")
                return []
            
            # Check if call was successful
            if not artists_data.get("success", False):
                logger.warning("⚠️ Qloo artists call was not successful")
                return []
            
            # Extract entities safely
            entities = artists_data.get("entities", [])
            
            # CRITICAL FIX: Ensure entities is a list
            if not isinstance(entities, list):
                logger.warning(f"⚠️ entities is not a list: {type(entities)}")
                return []
            
            # Extract artist names with safe iteration
            artist_names = []
            for entity in entities:
                # CRITICAL FIX: Check if entity is a dict before calling .get()
                if isinstance(entity, dict):
                    name = entity.get("name", "")
                    if name and isinstance(name, str):
                        artist_names.append(name.lower())
                elif isinstance(entity, str):
                    # Handle case where entity is just a string
                    artist_names.append(entity.lower())
                else:
                    logger.warning(f"⚠️ Unexpected entity type: {type(entity)}")
            
            logger.info(f"✅ Successfully extracted {len(artist_names)} artist names")
            return artist_names
            
        except Exception as e:
            logger.error(f"❌ Error extracting Qloo artists: {e}")
            logger.error(f"❌ enhanced_profile structure: {enhanced_profile.keys()}")
            
            # Try to log the problematic data for debugging
            try:
                qloo_data = enhanced_profile.get("qloo_intelligence", {})
                logger.error(f"❌ qloo_intelligence keys: {qloo_data.keys() if isinstance(qloo_data, dict) else 'not a dict'}")
                
                cultural_recs = qloo_data.get("cultural_recommendations", {}) if isinstance(qloo_data, dict) else {}
                logger.error(f"❌ cultural_recommendations keys: {cultural_recs.keys() if isinstance(cultural_recs, dict) else 'not a dict'}")
                
                artists_data = cultural_recs.get("artists", {}) if isinstance(cultural_recs, dict) else {}
                logger.error(f"❌ artists_data: {artists_data}")
                
            except Exception as debug_error:
                logger.error(f"❌ Debug logging failed: {debug_error}")
            
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
            logger.info(f"🔍 YouTube search: {search_query} classical music audio (Creative Commons)")
            
            # Use the FIXED YouTubeAPI.search_videos method
            results = await self.youtube_tool.search_videos(
                query=f"{search_query} classical music audio",
                max_results=1,
                audio_only=True  # Prioritize audio-only content
            )
            
            if results and len(results) > 0:
                video = results[0]
                logger.info(f"✅ Found {len(results)} Creative Commons videos")
                return {
                    "url": f"https://www.youtube.com/watch?v={video.get('videoId', '')}",
                    "title": video.get("title", "Classical Music"),
                    "embedUrl": f"https://www.youtube.com/embed/{video.get('videoId', '')}",
                    "duration": video.get("duration", "unknown"),
                    "channelTitle": video.get("channelTitle", ""),
                    "license": "Creative Commons"
                }
            else:
                logger.warning("⚠️ No Creative Commons videos found")
                return self._youtube_fallback()
                
        except Exception as e:
            logger.error(f"❌ YouTube search failed: {e}")
            return self._youtube_fallback()
    
    def _youtube_fallback(self) -> Dict[str, Any]:
        """Fallback when YouTube search fails"""
        return {
            "url": None,
            "title": "Classical Music (Audio not available)",
            "embedUrl": None,
            "duration": "unknown",
            "channelTitle": "Fallback",
            "license": "Fallback"
        }
    
    def _emergency_fallback(self) -> Dict[str, Any]:
        """Emergency fallback when everything fails"""
        
        logger.warning("🔄 Using emergency fallback for music curation")
        
        # Default to Bach
        default_composer = self.classical_database[0]
        
        return {
            "music_content": {
                "artist": default_composer["artist"],
                "piece_title": default_composer["pieces"][0],
                "search_query": f"{default_composer['search_name']} {default_composer['pieces'][0]}",
                "youtube_url": None,
                "youtube_title": None,
                "youtube_embed": None,
                "conversation_starters": default_composer["conversation_starters"],
                "fun_fact": default_composer["fun_fact"]
            },
            "metadata": {
                "heritage_match": False,
                "selection_method": "emergency_fallback",
                "agent": "music_curation_agent_4a"
            }
        }

# Export the main class
__all__ = ["MusicCurationAgent"]