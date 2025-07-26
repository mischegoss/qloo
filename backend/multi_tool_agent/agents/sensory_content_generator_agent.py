"""
Sensory Content Generator Agent - SAFE CONTENT with Qloo → YouTube Pipeline
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

NEW FEATURES:
- Qloo → YouTube public domain pipeline
- Classical music focus for copyright safety
- Vintage TV content filtering
- Heritage-aware classical music selection
- Copyright-compliant content generation
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent:
    """
    Agent 4: Generates sensory content using SAFE COPYRIGHT-COMPLIANT pipeline.
    
    SAFE CONTENT WORKFLOW:
    1. Use Qloo for cultural intelligence (classical composers, vintage TV)
    2. Search YouTube for public domain versions
    3. Generate dementia-friendly recipes 
    4. Focus on pre-1970 content for copyright safety
    """
    
    def __init__(self, gemini_tool=None, youtube_tool=None):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        logger.info("🎨 Sensory Content Generator initialized with SAFE CONTENT pipeline")
        logger.info("🎼 Focus: Classical music + vintage TV (public domain)")
    
    async def run(self, consolidated_info: Dict[str, Any], 
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate safe sensory content using Qloo → YouTube public domain pipeline.
        """
        
        logger.info("🎨 Agent 4: Generating SAFE sensory content (classical + vintage)")
        
        try:
            # Extract patient information
            patient_profile = consolidated_info.get("patient_profile", {})
            current_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
            
            heritage = patient_profile.get("cultural_heritage", "universal")
            birth_year = patient_profile.get("birth_year", 1945)
            gender = patient_profile.get("gender")
            
            # Calculate age group for Qloo
            current_year = datetime.now().year
            age = current_year - birth_year if birth_year else 80
            age_group = "75_and_older" if age >= 75 else "55_to_74"
            
            logger.info(f"🎯 Generating safe content for {heritage}, age group {age_group}")
            
            # Generate content using safe pipeline
            sensory_content = await self._generate_safe_sensory_content(
                heritage=heritage,
                age_group=age_group,
                gender=gender,
                current_theme=current_theme,
                qloo_intelligence=qloo_intelligence
            )
            
            logger.info("✅ Agent 4: Safe sensory content generated successfully")
            return {
                "sensory_content": sensory_content,
                "generation_metadata": {
                    "content_safety": "PUBLIC_DOMAIN_ONLY",
                    "heritage": heritage,
                    "age_group": age_group,
                    "pipeline": "qloo_youtube_safe",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._generate_safe_fallback_content(heritage)
    
    async def _generate_safe_sensory_content(self,
                                           heritage: str,
                                           age_group: str, 
                                           gender: Optional[str],
                                           current_theme: Dict[str, Any],
                                           qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate safe sensory content using Qloo intelligence + YouTube public domain search.
        """
        
        logger.info("🔄 Starting Qloo → YouTube safe content pipeline")
        
        # Step 1: Get Qloo recommendations for safe content
        if hasattr(self.youtube_tool, 'qloo_tool'):
            qloo_tool = self.youtube_tool.qloo_tool
        else:
            # Extract Qloo tool from intelligence data or use fallback
            qloo_tool = None
        
        # Generate classical music content
        music_content = await self._generate_safe_music_content(
            heritage, age_group, gender, current_theme, qloo_intelligence
        )
        
        # Generate vintage TV content  
        tv_content = await self._generate_safe_tv_content(
            heritage, age_group, gender, current_theme, qloo_intelligence
        )
        
        # Generate safe recipe content
        recipe_content = await self._generate_safe_recipe_content(
            heritage, current_theme
        )
        
        return {
            "content_by_sense": {
                "auditory": {
                    "elements": [music_content],
                    "primary_focus": "classical_music",
                    "safety_level": "public_domain"
                },
                "visual": {
                    "elements": [tv_content], 
                    "primary_focus": "vintage_television",
                    "safety_level": "public_domain"
                },
                "gustatory": {
                    "elements": [recipe_content],
                    "primary_focus": "traditional_recipes",
                    "safety_level": "original_content"
                }
            },
            "content_safety": {
                "copyright_status": "SAFE",
                "music_type": "classical_public_domain", 
                "tv_type": "vintage_public_domain",
                "recipe_type": "ai_generated"
            }
        }
    
    async def _generate_safe_music_content(self,
                                         heritage: str,
                                         age_group: str,
                                         gender: Optional[str], 
                                         current_theme: Dict[str, Any],
                                         qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safe classical music content"""
        
        logger.info(f"🎼 Generating safe classical music for {heritage}")
        
        try:
            # Try to get Qloo classical recommendations from existing intelligence
            classical_recommendations = self._extract_classical_from_qloo(qloo_intelligence, heritage)
            
            # Search YouTube for public domain classical content
            if self.youtube_tool:
                youtube_result = await self.youtube_tool.search_public_domain_classical(
                    classical_recommendations
                )
                
                if youtube_result and youtube_result.get("items"):
                    item = youtube_result["items"][0]
                    snippet = item.get("snippet", {})
                    
                    return {
                        "name": snippet.get("title", "Classical Music"),
                        "artist": snippet.get("channelTitle", "Classical Composer"),
                        "youtube_url": item.get("embeddable_url", ""),
                        "genre": "Classical",
                        "era": "Public Domain",
                        "theme_relevance": current_theme.get("name", "Memory"),
                        "safety_status": "public_domain",
                        "source": "qloo_youtube_classical"
                    }
            
            # Fallback to safe classical content
            return self._get_classical_music_fallback(heritage)
            
        except Exception as e:
            logger.error(f"Error generating safe music: {e}")
            return self._get_classical_music_fallback(heritage)
    
    async def _generate_safe_tv_content(self,
                                      heritage: str,
                                      age_group: str,
                                      gender: Optional[str],
                                      current_theme: Dict[str, Any],
                                      qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safe vintage TV content"""
        
        logger.info(f"📺 Generating safe vintage TV for {heritage}")
        
        try:
            # Try to get vintage TV recommendations from Qloo
            vintage_recommendations = self._extract_vintage_tv_from_qloo(qloo_intelligence)
            
            # Search YouTube for public domain vintage TV
            if self.youtube_tool:
                youtube_result = await self.youtube_tool.search_public_domain_vintage_tv(
                    vintage_recommendations
                )
                
                if youtube_result and youtube_result.get("items"):
                    item = youtube_result["items"][0]
                    snippet = item.get("snippet", {})
                    
                    return {
                        "name": snippet.get("title", "Classic Television"),
                        "youtube_url": item.get("embeddable_url", ""),
                        "description": snippet.get("description", "Vintage family entertainment"),
                        "era": "1940s-1950s",
                        "theme_relevance": current_theme.get("name", "Memory"),
                        "safety_status": "public_domain",
                        "source": "qloo_youtube_vintage"
                    }
            
            # Fallback to safe vintage content
            return self._get_vintage_tv_fallback()
            
        except Exception as e:
            logger.error(f"Error generating safe TV: {e}")
            return self._get_vintage_tv_fallback()
    
    async def _generate_safe_recipe_content(self,
                                          heritage: str,
                                          current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safe recipe content using Gemini AI"""
        
        logger.info(f"🍽️ Generating safe recipe for {heritage}")
        
        try:
            if self.gemini_tool:
                # Use traditional/heritage recipes (no copyright issues)
                theme_name = current_theme.get("name", "comfort")
                recipe_result = await self.gemini_tool.get_recipe_suggestion(
                    cultural_heritage=heritage,
                    theme_context=f"Traditional {heritage} cooking for {theme_name} theme"
                )
                
                if recipe_result:
                    return {
                        "name": recipe_result.get("name", "Traditional Recipe"),
                        "ingredients": recipe_result.get("ingredients", []),
                        "instructions": recipe_result.get("instructions", []),
                        "prep_time": recipe_result.get("total_time", "30 minutes"),
                        "difficulty": "Easy",
                        "cultural_context": heritage,
                        "safety_status": "ai_generated_original",
                        "source": "gemini_ai"
                    }
            
            # Fallback recipe
            return self._get_safe_recipe_fallback(heritage)
            
        except Exception as e:
            logger.error(f"Error generating safe recipe: {e}")
            return self._get_safe_recipe_fallback(heritage)
    
    def _extract_classical_from_qloo(self, qloo_intelligence: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Extract classical music recommendations from Qloo data"""
        
        # Look for classical composers in Qloo results
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        artists_data = cultural_recommendations.get("artists", {})
        entities = artists_data.get("entities", [])
        
        classical_entities = []
        classical_keywords = ["classical", "opera", "symphony", "baroque", "romantic"]
        
        for entity in entities:
            name = entity.get("name", "").lower()
            tags = [tag.get("name", "").lower() for tag in entity.get("tags", [])]
            
            # Check if it's classical music
            is_classical = any(keyword in name or any(keyword in tag for tag in tags)
                              for keyword in classical_keywords)
            
            if is_classical:
                classical_entities.append(entity)
        
        return {
            "success": len(classical_entities) > 0,
            "entities": classical_entities,
            "heritage": heritage
        }
    
    def _extract_vintage_tv_from_qloo(self, qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Extract vintage TV recommendations from Qloo data"""
        
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        tv_data = cultural_recommendations.get("tv_shows", {})
        entities = tv_data.get("entities", [])
        
        vintage_entities = []
        vintage_keywords = ["classic", "vintage", "1940", "1950", "1960", "anthology", "variety"]
        
        for entity in entities:
            name = entity.get("name", "").lower()
            tags = [tag.get("name", "").lower() for tag in entity.get("tags", [])]
            
            # Check if it's vintage content
            is_vintage = any(keyword in name or any(keyword in tag for tag in tags)
                            for keyword in vintage_keywords)
            
            if is_vintage:
                vintage_entities.append(entity)
        
        return {
            "success": len(vintage_entities) > 0,
            "entities": vintage_entities
        }
    
    def _get_classical_music_fallback(self, heritage: str) -> Dict[str, Any]:
        """Safe classical music fallback"""
        
        heritage_composers = {
            "Italian-American": {"artist": "Vivaldi", "name": "Four Seasons"},
            "German": {"artist": "Beethoven", "name": "Moonlight Sonata"},
            "universal": {"artist": "Mozart", "name": "Eine kleine Nachtmusik"}
        }
        
        composer_info = heritage_composers.get(heritage, heritage_composers["universal"])
        
        return {
            "name": composer_info["name"],
            "artist": composer_info["artist"],
            "youtube_url": "",  # No specific URL for safety
            "genre": "Classical",
            "era": "Public Domain",
            "safety_status": "classical_fallback",
            "source": "safe_fallback"
        }
    
    def _get_vintage_tv_fallback(self) -> Dict[str, Any]:
        """Safe vintage TV fallback"""
        return {
            "name": "Classic Family Variety Show",
            "youtube_url": "",  # No specific URL for safety
            "description": "Wholesome family entertainment from the 1950s",
            "era": "1950s",
            "safety_status": "vintage_fallback",
            "source": "safe_fallback"
        }
    
    def _get_safe_recipe_fallback(self, heritage: str) -> Dict[str, Any]:
        """Safe recipe fallback"""
        return {
            "name": f"Traditional {heritage} Comfort Food",
            "ingredients": ["Simple, wholesome ingredients"],
            "instructions": ["Easy preparation steps"],
            "prep_time": "20 minutes",
            "difficulty": "Easy",
            "cultural_context": heritage,
            "safety_status": "traditional_recipe",
            "source": "safe_fallback"
        }
    
    def _generate_safe_fallback_content(self, heritage: str) -> Dict[str, Any]:
        """Generate complete safe fallback content"""
        return {
            "sensory_content": {
                "content_by_sense": {
                    "auditory": {
                        "elements": [self._get_classical_music_fallback(heritage)],
                        "safety_level": "public_domain"
                    },
                    "visual": {
                        "elements": [self._get_vintage_tv_fallback()],
                        "safety_level": "public_domain"
                    },
                    "gustatory": {
                        "elements": [self._get_safe_recipe_fallback(heritage)],
                        "safety_level": "original_content"
                    }
                }
            },
            "generation_metadata": {
                "content_safety": "SAFE_FALLBACK",
                "pipeline": "fallback_only"
            }
        }

# Export the main class
__all__ = ["SensoryContentGeneratorAgent"]