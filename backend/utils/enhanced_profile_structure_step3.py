"""
Step 3: Enhanced Profile Structure Extension
File: backend/utils/enhanced_profile_structure_step3.py

Extends the profile structure to include cultural intelligence data from Step 3.
Maintains clean data contracts for Step 4 (Gemini Content Curation).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def validate_step3_output(enhanced_profile: Dict[str, Any]) -> Dict[str, bool]:
    """
    Validate that Step 3 completed successfully and profile is ready for Step 4
    
    Args:
        enhanced_profile: Complete profile from Steps 1-3
        
    Returns:
        Validation results with detailed checks
    """
    
    validation = {
        "valid": False,
        "has_cultural_intelligence": False,
        "has_artists_data": False,
        "has_places_data": False,
        "pipeline_state_valid": False,
        "ready_for_step4": False,
        "data_structure_valid": False
    }
    
    try:
        # Check for cultural intelligence section
        cultural_intelligence = enhanced_profile.get("cultural_intelligence")
        if cultural_intelligence:
            validation["has_cultural_intelligence"] = True
            
            # Check cultural recommendations
            cultural_recs = cultural_intelligence.get("cultural_recommendations", {})
            
            # Validate artists data
            artists_data = cultural_recs.get("artists", {})
            if (artists_data.get("available") or 
                artists_data.get("status") == "skipped" or
                artists_data.get("method") == "fallback"):
                validation["has_artists_data"] = True
            
            # Validate places data
            places_data = cultural_recs.get("places", {})
            if (places_data.get("available") or 
                places_data.get("status") == "skipped" or
                places_data.get("method") == "fallback"):
                validation["has_places_data"] = True
            
            # Check metadata
            metadata = cultural_intelligence.get("metadata", {})
            if (metadata.get("agent") == "qloo_cultural_analysis" and
                metadata.get("step") == 3):
                validation["data_structure_valid"] = True
        
        # Check pipeline state
        pipeline_state = enhanced_profile.get("pipeline_state", {})
        if (pipeline_state.get("current_step") == 3 and
            pipeline_state.get("next_step") == 4 and
            pipeline_state.get("ready_for_step4")):
            validation["pipeline_state_valid"] = True
            validation["ready_for_step4"] = True
        
        # Overall validation
        validation["valid"] = (
            validation["has_cultural_intelligence"] and
            validation["has_artists_data"] and
            validation["has_places_data"] and
            validation["pipeline_state_valid"] and
            validation["data_structure_valid"]
        )
        
        return validation
        
    except Exception as e:
        logger.error(f"❌ Step 3 validation failed: {e}")
        return validation

def extract_for_step4(enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract data needed for Step 4 (Gemini Content Curation)
    
    Args:
        enhanced_profile: Complete profile from Steps 1-3
        
    Returns:
        Clean data package for Step 4
    """
    
    try:
        # Extract core profile data
        patient_info = enhanced_profile.get("patient_info", {})
        theme_info = enhanced_profile.get("theme_info", {})
        photo_analysis = enhanced_profile.get("photo_analysis", {})
        cultural_intelligence = enhanced_profile.get("cultural_intelligence", {})
        
        # Extract cultural recommendations
        cultural_recs = cultural_intelligence.get("cultural_recommendations", {})
        artists_data = cultural_recs.get("artists", {})
        places_data = cultural_recs.get("places", {})
        
        # Package for Step 4
        step4_data = {
            # Patient context
            "patient_context": {
                "first_name": patient_info.get("first_name", ""),
                "cultural_heritage": patient_info.get("cultural_heritage", "American"),
                "birth_year": patient_info.get("birth_year", 1945),
                "age_demographic": cultural_intelligence.get("metadata", {}).get("age_demographic", "55_and_older")
            },
            
            # Theme context
            "theme_context": {
                "theme_name": theme_info.get("name", "Unknown"),
                "theme_id": theme_info.get("id", "unknown"),
                "photo_filename": theme_info.get("photo_filename", ""),
                "conversation_starters": theme_info.get("conversation_starters", [])
            },
            
            # Photo analysis for curation
            "photo_context": {
                "analysis_data": photo_analysis.get("analysis_data", {}),
                "theme_connection": photo_analysis.get("theme_connection", ""),
                "conversation_starters": photo_analysis.get("analysis_data", {}).get("conversation_starters", [])
            },
            
            # Cultural recommendations for curation
            "cultural_recommendations": {
                "artists": {
                    "available": artists_data.get("available", False),
                    "entities": artists_data.get("entities", []),
                    "entity_count": artists_data.get("entity_count", 0),
                    "method": artists_data.get("method", "unknown")
                },
                "places": {
                    "available": places_data.get("available", False),
                    "entities": places_data.get("entities", []),
                    "entity_count": places_data.get("entity_count", 0),
                    "method": places_data.get("method", "unknown"),
                    "heritage": places_data.get("heritage", "")
                }
            },
            
            # Metadata for Step 4
            "metadata": {
                "steps_completed": [1, 2, 3],
                "ready_for_gemini_curation": True,
                "cultural_intelligence_method": cultural_intelligence.get("metadata", {}).get("method", ""),
                "successful_qloo_calls": cultural_intelligence.get("metadata", {}).get("successful_calls", 0),
                "extraction_timestamp": datetime.now().isoformat()
            }
        }
        
        logger.info("✅ Step 4 data extraction completed")
        return step4_data
        
    except Exception as e:
        logger.error(f"❌ Step 4 data extraction failed: {e}")
        return {"error": str(e), "ready_for_gemini_curation": False}

