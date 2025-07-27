"""
Agent 4A: Music Curation Agent - WITH RECENT SELECTION AVOIDANCE
File: backend/multi_tool_agent/agents/music_curation_agent.py

NEW FEATURES:
- Checks recent_music.json to avoid repeating same artist/piece
- Simple rotation system - if same artist was used recently, pick different one
- Dashboard Synthesizer will write current selection back to the file
"""

import logging
import random
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MusicCurationAgent:
    """
    Agent 4A: Music Curation Agent with Recent Selection Avoidance
    """
    
    def __init__(self, youtube_tool=None, gemini_tool=None):
        self.youtube_tool = youtube_tool
        self.gemini_tool = gemini_tool
        
        # Path to recent music tracking file
        self.recent_music_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "recent_music.json"
        )
        
        # Classical composers database
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
            },
            {
                "artist": "Claude Debussy",
                "search_name": "debussy",
                "pieces": ["Clair de Lune", "Arabesque No. 1", "The Girl with the Flaxen Hair"],
                "heritage_tags": ["french", "european"],
                "conversation_starters": [
                    "Debussy's music flows like water",
                    "This music paints such beautiful pictures"
                ],
                "fun_fact": "Debussy was a leader in musical impressionism"
            }
        ]
        
        logger.info("🎵 Agent 4A: Music Curation initialized with recent selection tracking")
    
    def _load_recent_music(self) -> Dict[str, Any]:
        """Load recent music selection to avoid repetition"""
        
        try:
            if os.path.exists(self.recent_music_file):
                with open(self.recent_music_file, 'r', encoding='utf-8') as f:
                    recent_data = json.load(f)
                logger.info(f"📖 Previous selection: {recent_data.get('artist', 'none')} - {recent_data.get('piece_title', 'none')}")
                return recent_data
            else:
                logger.info("📖 No recent music file found - first time selection")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error loading recent music: {e}")
            return {}
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution with recent selection avoidance"""
        
        try:
            logger.info("🎵 Agent 4A: Starting music curation with repetition avoidance")
            
            # Load recent selection to avoid repetition
            recent_music = self._load_recent_music()
            recent_artist = recent_music.get("artist", "").lower()
            recent_piece = recent_music.get("piece_title", "").lower()
            
            # Extract context
            heritage = self._extract_heritage(enhanced_profile)
            qloo_artists = self._extract_qloo_artists_safe(enhanced_profile)
            
            logger.info(f"👤 Heritage: {heritage}")
            logger.info(f"🎼 Qloo artists available: {len(qloo_artists)}")
            logger.info(f"🚫 Avoiding: {recent_artist} ({recent_piece})")
            
            # Try Gemini-powered curation first
            curated_selection = await self._try_gemini_curation(heritage, qloo_artists)
            
            if curated_selection:
                # Use Gemini's smart selection
                selected_composer = self._find_composer_by_name(curated_selection["selected_artist"])
                selected_piece = curated_selection["piece_suggestions"][0] if curated_selection["piece_suggestions"] else "classical piece"
                conversation_starters = curated_selection["conversation_starters"]
                fun_fact = curated_selection["fun_fact"]
                curation_method = "gemini_powered"
            else:
                # Fall back to smart selection avoiding recent choice
                selected_composer, selected_piece = self._select_avoiding_recent(heritage, qloo_artists, recent_artist, recent_piece)
                conversation_starters = selected_composer["conversation_starters"]
                fun_fact = selected_composer["fun_fact"]
                curation_method = "smart_rotation"
            
            # Create YouTube search query
            search_query = f"{selected_composer['search_name']} {selected_piece.lower()}"
    
            # Search YouTube
            youtube_result = await self._search_youtube(search_query)
            
            # Return result (Dashboard Synthesizer will save this to recent_music.json)
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
                    "avoided_repetition": bool(recent_artist),
                    "agent": "music_curation_agent_4a"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4A failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self._emergency_fallback()
    
    def _select_avoiding_recent(self, heritage: str, qloo_artists: List[str], recent_artist: str, recent_piece: str) -> tuple:
        """Select composer and piece while avoiding recent selection"""
        
        # Filter out recent artist from available options
        available_composers = []
        for composer in self.classical_database:
            if composer["artist"].lower() != recent_artist and composer["search_name"] != recent_artist:
                available_composers.append(composer)
        
        # If we filtered out everything, use full list (better than same artist)
        if not available_composers:
            available_composers = self.classical_database
            logger.warning("⚠️ All composers were recent - using full list")
        
        # Try heritage match first (from filtered list)
        heritage_matches = []
        for composer in available_composers:
            if any(tag in heritage for tag in composer["heritage_tags"]):
                heritage_matches.append(composer)
        
        if heritage_matches:
            selected_composer = random.choice(heritage_matches)
            logger.info(f"✅ Heritage match (avoiding recent): {selected_composer['artist']}")
        else:
            # Random selection from available (non-recent) composers
            selected_composer = random.choice(available_composers)
            logger.info(f"✅ Random selection (avoiding recent): {selected_composer['artist']}")
        
        # Select piece, avoiding recent piece if same composer
        available_pieces = selected_composer["pieces"].copy()
        if selected_composer["artist"].lower() == recent_artist:
            # Same composer - try to avoid same piece
            available_pieces = [p for p in available_pieces if p.lower() != recent_piece]
            if not available_pieces:
                available_pieces = selected_composer["pieces"]  # Use all if we filtered everything
        
        selected_piece = random.choice(available_pieces)
        
        return selected_composer, selected_piece
    
    # ... (keeping all the existing helper methods unchanged)
    def _extract_heritage(self, enhanced_profile: Dict[str, Any]) -> str:
        """Extract heritage from enhanced profile"""
        patient_info = enhanced_profile.get("patient_info", {})
        heritage = patient_info.get("cultural_heritage", "Universal")
        return heritage.lower()
    
    def _extract_qloo_artists_safe(self, enhanced_profile: Dict[str, Any]) -> List[str]:
        """Safe extraction of Qloo artist names with type checking"""
        try:
            qloo_data = enhanced_profile.get("qloo_intelligence", {})
            
            if "qloo_intelligence" in qloo_data and isinstance(qloo_data["qloo_intelligence"], dict):
                qloo_data = qloo_data["qloo_intelligence"]
            
            cultural_recs = qloo_data.get("cultural_recommendations", {})
            artists_data = cultural_recs.get("artists", {})
            
            if not isinstance(artists_data, dict):
                logger.warning(f"⚠️ artists_data is not a dict: {type(artists_data)}")
                return []
            
            if not artists_data.get("success", False):
                logger.warning("⚠️ Qloo artists call was not successful")
                return []
            
            entities = None
            if "results" in artists_data and isinstance(artists_data["results"], dict):
                entities = artists_data["results"].get("entities", [])
            else:
                entities = artists_data.get("entities", [])
            
            if not isinstance(entities, list):
                logger.warning(f"⚠️ entities is not a list: {type(entities)}")
                if isinstance(entities, dict) and "entities" in entities:
                    entities = entities["entities"]
                    if not isinstance(entities, list):
                        return []
                else:
                    return []
            
            artist_names = []
            for entity in entities:
                if isinstance(entity, dict):
                    name = entity.get("name", "")
                    if name and isinstance(name, str):
                        artist_names.append(name.lower())
                elif isinstance(entity, str):
                    artist_names.append(entity.lower())
            
            logger.info(f"✅ Successfully extracted {len(artist_names)} artist names")
            return artist_names
            
        except Exception as e:
            logger.error(f"❌ Error extracting Qloo artists: {e}")
            return []
    
    async def _try_gemini_curation(self, heritage: str, qloo_artists: List[str]) -> Optional[Dict[str, Any]]:
        """Try to use Gemini for intelligent music curation"""
        if not self.gemini_tool:
            return None
       
        try:
            logger.info("🤖 Trying Gemini-powered music curation")
            
            result = await self.gemini_tool.curate_music_selection(
                heritage=heritage,
                available_artists=qloo_artists,
                theme="classical music"
            )
            
            if result and result.get("selected_artist"):
                logger.info(f"✅ Gemini selected: {result['selected_artist']}")
                return result
            else:
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
        
        return self.classical_database[0]
    
    def _heritage_matches(self, heritage: str, composer: Dict[str, Any]) -> bool:
        """Check if heritage matches composer"""
        return any(tag in heritage for tag in composer["heritage_tags"])
    
    async def _search_youtube(self, search_query: str) -> Optional[Dict[str, Any]]:
        """Search YouTube using the Creative Commons API"""
        if not self.youtube_tool:
            return self._youtube_fallback()
        
        try:
            logger.info(f"🔍 YouTube search: {search_query} classical music audio")
            
            results = await self.youtube_tool.search_videos(
                query=f"{search_query} classical music audio",
                max_results=1,
                audio_only=True
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