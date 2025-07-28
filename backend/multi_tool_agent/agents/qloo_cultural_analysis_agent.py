"""
Agent 3: Qloo Cultural Analysis - UPDATED FOR ANONYMIZED PROFILES
File: backend/multi_tool_agent/agents/qloo_cultural_analysis_agent.py

UPDATED FOR PII COMPLIANCE:
- Accepts anonymized profile format (no names, no location)
- Works with age_group, cultural_heritage, interests only
- Heritage → classical artists + cuisine places
- No complex age/location/URN filtering  
- Uses new simplified qloo_tools.py methods
- Clean, reliable, fast, PII-compliant
"""

import logging
from datetime import datetime, date
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class QlooCulturalAnalysisAgent:
    """
    UPDATED Agent 3: Cultural Analysis using anonymized profile approach.
    PII-COMPLIANT: Works with anonymized data only.
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("✅ Step 3: PII-Compliant Qloo Cultural Analysis Agent initialized")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        UPDATED: Generate cultural intelligence using anonymized profile only.
        PII-COMPLIANT: No names, no location data used.
        
        Args:
            consolidated_info: Contains anonymized patient_profile with cultural_heritage, age_group, interests
            cultural_profile: Optional cultural profile data (not used in simplified version)
        """
        
        logger.info("🚀 Step 3: Starting PII-Compliant Qloo Cultural Analysis")
        
        try:
            # Extract anonymized profile from consolidated info
            patient_profile = consolidated_info.get("patient_profile", {})
            
            # Fallback to patient_info if patient_profile not found
            if not patient_profile:
                patient_profile = consolidated_info.get("patient_info", {})
            
            # ANONYMIZED DATA EXTRACTION - No PII
            cultural_heritage = patient_profile.get("cultural_heritage", "American")
            age_group = patient_profile.get("age_group", "senior")
            birth_year = patient_profile.get("birth_year")
            interests = patient_profile.get("interests", [])
            profile_complete = patient_profile.get("profile_complete", False)
            
            # PII VALIDATION - Ensure no names or location data present
            pii_detected = any(field in patient_profile for field in 
                             ["first_name", "last_name", "name", "city", "state", "address"])
            
            if pii_detected:
                logger.warning("🚨 PII detected in profile - using fallback approach")
                return self._create_fallback_response(cultural_heritage, age_group)
            
            logger.info(f"🔒 Anonymized profile validated:")
            logger.info(f"   - Cultural heritage: {cultural_heritage}")
            logger.info(f"   - Age group: {age_group}")
            logger.info(f"   - Birth year: {birth_year or 'not provided'}")
            logger.info(f"   - Interests: {interests}")
            logger.info(f"   - Profile complete: {profile_complete}")
            
            # Check if Qloo tool is available
            if not self.qloo_tool:
                logger.info("⚠️ No Qloo tool - will use fallback data only")
                return self._create_fallback_response(cultural_heritage, age_group)
            
            logger.info("✅ Qloo tool available - will attempt API calls")
            
            # Generate daily seed for variety
            today_str = date.today().isoformat()
            daily_seed = hash(f"{today_str}-{cultural_heritage}-{age_group}")
            logger.info(f"📅 Daily seed: {daily_seed}")
            
            # ANONYMIZED QLOO CALLS: Make heritage-based cultural calls
            logger.info("🎵🍽️ Making focused Qloo calls with anonymized data: Artists + Places")
            
            cultural_results = await self.qloo_tool.make_cultural_calls(cultural_heritage)
            
            # Check results
            successful_calls = cultural_results.get("successful_calls", 0)
            total_results = cultural_results.get("total_results", 0)
            
            logger.info(f"🎯 Cultural calls completed: {successful_calls}/2 successful")
            
            # Format response with anonymized metadata
            qloo_intelligence = {
                "cultural_recommendations": cultural_results.get("cultural_recommendations", {}),
                "metadata": {
                    "agent": "qloo_cultural_analysis",
                    "version": "anonymized_heritage_only",
                    "approach": "pii_compliant_heritage_calls",
                    "cultural_heritage": cultural_heritage,
                    "age_group": age_group,
                    "birth_year": birth_year,
                    "interests_count": len(interests),
                    "profile_complete": profile_complete,
                    "successful_calls": successful_calls,
                    "total_results": total_results,
                    "daily_seed": daily_seed,
                    "anonymized": True,
                    "pii_compliant": True,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            logger.info("✅ Step 3: PII-compliant Qloo cultural analysis completed")
            
            return {"qloo_intelligence": qloo_intelligence}
            
        except Exception as e:
            logger.error(f"❌ Step 3: Cultural analysis failed: {e}")
            # Extract safe fallback data
            heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
            age_group = consolidated_info.get("patient_profile", {}).get("age_group", "senior")
            
            if not heritage:
                heritage = consolidated_info.get("patient_info", {}).get("cultural_heritage", "American")
                age_group = consolidated_info.get("patient_info", {}).get("age_group", "senior")
                
            return self._create_fallback_response(heritage, age_group)
    
    def _create_fallback_response(self, heritage: str, age_group: str = "senior") -> Dict[str, Any]:
        """
        Create fallback cultural intelligence when Qloo is unavailable.
        UPDATED: Uses anonymized data only.
        """
        
        logger.info(f"🔄 Creating anonymized fallback cultural intelligence for {heritage} ({age_group})")
        
        # Heritage-specific fallbacks with age-appropriate content
        heritage_data = {
            "Italian-American": {
                "artists": [
                    {"name": "Luciano Pavarotti", "type": "Opera singer", "era": "1935-2007"},
                    {"name": "Antonio Vivaldi", "type": "Baroque composer", "era": "1678-1741"},
                    {"name": "Giacomo Puccini", "type": "Opera composer", "era": "1858-1924"}
                ],
                "places": [
                    {"name": "Traditional Italian Trattoria", "type": "Italian restaurant"},
                    {"name": "Family-Style Italian Kitchen", "type": "Casual Italian dining"},
                    {"name": "Classic Italian Bakery", "type": "Italian pastries"}
                ]
            },
            "Irish": {
                "artists": [
                    {"name": "Celtic Orchestra", "type": "Traditional ensemble"},
                    {"name": "Irish Traditional Musicians", "type": "Folk group"},
                    {"name": "Dublin Philharmonic", "type": "Classical orchestra"}
                ],
                "places": [
                    {"name": "Traditional Irish Pub", "type": "Irish restaurant"},
                    {"name": "Celtic Kitchen", "type": "Irish comfort food"},
                    {"name": "Irish Family Restaurant", "type": "Traditional Irish"}
                ]
            },
            "Mexican": {
                "artists": [
                    {"name": "Mariachi Vargas", "type": "Traditional mariachi", "era": "1897-present"},
                    {"name": "Agustín Lara", "type": "Mexican composer", "era": "1897-1970"},
                    {"name": "José Alfredo Jiménez", "type": "Ranchera singer", "era": "1926-1973"}
                ],
                "places": [
                    {"name": "Traditional Mexican Restaurant", "type": "Mexican cuisine"},
                    {"name": "Family Mexican Kitchen", "type": "Home-style Mexican"},
                    {"name": "Mexican Cantina", "type": "Traditional Mexican"}
                ]
            },
            "American": {
                "artists": [
                    {"name": "Aaron Copland", "type": "American composer", "era": "1900-1990"},
                    {"name": "George Gershwin", "type": "American composer", "era": "1898-1937"},
                    {"name": "John Philip Sousa", "type": "March composer", "era": "1854-1932"}
                ],
                "places": [
                    {"name": "Classic American Diner", "type": "American restaurant"},
                    {"name": "Hometown Comfort Food", "type": "Family dining"},
                    {"name": "Traditional American Cafe", "type": "American classics"}
                ]
            }
        }
        
        # Get appropriate fallback data
        fallback_data = heritage_data.get(heritage, heritage_data["American"])
        
        # Age-appropriate adjustments for oldest_senior
        if age_group == "oldest_senior":
            # Emphasize more classical/traditional options
            if heritage == "Italian-American":
                fallback_data["artists"] = [
                    {"name": "Enrico Caruso", "type": "Opera tenor", "era": "1873-1921"},
                    {"name": "Antonio Vivaldi", "type": "Baroque composer", "era": "1678-1741"},
                    {"name": "Giuseppe Verdi", "type": "Opera composer", "era": "1813-1901"}
                ]
        
        qloo_intelligence = {
            "cultural_recommendations": {
                "artists": {
                    "success": True,
                    "entities": fallback_data["artists"],
                    "entity_count": len(fallback_data["artists"]),
                    "content_type": "fallback"
                },
                "places": {
                    "success": True,
                    "entities": fallback_data["places"],
                    "entity_count": len(fallback_data["places"]),
                    "content_type": "fallback"
                }
            },
            "metadata": {
                "agent": "qloo_cultural_analysis",
                "version": "anonymized_heritage_only",
                "approach": "fallback_heritage_data",
                "cultural_heritage": heritage,
                "age_group": age_group,
                "successful_calls": 0,
                "total_results": len(fallback_data["artists"]) + len(fallback_data["places"]),
                "fallback_reason": "qloo_unavailable_or_pii_detected",
                "anonymized": True,
                "pii_compliant": True,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return {"qloo_intelligence": qloo_intelligence}

# Export for backwards compatibility with existing imports
QlooCulturalIntelligenceAgent = QlooCulturalAnalysisAgent

# Export for imports
__all__ = ["QlooCulturalAnalysisAgent", "QlooCulturalIntelligenceAgent"]