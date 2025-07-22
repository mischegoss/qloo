"""
Agent 2: Cultural Profile Builder
Role: Transform patient information into cultural intelligence framework
Follows Responsible Development Guide principles - NO cultural assumptions
"""

from typing import Dict, Any, Optional, List, Set
import re
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class CulturalProfileBuilderAgent(Agent):
    """
    Agent 2: Cultural Profile Builder
    
    Purpose: Transform patient information into cultural intelligence framework
    Input: Consolidated information from Agent 1
    Output: Rich cultural profile with era mapping, heritage context, sensory preferences
    
    Anti-Bias Principles:
    - NO cultural assumptions or stereotypes
    - Individual preferences override demographic patterns
    - Open-ended cultural processing, not predetermined categories
    - Era context without generational assumptions
    """
    
    def __init__(self):
        super().__init__(
            name="cultural_profile_builder",
            description="Builds cultural intelligence framework without assumptions or stereotypes"
        )
    
    async def run(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build cultural profile from consolidated information.
        
        Args:
            consolidated_info: Output from Agent 1 (Information Consolidator)
            
        Returns:
            Cultural profile framework for Qloo API integration
        """
        
        try:
            logger.info("Building cultural profile without assumptions")
            
            # Extract basic demographics safely
            demographics = consolidated_info.get("basic_demographics", {})
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            
            # Build era context (factual, no assumptions)
            era_context = self._build_era_context(demographics.get("birth_context", {}))
            
            # Process cultural sharing (open-ended, no categories)
            cultural_elements = self._process_cultural_sharing(demographics.get("cultural_sharing", {}))
            
            # Map to sensory domains (broad possibilities)
            sensory_mapping = self._create_sensory_mapping(request_context, cultural_elements)
            
            # Build Qloo query framework (anti-bias)
            qloo_framework = self._build_qloo_framework(era_context, cultural_elements, demographics)
            
            # Integrate feedback patterns (individual trumps demographics)
            preference_indicators = self._integrate_feedback_patterns(feedback_patterns)
            
            # Create cultural profile
            cultural_profile = {
                "profile_metadata": {
                    "created_timestamp": datetime.utcnow().isoformat(),
                    "processing_approach": "individual_first_no_assumptions",
                    "cultural_bias_prevention": "active"
                },
                "era_context": era_context,
                "cultural_elements": cultural_elements,
                "sensory_mapping": sensory_mapping,
                "qloo_framework": qloo_framework,
                "preference_indicators": preference_indicators,
                "anti_bias_notes": {
                    "heritage_approach": "open_ended_no_categories",
                    "era_approach": "factual_context_no_assumptions",
                    "individual_priority": "preferences_override_demographics"
                }
            }
            
            # Validate no stereotypes were introduced
            self._validate_anti_bias_compliance(cultural_profile)
            
            logger.info("Cultural profile built successfully without assumptions")
            return {"cultural_profile": cultural_profile}
            
        except Exception as e:
            logger.error(f"Error building cultural profile: {str(e)}")
            return self._create_fallback_cultural_profile(consolidated_info)
    
    def _build_era_context(self, birth_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build factual era context without generational assumptions.
        """
        birth_year = birth_context.get("birth_year")
        birth_month = birth_context.get("birth_month")
        age_range = birth_context.get("age_range", "age_unknown")
        
        if not birth_year:
            return {
                "has_era_context": False,
                "age_range": age_range,
                "approach": "no_era_assumptions"
            }
        
        # Factual era mapping (no cultural assumptions)
        era_context = {
            "has_era_context": True,
            "birth_year": birth_year,
            "birth_month": birth_month,
            "age_range": age_range,
            "decades_lived": self._calculate_decades_lived(birth_year),
            "historical_periods": self._map_historical_periods(birth_year),
            "cultural_eras": self._map_cultural_eras(birth_year),
            "seasonal_context": self._get_seasonal_context(birth_month),
            "approach": "factual_no_assumptions"
        }
        
        return era_context
    
    def _calculate_decades_lived(self, birth_year: int) -> List[str]:
        """Calculate which decades person has lived through (factual)."""
        current_year = datetime.now().year
        decades = []
        
        # Start from birth decade
        start_decade = (birth_year // 10) * 10
        current_decade = (current_year // 10) * 10
        
        decade = start_decade
        while decade <= current_decade:
            decades.append(f"{decade}s")
            decade += 10
        
        return decades
    
    def _map_historical_periods(self, birth_year: int) -> List[str]:
        """Map to broad historical periods (factual, no cultural assumptions)."""
        periods = []
        
        # Factual historical periods
        historical_mapping = {
            "pre_wwii": (1900, 1939),
            "wwii_era": (1939, 1945),
            "post_war_boom": (1945, 1960),
            "cultural_revolution_60s": (1960, 1970),
            "modern_era": (1970, 1990),
            "digital_transition": (1990, 2010),
            "digital_native": (2010, 2025)
        }
        
        for period, (start_year, end_year) in historical_mapping.items():
            # Check if they lived through this period (age 5+ for memories)
            if birth_year + 5 <= end_year and birth_year <= start_year:
                periods.append(period)
        
        return periods
    
    def _map_cultural_eras(self, birth_year: int) -> Dict[str, List[str]]:
        """Map to cultural eras without stereotypical assumptions."""
        
        # Factual cultural periods (no assumptions about what they liked)
        cultural_eras = {
            "music_eras_lived": [],
            "entertainment_eras": [],
            "technology_eras": [],
            "social_movements": []
        }
        
        current_year = datetime.now().year
        
        # Music eras (factual periods, not preference assumptions)
        music_mapping = {
            "swing_big_band": (1930, 1950),
            "early_rock_roll": (1950, 1960),
            "folk_protest": (1960, 1970),
            "disco_funk": (1970, 1980),
            "mtv_generation": (1980, 1990),
            "grunge_alternative": (1990, 2000),
            "digital_music": (2000, 2010),
            "streaming_era": (2010, 2025)
        }
        
        for era, (start, end) in music_mapping.items():
            # They were between ages 10-30 during this era (formative years)
            if (birth_year + 10 <= end) and (birth_year + 30 >= start):
                cultural_eras["music_eras_lived"].append(era)
        
        # Entertainment eras
        entertainment_mapping = {
            "radio_golden_age": (1930, 1950),
            "early_television": (1950, 1970),
            "cable_expansion": (1970, 1990),
            "home_video": (1980, 2000),
            "internet_content": (1995, 2010),
            "streaming_services": (2010, 2025)
        }
        
        for era, (start, end) in entertainment_mapping.items():
            if (birth_year + 5 <= end) and (birth_year <= start + 20):
                cultural_eras["entertainment_eras"].append(era)
        
        return cultural_eras
    
    def _get_seasonal_context(self, birth_month: Optional[str]) -> Dict[str, Any]:
        """Get seasonal context for cultural elements."""
        if not birth_month:
            return {"has_seasonal_context": False}
        
        seasonal_mapping = {
            "winter": ["december", "january", "february"],
            "spring": ["march", "april", "may"],
            "summer": ["june", "july", "august"],
            "fall": ["september", "october", "november"]
        }
        
        season = None
        for season_name, months in seasonal_mapping.items():
            if birth_month in months:
                season = season_name
                break
        
        return {
            "has_seasonal_context": True,
            "birth_season": season,
            "birth_month": birth_month,
            "seasonal_cultural_elements": self._get_seasonal_cultural_elements(season)
        }
    
    def _get_seasonal_cultural_elements(self, season: str) -> List[str]:
        """Get seasonal cultural elements (broad possibilities)."""
        seasonal_elements = {
            "winter": ["holiday_traditions", "comfort_foods", "indoor_activities", "warm_gathering_spaces"],
            "spring": ["renewal_themes", "fresh_foods", "outdoor_activities", "growth_metaphors"],
            "summer": ["outdoor_celebrations", "fresh_produce", "travel_memories", "light_activities"],
            "fall": ["harvest_themes", "transition_times", "cozy_environments", "reflection_activities"]
        }
        
        return seasonal_elements.get(season, [])
    
    def _process_cultural_sharing(self, cultural_sharing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process cultural sharing information without assumptions.
        Open-ended approach respecting individual complexity.
        """
        heritage_info = cultural_sharing.get("heritage_info", "").strip()
        languages = cultural_sharing.get("languages", "").strip()
        spiritual_traditions = cultural_sharing.get("spiritual_traditions", "").strip()
        additional_context = cultural_sharing.get("additional_context", "").strip()
        
        # Extract cultural keywords without making assumptions
        cultural_keywords = self._extract_cultural_keywords(heritage_info, languages, spiritual_traditions, additional_context)
        
        # Process languages (factual)
        language_elements = self._process_languages(languages)
        
        # Process spiritual/cultural traditions (open-ended)
        tradition_elements = self._process_traditions(spiritual_traditions)
        
        # Process heritage information (no stereotypes)
        heritage_elements = self._process_heritage(heritage_info)
        
        # Additional context processing
        additional_elements = self._process_additional_context(additional_context)
        
        return {
            "has_cultural_info": bool(heritage_info or languages or spiritual_traditions or additional_context),
            "cultural_keywords": cultural_keywords,
            "language_elements": language_elements,
            "tradition_elements": tradition_elements,
            "heritage_elements": heritage_elements,
            "additional_elements": additional_elements,
            "processing_approach": "open_ended_no_assumptions",
            "complexity_respected": "mixed_heritage_welcomed"
        }
    
    def _extract_cultural_keywords(self, *text_inputs) -> Set[str]:
        """Extract cultural keywords without assumptions."""
        all_text = " ".join(filter(None, text_inputs)).lower()
        
        # Extract meaningful cultural terms (no assumptions about what they mean)
        cultural_patterns = [
            r'\b(\w+)[\s\-]?american\b',  # X-American heritage
            r'\b(\w+)[\s\-]?heritage\b',  # X heritage
            r'\b(\w+)[\s\-]?tradition\b', # X tradition
            r'\b(\w+)[\s\-]?culture\b',   # X culture
            r'\b(\w+)[\s\-]?family\b',    # X family
            r'\b(\w+)[\s\-]?background\b', # X background
            r'\b(\w+)[\s\-]?roots\b',     # X roots
            r'\b(\w+)[\s\-]?community\b', # X community
        ]
        
        keywords = set()
        for pattern in cultural_patterns:
            matches = re.findall(pattern, all_text)
            keywords.update(matches)
        
        # Also extract standalone cultural/geographic terms
        potential_cultural_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', " ".join(text_inputs))
        
        # Filter for likely cultural terms (simple heuristic)
        for term in potential_cultural_terms:
            if len(term) > 3 and term.lower() not in ['the', 'and', 'but', 'they', 'were', 'have', 'with']:
                keywords.add(term.lower())
        
        return keywords
    
    def _process_languages(self, languages: str) -> Dict[str, Any]:
        """Process language information factually."""
        if not languages:
            return {"has_languages": False}
        
        # Simple language extraction
        language_list = [lang.strip() for lang in re.split(r'[,;]+', languages) if lang.strip()]
        
        return {
            "has_languages": True,
            "languages": language_list,
            "multilingual": len(language_list) > 1,
            "primary_language": language_list[0] if language_list else None
        }
    
    def _process_traditions(self, spiritual_traditions: str) -> Dict[str, Any]:
        """Process spiritual/cultural traditions without assumptions."""
        if not spiritual_traditions:
            return {"has_traditions": False}
        
        # Extract tradition keywords
        tradition_keywords = self._extract_cultural_keywords(spiritual_traditions)
        
        return {
            "has_traditions": True,
            "tradition_text": spiritual_traditions[:200],  # Limit for privacy
            "tradition_keywords": list(tradition_keywords),
            "approach": "open_ended_respectful"
        }
    
    def _process_heritage(self, heritage_info: str) -> Dict[str, Any]:
        """Process heritage information without stereotypes."""
        if not heritage_info:
            return {"has_heritage": False}
        
        # Extract heritage keywords
        heritage_keywords = self._extract_cultural_keywords(heritage_info)
        
        return {
            "has_heritage": True,
            "heritage_text": heritage_info[:200],  # Limit for privacy
            "heritage_keywords": list(heritage_keywords),
            "complexity_note": "mixed_heritage_respected",
            "approach": "individual_not_stereotypical"
        }
    
    def _process_additional_context(self, additional_context: str) -> Dict[str, Any]:
        """Process additional context provided by caregiver."""
        if not additional_context:
            return {"has_additional": False}
        
        # Extract any additional cultural elements
        additional_keywords = self._extract_cultural_keywords(additional_context)
        
        return {
            "has_additional": True,
            "context_text": additional_context[:300],  # Limit for privacy
            "additional_keywords": list(additional_keywords),
            "source": "caregiver_provided"
        }
    
    def _create_sensory_mapping(self, request_context: Dict[str, Any], cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map cultural elements to sensory domains for multi-sensory experiences.
        """
        request_type = request_context.get("request_type", "dashboard")
        context = request_context.get("context", {})
        sensory_focus = context.get("sensory_focus", ["all_senses"])
        
        # Cultural elements that could map to different senses
        cultural_keywords = cultural_elements.get("cultural_keywords", set())
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        language_elements = cultural_elements.get("language_elements", {})
        
        sensory_mapping = {
            "primary_senses": sensory_focus,
            "cultural_sensory_connections": {
                "auditory": {
                    "music_cultural_keywords": list(cultural_keywords),
                    "language_connections": language_elements,
                    "potential_genres": []  # Will be filled by Qloo
                },
                "gustatory": {
                    "cuisine_cultural_keywords": list(heritage_keywords),
                    "potential_cuisines": [],  # Will be filled by Qloo
                    "dietary_considerations": []
                },
                "visual": {
                    "cultural_imagery_keywords": list(cultural_keywords),
                    "potential_content": [],  # Will be filled by Qloo
                    "visual_themes": []
                },
                "olfactory": {
                    "scent_cultural_connections": list(heritage_keywords),
                    "potential_aromatherapy": [],
                    "cooking_scents": []
                },
                "tactile": {
                    "texture_cultural_connections": list(cultural_keywords),
                    "craft_traditions": [],
                    "comfort_objects": []
                }
            },
            "cross_sensory_themes": self._identify_cross_sensory_themes(cultural_elements),
            "approach": "broad_possibilities_no_assumptions"
        }
        
        return sensory_mapping
    
    def _identify_cross_sensory_themes(self, cultural_elements: Dict[str, Any]) -> List[str]:
        """Identify themes that could work across multiple senses."""
        themes = []
        
        cultural_keywords = cultural_elements.get("cultural_keywords", set())
        
        # Broad thematic connections (no stereotypes)
        for keyword in cultural_keywords:
            if any(food_word in keyword for food_word in ['food', 'cooking', 'meal', 'kitchen']):
                themes.append("culinary_experiences")
            if any(music_word in keyword for music_word in ['music', 'song', 'dance', 'instrument']):
                themes.append("musical_experiences")
            if any(family_word in keyword for family_word in ['family', 'tradition', 'celebration']):
                themes.append("family_traditions")
            if any(place_word in keyword for place_word in ['home', 'neighborhood', 'city', 'country']):
                themes.append("place_connections")
        
        return themes
    
    def _build_qloo_framework(self, era_context: Dict[str, Any], cultural_elements: Dict[str, Any], demographics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build framework for Qloo API calls without cultural assumptions.
        """
        age_range = demographics.get("birth_context", {}).get("age_range", "age_unknown")
        general_location = demographics.get("general_location", {})
        
        # Build Qloo query parameters (individual-first approach)
        qloo_framework = {
            "demographic_signals": {
                "age_range": age_range,
                "general_location": {
                    "city_region": general_location.get("city_region", ""),
                    "state_region": general_location.get("state_region", "")
                }
            },
            "cultural_signals": {
                "heritage_keywords": cultural_elements.get("heritage_elements", {}).get("heritage_keywords", []),
                "tradition_keywords": cultural_elements.get("tradition_elements", {}).get("tradition_keywords", []),
                "language_elements": cultural_elements.get("language_elements", {}).get("languages", []),
                "additional_keywords": cultural_elements.get("additional_elements", {}).get("additional_keywords", [])
            },
            "era_signals": {
                "birth_year": era_context.get("birth_year"),
                "decades_lived": era_context.get("decades_lived", []),
                "cultural_eras": era_context.get("cultural_eras", {}),
                "historical_periods": era_context.get("historical_periods", [])
            },
            "query_approach": {
                "method": "broad_exploration_no_assumptions",
                "bias_prevention": "individual_overrides_demographics",
                "cultural_respect": "open_ended_discovery"
            }
        }
        
        return qloo_framework
    
    def _integrate_feedback_patterns(self, feedback_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate feedback patterns - individual preferences override everything.
        """
        if not feedback_patterns.get("has_feedback"):
            return {
                "has_preferences": False,
                "approach": "open_discovery"
            }
        
        blocked_content = feedback_patterns.get("blocked_content", {})
        positive_patterns = feedback_patterns.get("positive_patterns", {})
        negative_patterns = feedback_patterns.get("negative_patterns", {})
        
        return {
            "has_preferences": True,
            "blocked_content": blocked_content,
            "successful_patterns": positive_patterns,
            "avoided_patterns": negative_patterns,
            "preference_priority": "individual_first",
            "override_note": "individual_preferences_override_cultural_demographics"
        }
    
    def _validate_anti_bias_compliance(self, cultural_profile: Dict[str, Any]) -> None:
        """
        Validate that no cultural stereotypes or assumptions were introduced.
        """
        # Check for stereotypical assumptions
        cultural_elements = cultural_profile.get("cultural_elements", {})
        qloo_framework = cultural_profile.get("qloo_framework", {})
        
        # Ensure no predetermined cultural "packages"
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        
        # Log if any suspicious patterns detected
        stereotype_indicators = ["must", "always", "typical", "traditional", "should", "expected"]
        
        for element in str(cultural_profile).lower().split():
            if element in stereotype_indicators:
                logger.warning(f"Potential stereotype language detected: {element}")
        
        # Ensure individual approach is maintained
        if not cultural_profile.get("anti_bias_notes", {}).get("individual_priority"):
            logger.warning("Individual priority not properly documented")
        
        logger.info("Anti-bias compliance validation completed")
    
    def _create_fallback_cultural_profile(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create safe fallback cultural profile."""
        return {
            "cultural_profile": {
                "profile_metadata": {
                    "created_timestamp": datetime.utcnow().isoformat(),
                    "processing_approach": "safe_fallback_no_assumptions",
                    "cultural_bias_prevention": "active"
                },
                "era_context": {"has_era_context": False, "approach": "no_assumptions"},
                "cultural_elements": {"has_cultural_info": False, "approach": "open_discovery"},
                "sensory_mapping": {"primary_senses": ["all_senses"], "approach": "broad_exploration"},
                "qloo_framework": {"query_approach": {"method": "general_discovery", "bias_prevention": "active"}},
                "preference_indicators": {"has_preferences": False, "approach": "open_discovery"},
                "anti_bias_notes": {
                    "heritage_approach": "no_assumptions_made",
                    "era_approach": "no_generational_stereotypes",
                    "individual_priority": "preferences_over_demographics",
                    "fallback_mode": True
                }
            }
        }