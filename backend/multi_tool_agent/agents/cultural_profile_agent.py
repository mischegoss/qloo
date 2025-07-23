"""
Agent 2: Cultural Profile Builder - ENHANCED VERSION
File: backend/multi_tool_agent/agents/cultural_profile_agent.py

Enhanced to use cultural mappings and create Qloo tag mappings for Agent 3.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime


# Import our cultural mappings
from config.cultural_mappings import get_heritage_tags, get_interest_tags, get_age_demographic

logger = logging.getLogger(__name__)

class CulturalProfileBuilderAgent(Agent):
    """
    Agent 2: Cultural Profile Builder - ENHANCED
    
    ENHANCEMENTS:
    - Uses cultural heritage mappings to create Qloo tags
    - Maps interests to additional tags
    - Creates enhanced cultural context
    - Provides ready-to-use tag mappings for Agent 3
    - No complex bias prevention - just reliable mapping
    """
    
    def __init__(self):
        super().__init__(
            name="cultural_profile_builder_enhanced",
            description="Creates enhanced cultural profiles with Qloo tag mappings"
        )
        logger.info("Cultural Profile Builder Agent initialized with mapping enhancements")
    
    async def run(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create enhanced cultural profile with Qloo tag mappings.
        
        Args:
            consolidated_info: Output from Agent 1
            
        Returns:
            Enhanced cultural profile with tag mappings
        """
        
        try:
            logger.info("Building enhanced cultural profile with tag mappings")
            
            # Extract basic information
            patient_profile = consolidated_info.get("patient_profile", {})
            request_context = consolidated_info.get("request_context", {})
            
            # STEP 1: Extract cultural heritage
            heritage = self._extract_heritage(patient_profile, request_context)
            
            # STEP 2: Extract interests and preferences
            interests = self._extract_interests(patient_profile)
            
            # STEP 3: Extract era context
            era_context = self._extract_era_context(patient_profile)
            
            # STEP 4: Map heritage to Qloo tags
            heritage_tags = get_heritage_tags(heritage)
            
            # STEP 5: Map interests to additional tags
            interest_tags = get_interest_tags(interests)
            
            # STEP 6: Build comprehensive cultural elements
            cultural_elements = self._build_cultural_elements(
                heritage=heritage,
                interests=interests,
                era_context=era_context,
                heritage_tags=heritage_tags,
                interest_tags=interest_tags
            )
            
            # STEP 7: Create Qloo tag mappings for Agent 3
            qloo_tag_mappings = self._create_qloo_tag_mappings(heritage_tags, interest_tags)
            
            # STEP 8: Build final cultural profile
            cultural_profile = {
                "cultural_elements": cultural_elements,
                "qloo_tag_mappings": qloo_tag_mappings,
                "era_context": era_context,
                "metadata": {
                    "heritage_source": heritage,
                    "interests_found": len(interests),
                    "heritage_tags_mapped": len(heritage_tags),
                    "interest_tags_mapped": len(interest_tags),
                    "profile_generation_timestamp": datetime.now().isoformat(),
                    "agent_version": "enhanced_with_mappings"
                }
            }
            
            logger.info(f"Cultural profile built: {heritage} heritage with {len(interests)} interests")
            
            return {"cultural_profile": cultural_profile}
            
        except Exception as e:
            logger.error(f"❌ Cultural Profile Builder failed: {e}")
            return self._create_fallback_profile()
    
    def _extract_heritage(self, patient_profile: Dict[str, Any], request_context: Dict[str, Any]) -> str:
        """Extract cultural heritage from patient information."""
        
        # Try patient profile first
        heritage = patient_profile.get("cultural_heritage")
        if heritage:
            return heritage.strip()
        
        # Try request context
        heritage = request_context.get("cultural_heritage")
        if heritage:
            return heritage.strip()
        
        # Default
        logger.warning("No cultural heritage specified, using American")
        return "American"
    
    def _extract_interests(self, patient_profile: Dict[str, Any]) -> List[str]:
        """Extract interests and preferences from patient information."""
        
        interests = []
        
        # Extract from additional_context
        additional_context = patient_profile.get("additional_context", "")
        if additional_context:
            context_lower = additional_context.lower()
            
            # Look for specific interest keywords
            interest_keywords = [
                "music", "cooking", "reading", "gardening", "dancing", 
                "movies", "travel", "sports", "arts", "crafts", "family"
            ]
            
            for keyword in interest_keywords:
                if keyword in context_lower:
                    interests.append(keyword)
        
        # Extract from caregiver_notes
        caregiver_notes = patient_profile.get("caregiver_notes", "")
        if caregiver_notes:
            notes_lower = caregiver_notes.lower()
            
            if "music" in notes_lower:
                interests.append("music")
            if "cook" in notes_lower:
                interests.append("cooking")
            if "family" in notes_lower:
                interests.append("family activities")
        
        # Remove duplicates
        interests = list(set(interests))
        
        logger.info(f"Extracted interests: {interests}")
        return interests
    
    def _extract_era_context(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract era and generational context."""
        
        birth_year = patient_profile.get("birth_year")
        
        if not birth_year:
            return {"has_era_context": False}
        
        current_year = 2024
        age = current_year - birth_year
        
        # Calculate key decades
        childhood_decade = ((birth_year + 10) // 10) * 10  # Approximate childhood decade
        teen_decade = ((birth_year + 15) // 10) * 10       # Approximate teen decade
        young_adult_decade = ((birth_year + 25) // 10) * 10  # Approximate young adult decade
        
        return {
            "has_era_context": True,
            "birth_year": birth_year,
            "current_age": age,
            "age_demographic": get_age_demographic(birth_year),
            "childhood_decade": childhood_decade,
            "teen_decade": teen_decade,
            "young_adult_decade": young_adult_decade,
            "formative_decades": [childhood_decade, teen_decade, young_adult_decade],
            "generation_context": self._get_generation_context(birth_year)
        }
    
    def _get_generation_context(self, birth_year: int) -> str:
        """Get generational context for cultural understanding."""
        
        if birth_year <= 1928:
            return "Silent Generation"
        elif birth_year <= 1945:
            return "Greatest Generation"
        elif birth_year <= 1964:
            return "Baby Boomer"
        elif birth_year <= 1980:
            return "Generation X"
        elif birth_year <= 1996:
            return "Millennial"
        else:
            return "Generation Z"
    
    def _build_cultural_elements(self, 
                                heritage: str,
                                interests: List[str],
                                era_context: Dict[str, Any],
                                heritage_tags: Dict[str, str],
                                interest_tags: List[str]) -> Dict[str, Any]:
        """Build comprehensive cultural elements structure."""
        
        # Create heritage keywords for context
        heritage_keywords = [heritage]
        if "-" in heritage:
            heritage_keywords.extend(heritage.split("-"))
        heritage_keywords.append("family traditions")
        
        # Map interests to preference categories
        cuisine_preferences = ["comfort food"]
        music_preferences = []
        activity_preferences = []
        
        for interest in interests:
            if interest in ["cooking"]:
                cuisine_preferences.append("home cooking")
            elif interest in ["music"]:
                music_preferences.append("traditional")
            elif interest in ["family"]:
                activity_preferences.append("family time")
            else:
                activity_preferences.append(interest)
        
        # Add heritage-based preferences
        heritage_base = heritage.split("-")[0] if "-" in heritage else heritage
        if heritage_base.lower() != "american":
            cuisine_preferences.append(heritage_base.lower())
            music_preferences.append("traditional")
        
        return {
            "heritage": heritage,
            "heritage_keywords": heritage_keywords,
            "cuisine_preferences": list(set(cuisine_preferences)),
            "music_preferences": list(set(music_preferences)) or ["classical"],
            "activity_preferences": list(set(activity_preferences)) or ["family activities"],
            "interests": interests,
            "era_informed": era_context.get("has_era_context", False)
        }
    
    def _create_qloo_tag_mappings(self, heritage_tags: Dict[str, str], interest_tags: List[str]) -> Dict[str, Any]:
        """Create ready-to-use Qloo tag mappings for Agent 3."""
        
        # Base mappings from heritage
        mappings = heritage_tags.copy()
        
        # Enhance with interest tags if available
        if interest_tags:
            # Add first interest tag as additional signal
            mappings["additional_interest"] = interest_tags[0]
        
        return {
            "cuisine": mappings.get("cuisine"),
            "music": mappings.get("music"), 
            "movies": mappings.get("movies"),
            "additional_tags": interest_tags,
            "mapping_source": "cultural_heritage_with_interests"
        }
    
    def _create_fallback_profile(self) -> Dict[str, Any]:
        """Create fallback cultural profile when extraction fails."""
        
        logger.warning("Creating fallback cultural profile")
        
        fallback_tags = {
            "cuisine": "urn:tag:cuisine:comfort",
            "music": "urn:tag:genre:music:popular",
            "movies": "urn:tag:genre:media:family"
        }
        
        return {
            "cultural_profile": {
                "cultural_elements": {
                    "heritage": "American",
                    "heritage_keywords": ["American", "family traditions"],
                    "cuisine_preferences": ["comfort food"],
                    "music_preferences": ["popular"],
                    "activity_preferences": ["family activities"],
                    "interests": [],
                    "era_informed": False
                },
                "qloo_tag_mappings": fallback_tags,
                "era_context": {"has_era_context": False},
                "metadata": {
                    "heritage_source": "fallback",
                    "profile_generation_timestamp": datetime.now().isoformat(),
                    "agent_version": "fallback"
                }
            }
        }

# Test function
def test_cultural_profile_builder():
    """Test the enhanced cultural profile builder."""
    
    agent = CulturalProfileBuilderAgent()
    
    # Test data matching the curl example
    test_consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "additional_context": "Loves music and cooking",
            "city": "Brooklyn",
            "state": "New York"
        },
        "request_context": {
            "request_type": "dashboard"
        }
    }
    
    # Run the test
    import asyncio
    
    async def run_test():
        result = await agent.run(test_consolidated_info)
        
        profile = result.get("cultural_profile", {})
        elements = profile.get("cultural_elements", {})
        mappings = profile.get("qloo_tag_mappings", {})
        
        print("Cultural Profile Builder Test Results:")
        print(f"Heritage: {elements.get('heritage')}")
        print(f"Interests: {elements.get('interests')}")
        print(f"Era context: {profile.get('era_context', {}).get('has_era_context')}")
        print(f"Qloo mappings: {mappings}")
        
        return result
    
    return asyncio.run(run_test())

if __name__ == "__main__":
    test_cultural_profile_builder()