"""
Photo Cultural Analyzer Agent - SIMPLIFIED for Dementia Care
File: backend/multi_tool_agent/agents/photo_cultural_analyzer_agent.py

FIXES:
- Simple, short conversation starters (2-3 questions)
- Plain language appropriate for dementia patients
- Removed complex multi-part questions
"""

import logging
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class PhotoCulturalAnalyzerAgent:
    """
    Agent 5: Photo Cultural Analyzer with SIMPLIFIED conversation starters for dementia care.
    
    SIMPLIFIED APPROACH:
    - Short, simple questions (5-10 words)
    - Plain language only
    - 2-3 questions maximum
    - Easy to understand for dementia patients
    """
    
    def __init__(self, vision_ai_tool):
        self.vision_ai_tool = vision_ai_tool
        logger.info("Photo Cultural Analyzer initialized with SIMPLIFIED conversation starters")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_of_the_day: str,
                  stored_photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze photo and generate SIMPLE conversation starters for dementia care.
        """
        
        try:
            logger.info("🔍 Starting photo cultural analysis with SIMPLE conversation starters")
            logger.info(f"📷 Processing photo: {photo_of_the_day}")
            
            # Extract patient info
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            
            # Use stored vision analysis data
            vision_analysis = stored_photo_analysis.get("vision_analysis", {})
            logger.info(f"🔍 Vision data: {len(vision_analysis.get('objects', []))} objects, {len(vision_analysis.get('labels', []))} labels")
            
            # Generate SIMPLE conversation starters
            conversation_starters = self._generate_simple_conversation_starters(
                vision_analysis, heritage, birth_year
            )
            
            # Generate simple memory triggers
            memory_triggers = self._generate_simple_memory_triggers(vision_analysis, heritage)
            
            # Cultural integration (simplified)
            cultural_integration = self._analyze_cultural_alignment(vision_analysis, heritage)
            
            logger.info(f"✅ Photo analysis completed: {len(conversation_starters)} simple conversation starters generated")
            
            return {
                "photo_analysis": {
                    "status": "success",
                    "photo_path": photo_of_the_day,
                    "analysis_source": "stored_vision_with_simple_conversation",
                    "vision_analysis": vision_analysis,
                    "cultural_integration": cultural_integration,
                    "conversation_starters": conversation_starters,
                    "memory_triggers": memory_triggers,
                    "era_analysis": self._simple_era_analysis(birth_year),
                    "processing_metadata": {
                        "agent": "photo_cultural_analyzer",
                        "analysis_type": "stored_with_simple_conversation",
                        "cultural_alignment": cultural_integration.get("cultural_alignment_detected", False),
                        "conversation_count": len(conversation_starters),
                        "memory_trigger_count": len(memory_triggers),
                        "simplified_approach": True
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Photo cultural analysis failed: {e}")
            return self._create_simple_fallback_analysis(photo_of_the_day, consolidated_info)
    
    def _generate_simple_conversation_starters(self, 
                                             vision_analysis: Dict[str, Any], 
                                             heritage: str, 
                                             birth_year: Optional[int]) -> List[Dict[str, Any]]:
        """
        Generate 2-3 SIMPLE conversation starters for dementia patients.
        
        RULES:
        - Maximum 10 words per question
        - Plain, simple language
        - No complex sentences
        - Easy to understand
        """
        
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        people = vision_analysis.get("people", [])
        activities = vision_analysis.get("activities", [])
        
        simple_starters = []
        
        # SIMPLE questions based on what's in the photo
        
        # People questions (if people detected)
        if people or "people" in objects:
            simple_starters.append({
                "type": "people",
                "starter": "Who do you see here?",
                "follow_up": "Tell me about them.",
                "caregiver_guidance": "Let them share memories about people they know"
            })
        
        # Family/celebration questions
        if any(word in labels for word in ["family", "celebration", "wedding", "gathering"]):
            simple_starters.append({
                "type": "celebration",
                "starter": "What celebration is this?",
                "follow_up": "Do you like parties?",
                "caregiver_guidance": "Encourage sharing about happy times"
            })
        
        # Home/kitchen questions
        if any(word in labels for word in ["home", "kitchen", "cooking"]):
            simple_starters.append({
                "type": "home",
                "starter": "What room is this?",
                "follow_up": "Do you like to cook?",
                "caregiver_guidance": "Ask about their favorite foods or cooking memories"
            })
        
        # Clothing/fashion questions
        if any(word in objects for word in ["dress", "clothes"]) or "formal wear" in labels:
            simple_starters.append({
                "type": "clothing",
                "starter": "What pretty clothes!",
                "follow_up": "What did you like to wear?",
                "caregiver_guidance": "Talk about their favorite outfits or fashion"
            })
        
        # Church/religious questions
        if "church" in objects or "ceremony" in labels:
            simple_starters.append({
                "type": "church",
                "starter": "Is this a church?",
                "follow_up": "Did you go to church?",
                "caregiver_guidance": "Share memories about faith or community"
            })
        
        # Food questions
        if "food" in objects or "cooking" in activities:
            simple_starters.append({
                "type": "food",
                "starter": "What food do you see?",
                "follow_up": "What's your favorite meal?",
                "caregiver_guidance": "Talk about favorite foods and family meals"
            })
        
        # Generic fallback questions (always available)
        fallback_starters = [
            {
                "type": "memory",
                "starter": "What do you see here?",
                "follow_up": "Does this remind you of anything?",
                "caregiver_guidance": "Let them describe what they notice"
            },
            {
                "type": "feeling",
                "starter": "How does this make you feel?",
                "follow_up": "Tell me more.",
                "caregiver_guidance": "Focus on emotions and feelings, not specific details"
            },
            {
                "type": "story",
                "starter": "What story does this tell?",
                "follow_up": "What happened next?",
                "caregiver_guidance": "Encourage storytelling at their own pace"
            }
        ]
        
        # If no specific starters, use fallback
        if not simple_starters:
            simple_starters = fallback_starters
        
        # Limit to 3 starters maximum
        selected_starters = simple_starters[:3]
        
        # Add cultural context for heritage if available
        if heritage and heritage != "American":
            heritage_simple = heritage.split("-")[0]  # "Italian" from "Italian-American"
            for starter in selected_starters:
                starter["cultural_context"] = heritage_simple
        
        logger.info(f"Generated {len(selected_starters)} simple conversation starters")
        return selected_starters
    
    def _generate_simple_memory_triggers(self, vision_analysis: Dict[str, Any], heritage: str) -> List[Dict[str, Any]]:
        """Generate simple memory triggers based on photo content."""
        
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        activities = vision_analysis.get("activities", [])
        
        simple_triggers = []
        
        # Simple activity-based triggers
        if "cooking" in activities or "food" in objects:
            simple_triggers.append({
                "type": "activity",
                "activity": "cooking together",
                "context": "family time",
                "connection_to_photo": "Food and cooking in photo"
            })
        
        if "celebration" in labels or "wedding" in labels:
            simple_triggers.append({
                "type": "activity", 
                "activity": "family celebrations",
                "context": "happy times",
                "connection_to_photo": "Celebration in photo"
            })
        
        if "home" in labels or "kitchen" in objects:
            simple_triggers.append({
                "type": "activity",
                "activity": "time at home",
                "context": "family",
                "connection_to_photo": "Home setting in photo"
            })
        
        # Limit to 3 triggers
        return simple_triggers[:3]
    
    def _analyze_cultural_alignment(self, vision_analysis: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Simple cultural alignment analysis."""
        
        labels = vision_analysis.get("labels", [])
        objects = vision_analysis.get("objects", [])
        
        # Simple heritage connections
        heritage_keywords = {
            "Italian-American": ["family", "cooking", "celebration", "church", "food"],
            "Irish-American": ["family", "church", "celebration", "home"],
            "Mexican-American": ["family", "celebration", "cooking", "gathering"],
            "American": ["family", "home", "celebration"]
        }
        
        heritage_words = heritage_keywords.get(heritage, heritage_keywords["American"])
        
        # Check for matches
        connections = []
        for keyword in heritage_words:
            if keyword in labels or keyword in objects:
                connections.append({
                    "heritage": heritage.split("-")[0],  # "Italian" from "Italian-American"
                    "keyword": keyword,
                    "connection_strength": "strong"
                })
        
        return {
            "cultural_alignment_detected": len(connections) > 0,
            "heritage_connections": connections[:3],  # Limit to 3
            "era_consistency": True,  # Simplified - assume consistent
            "family_context_likely": "family" in labels or "people" in objects
        }
    
    def _simple_era_analysis(self, birth_year: Optional[int]) -> Dict[str, Any]:
        """Simple era analysis for context."""
        
        if not birth_year:
            return {
                "has_era_context": False,
                "estimated_decade": 1960,
                "era_indicators": [],
                "generation_context": "Unknown"
            }
        
        # Simple generation mapping
        if birth_year <= 1945:
            generation = "Greatest Generation"
            decade = 1960
        elif birth_year <= 1965:
            generation = "Silent Generation" 
            decade = 1970
        else:
            generation = "Baby Boomer"
            decade = 1980
        
        return {
            "has_era_context": True,
            "estimated_decade": decade,
            "era_indicators": [],
            "generation_context": generation
        }
    
    def _create_simple_fallback_analysis(self, photo_path: str, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create simple fallback analysis when processing fails."""
        
        heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
        
        # Very simple fallback conversation starters
        simple_fallback_starters = [
            {
                "type": "general",
                "starter": "What do you see here?",
                "follow_up": "Tell me more.",
                "caregiver_guidance": "Let them describe what they notice"
            },
            {
                "type": "feeling",
                "starter": "How does this make you feel?",
                "follow_up": "That's nice.",
                "caregiver_guidance": "Focus on their emotions"
            },
            {
                "type": "memory",
                "starter": "Does this remind you of anything?",
                "follow_up": "What do you remember?",
                "caregiver_guidance": "Encourage sharing memories"
            }
        ]
        
        return {
            "photo_analysis": {
                "status": "fallback",
                "photo_path": photo_path,
                "analysis_source": "simple_fallback",
                "vision_analysis": {
                    "objects": [],
                    "labels": [],
                    "people": [],
                    "activities": [],
                    "settings": []
                },
                "cultural_integration": {
                    "cultural_alignment_detected": False,
                    "heritage_connections": [],
                    "era_consistency": False,
                    "family_context_likely": False
                },
                "conversation_starters": simple_fallback_starters,
                "memory_triggers": [],
                "era_analysis": {
                    "has_era_context": False,
                    "estimated_decade": 1960,
                    "era_indicators": [],
                    "generation_context": "Unknown"
                },
                "processing_metadata": {
                    "agent": "photo_cultural_analyzer",
                    "analysis_type": "simple_fallback",
                    "cultural_alignment": False,
                    "conversation_count": 3,
                    "memory_trigger_count": 0,
                    "simplified_approach": True
                }
            }
        }