def get_cultural_insights_summary(enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of cultural insights for logging/debugging
    
    Args:
        enhanced_profile: Complete profile from Steps 1-3
        
    Returns:
        Summary of cultural intelligence insights
    """
    
    try:
        cultural_intelligence = enhanced_profile.get("cultural_intelligence", {})
        cultural_recs = cultural_intelligence.get("cultural_recommendations", {})
        metadata = cultural_intelligence.get("metadata", {})
        
        # Extract artists summary
        artists_data = cultural_recs.get("artists", {})
        artists_summary = {
            "available": artists_data.get("available", False),
            "count": artists_data.get("entity_count", 0),
            "method": artists_data.get("method", "unknown"),
            "sample_artists": [
                entity.get("name", "Unknown") 
                for entity in artists_data.get("entities", [])[:3]
            ]
        }
        
        # Extract places summary
        places_data = cultural_recs.get("places", {})
        places_summary = {
            "available": places_data.get("available", False),
            "count": places_data.get("entity_count", 0),
            "method": places_data.get("method", "unknown"),
            "heritage": places_data.get("heritage", ""),
            "sample_places": [
                entity.get("name", "Unknown") 
                for entity in places_data.get("entities", [])[:3]
            ]
        }
        
        return {
            "cultural_heritage": metadata.get("heritage", "Unknown"),
            "age_demographic": metadata.get("age_demographic", "Unknown"),
            "successful_calls": metadata.get("successful_calls", 0),
            "total_results": metadata.get("total_results", 0),
            "artists": artists_summary,
            "places": places_summary,
            "timestamp": metadata.get("timestamp", ""),
            "ready_for_curation": True
        }
        
    except Exception as e:
        logger.error(f"❌ Cultural insights summary failed: {e}")
        return {"error": str(e), "ready_for_curation": False}

def create_step3_test_profile() -> Dict[str, Any]:
    """
    Create a test enhanced profile with Step 3 data for testing Step 4
    
    Returns:
        Mock enhanced profile with cultural intelligence data
    """
    
    return {
        "patient_info": {
            "first_name": "Maria",
            "birth_year": 1945,
            "cultural_heritage": "Italian-American",
            "city": "Brooklyn",
            "state": "New York"
        },
        
        "theme_info": {
            "id": "birthday",
            "name": "Birthday",
            "photo_filename": "birthday.png",
            "conversation_starters": [
                "What was your favorite birthday memory?",
                "How did your family celebrate birthdays?"
            ]
        },
        
        "photo_analysis": {
            "photo_filename": "birthday.png",
            "analysis_method": "pre_analyzed",
            "analysis_data": {
                "description": "A warm birthday celebration scene",
                "conversation_starters": [
                    "This reminds me of birthday parties - what was your favorite cake?",
                    "Do you remember blowing out candles as a child?"
                ]
            },
            "theme_connection": "Birthday",
            "success": True
        },
        
        "cultural_intelligence": {
            "cultural_recommendations": {
                "artists": {
                    "available": True,
                    "entities": [
                        {"name": "Dean Martin", "music_genre": "jazz", "properties": {"year": "1950s"}},
                        {"name": "Frank Sinatra", "music_genre": "traditional pop", "properties": {"year": "1940s"}},
                        {"name": "Tony Bennett", "music_genre": "traditional pop", "properties": {"year": "1950s"}}
                    ],
                    "entity_count": 3,
                    "method": "qloo_api"
                },
                "places": {
                    "available": True,
                    "entities": [
                        {"name": "Mama's Italian Kitchen", "properties": {"cuisine": "Italian", "specialties": ["pasta", "marinara"]}},
                        {"name": "Tony's Family Restaurant", "properties": {"cuisine": "Italian", "specialties": ["pizza", "garlic bread"]}},
                        {"name": "Little Italy Bistro", "properties": {"cuisine": "Italian", "specialties": ["lasagna", "tiramisu"]}}
                    ],
                    "entity_count": 3,
                    "method": "qloo_api",
                    "heritage": "Italian-American"
                }
            },
            "metadata": {
                "agent": "qloo_cultural_analysis",
                "step": 3,
                "approach": "simplified_two_calls",
                "heritage": "Italian-American",
                "age_demographic": "55_and_older",
                "successful_calls": 2,
                "total_results": 6,
                "timestamp": datetime.now().isoformat()
            }
        },
        
        "pipeline_state": {
            "current_step": 3,
            "next_step": 4,
            "step_name": "qloo_cultural_analysis",
            "completion_time": datetime.now().isoformat(),
            "ready_for_step4": True
        }
    }