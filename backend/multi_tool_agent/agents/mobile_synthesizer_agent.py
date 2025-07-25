"""
Mobile Synthesizer Agent - COMPLETE with Enhanced Multi-Genre Music Selection
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

ENHANCEMENTS:
- Enhanced music selection from multiple genres (classical, jazz, easy listening)
- Weighted selection favoring calming music for dementia care
- Improved fallback options with classical emphasis
- Better variety logic with daily seeds
- Enhanced error handling and logging
"""

import logging
import json
import os
import random
import hashlib
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger FIRST
logger = logging.getLogger(__name__)

# Import theme manager for theme-aware functionality
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Mobile Synthesizer: theme_manager imported successfully")
except ImportError as e:
    logger.error(f"❌ Mobile Synthesizer: Failed to import theme_manager: {e}")
    theme_manager = None
except Exception as e:
    logger.error(f"❌ Mobile Synthesizer: Error with theme_manager: {e}")
    theme_manager = None

class MobileSynthesizerAgent:
    """
    Agent 6: Mobile Synthesizer with Enhanced Multi-Genre Music Selection
    
    ENHANCEMENTS:
    - Multi-genre music selection (classical, jazz, easy listening)
    - Weighted selection favoring calming music
    - Enhanced fallbacks with classical emphasis
    - Daily variety with consistent seeds
    - Improved data structure handling
    """
    
    def __init__(self):
        self.fallback_data = self._load_enhanced_fallback_content()
        logger.info("Mobile Synthesizer initialized with enhanced multi-genre music selection")
    
    async def run(self, audio_content: Dict[str, Any], 
                  visual_content: Dict[str, Any], 
                  sensory_content: Dict[str, Any],
                  daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for the Enhanced Mobile Synthesizer Agent
        """
        logger.info("🚀 Mobile Synthesizer Agent starting with enhanced multi-genre music")
        return self.synthesize_dashboard_content(audio_content, visual_content, sensory_content, daily_theme)
    
    def _load_enhanced_fallback_content(self) -> Dict[str, Any]:
        """Load enhanced fallback content with classical music emphasis."""
        try:
            fallback_path = os.path.join(os.path.dirname(__file__), "../../data/fallback_content.json")
            with open(fallback_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load fallback content: {e}")
            return self._get_enhanced_hardcoded_fallbacks()
    
    def _get_enhanced_hardcoded_fallbacks(self) -> Dict[str, Any]:
        """Enhanced hardcoded fallbacks with classical music emphasis."""
        return {
            "music": [
                # Classical music (most therapeutic)
                {"artist": "Johann Sebastian Bach", "song": "Air on the G String", "genre": "classical", "youtube_url": ""},
                {"artist": "Wolfgang Amadeus Mozart", "song": "Eine kleine Nachtmusik", "genre": "classical", "youtube_url": ""},
                {"artist": "Ludwig van Beethoven", "song": "Moonlight Sonata", "genre": "classical", "youtube_url": ""},
                {"artist": "Frédéric Chopin", "song": "Nocturne in E-flat", "genre": "classical", "youtube_url": ""},
                
                # Jazz standards (nostalgic)
                {"artist": "Frank Sinatra", "song": "The Way You Look Tonight", "genre": "jazz", "youtube_url": ""},
                {"artist": "Ella Fitzgerald", "song": "Dream a Little Dream", "genre": "jazz", "youtube_url": ""},
                {"artist": "Nat King Cole", "song": "Unforgettable", "genre": "jazz", "youtube_url": ""},
                
                # Easy listening (gentle)
                {"artist": "Perry Como", "song": "It's Impossible", "genre": "easy_listening", "youtube_url": ""}
            ],
            "tv_shows": [
                {"name": "I Love Lucy", "genre": "Comedy", "youtube_url": ""},
                {"name": "The Andy Griffith Show", "genre": "Comedy", "youtube_url": ""},
                {"name": "The Ed Sullivan Show", "genre": "Variety", "youtube_url": ""}
            ],
            "recipes": [{
                "name": "Simple Comfort Food",
                "ingredients": ["Basic ingredients"],
                "instructions": ["Simple preparation"],
                "notes": {"text": "A comforting choice", "theme": "food"},
                "conversation_starters": ["What comfort foods do you remember?"]
            }]
        }
    
    def synthesize_dashboard_content(self, audio_content: Dict[str, Any], 
                                   visual_content: Dict[str, Any], 
                                   sensory_content: Dict[str, Any],
                                   daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize content for mobile dashboard with enhanced music selection
        """
        
        current_theme = daily_theme.get("theme_of_the_day", {})
        theme_name = current_theme.get("name", "Unknown")
        
        logger.info(f"🎯 Synthesizing dashboard content for theme: {theme_name}")
        
        try:
            # Enhanced content selection with multi-genre music
            selected_content = {
                "music": self._select_enhanced_music_content(audio_content, current_theme),
                "tv_show": self._select_tv_content(visual_content, current_theme),
                "recipe": self._select_recipe_content(sensory_content, current_theme),
                "theme_info": {
                    "name": theme_name,
                    "description": current_theme.get("description", ""),
                    "id": current_theme.get("id", "")
                }
            }
            
            # Generate theme-aware conversation starters
            conversation_starters = self._generate_conversation_starters(selected_content, current_theme)
            
            # Create enhanced dashboard response
            dashboard_result = {
                "status": "success",
                "dashboard_content": {
                    "theme_of_the_day": {
                        "name": theme_name,
                        "description": current_theme.get("description", "Today's theme for memory sharing"),
                        "id": current_theme.get("id", "")
                    },
                    
                    # Main content cards
                    "music": selected_content["music"],
                    "tv_show": selected_content["tv_show"], 
                    "recipe": selected_content["recipe"],
                    "conversation_starter": {
                        "question": conversation_starters[0] if conversation_starters else "Tell me about a favorite memory.",
                        "alternatives": conversation_starters[1:3] if len(conversation_starters) > 1 else [],
                        "theme_connection": f"Connected to today's {theme_name} theme"
                    },
                    
                    "generation_metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "theme_selection_quality": self._assess_content_quality(selected_content),
                        "agent": "MobileSynthesizer",
                        "version": "enhanced_multi_genre_music",
                        "music_enhancement": "classical_jazz_easy_listening_selection"
                    }
                },
                
                # Backend processing info
                "content": {
                    "mobile_experience": {
                        "dashboard_content": {
                            "theme_of_the_day": {
                                "name": theme_name,
                                "description": current_theme.get("description", "Today's theme"),
                                "id": current_theme.get("id", "")
                            },
                            "music": selected_content["music"],
                            "tv_show": selected_content["tv_show"],
                            "recipe": selected_content["recipe"],
                            "conversation_starter": {
                                "question": conversation_starters[0] if conversation_starters else "Tell me about a favorite memory.",
                                "theme_connection": f"Connected to today's {theme_name} theme"
                            }
                        }
                    }
                }
            }
            
            logger.info(f"✅ Dashboard content synthesized successfully for theme: {theme_name}")
            logger.info(f"🎵 Selected music: {selected_content['music'].get('artist', 'Unknown')} - {selected_content['music'].get('song', 'Unknown')} ({selected_content['music'].get('genre', 'unknown')})")
            logger.info(f"📺 Selected TV show: {selected_content['tv_show'].get('name', 'Unknown')}")
            logger.info(f"🍽️ Selected recipe: {selected_content['recipe'].get('name', 'Unknown')}")
            
            return dashboard_result
            
        except Exception as e:
            logger.error(f"❌ Error synthesizing dashboard content: {e}")
            return self._generate_fallback_dashboard(current_theme)
    
    def _select_enhanced_music_content(self, audio_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Select music from multiple genres with therapeutic weighting"""
        logger.info("🎵 Extracting music content from enhanced multi-genre Qloo results")
        
        try:
            # Extract from correct Qloo data structure
            qloo_intelligence = audio_content.get("qloo_intelligence", {})
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # Extract from nested "entities" array (now contains multiple genres)
            artists_data = cultural_recommendations.get("artists", {})
            artists = artists_data.get("entities", []) if isinstance(artists_data, dict) else []
            
            logger.info(f"🔍 Found {len(artists)} artists from multiple genres")
            
            # 🎭 DEBUG: Show all available artists with their genres
            if artists:
                genres_found = {}
                for artist in artists:
                    genre = artist.get("music_genre", "unknown")
                    if genre not in genres_found:
                        genres_found[genre] = []
                    genres_found[genre].append(artist.get("name", "Unknown"))
                
                for genre, artist_names in genres_found.items():
                    sample_display = ', '.join(artist_names[:3]) + ('...' if len(artist_names) > 3 else '')
                    logger.info(f"🎼 {genre.title()} artists ({len(artist_names)}): {sample_display}")
            
            if artists and len(artists) > 0:
                # 🎯 ENHANCED: Variety selection with therapeutic genre weighting
                today = date.today().isoformat()
                theme_name = current_theme.get("name", "default")
                seed_string = f"{today}-{theme_name}-music"
                daily_seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)
                
                # 🎵 ENHANCED: Weighted selection favoring calming genres
                weighted_artists = []
                genre_weights = {"classical": 3, "jazz": 2, "easy_listening": 1}  # Classical gets 3x weight
                
                for artist in artists:
                    genre = artist.get("music_genre", "unknown")
                    weight = genre_weights.get(genre, 1)
                    
                    # Add multiple copies based on therapeutic value
                    weighted_artists.extend([artist] * weight)
                
                # Use daily seed for consistent but varied selection
                random.seed(daily_seed)
                selected_artist = random.choice(weighted_artists)
                
                artist_name = selected_artist.get("name", "Unknown Artist")
                artist_genre = selected_artist.get("music_genre", "unknown")
                selection_rationale = selected_artist.get("selection_rationale", "")
                
                logger.info(f"✅ Selected artist: {artist_name} ({artist_genre})")
                logger.info(f"🎯 Selection rationale: {selection_rationale}")
                logger.info(f"🎲 Selected from {len(artists)} total artists ({len(weighted_artists)} weighted options)")
                
                # Map embeddable_url to youtube_url for frontend
                youtube_url = selected_artist.get("embeddable_url", "")
                
                return {
                    "artist": artist_name,
                    "song": selected_artist.get("title", selected_artist.get("name", "Unknown Song")),
                    "youtube_url": youtube_url,
                    "year": selected_artist.get("properties", {}).get("year"),
                    "genre": artist_genre,
                    "description": f"Music by {artist_name}",
                    "theme_connection": f"Therapeutic {artist_genre} music for {current_theme.get('name', 'today')}'s theme",
                    "selection_rationale": selection_rationale,
                    "source": "qloo_intelligence_multi_genre",
                    "selection_method": "daily_variety_weighted_calming",
                    "available_options": len(artists),
                    "weighted_options": len(weighted_artists)
                }
        except Exception as e:
            logger.warning(f"Error selecting enhanced music content from Qloo: {e}")
        
        # Enhanced fallback with classical music emphasis
        logger.info("🔄 Using enhanced fallback music with classical emphasis")
        enhanced_fallback_options = self.fallback_data.get("music", [])
        
        # Weight fallback selection toward classical even in fallback
        weighted_fallback = []
        for option in enhanced_fallback_options:
            genre = option.get("genre", "unknown")
            if genre == "classical":
                weighted_fallback.extend([option] * 3)  # 3x weight for classical
            elif genre == "jazz":
                weighted_fallback.extend([option] * 2)  # 2x weight for jazz
            else:
                weighted_fallback.append(option)  # 1x weight for others
        
        # Pick different fallback each day with classical preference
        daily_fallback_seed = hash(date.today().isoformat())
        random.seed(daily_fallback_seed)
        selected_fallback = random.choice(weighted_fallback) if weighted_fallback else enhanced_fallback_options[0]
        
        logger.info(f"🎲 Selected enhanced fallback: {selected_fallback.get('artist', 'Unknown')} ({selected_fallback.get('genre', 'unknown')})")
        
        return {
            "artist": selected_fallback.get("artist", "Classical Artist"),
            "song": selected_fallback.get("song", "Calming Song"),
            "youtube_url": selected_fallback.get("youtube_url", ""),
            "genre": selected_fallback.get("genre", "classical"),
            "description": f"Music by {selected_fallback.get('artist', 'Classical Artist')}",
            "theme_connection": f"Calming {selected_fallback.get('genre', 'classical')} music for {current_theme.get('name', 'today')}'s theme",
            "selection_rationale": "Calming and therapeutic for dementia care",
            "source": "enhanced_fallback",
            "selection_method": "daily_fallback_classical_weighted"
        }
    
    def _select_tv_content(self, visual_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select TV content from Qloo results or fallback"""
        logger.info("📺 Extracting TV content from Qloo results")
        
        try:
            # Extract from correct Qloo data structure
            qloo_intelligence = visual_content.get("qloo_intelligence", {})
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # Extract from nested "entities" array
            tv_shows_data = cultural_recommendations.get("tv_shows", {})
            tv_shows = tv_shows_data.get("entities", []) if isinstance(tv_shows_data, dict) else []
            
            logger.info(f"🔍 Found {len(tv_shows)} TV shows from Qloo")
            
            if tv_shows and len(tv_shows) > 0:
                # Use daily variety for TV show selection too
                today = date.today().isoformat()
                theme_name = current_theme.get("name", "default")
                seed_string = f"{today}-{theme_name}-tv"
                daily_seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)
                
                random.seed(daily_seed)
                selected_show = random.choice(tv_shows)
                show_name = selected_show.get("name", "Unknown Show")
                
                logger.info(f"✅ Selected TV show from Qloo: {show_name}")
                
                # Map embeddable_url to youtube_url for frontend
                youtube_url = selected_show.get("embeddable_url", "")
                
                return {
                    "name": show_name,
                    "youtube_url": youtube_url,
                    "genre": selected_show.get("properties", {}).get("genre"),
                    "year": selected_show.get("properties", {}).get("year"),
                    "description": f"Entertainment from the era",
                    "theme_connection": f"Perfect viewing for {current_theme.get('name', 'today')}'s theme",
                    "source": "qloo_intelligence"
                }
        except Exception as e:
            logger.warning(f"Error selecting TV content from Qloo: {e}")
        
        # Fallback with variety
        logger.info("🔄 Using fallback TV content")
        fallback_tv_options = self.fallback_data.get("tv_shows", [
            {"name": "I Love Lucy", "genre": "Comedy", "youtube_url": ""},
            {"name": "The Andy Griffith Show", "genre": "Comedy", "youtube_url": ""},
            {"name": "The Ed Sullivan Show", "genre": "Variety", "youtube_url": ""}
        ])
        
        # Daily variety for fallback too
        daily_seed = hash(date.today().isoformat()) % len(fallback_tv_options)
        selected_fallback = fallback_tv_options[daily_seed]
        
        return {
            "name": selected_fallback.get("name", "Classic Television"),
            "youtube_url": selected_fallback.get("youtube_url", ""),
            "genre": selected_fallback.get("genre"),
            "description": "Classic family entertainment",
            "theme_connection": f"Nostalgic viewing for {current_theme.get('name', 'today')}'s theme",
            "source": "fallback"
        }
    
    def _select_recipe_content(self, sensory_content: Dict[str, Any], 
                             current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select recipe content with improved data structure navigation
        """
        
        logger.info(f"🔍 Selecting recipe content for theme: {current_theme.get('name', 'Unknown')}")
        
        # Improved recipe data extraction with better error handling
        recipe_data = None
        selection_method = "unknown"
        
        try:
            # Path 1: Enhanced gustatory content structure (expected from Agent 4)
            gustatory_content = sensory_content.get("content_by_sense", {}).get("gustatory", {})
            
            # Try primary recipe first (new enhanced structure)
            if gustatory_content.get("primary_recipe"):
                recipe_data = gustatory_content["primary_recipe"]
                selection_method = "primary_recipe"
                logger.info(f"✅ Found recipe via primary_recipe: {recipe_data.get('name', 'Unknown')}")
            
            # Fallback to elements array
            elif gustatory_content.get("elements") and len(gustatory_content["elements"]) > 0:
                recipe_data = gustatory_content["elements"][0]
                selection_method = "gustatory_elements"
                logger.info(f"✅ Found recipe via gustatory elements: {recipe_data.get('name', 'Unknown')}")
            
            # Path 2: Direct sensory content structure (older format)
            elif sensory_content.get("primary_recipe"):
                recipe_data = sensory_content["primary_recipe"]
                selection_method = "direct_primary_recipe"
                logger.info(f"✅ Found recipe via direct primary_recipe: {recipe_data.get('name', 'Unknown')}")
            
            # Path 3: Sensory elements fallback
            elif sensory_content.get("sensory_elements"):
                sensory_elements = sensory_content["sensory_elements"]
                for element in sensory_elements:
                    if element.get("sense") == "gustatory" and element.get("item"):
                        recipe_data = element["item"]
                        selection_method = "sensory_elements"
                        logger.info(f"✅ Found recipe via sensory elements: {recipe_data.get('name', 'Unknown')}")
                        break
            
            if recipe_data:
                logger.info(f"🍽️ Recipe selection complete: '{recipe_data.get('name', 'Unknown')}' (method: {selection_method})")
                
                return {
                    "name": recipe_data.get("name", "Unknown Recipe"),
                    "ingredients": recipe_data.get("ingredients", []),
                    "instructions": recipe_data.get("instructions", []),
                    "total_time": recipe_data.get("total_time", "Unknown"),
                    "notes": recipe_data.get("notes", {}),
                    "conversation_starters": recipe_data.get("conversation_starters", []),
                    "theme_connection": recipe_data.get("theme_connection", f"Perfect recipe for {current_theme.get('name', 'today')}'s theme"),
                    "description": f"A {current_theme.get('name', 'themed')} recipe to share and enjoy",
                    "source": "sensory_content",
                    "selection_method": selection_method
                }
                
        except Exception as e:
            logger.warning(f"Error selecting recipe content: {e}")
        
        # Final fallback
        logger.info("🔄 Using fallback recipe content")
        fallback_recipe = self.fallback_data.get("recipes", [{}])[0]
        return {
            "name": fallback_recipe.get("name", "Simple Comfort Food"),
            "ingredients": fallback_recipe.get("ingredients", ["Basic ingredients"]),
            "instructions": fallback_recipe.get("instructions", ["Simple preparation"]),
            "total_time": "15 minutes",
            "notes": fallback_recipe.get("notes", {"text": "A comforting choice"}),
            "conversation_starters": fallback_recipe.get("conversation_starters", ["What comfort foods do you remember?"]),
            "theme_connection": f"Comforting recipe for {current_theme.get('name', 'today')}'s theme",
            "description": "A simple, comforting recipe to share",
            "source": "fallback"
        }
    
    def _generate_conversation_starters(self, selected_content: Dict[str, Any], current_theme: Dict[str, Any]) -> List[str]:
        """Generate theme-aware conversation starters"""
        
        theme_name = current_theme.get("name", "memories")
        
        # Base conversation starters from content
        starters = []
        
        # Music-based starters
        music = selected_content.get("music", {})
        if music.get("artist"):
            starters.append(f"Do you remember listening to {music['artist']}?")
            if music.get("genre") == "classical":
                starters.append(f"What classical music brings you peace?")
            elif music.get("genre") == "jazz":
                starters.append(f"Did you ever dance to jazz music?")
        
        # TV show-based starters
        tv_show = selected_content.get("tv_show", {})
        if tv_show.get("name"):
            starters.append(f"Did you watch {tv_show['name']} with your family?")
        
        # Recipe-based starters
        recipe = selected_content.get("recipe", {})
        if recipe.get("name"):
            starters.append(f"Have you ever made something like {recipe['name']}?")
        
        # Theme-specific starters
        theme_starters = {
            "Travel": ["What's the most memorable trip you've taken?", "Tell me about a place you'd love to visit again."],
            "Family": ["Tell me about your favorite family tradition.", "What made family gatherings special?"],
            "Music": ["What song always makes you smile?", "Did you play any instruments?"],
            "Food": ["What's your favorite comfort food?", "Tell me about a memorable meal."],
            "Pets": ["Tell me about a pet you loved.", "What animals bring you joy?"],
            "Seasons": ["What's your favorite season and why?", "What seasonal activities do you enjoy?"]
        }
        
        if theme_name in theme_starters:
            starters.extend(theme_starters[theme_name])
        
        # Ensure we have at least 3 starters
        while len(starters) < 3:
            starters.append(f"Tell me about a happy memory related to {theme_name.lower()}.")
        
        return starters[:5]  # Return top 5
    
    def _assess_content_quality(self, selected_content: Dict[str, Any]) -> str:
        """Assess the quality of content selection"""
        
        sources = [
            selected_content.get("music", {}).get("source", "unknown"),
            selected_content.get("tv_show", {}).get("source", "unknown"),
            selected_content.get("recipe", {}).get("source", "unknown")
        ]
        
        qloo_count = sum(1 for s in sources if "qloo" in s)
        
        if qloo_count >= 2:
            return "high_quality_mostly_qloo"
        elif qloo_count >= 1:
            return "medium_quality_mixed_sources"
        else:
            return "fallback_quality_all_fallbacks"
    
    def _generate_fallback_dashboard(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete fallback dashboard when synthesis fails"""
        
        logger.warning("🔄 Generating complete fallback dashboard")
        
        theme_name = current_theme.get("name", "Memory Lane")
        
        return {
            "status": "fallback",
            "dashboard_content": {
                "theme_of_the_day": {
                    "name": theme_name,
                    "description": "Today's theme for memory sharing",
                    "id": current_theme.get("id", "fallback")
                },
                "music": {
                    "artist": "Johann Sebastian Bach",
                    "song": "Air on the G String",
                    "genre": "classical",
                    "youtube_url": "",
                    "description": "Calming classical music",
                    "source": "fallback"
                },
                "tv_show": {
                    "name": "I Love Lucy",
                    "genre": "Comedy",
                    "youtube_url": "",
                    "description": "Classic family entertainment",
                    "source": "fallback"
                },
                "recipe": {
                    "name": "Simple Comfort Food",
                    "ingredients": ["Basic ingredients"],
                    "instructions": ["Simple preparation"],
                    "source": "fallback"
                },
                "conversation_starter": {
                    "question": f"Tell me about a happy memory related to {theme_name.lower()}.",
                    "theme_connection": f"Connected to today's {theme_name} theme"
                }
            }
        }

# Export the main class
__all__ = ["MobileSynthesizerAgent"]