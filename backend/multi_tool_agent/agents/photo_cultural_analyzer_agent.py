"""
Revised Photo Cultural Analyzer Agent - Places Photos Only
File: backend/multi_tool_agent/agents/photo_cultural_analyzer_agent.py

REVISED: Now analyzes ONLY Qloo place photos with Google Vision
- Finds theme-relevant places from Qloo results
- Analyzes place photos with Google Vision API
- Provides rich visual context for conversation starters
- Clean fallback for rural areas with no places
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class PhotoCulturalAnalyzerAgent:
    """
    Agent 5: Photo Cultural Analyzer - REVISED for Places Only
    
    NEW ROLE: Analyze place photos from Qloo results using Google Vision
    - Takes Qloo intelligence containing places data
    - Finds theme-relevant places  
    - Analyzes place photos with Vision API
    - Returns rich visual analysis for conversation starters
    """
    
    def __init__(self, vision_tool):
        self.vision_tool = vision_tool
        logger.info("✅ Photo Cultural Analyzer initialized - PLACES PHOTOS ONLY")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze place photos from Qloo results with Google Vision
        
        Args:
            consolidated_info: Contains daily theme and location info
            cultural_profile: Cultural profile data (passed through)
            qloo_intelligence: Qloo results containing places data
            sensory_content: Sensory content (passed through)
            
        Returns:
            Enhanced data with place photo analysis
        """
        
        logger.info("📸 Agent 5: Starting place photo analysis with Google Vision")
        
        try:
            # Extract key information
            daily_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
            location_info = self._extract_location_info(consolidated_info)
            
            # Analyze place photos from Qloo results
            place_analysis = await self._analyze_qloo_places(qloo_intelligence, daily_theme, location_info)
            
            return {
                "place_photo_analysis": place_analysis,
                "location_context": location_info,
                "agent_metadata": {
                    "agent": "PhotoCulturalAnalyzer",
                    "mode": "places_photos_only",
                    "vision_analysis": place_analysis.get("available", False),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 5 failed: {e}")
            return self._create_fallback_response()
    
    def _extract_location_info(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and prioritize location information"""
        patient_profile = consolidated_info.get("patient_profile", {})
        
        # Prioritize hometown over location
        hometown = patient_profile.get("hometown", "").strip()
        location = patient_profile.get("location", "").strip()
        city = patient_profile.get("city", "").strip()
        state = patient_profile.get("state", "").strip()
        
        # Build primary location with preference order
        primary_location = hometown or location or f"{city}, {state}".strip(", ")
        location_type = "hometown" if hometown else "location"
        
        return {
            "primary_location": primary_location,
            "location_type": location_type,
            "hometown": hometown,
            "current_location": location,
            "city": city,
            "state": state,
            "available": bool(primary_location)
        }
    
    async def _analyze_qloo_places(self, qloo_intelligence: Dict[str, Any], 
                                   current_theme: Dict[str, Any],
                                   location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze places from Qloo results with theme relevance"""
        
        logger.info(f"🔍 Analyzing Qloo places for theme: {current_theme.get('name', 'Unknown')}")
        
        # Extract places from Qloo intelligence
        places_data = qloo_intelligence.get("cultural_recommendations", {}).get("places", {})
        places = places_data.get("entities", [])
        
        if not places or len(places) == 0:
            logger.info("📍 No places found in Qloo results - using rural fallback")
            return self._create_rural_fallback(current_theme, location_info)
        
        logger.info(f"📍 Found {len(places)} places from Qloo")
        
        # Find theme-relevant place
        relevant_place = self._find_theme_matching_place(places, current_theme)
        
        if not relevant_place:
            logger.info("🔄 No theme match - using first available place")
            relevant_place = places[0]
        
        # Analyze the place photo with Google Vision
        return await self._analyze_place_photo(relevant_place, current_theme, location_info)
    
    def _find_theme_matching_place(self, places: List[Dict[str, Any]], 
                                   current_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find place that best matches current theme"""
        
        theme_id = current_theme.get("id", "")
        theme_keywords = self._get_theme_keywords(theme_id)
        
        logger.info(f"🔍 Looking for places matching theme '{theme_id}' with keywords: {theme_keywords}")
        
        best_place = None
        highest_score = 0
        
        for place in places:
            score = self._calculate_theme_relevance_score(place, theme_keywords)
            
            if score > highest_score:
                highest_score = score
                best_place = place
                
            logger.debug(f"Place '{place.get('name', 'Unknown')}' theme relevance score: {score}")
        
        if best_place:
            logger.info(f"✅ Selected theme-relevant place: {best_place.get('name', 'Unknown')} (score: {highest_score})")
        
        return best_place
    
    def _get_theme_keywords(self, theme_id: str) -> List[str]:
        """Get keywords for theme matching"""
        theme_keywords = {
            "school": ["school", "library", "education", "academy", "university", "college", "learning", "historic", "building"],
            "birthday": ["bakery", "restaurant", "celebration", "party", "sweet", "cake", "festive"],
            "music": ["theater", "venue", "hall", "music", "concert", "performance", "cultural", "arts"],
            "food": ["restaurant", "market", "italian", "bakery", "dining", "cuisine", "culinary"],
            "travel": ["tourist", "landmark", "historic", "museum", "attraction", "destination"],
            "weather": ["park", "outdoor", "garden", "nature", "seasonal"],
            "holidays": ["cultural", "historic", "traditional", "celebration", "religious", "community"],
            "seasons": ["park", "garden", "outdoor", "nature", "seasonal", "market"],
            "pets": ["park", "outdoor", "family", "community", "neighborhood"],
            "clothing": ["historic", "cultural", "traditional", "vintage", "classic"]
        }
        
        return theme_keywords.get(theme_id, ["historic", "cultural", "landmark"])
    
    def _calculate_theme_relevance_score(self, place: Dict[str, Any], theme_keywords: List[str]) -> int:
        """Calculate how well a place matches theme keywords"""
        score = 0
        
        # Check place name
        place_name = place.get("name", "").lower()
        for keyword in theme_keywords:
            if keyword in place_name:
                score += 3
        
        # Check description
        description = place.get("properties", {}).get("description", "").lower()
        for keyword in theme_keywords:
            if keyword in description:
                score += 2
        
        # Check tags
        tags = place.get("tags", [])
        for tag in tags:
            tag_name = tag.get("name", "").lower()
            for keyword in theme_keywords:
                if keyword in tag_name:
                    score += 1
        
        return score
    
    async def _analyze_place_photo(self, place: Dict[str, Any], 
                                   current_theme: Dict[str, Any],
                                   location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual place photo with Google Vision"""
        
        place_name = place.get("name", "Unknown Place")
        logger.info(f"📸 Analyzing photo for: {place_name}")
        
        # Get photo URL from place data
        images = place.get("images", [])
        if not images or len(images) == 0:
            logger.warning(f"📸 No images available for {place_name}")
            return self._create_no_photo_fallback(place, current_theme, location_info)
        
        photo_url = images[0].get("url", "")
        if not photo_url:
            logger.warning(f"📸 No valid photo URL for {place_name}")
            return self._create_no_photo_fallback(place, current_theme, location_info)
        
        try:
            # Analyze with Google Vision
            logger.info(f"🔍 Running Google Vision analysis on: {photo_url}")
            vision_result = await self.vision_tool.analyze_image(photo_url)
            
            if vision_result.get("success"):
                logger.info(f"✅ Vision analysis successful for {place_name}")
                
                return {
                    "available": True,
                    "place_data": {
                        "name": place_name,
                        "description": place.get("properties", {}).get("description", ""),
                        "address": place.get("properties", {}).get("address", ""),
                        "neighborhood": place.get("neighborhood", ""),
                        "tags": [tag.get("name", "") for tag in place.get("tags", [])[:5]]  # Top 5 tags
                    },
                    "photo_url": photo_url,
                    "vision_analysis": {
                        "labels": vision_result.get("labels", []),
                        "objects": vision_result.get("objects", []),
                        "text": vision_result.get("text", []),
                        "landmarks": vision_result.get("landmarks", []),
                        "architectural_details": self._extract_architectural_details(vision_result),
                        "atmosphere_description": self._create_atmosphere_description(vision_result)
                    },
                    "theme_relevance": {
                        "theme_id": current_theme.get("id", ""),
                        "theme_name": current_theme.get("name", ""),
                        "relevance_explanation": self._explain_theme_relevance(place, current_theme)
                    },
                    "source": "qloo_vision_analysis"
                }
            else:
                logger.warning(f"⚠️ Vision analysis failed for {place_name}: {vision_result.get('error', 'Unknown error')}")
                return self._create_no_photo_fallback(place, current_theme, location_info)
                
        except Exception as e:
            logger.error(f"❌ Vision analysis exception for {place_name}: {e}")
            return self._create_no_photo_fallback(place, current_theme, location_info)
    
    def _extract_architectural_details(self, vision_result: Dict[str, Any]) -> str:
        """Extract architectural details from vision analysis"""
        labels = vision_result.get("labels", [])
        objects = vision_result.get("objects", [])
        
        architectural_terms = []
        
        # Look for architectural labels
        for label in labels[:10]:  # Top 10 labels
            label_name = label.get("description", "").lower()
            if any(term in label_name for term in ["building", "architecture", "facade", "window", "door", "column", "brick", "stone"]):
                architectural_terms.append(label.get("description", ""))
        
        # Look for architectural objects
        for obj in objects[:5]:  # Top 5 objects
            obj_name = obj.get("name", "").lower()
            if any(term in obj_name for term in ["building", "window", "door", "sign", "entrance"]):
                architectural_terms.append(obj.get("name", ""))
        
        if architectural_terms:
            return f"I can see {', '.join(architectural_terms[:3])} in this image."
        else:
            return "This appears to be an interesting building with distinctive features."
    
    def _create_atmosphere_description(self, vision_result: Dict[str, Any]) -> str:
        """Create atmosphere description from vision analysis"""
        labels = vision_result.get("labels", [])
        
        atmosphere_terms = []
        
        # Look for atmosphere-related labels
        for label in labels[:15]:  # Top 15 labels
            label_name = label.get("description", "").lower()
            if any(term in label_name for term in ["cozy", "bright", "historic", "elegant", "bustling", "quiet", "charming", "welcoming"]):
                atmosphere_terms.append(label.get("description", ""))
        
        if atmosphere_terms:
            return f"The atmosphere looks {', '.join(atmosphere_terms[:2])}."
        else:
            return "This place has a distinctive character and atmosphere."
    
    def _explain_theme_relevance(self, place: Dict[str, Any], current_theme: Dict[str, Any]) -> str:
        """Explain why this place is relevant to the current theme"""
        theme_id = current_theme.get("id", "")
        place_name = place.get("name", "this place")
        
        explanations = {
            "school": f"{place_name} represents the kind of educational or historic building you might have encountered during your school years.",
            "birthday": f"{place_name} is the type of place where families might have celebrated special occasions like birthdays.",
            "music": f"{place_name} represents the cultural venues where music and performances brought communities together.",
            "food": f"{place_name} represents the dining traditions and food culture of your area.",
            "travel": f"{place_name} is a landmark that represents the places people visited for special trips.",
            "weather": f"{place_name} represents the outdoor spaces where people experienced different seasons and weather.",
            "holidays": f"{place_name} represents the community spaces where people gathered for celebrations and traditions.",
            "seasons": f"{place_name} represents the places that changed with the seasons in your community.",
            "pets": f"{place_name} represents the community spaces where families and their pets spent time together.",
            "clothing": f"{place_name} represents the historic and cultural context of fashion and style from your era."
        }
        
        return explanations.get(theme_id, f"{place_name} represents an important part of your community's cultural heritage.")
    
    def _create_no_photo_fallback(self, place: Dict[str, Any], 
                                  current_theme: Dict[str, Any],
                                  location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback when place has no analyzable photo"""
        
        place_name = place.get("name", "Unknown Place")
        description = place.get("properties", {}).get("description", "")
        
        logger.info(f"📝 Creating text-only analysis for {place_name}")
        
        return {
            "available": True,
            "place_data": {
                "name": place_name,
                "description": description,
                "address": place.get("properties", {}).get("address", ""),
                "neighborhood": place.get("neighborhood", ""),
                "tags": [tag.get("name", "") for tag in place.get("tags", [])[:5]]
            },
            "photo_url": "",
            "vision_analysis": {
                "labels": [],
                "objects": [],
                "text": [],
                "landmarks": [],
                "architectural_details": "This historic location has distinctive architectural features.",
                "atmosphere_description": "This place has a welcoming community atmosphere."
            },
            "theme_relevance": {
                "theme_id": current_theme.get("id", ""),
                "theme_name": current_theme.get("name", ""),
                "relevance_explanation": self._explain_theme_relevance(place, current_theme)
            },
            "source": "qloo_text_only"
        }
    
    def _create_rural_fallback(self, current_theme: Dict[str, Any], 
                               location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback for rural areas with no Qloo places"""
        
        primary_location = location_info.get("primary_location", "your area")
        location_type = location_info.get("location_type", "location")
        
        logger.info(f"🏡 Creating rural area fallback for {primary_location}")
        
        return {
            "available": False,
            "rural_fallback": True,
            "location_context": {
                "primary_location": primary_location,
                "location_type": location_type,
                "fallback_reason": "no_places_found"
            },
            "theme_context": {
                "theme_id": current_theme.get("id", ""),
                "theme_name": current_theme.get("name", ""),
                "rural_prompt_ready": True
            },
            "source": "rural_fallback"
        }
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response when agent fails completely"""
        
        logger.warning("⚠️ Creating complete fallback response")
        
        return {
            "place_photo_analysis": {
                "available": False,
                "error": True,
                "fallback_reason": "agent_failure"
            },
            "location_context": {
                "available": False
            },
            "agent_metadata": {
                "agent": "PhotoCulturalAnalyzer",
                "mode": "error_fallback",
                "vision_analysis": False,
                "timestamp": datetime.now().isoformat()
            }
        }

# Export the main class
__all__ = ["PhotoCulturalAnalyzerAgent"]