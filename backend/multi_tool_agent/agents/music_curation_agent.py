"""
Agent 4A: Music Curation Agent - FIXED WITH RECENT MUSIC AVOIDANCE
File: backend/multi_tool_agent/agents/music_curation_agent.py

CRITICAL FIXES:
- Reads recent_music.json to avoid repeating selections
- Excludes recent artist/piece from next selection
- Maintains all existing fallback mechanisms
- Ensures artist and piece always match (atomic selection)
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
    
    NEW FEATURES:
    - Reads recent_music.json to avoid duplicates
    - Excludes recent artist/piece from selection pool
    - Maintains atomic artist/piece selection
    - Enhanced fallback mechanisms
    """
    
    def __init__(self, youtube_tool=None, gemini_tool=None):
        self.youtube_tool = youtube_tool
        self.gemini_tool = gemini_tool
        
        # Path to recent music tracking file
        self.recent_music_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "recent_music.json"
        )
        
        # Classical composers database with heritage mapping
        self.classical_database = [
            {
                "artist": "Johann Sebastian Bach",
                "search_name": "bach",
                "pieces": ["Air on the G String", "Brandenburg Concerto No. 3", "Well-Tempered Clavier"],
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
                "artist": "Giacomo Puccini",
                "search_name": "puccini",
                "pieces": ["Nessun Dorma (from Turandot)", "O Mio Babbino Caro", "La Bohème"],
                "heritage_tags": ["italian", "european"],
                "conversation_starters": [
                    "Puccini's operas tell such beautiful stories",
                    "This music feels so dramatic and romantic"
                ],
                "fun_fact": "Puccini wrote some of the most beloved operas in history"
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
                "artist": "Giuseppe Verdi",
                "search_name": "verdi",
                "pieces": ["La Traviata", "Aida", "Rigoletto"],
                "heritage_tags": ["italian", "european"],
                "conversation_starters": [
                    "Verdi's music is so powerful and moving",
                    "This brings back memories of grand opera houses"
                ],
                "fun_fact": "Verdi is considered the greatest Italian opera composer"
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
            },
            {
                "artist": "Pyotr Ilyich Tchaikovsky",
                "search_name": "tchaikovsky",
                "pieces": ["Swan Lake", "1812 Overture", "The Nutcracker Suite"],
                "heritage_tags": ["russian", "european"],
                "conversation_starters": [
                    "Tchaikovsky's music is so dramatic and emotional",
                    "This music tells such wonderful stories"
                ],
                "fun_fact": "Tchaikovsky wrote three of the most famous ballets ever"
            }
        ]
        
        logger.info("🎵 Agent 4A: Music Curation initialized with recent selection avoidance")
    
    def _load_recent_music(self) -> Dict[str, Any]:
        """Load recent music selection to avoid repetition"""
        
        try:
            if os.path.exists(self.recent_music_file):
                with open(self.recent_music_file, 'r', encoding='utf-8') as f:
                    recent_data = json.load(f)
                    
                recent_artist = recent_data.get('artist', '')
                recent_piece = recent_data.get('piece_title', '')
                
                logger.info(f"📖 Previous selection: {recent_artist} - {recent_piece}")
                return recent_data
            else:
                logger.info("📖 No recent music file found - first time selection")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error loading recent music: {e}")
            return {}

    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution with recent selection avoidance
        """
        try:
            logger.info("🎵 Agent 4A: Starting music curation with repetition avoidance")
            
            # Load recent selection to avoid repetition
            recent_music = self._load_recent_music()
            recent_artist = recent_music.get("artist", "").lower()
            recent_piece = recent_music.get("piece_title", "").lower()
            
            # Extract context with safe data handling
            heritage = self._extract_heritage(enhanced_profile)
            qloo_artists = self._extract_qloo_artists_safe(enhanced_profile)
            
            logger.info(f"👤 Heritage: {heritage}")
            logger.info(f"🎼 Qloo artists available: {len(qloo_artists)}")
            logger.info(f"🚫 Avoiding recent: {recent_artist} ({recent_piece})")
            
            # CRITICAL FIX: Select composer avoiding recent choice
            selected_composer = self._select_composer_avoiding_recent(
                heritage, qloo_artists, recent_artist, recent_piece
            )
            
            # ATOMIC SELECTION: Piece is ALWAYS from the selected composer
            selected_piece = self._select_piece_avoiding_recent(
                selected_composer, recent_artist, recent_piece
            )
            
            logger.info(f"✅ NEW SELECTION: {selected_composer['artist']} - {selected_piece}")
            
            # Verify they match (sanity check)
            if self._verify_artist_piece_match(selected_composer["artist"], selected_piece):
                logger.info("✅ Artist and piece match verified")
            else:
                logger.error("❌ CRITICAL: Artist/piece mismatch detected!")
            
            # Create YouTube search query
            search_query = f"{selected_composer['search_name']} {selected_piece.lower()}"
            
            # Search YouTube
            youtube_result = await self._search_youtube(search_query)
            
            # Build final result
            result = {
                "music_content": {
                    "artist": selected_composer["artist"],
                    "piece_title": selected_piece,
                    "search_query": search_query,
                    "youtube_url": youtube_result.get("url"),
                    "youtube_title": youtube_result.get("title"),
                    "youtube_embed": youtube_result.get("embedUrl"),
                    "conversation_starters": selected_composer["conversation_starters"],
                    "fun_fact": selected_composer["fun_fact"]
                },
                "metadata": {
                    "heritage_match": self._heritage_matches(heritage, selected_composer),
                    "selection_method": "recent_avoidance",
                    "avoided_repetition": bool(recent_artist),
                    "recent_artist": recent_artist,
                    "agent": "music_curation_agent_4a_fixed"
                }
            }
            
            logger.info(f"🎵 ✅ Result: {result['music_content']['artist']} - {result['music_content']['piece_title']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Music curation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self._emergency_fallback()
    
    def _select_composer_avoiding_recent(self, heritage: str, qloo_artists: List[str], 
                                       recent_artist: str, recent_piece: str) -> Dict[str, Any]:
        """
        Select composer while avoiding recent selection
        """
        
        # Filter out recent artist from available options
        available_composers = []
        for composer in self.classical_database:
            composer_name_lower = composer["artist"].lower()
            search_name_lower = composer["search_name"].lower()
            
            # Skip if this is the recent artist
            if (composer_name_lower == recent_artist or 
                search_name_lower == recent_artist or
                recent_artist in composer_name_lower):
                logger.info(f"🚫 Skipping recent artist: {composer['artist']}")
                continue
            
            available_composers.append(composer)
        
        # If we filtered out everything, use full list (better than repeating)
        if not available_composers:
            available_composers = self.classical_database
            logger.warning("⚠️ All composers were recent - using full list to avoid complete failure")
        
        logger.info(f"📋 Available composers after filtering: {len(available_composers)}")
        
        # Apply heritage priority to available composers
        return self._select_best_composer_from_pool(heritage, qloo_artists, available_composers)
    
    def _select_best_composer_from_pool(self, heritage: str, qloo_artists: List[str], 
                                      composer_pool: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Select best composer from available pool with heritage priority
        """
        
        # First try: Perfect match (heritage + Qloo) from available pool
        for composer in composer_pool:
            composer_name = composer["search_name"]
            heritage_match = any(tag in heritage.lower() for tag in composer["heritage_tags"])
            qloo_match = any(composer_name in qloo_artist.lower() for qloo_artist in qloo_artists)
            
            if heritage_match and qloo_match:
                logger.info(f"✅ Perfect match (heritage + Qloo): {composer['artist']}")
                return composer
        
        # Second try: Heritage match from available pool
        heritage_matches = []
        for composer in composer_pool:
            if any(tag in heritage.lower() for tag in composer["heritage_tags"]):
                heritage_matches.append(composer)
        
        if heritage_matches:
            selected = random.choice(heritage_matches)
            logger.info(f"✅ Heritage match: {selected['artist']} for {heritage}")
            return selected
        
        # Third try: Any Qloo match from available pool
        for composer in composer_pool:
            composer_name = composer["search_name"]
            if any(composer_name in qloo_artist.lower() for qloo_artist in qloo_artists):
                logger.info(f"✅ Qloo match found: {composer['artist']}")
                return composer
        
        # Fourth try: Random from available pool
        selected = random.choice(composer_pool)
        logger.info(f"✅ Random selection from available: {selected['artist']}")
        return selected
    
    def _select_piece_avoiding_recent(self, composer: Dict[str, Any], 
                                    recent_artist: str, recent_piece: str) -> str:
        """
        Select piece from composer, avoiding recent piece if same artist
        """
        
        available_pieces = composer["pieces"].copy()
        composer_name_lower = composer["artist"].lower()
        
        # If this is the same composer as recent, try to avoid the same piece
        if composer_name_lower == recent_artist:
            # Remove recent piece from options
            available_pieces = [
                piece for piece in available_pieces 
                if piece.lower() != recent_piece
            ]
            
            # If we filtered out everything, use all pieces (better than failing)
            if not available_pieces:
                available_pieces = composer["pieces"]
                logger.warning(f"⚠️ All pieces for {composer['artist']} were recent - using all pieces")
            else:
                logger.info(f"✅ Avoided recent piece '{recent_piece}' for {composer['artist']}")
        
        selected_piece = random.choice(available_pieces)
        logger.info(f"🎼 Selected piece: {selected_piece}")
        return selected_piece
    
    def _verify_artist_piece_match(self, artist: str, piece: str) -> bool:
        """Verify that the artist and piece actually match"""
        
        artist_lower = artist.lower()
        
        # Find the composer in database
        for composer in self.classical_database:
            if composer["artist"].lower() == artist_lower:
                # Check if piece is in their repertoire
                return piece in composer["pieces"]
        
        return False
    
    def _extract_heritage(self, enhanced_profile: Dict[str, Any]) -> str:
        """Safely extract heritage from profile - FIXED to check all possible locations"""
        try:
            # Check multiple possible locations for heritage
            heritage_locations = [
                enhanced_profile.get("patient_info", {}).get("cultural_heritage"),
                enhanced_profile.get("patient_info", {}).get("heritage"),
                enhanced_profile.get("profile", {}).get("cultural_heritage"),
                enhanced_profile.get("heritage"),
                enhanced_profile.get("cultural_heritage")
            ]
            
            # Return first non-empty heritage found
            for heritage in heritage_locations:
                if heritage and heritage.strip():
                    logger.info(f"✅ Heritage found: {heritage}")
                    return heritage.lower()
            
            logger.warning("⚠️ No heritage found in any location")
            return "unknown"
            
        except Exception as e:
            logger.warning(f"⚠️ Heritage extraction failed: {e}")
            return "unknown"
    
    def _extract_qloo_artists_safe(self, enhanced_profile: Dict[str, Any]) -> List[str]:
        """
        Safely extract Qloo artist data with proper type checking
        """
        try:
            qloo_data = enhanced_profile.get("qloo_cultural_recs", {})
            
            if not isinstance(qloo_data, dict):
                logger.warning("⚠️ Qloo data is not a dictionary")
                return []
            
            # Try to extract artists safely
            if "artists" in qloo_data:
                artists_data = qloo_data["artists"]
                
                if isinstance(artists_data, list):
                    # Extract names from list of artist objects
                    artist_names = []
                    for artist in artists_data:
                        if isinstance(artist, dict) and "name" in artist:
                            artist_names.append(artist["name"])
                        elif isinstance(artist, str):
                            artist_names.append(artist)
                    
                    logger.info(f"✅ Extracted {len(artist_names)} Qloo artists")
                    return artist_names
                
                elif isinstance(artists_data, dict):
                    # Handle case where artists is a dict
                    return list(artists_data.keys())
            
            logger.warning("⚠️ No valid artists found in Qloo data")
            return []
            
        except Exception as e:
            logger.error(f"❌ Qloo artist extraction failed: {e}")
            return []
    
    def _heritage_matches(self, heritage: str, composer: Dict[str, Any]) -> bool:
        """Check if heritage matches composer"""
        return any(tag in heritage.lower() for tag in composer["heritage_tags"])
    
    async def _search_youtube(self, search_query: str) -> Optional[Dict[str, Any]]:
        """Search YouTube using the Creative Commons API"""
        
        if not self.youtube_tool:
            logger.warning("⚠️ YouTube tool not available")
            return self._youtube_fallback()
        
        try:
            logger.info(f"🔍 YouTube search: {search_query}")
            
            results = await self.youtube_tool.search_videos(
                query=f"{search_query} classical music",
                max_results=1,
                audio_only=True
            )
            
            if results and len(results) > 0:
                video = results[0]
                logger.info(f"✅ Found YouTube video: {video.get('title', '')[:50]}...")
                return {
                    "url": f"https://www.youtube.com/watch?v={video.get('videoId', '')}",
                    "title": video.get("title", "Classical Music"),
                    "embedUrl": f"https://www.youtube.com/embed/{video.get('videoId', '')}",
                    "duration": video.get("duration", "unknown"),
                    "channelTitle": video.get("channelTitle", ""),
                    "license": "Creative Commons"
                }
            else:
                logger.warning("⚠️ No YouTube videos found")
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
        
        # Default to Mozart (different from Bach to provide variety)
        default_composer = self.classical_database[1]  # Mozart
        default_piece = default_composer["pieces"][0]    # His first piece
        
        return {
            "music_content": {
                "artist": default_composer["artist"],
                "piece_title": default_piece,
                "search_query": f"{default_composer['search_name']} {default_piece}",
                "youtube_url": None,
                "youtube_title": None,
                "youtube_embed": None,
                "conversation_starters": default_composer["conversation_starters"],
                "fun_fact": default_composer["fun_fact"]
            },
            "metadata": {
                "heritage_match": False,
                "selection_method": "emergency_fallback",
                "agent": "music_curation_agent_4a_fixed"
            }
        }

# Export the main class
__all__ = ["MusicCurationAgent"]