"""
Agent 2: Cultural Profile Builder - UPDATED for Nostalgia-Based Mappings
File: backend/multi_tool_agent/agents/cultural_profile_agent.py

UPDATED: Now uses the new nostalgia & age-based mapping system.
- Heritage used only for cuisine (non-stereotypical)
- Music & TV shows based on age/nostalgia (dementia-friendly)
- Passes birth_year to mapping functions
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from google.adk.agents import Agent


# Import our updated nostalgia-based mappings
from config.cultural_mappings import get_heritage_tags, get_interest_tags, get_age_demographic

logger = logging.getLogger(__name__)

class CulturalProfileBuilderAgent(Agent):
    """
    Agent 2: Cultural Profile Builder - UPDATED for Nostalgia-Based Mappings
    
    UPDATES:
    - Uses nostalgia & age-based mappings (non-stereotypical) 
    - Heritage only affects cuisine (appropriate)
    - Music & TV shows based on formative years (dementia-friendly)
    - Passes birth_year to mapping functions
    - Creates dementia-appropriate content selection
    """
    
    def __init__(self):
        super().__init__(
            name="cultural_profile_builder_nostalgia",
            description="Creates nostalgia-based cultural profiles with dementia-friendly tag mappings"
        )
        logger.info("Cultural Profile Builder Agent initialized with nostalgia-based mappings")
    
    async def run(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create enhanced cultural profile with nostalgia-based tag mappings.
        
        Args:
            consolidated_info: Output from Agent 1
            
        Returns:
            Enhanced cultural profile with age-appropriate tag mappings
        """
        
        try:
            logger.info("Building nostalgia-based cultural profile with dementia-friendly mappings")
            
            # Extract basic information
            patient_profile = consolidated_info.get("patient_profile", {})
            request_context = consolidated_info.get("request_context", {})
            
            # STEP 1: Extract cultural heritage (for cuisine only)
            heritage = self._extract_heritage(patient_profile, request_context)
            
            # STEP 2: Extract birth year (critical for nostalgia mapping)
            birth_year = patient_profile.get("birth_year")
            
            # STEP 3: Extract interests and preferences
            interests = self._extract_interests(patient_profile)
            
            # STEP 4: Extract era context
            era_context = self._extract_era_context(patient_profile)
            
            # STEP 5: Map heritage + age to Qloo tags (UPDATED to pass birth_year)
            heritage_tags = get_heritage_tags(heritage, birth_year)
            
            # STEP 6: Map interests to additional dementia-friendly tags
            interest_tags = get_interest_tags(interests)
            
            # STEP 7: Build comprehensive cultural elements
            cultural_elements = self._build_cultural_elements(
                heritage=heritage,
                interests=interests,
                era_context=era_context,
                heritage_tags=heritage_tags,
                interest_tags=interest_tags,
                birth_year=birth_year
            )
            
            # STEP 8: Create Qloo tag mappings for Agent 3
            qloo_tag_mappings = self._create_qloo_tag_mappings(heritage_tags, interest_tags)
            
            # STEP 9: Build final cultural profile
            cultural_profile = {
                "cultural_elements": cultural_elements,
                "qloo_tag_mappings": qloo_tag_mappings,
                "era_context": era_context,
                "metadata": {
                    "heritage_source": heritage,
                    "birth_year_used": birth_year,
                    "interests_found": len(interests),
                    "heritage_tags_mapped": len(heritage_tags),
                    "interest_tags_mapped": len(interest_tags),
                    "profile_generation_timestamp": datetime.now().isoformat(),
                    "agent_version": "nostalgia_based_mappings",
                    "mapping_approach": "heritage_for_cuisine_age_for_media"
                }
            }
            
            logger.info(f"Nostalgia-based profile built: {heritage} heritage, born {birth_year}, {len(interests)} interests")
            
            return {"cultural_profile": cultural_profile}
            
        except Exception as e:
            logger.error(f"❌ Cultural Profile Builder failed: {e}")
            return self._create_fallback_profile()
    
    def _extract_heritage(self, patient_profile: Dict[str, Any], request_context: Dict[str, Any]) -> str:
        """Extract cultural heritage from patient information (used only for cuisine)."""
        
        # Try patient profile first
        heritage = patient_profile.get("cultural_heritage")
        if heritage:
            return heritage.strip()
        
        # Try request context
        heritage = request_context.get("cultural_heritage")
        if heritage:
            return heritage.strip()
        
        # Default
        logger.info("No cultural heritage specified, using American (affects cuisine only)")
        return "American"
    
    def _extract_interests(self, patient_profile: Dict[str, Any]) -> List[str]:
        """Extract interests and preferences from patient information."""
        
        interests = []
        
        # Extract from additional_context
        additional_context = patient_profile.get("additional_context", "")
        if additional_context:
            context_lower = additional_context.lower()
            
            # Look for dementia-friendly interest keywords
            interest_keywords = [
                "music", "cooking", "reading", "gardening", "dancing", 
                "tv shows", "travel", "sports", "arts", "crafts", "family", "animals"
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
        
        logger.info(f"Extracted dementia-friendly interests: {interests}")
        return interests
    
    def _extract_era_context(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract era and generational context for nostalgia mapping."""
        
        birth_year = patient_profile.get("birth_year")
        
        if not birth_year:
            logger.warning("No birth year provided - nostalgia mapping will use universal fallback")
            return {"has_era_context": False}
        
        current_year = 2024
        age = current_year - birth_year
        
        # Calculate key decades (formative years for strongest memories)
        childhood_decade = ((birth_year + 10) // 10) * 10  # Age ~10
        teen_decade = ((birth_year + 15) // 10) * 10       # Age ~15-19 (strongest music memories)
        young_adult_decade = ((birth_year + 25) // 10) * 10  # Age ~20-29 (cultural formation)
        
        # Import generation detection from mappings
        from config.cultural_mappings import get_generation_from_birth_year
        generation = get_generation_from_birth_year(birth_year)
        
        return {
            "has_era_context": True,
            "birth_year": birth_year,
            "current_age": age,
            "age_demographic": get_age_demographic(birth_year),
            "childhood_decade": childhood_decade,
            "teen_decade": teen_decade,
            "young_adult_decade": young_adult_decade,
            "formative_decades": [childhood_decade, teen_decade, young_adult_decade],
            "generation_context": self._get_generation_context(birth_year),
            "nostalgia_generation": generation
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
                                interest_tags: List[str],
                                birth_year: int = None) -> Dict[str, Any]:
        """Build comprehensive cultural elements structure with nostalgia focus."""
        
        # Create heritage keywords for context (cuisine only)
        heritage_keywords = [heritage]
        if "-" in heritage:
            heritage_keywords.extend(heritage.split("-"))
        heritage_keywords.append("family traditions")
        
        # Map interests to preference categories (dementia-friendly)
        cuisine_preferences = ["comfort food"]
        music_preferences = []
        activity_preferences = []
        
        for interest in interests:
            if interest in ["cooking"]:
                cuisine_preferences.append("home cooking")
            elif interest in ["music"]:
                music_preferences.append("nostalgic music")  # Age-appropriate
            elif interest in ["family"]:
                activity_preferences.append("family time")
            else:
                activity_preferences.append(interest)
        
        # Add heritage-based cuisine preferences (appropriate cultural connection)
        heritage_base = heritage.split("-")[0] if "-" in heritage else heritage
        if heritage_base.lower() != "american":
            cuisine_preferences.append(heritage_base.lower())
        
        # Age-based music preferences (non-stereotypical)
        if birth_year:
            age = 2024 - birth_year
            if age >= 80:
                music_preferences.append("big band era")
            elif age >= 70:
                music_preferences.append("folk and early rock")
            elif age >= 60:
                music_preferences.append("classic rock")
            else:
                music_preferences.append("contemporary")
        
        return {
            "heritage": heritage,
            "heritage_keywords": heritage_keywords,
            "cuisine_preferences": list(set(cuisine_preferences)),
            "music_preferences": list(set(music_preferences)) or ["nostalgic"],
            "activity_preferences": list(set(activity_preferences)) or ["family activities"],
            "interests": interests,
            "era_informed": era_context.get("has_era_context", False),
            "nostalgia_based": True,
            "birth_year": birth_year
        }
    
    def _create_qloo_tag_mappings(self, heritage_tags: Dict[str, str], interest_tags: List[str]) -> Dict[str, Any]:
        """Create ready-to-use Qloo tag mappings for Agent 3 (nostalgia-based)."""
        
        # Base mappings from heritage + age
        mappings = heritage_tags.copy()
        
        # Enhance with interest tags if available
        if interest_tags:
            # Add first interest tag as additional signal
            mappings["additional_interest"] = interest_tags[0]
        
        return {
            "cuisine": mappings.get("cuisine"),      # Heritage-based (appropriate)
            "music": mappings.get("music"),          # Age-based (nostalgic)
            "tv_shows": mappings.get("tv_shows"),    # Age-based (dementia-friendly)
            "additional_tags": interest_tags,
            "mapping_source": "nostalgia_based_heritage_for_cuisine_only",
            "approach": "dementia_friendly_non_stereotypical"
        }
    
    def _create_fallback_profile(self) -> Dict[str, Any]:
        """Create fallback cultural profile using universal dementia-friendly tags."""
        
        logger.warning("Creating fallback cultural profile with universal dementia-friendly tags")
        
        # Use the universal fallback from our new mappings
        from config.cultural_mappings import UNIVERSAL_FALLBACK
        
        fallback_tags = {
            "cuisine": UNIVERSAL_FALLBACK["cuisine"],
            "music": UNIVERSAL_FALLBACK["music"],
            "tv_shows": UNIVERSAL_FALLBACK["tv_shows"]
        }
        
        return {
            "cultural_profile": {
                "cultural_elements": {
                    "heritage": "American",
                    "heritage_keywords": ["American", "family traditions"],
                    "cuisine_preferences": ["comfort food"],
                    "music_preferences": ["classical", "nostalgic"],
                    "activity_preferences": ["family activities"],
                    "interests": [],
                    "era_informed": False,
                    "nostalgia_based": True,
                    "birth_year": None
                },
                "qloo_tag_mappings": fallback_tags,
                "era_context": {"has_era_context": False},
                "metadata": {
                    "heritage_source": "fallback",
                    "mapping_approach": "universal_dementia_friendly",
                    "profile_generation_timestamp": datetime.now().isoformat(),
                    "agent_version": "nostalgia_fallback"
                }
            }
        }

# Test function
def test_cultural_profile_builder():
    """Test the updated nostalgia-based cultural profile builder."""
    
    agent = CulturalProfileBuilderAgent()
    
    # Test data matching the curl example
    test_consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,  # Key for nostalgia mapping
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
        
        print("Nostalgia-Based Cultural Profile Builder Test Results:")
        print(f"Heritage: {elements.get('heritage')} (cuisine only)")
        print(f"Birth Year: {elements.get('birth_year')} (for nostalgia)")
        print(f"Interests: {elements.get('interests')}")
        print(f"Era context: {profile.get('era_context', {}).get('has_era_context')}")
        print(f"Qloo mappings: {mappings}")
        print(f"Approach: {mappings.get('approach')}")
        
        return result
    
    return asyncio.run(run_test())

if __name__ == "__main__":
    test_cultural_profile_builder()