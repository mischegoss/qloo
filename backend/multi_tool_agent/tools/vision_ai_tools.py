"""
Fixed Google Vision AI Tools
File: backend/multi_tool_agent/tools/vision_ai_tools.py

Provides interface to Google Cloud Vision AI for photo cultural analysis
"""

import httpx
import logging
import base64
from typing import Dict, Any, Optional, List

# Configure logger
logger = logging.getLogger(__name__)

class VisionAIAnalyzer:
    """
    Google Cloud Vision AI tool for photo cultural analysis.
    Used by Agent 5: Photo Cultural Analyzer Agent
    
    This is the MAIN class that should be imported.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://vision.googleapis.com/v1"
        logger.info("VisionAIAnalyzer initialized")
        
    async def analyze_photo(self, photo_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze photo for cultural context and elements.
        
        Args:
            photo_data: Dictionary containing photo information
                       Expected format: {
                           "photo_type": "family_photo",
                           "caregiver_context": "Wedding photo from 1960s",
                           "analysis_focus": ["objects", "people", "settings", "era_indicators"]
                       }
            
        Returns:
            Analysis results with cultural elements or None if failed
        """
        
        try:
            # For demo purposes, we'll simulate photo analysis
            # In production, this would process actual photo data
            logger.info("Starting Vision AI photo analysis")
            
            photo_type = photo_data.get("photo_type", "family_photo")
            caregiver_context = photo_data.get("caregiver_context", "")
            analysis_focus = photo_data.get("analysis_focus", [])
            
            # Simulate comprehensive analysis based on context
            analysis_results = self._simulate_photo_analysis(photo_type, caregiver_context)
            
            logger.info("Vision AI photo analysis completed")
            return {
                "success": True,
                "analysis_type": "cultural_context_extraction",
                "photo_type": photo_type,
                "caregiver_context": caregiver_context,
                **analysis_results
            }
            
        except Exception as e:
            logger.error(f"Vision AI photo analysis exception: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _simulate_photo_analysis(self, photo_type: str, context: str) -> Dict[str, Any]:
        """
        Simulate photo analysis results based on type and context.
        In production, this would be replaced with actual Vision AI calls.
        """
        
        # Simulate different analysis based on photo type
        if photo_type == "family_photo":
            return {
                "objects": ["people", "furniture", "clothing"],
                "people": ["family_members"],
                "settings": ["indoor", "home", "living_room"],
                "era_indicators": self._extract_era_from_context(context),
                "activities": ["family_gathering", "celebration"],
                "photo_quality": "vintage" if "1960" in context else "modern",
                "cultural_markers": self._extract_cultural_markers(context)
            }
        elif photo_type == "wedding_photo":
            return {
                "objects": ["wedding_dress", "flowers", "ceremony_items"],
                "people": ["bride", "groom", "wedding_party"],
                "settings": ["ceremony_venue", "celebration"],
                "era_indicators": self._extract_era_from_context(context),
                "activities": ["wedding_ceremony", "celebration"],
                "photo_quality": "formal",
                "cultural_markers": ["wedding_traditions", "formal_attire"]
            }
        else:
            return {
                "objects": ["various_items"],
                "people": ["individuals"],
                "settings": ["unknown_setting"],
                "era_indicators": [],
                "activities": ["daily_life"],
                "photo_quality": "standard",
                "cultural_markers": []
            }
    
    def _extract_era_from_context(self, context: str) -> List[str]:
        """Extract era indicators from caregiver context."""
        
        era_indicators = []
        
        # Decade detection
        decades = ["1940", "1950", "1960", "1970", "1980", "1990", "2000", "2010"]
        for decade in decades:
            if decade in context:
                era_indicators.append(f"{decade}s")
        
        # Era keywords
        if any(word in context.lower() for word in ["vintage", "old", "antique"]):
            era_indicators.append("vintage")
        if any(word in context.lower() for word in ["modern", "recent", "new"]):
            era_indicators.append("modern")
            
        return era_indicators
    
    def _extract_cultural_markers(self, context: str) -> List[str]:
        """Extract cultural markers from context."""
        
        markers = []
        
        # Cultural keywords
        cultural_terms = [
            "traditional", "ceremony", "celebration", "wedding", "festival",
            "religious", "cultural", "heritage", "family", "gathering"
        ]
        
        for term in cultural_terms:
            if term in context.lower():
                markers.append(term)
                
        return markers
    
    async def analyze_with_google_vision(self, image_base64: str) -> Optional[Dict[str, Any]]:
        """
        Analyze image using Google Cloud Vision AI.
        
        Args:
            image_base64: Base64-encoded image data
            
        Returns:
            Google Vision AI results or None if failed
        """
        
        try:
            url = f"{self.base_url}/images:annotate?key={self.api_key}"
            
            payload = {
                "requests": [{
                    "image": {"content": image_base64},
                    "features": [
                        {"type": "LABEL_DETECTION", "maxResults": 10},
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 10},
                        {"type": "FACE_DETECTION", "maxResults": 5},
                        {"type": "SAFE_SEARCH_DETECTION"},
                        {"type": "IMAGE_PROPERTIES"}
                    ]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info("Google Vision AI analysis successful")
                    return self._process_vision_results(data)
                else:
                    logger.error(f"Google Vision AI error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Google Vision AI exception: {str(e)}")
            return None
    
    def _process_vision_results(self, vision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process Google Vision AI results into CareConnect format."""
        
        if not vision_data.get("responses"):
            return {"success": False, "error": "No response data"}
        
        response = vision_data["responses"][0]
        
        # Extract labels
        labels = []
        if response.get("labelAnnotations"):
            labels = [label["description"] for label in response["labelAnnotations"]]
        
        # Extract objects
        objects = []
        if response.get("localizedObjectAnnotations"):
            objects = [obj["name"] for obj in response["localizedObjectAnnotations"]]
        
        # Extract face information
        faces = []
        if response.get("faceAnnotations"):
            faces = [f"person_{i+1}" for i in range(len(response["faceAnnotations"]))]
        
        return {
            "success": True,
            "objects": objects,
            "labels": labels,
            "people": faces,
            "settings": [label for label in labels if any(setting in label.lower() 
                        for setting in ["room", "building", "outdoor", "indoor", "home"])],
            "activities": [label for label in labels if any(activity in label.lower()
                          for activity in ["celebration", "gathering", "meal", "ceremony"])],
            "photo_quality": "digital_analysis",
            "confidence_scores": self._extract_confidence_scores(response)
        }
    
    def _extract_confidence_scores(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Extract confidence scores from Vision AI response."""
        
        scores = {}
        
        if response.get("labelAnnotations"):
            scores["labels"] = sum(label.get("score", 0) for label in response["labelAnnotations"]) / len(response["labelAnnotations"])
        
        if response.get("localizedObjectAnnotations"):
            scores["objects"] = sum(obj.get("score", 0) for obj in response["localizedObjectAnnotations"]) / len(response["localizedObjectAnnotations"])
        
        return scores
    
    async def test_connection(self) -> bool:
        """
        Test connection to Google Vision AI.
        
        Returns:
            True if connection successful, False otherwise
        """
        
        try:
            # Test with a minimal image (1x1 pixel PNG)
            test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            
            result = await self.analyze_with_google_vision(test_image)
            
            if result and result.get("success"):
                logger.info("Vision AI connection test successful")
                return True
            else:
                logger.error("Vision AI connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"Vision AI connection test exception: {str(e)}")
            return False

# Backward compatibility aliases
GoogleVisionAI = VisionAIAnalyzer
VisionAITool = VisionAIAnalyzer

# Export the main class
__all__ = ["VisionAIAnalyzer", "GoogleVisionAI", "VisionAITool"]