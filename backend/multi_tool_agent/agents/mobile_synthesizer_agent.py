"""
Mobile Synthesizer Agent - Clean Dashboard Only Response
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

Agent 6: Returns ONLY the clean dashboard, not all raw agent outputs
"""

import logging
import json
import os
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class MobileSynthesizerAgent:
    """
    Agent 6: Mobile Synthesizer - Clean Dashboard Only
    
    Returns exactly one result per category in a clean, small response structure.
    No more huge raw agent outputs - just the essential dashboard data.
    """
    
    def __init__(self):
        self.fallback_data = self._load_fallback_content()
        logger.info("Mobile Synthesizer initialized for clean dashboard responses")
    
    def _load_fallback_content(self) -> Dict[str, Any]:
        """Load fallback content from JSON file."""
        try:
            fallback_path = os.path.join(os.path.dirname(__file__), "../../data/fallback_content.json")
            with open(fallback_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load fallback content: {e}")
            return self._get_hardcoded_fallbacks()
    
    def _get_hardcoded_fallbacks(self) -> Dict[str, Any]:
        """Hardcoded fallbacks if JSON file unavailable."""
        return {
            "music": [
                {"artist": "Frank Sinatra", "song": "My Way", "youtube_url": "https://youtube.com/watch?v=qQzdAsjWGPg"},
                {"artist": "Ella Fitzgerald", "song": "Summertime", "youtube_url": "https://youtube.com/watch?v=MIDOmSQN6LU"}
            ],
            "tv_shows": [
                {"name": "I Love Lucy", "youtube_url": "https://youtube.com/watch?v=example1", "description": "Classic 1950s comedy"},
                {"name": "The Ed Sullivan Show", "youtube_url": "https://youtube.com/watch?v=example2", "description": "Variety show from the 1960s"}
            ],
            "conversation_starters": [
                "What was your favorite song when you were young?",
                "Tell me about TV shows your family watched together",
                "What foods remind you of home?"
            ]
        }
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create clean dashboard with exactly one result per category.
        
        Returns ONLY the dashboard - no raw agent outputs.
        """
        
        try:
            logger.info("📱 Agent 6: Creating clean dashboard (single results only)")
            
            # Set daily random seed for uniqueness (same as Qloo agent)
            today = date.today()
            daily_seed = hash(f"{today.year}-{today.month}-{today.day}")
            random.seed(daily_seed)
            
            # Select exactly one result per category
            selected_results = self._select_single_results(
                qloo_intelligence, sensory_content, photo_analysis, 
                consolidated_info.get("patient_profile", {})
            )
            
            # Create ONLY the clean dashboard - no extra data
            dashboard = {
                "music": selected_results["music"],
                "tv_show": selected_results["tv_show"], 
                "recipe": selected_results["recipe"],
                "photo": selected_results["photo"],
                "conversation_starters": selected_results["conversation_starters"]
            }
            
            logger.info("✅ Clean dashboard created - single results only")
            
            # Return ONLY the dashboard - not all the raw agent outputs
            return {
                "dashboard": dashboard,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "request_type": "dashboard",
                    "results_per_category": 1,
                    "daily_seed": daily_seed,
                    "fallbacks_used": selected_results.get("fallbacks_used", []),
                    "response_type": "clean_dashboard_only"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            return self._create_fallback_dashboard(consolidated_info)
    
    def _select_single_results(self, 
                              qloo_intelligence: Dict[str, Any],
                              sensory_content: Dict[str, Any], 
                              photo_analysis: Dict[str, Any],
                              patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Select exactly ONE result per category from filtered English data."""
        
        results = {}
        fallbacks_used = []
        
        # MUSIC: Pick one result from English-filtered data
        music_result = self._select_single_music(sensory_content)
        if not music_result:
            music_result = random.choice(self.fallback_data["music"])
            fallbacks_used.append("music")
        results["music"] = music_result
        logger.info(f"Selected music: {music_result.get('song', 'Unknown')}")
        
        # TV SHOWS: Pick one result from English-filtered data
        tv_result = self._select_single_tv_show(qloo_intelligence)
        if not tv_result:
            tv_result = random.choice(self.fallback_data["tv_shows"])
            fallbacks_used.append("tv_show")
        results["tv_show"] = tv_result
        logger.info(f"Selected TV show: {tv_result.get('name', 'Unknown')}")
        
        # RECIPE: Pick one result from recipes.json customization
        recipe_result = self._select_single_recipe(sensory_content)
        if not recipe_result:
            recipe_result = {
                "name": "Simple Comfort Recipe",
                "total_time": "15 minutes",
                "ingredients": ["Basic ingredients"],
                "instructions": ["Simple preparation steps"],
                "heritage_connection": "Traditional comfort food"
            }
            fallbacks_used.append("recipe")
        results["recipe"] = recipe_result
        logger.info(f"Selected recipe: {recipe_result.get('name', 'Unknown')}")
        
        # PHOTO: Pick one result (if available)
        photo_result = self._select_single_photo(photo_analysis, patient_profile)
        results["photo"] = photo_result
        
        # CONVERSATION: Generate 1-2 starters based on selected content
        conversation_starters = self._get_conversation_starters(
            results["music"], results["tv_show"], results["recipe"]
        )
        results["conversation_starters"] = conversation_starters
        
        results["fallbacks_used"] = fallbacks_used
        return results
    
    def _select_single_music(self, sensory_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select one music result from English-filtered sensory content."""
        try:
            music_data = sensory_content.get("content_by_sense", {}).get("auditory", {})
            if music_data.get("available") and music_data.get("elements"):
                # Pick one random music item (already English-filtered by Qloo agent)
                music_item = random.choice(music_data["elements"])
                
                # Extract clean data for dashboard
                return {
                    "artist": self._extract_artist_name(music_item.get("title", "Unknown Artist")),
                    "song": music_item.get("title", "Classic Song"),
                    "youtube_url": self._format_youtube_url(music_item.get("id", {})),
                    "description": music_item.get("description", "Era-appropriate music")[:100] + "..." if len(music_item.get("description", "")) > 100 else music_item.get("description", "")
                }
        except Exception as e:
            logger.warning(f"Music selection failed: {e}")
        return None
    
    def _extract_artist_name(self, title: str) -> str:
        """Extract artist name from YouTube title."""
        # Common patterns: "Artist - Song" or "Artist: Song" 
        if " - " in title:
            return title.split(" - ")[0].strip()
        elif ": " in title:
            return title.split(": ")[0].strip()
        elif " by " in title:
            parts = title.split(" by ")
            if len(parts) > 1:
                return parts[1].strip()
        
        # Default to first part if no clear pattern
        words = title.split()
        return " ".join(words[:2]) if len(words) >= 2 else title
    
    def _format_youtube_url(self, video_id: Dict[str, Any]) -> str:
        """Format YouTube URL from video ID object."""
        if isinstance(video_id, dict) and video_id.get("videoId"):
            return f"https://youtube.com/watch?v={video_id['videoId']}"
        return "https://youtube.com/results?search_query=classic+music"
    
    def _select_single_tv_show(self, qloo_intelligence: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select one TV show result from English-filtered Qloo data."""
        try:
            tv_data = qloo_intelligence.get("cultural_recommendations", {}).get("tv_shows", {})
            if tv_data.get("available") and tv_data.get("entities"):
                # Pick one random TV show (already English-filtered and randomized by Qloo agent)
                tv_show = random.choice(tv_data["entities"])
                
                return {
                    "name": tv_show.get("name", "Classic TV Show"),
                    "youtube_url": self._get_tv_youtube_link(tv_show.get("name", "Classic Show")),
                    "description": self._extract_english_description(tv_show)[:100] + "..." if len(self._extract_english_description(tv_show)) > 100 else self._extract_english_description(tv_show)
                }
        except Exception as e:
            logger.warning(f"TV show selection failed: {e}")
        return None
    
    def _extract_english_description(self, tv_show: Dict[str, Any]) -> str:
        """Extract English description from TV show properties."""
        properties = tv_show.get("properties", {})
        
        # Try main description first
        if "description" in properties:
            return properties["description"]
        
        # Try English short descriptions
        if "short_descriptions" in properties:
            for desc in properties["short_descriptions"]:
                if isinstance(desc, dict) and "en" in desc.get("languages", []):
                    return desc.get("value", "")
        
        return f"Classic show: {tv_show.get('name', 'TV Show')}"
    
    def _select_single_recipe(self, sensory_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select one recipe result from recipes.json customization."""
        try:
            recipe_data = sensory_content.get("content_by_sense", {}).get("gustatory", {})
            if recipe_data.get("available") and recipe_data.get("elements"):
                recipe = recipe_data["elements"][0]  # Take the customized recipe
                
                return {
                    "name": recipe.get("name", "Simple Recipe"),
                    "total_time": recipe.get("total_time", "20 minutes"),
                    "ingredients": recipe.get("ingredients", [])[:5],  # Max 5 for clean display
                    "instructions": recipe.get("instructions", [])[:6],  # Max 6 steps for clean display
                    "heritage_connection": recipe.get("cultural_context", "Comfort food"),
                    "description": recipe.get("description", "Simple, comforting recipe")
                }
        except Exception as e:
            logger.warning(f"Recipe selection failed: {e}")
        return None
    
    def _select_single_photo(self, photo_analysis: Dict[str, Any], patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Select one photo result."""
        try:
            # If photo analysis available, use it
            if photo_analysis.get("vision_analysis", {}).get("objects"):
                return {
                    "title": "Photo of the Day",
                    "path": photo_analysis.get("photo_path", "/static/default/photo.jpg"),
                    "description": "Personal memory photo"
                }
            
            # Use from patient profile if available
            photo_library = patient_profile.get("photo_library", [])
            if photo_library:
                return {
                    "title": "Memory Photo",
                    "path": random.choice(photo_library),
                    "description": "From your photo collection"
                }
        except Exception as e:
            logger.warning(f"Photo selection failed: {e}")
        
        # Default photo
        return {
            "title": "Today's Photo",
            "path": "/static/default/photo.jpg",
            "description": "Peaceful image for today"
        }
    
    def _get_conversation_starters(self, music: Dict[str, Any], tv_show: Dict[str, Any], recipe: Dict[str, Any]) -> List[str]:
        """Generate 1-2 conversation starters based on selected content."""
        starters = []
        
        try:
            if music and music.get("song"):
                starters.append(f"Do you remember dancing to songs like '{music['song']}'?")
            elif music and music.get("artist"):
                starters.append(f"What do you think of {music['artist']} music?")
            
            if tv_show and tv_show.get("name"):
                starters.append(f"Did you ever watch shows like '{tv_show['name']}'?")
            
            if recipe and recipe.get("name") and len(starters) < 2:
                starters.append(f"Does '{recipe['name']}' remind you of cooking with family?")
            
            # If no specific starters generated, use general ones
            if not starters:
                starters = random.sample(self.fallback_data.get("conversation_starters", [
                    "What was your favorite song when you were young?",
                    "Tell me about your family's favorite recipes"
                ]), 2)
                
        except Exception as e:
            logger.warning(f"Conversation starter generation failed: {e}")
            starters = ["Tell me about your day", "What makes you smile?"]
        
        return starters[:2]  # Max 2 conversation starters
    
    def _get_tv_youtube_link(self, show_name: str) -> str:
        """Generate YouTube search link for TV show."""
        search_query = show_name.replace(" ", "+")
        return f"https://youtube.com/results?search_query={search_query}+classic+episodes"
    
    def _create_fallback_dashboard(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete fallback dashboard when everything fails."""
        logger.warning("Creating complete fallback dashboard")
        
        return {
            "dashboard": {
                "music": random.choice(self.fallback_data["music"]),
                "tv_show": random.choice(self.fallback_data["tv_shows"]),
                "recipe": {
                    "name": "Simple Comfort Recipe",
                    "total_time": "15 minutes",
                    "ingredients": ["Basic ingredients as available"],
                    "instructions": ["Simple preparation"],
                    "heritage_connection": "Traditional comfort food"
                },
                "photo": {
                    "title": "Today's Photo",
                    "path": "/static/default/photo.jpg",
                    "description": "Peaceful image"
                },
                "conversation_starters": random.sample(self.fallback_data["conversation_starters"], 2)
            },
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "request_type": "dashboard",
                "status": "complete_fallback",
                "fallbacks_used": ["music", "tv_show", "recipe", "conversation"],
                "response_type": "clean_dashboard_only"
            }
        }