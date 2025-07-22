"""
Agent 4: Sensory Content Generator
Role: Create connected multi-sensory experiences
Follows Responsible Development Guide principles - practical implementation with caregiver guidance
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent(Agent):
    """
    Agent 4: Sensory Content Generator
    
    Purpose: Create connected multi-sensory experiences across all 5 senses
    Input: All previous agent outputs
    Output: Connected sensory content package with practical implementation
    
    Tools: youtube_music_search, gemini_recipe_generator
    
    Anti-Bias Principles:
    - Generate content across all 5 senses using cultural theme WITHOUT STEREOTYPES
    - Use conditional logic based on request type
    - Integrate Qloo suggestions with practical implementation  
    - Respect blocked content and individual preferences
    - NO predetermined cultural mappings or assumptions
    - Individual stories and preferences override heritage keywords
    - Open-ended exploration rather than stereotypical cultural "packages"
    """
    
    def __init__(self, youtube_tool, gemini_tool):
        super().__init__(
            name="sensory_content_generator",
            description="Creates practical multi-sensory experiences with caregiver implementation guidance"
        )
        self.youtube_tool = youtube_tool
        self.gemini_tool = gemini_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate connected sensory content across all 5 senses.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2  
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Connected sensory content package with implementation guidance
        """
        
        try:
            logger.info("Generating multi-sensory content experiences")
            
            # Extract context and preferences
            request_context = consolidated_info.get("request_context", {})
            request_type = request_context.get("request_type", "dashboard")
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            
            # Extract cultural intelligence
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            cross_domain_connections = qloo_intelligence.get("cross_domain_connections", {})
            thematic_intelligence = qloo_intelligence.get("thematic_intelligence", {})
            
            # Generate sensory content strategy
            sensory_strategy = self._build_sensory_strategy(
                request_type,
                cultural_recommendations,
                thematic_intelligence,
                cultural_profile
            )
            
            # Generate content for each sense
            sensory_content = await self._generate_all_sensory_content(
                sensory_strategy,
                cultural_recommendations,
                blocked_content
            )
            
            # Create cross-sensory experiences
            cross_sensory_experiences = self._create_cross_sensory_experiences(
                sensory_content,
                cross_domain_connections,
                request_type
            )
            
            # Generate caregiver implementation guidance
            implementation_guidance = self._generate_implementation_guidance(
                sensory_content,
                cross_sensory_experiences,
                request_type
            )
            
            # Build complete sensory package
            sensory_package = {
                "generation_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "senses_activated": list(sensory_content.keys()),
                    "cross_sensory_experiences": len(cross_sensory_experiences),
                    "blocked_content_respected": True,
                    "cultural_integration": "qloo_enhanced"
                },
                "sensory_content": sensory_content,
                "cross_sensory_experiences": cross_sensory_experiences,
                "implementation_guidance": implementation_guidance,
                "caregiver_notes": {
                    "approach": "start_simple_build_complexity",
                    "observation": "watch_for_positive_responses",
                    "flexibility": "adapt_based_on_individual_reaction",
                    "safety": "ensure_comfortable_environment"
                },
                "cultural_coherence": self._assess_cultural_coherence(sensory_content, cultural_profile)
            }
            
            # Validate anti-bias compliance in sensory content
            self._validate_anti_bias_compliance(sensory_package)
            
            # Validate sensory content quality
            self._validate_sensory_content_quality(sensory_package)
            
            logger.info("Multi-sensory content package generated successfully")
            return {"sensory_content": sensory_package}
            
        except Exception as e:
            logger.error(f"Error generating sensory content: {str(e)}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    def _build_sensory_strategy(self, 
                               request_type: str,
                               cultural_recommendations: Dict[str, Any],
                               thematic_intelligence: Dict[str, Any],
                               cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Build strategy for multi-sensory content generation."""
        
        # Determine primary and secondary senses based on request type
        sensory_priorities = {
            "meal": {
                "primary": ["gustatory", "olfactory"],
                "secondary": ["visual", "tactile", "auditory"],
                "focus": "culinary_experience"
            },
            "conversation": {
                "primary": ["auditory"],
                "secondary": ["visual", "tactile", "gustatory", "olfactory"],
                "focus": "communication_enhancement"
            },
            "music": {
                "primary": ["auditory"],
                "secondary": ["tactile", "visual", "gustatory", "olfactory"],
                "focus": "musical_engagement"
            },
            "video": {
                "primary": ["visual", "auditory"],
                "secondary": ["gustatory", "tactile", "olfactory"],
                "focus": "viewing_experience"
            },
            "dashboard": {
                "primary": ["auditory", "visual", "gustatory"],
                "secondary": ["tactile", "olfactory"],
                "focus": "comprehensive_daily_experience"
            },
            "photo_analysis": {
                "primary": ["visual"],
                "secondary": ["auditory", "gustatory", "tactile", "olfactory"],
                "focus": "memory_triggered_experience"
            }
        }
        
        strategy = sensory_priorities.get(request_type, sensory_priorities["dashboard"])
        
        # Extract common themes for coherence
        common_themes = thematic_intelligence.get("common_themes", [])
        
        # Build content generation plan
        generation_plan = {
            "sensory_priorities": strategy,
            "common_themes": common_themes,
            "cultural_elements": self._extract_cultural_elements_for_content(cultural_profile),
            "available_qloo_domains": list(cultural_recommendations.keys()),
            "content_approach": "thematically_coherent_multi_sensory"
        }
        
        return generation_plan
    
    def _extract_cultural_elements_for_content(self, cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cultural elements that can be used for content generation."""
        
        cultural_elements = cultural_profile.get("cultural_elements", {})
        era_context = cultural_profile.get("era_context", {})
        
        content_elements = {
            "heritage_keywords": cultural_elements.get("heritage_elements", {}).get("heritage_keywords", []),
            "tradition_keywords": cultural_elements.get("tradition_elements", {}).get("tradition_keywords", []),
            "languages": cultural_elements.get("language_elements", {}).get("languages", []),
            "birth_year": era_context.get("birth_year"),
            "decades_lived": era_context.get("decades_lived", []),
            "cultural_eras": era_context.get("cultural_eras", {}),
            "seasonal_context": era_context.get("seasonal_context", {})
        }
        
        return content_elements
    
    async def _generate_all_sensory_content(self, 
                                           sensory_strategy: Dict[str, Any],
                                           cultural_recommendations: Dict[str, Any],
                                           blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for all five senses."""
        
        sensory_content = {}
        
        # Generate auditory content
        sensory_content["auditory"] = await self._generate_auditory_content(
            sensory_strategy, cultural_recommendations, blocked_content
        )
        
        # Generate visual content
        sensory_content["visual"] = await self._generate_visual_content(
            sensory_strategy, cultural_recommendations, blocked_content
        )
        
        # Generate gustatory content
        sensory_content["gustatory"] = await self._generate_gustatory_content(
            sensory_strategy, cultural_recommendations, blocked_content
        )
        
        # Generate olfactory content
        sensory_content["olfactory"] = await self._generate_olfactory_content(
            sensory_strategy, cultural_recommendations, blocked_content
        )
        
        # Generate tactile content
        sensory_content["tactile"] = await self._generate_tactile_content(
            sensory_strategy, cultural_recommendations, blocked_content
        )
        
        return sensory_content
    
    async def _generate_auditory_content(self, 
                                        sensory_strategy: Dict[str, Any],
                                        cultural_recommendations: Dict[str, Any],
                                        blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate auditory content (music, sounds, conversation topics)."""
        
        auditory_content = {
            "available": True,
            "content_type": "auditory",
            "elements": []
        }
        
        # Check for music recommendations from Qloo
        music_entities = []
        for entity_type in ["urn:entity:artist", "urn:entity:album"]:
            if entity_type in cultural_recommendations:
                recommendation = cultural_recommendations[entity_type]
                if recommendation.get("available"):
                    music_entities.extend(recommendation.get("entities", []))
        
        # Generate YouTube music content
        if music_entities and not self._is_content_blocked("music", blocked_content):
            try:
                youtube_content = await self._generate_youtube_music_content(music_entities[:3])
                auditory_content["elements"].extend(youtube_content)
            except Exception as e:
                logger.warning(f"YouTube music generation failed: {str(e)}")
        
        # Generate conversation topics based on cultural recommendations
        conversation_topics = self._generate_conversation_topics(cultural_recommendations, sensory_strategy)
        auditory_content["elements"].extend(conversation_topics)
        
        # Generate ambient sound suggestions
        ambient_sounds = self._generate_ambient_sound_suggestions(sensory_strategy)
        auditory_content["elements"].extend(ambient_sounds)
        
        return auditory_content
    
    async def _generate_youtube_music_content(self, music_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate YouTube music content from Qloo music entities."""
        
        youtube_content = []
        
        for entity in music_entities:
            artist_name = entity.get("name", "")
            if not artist_name:
                continue
            
            try:
                # Search for artist on YouTube
                search_results = await self.youtube_tool.search_music(
                    query=f"{artist_name} best songs classic",
                    max_results=2
                )
                
                if search_results and search_results.get("items"):
                    for video in search_results["items"]:
                        youtube_content.append({
                            "content_subtype": "youtube_music",
                            "title": video.get("snippet", {}).get("title", ""),
                            "video_id": video.get("id", {}).get("videoId", ""),
                            "artist": artist_name,
                            "cultural_connection": entity.get("cultural_context", {}),
                            "youtube_url": f"https://www.youtube.com/watch?v={video.get('id', {}).get('videoId', '')}",
                            "caregiver_guidance": {
                                "implementation": f"Play this {artist_name} music during quiet times",
                                "observation": "Watch for foot tapping, humming, or positive facial expressions",
                                "duration": "Start with 5-10 minutes, extend if positive response"
                            },
                            "accessibility": {
                                "volume_control": "Keep at comfortable level",
                                "interruption": "Can pause anytime if overwhelmed",
                                "familiarity": "May trigger memories and emotions"
                            }
                        })
                
                # Rate limiting for YouTube API
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.warning(f"YouTube search failed for {artist_name}: {str(e)}")
        
        return youtube_content
    
    def _generate_conversation_topics(self, 
                                     cultural_recommendations: Dict[str, Any],
                                     sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate conversation topics based on cultural recommendations."""
        
        conversation_topics = []
        
        # Extract cultural elements for conversation starters
        cultural_elements = sensory_strategy.get("cultural_elements", {})
        heritage_keywords = cultural_elements.get("heritage_keywords", [])
        decades_lived = cultural_elements.get("decades_lived", [])
        
        # Generate heritage-based conversation topics
        for keyword in heritage_keywords[:2]:
            conversation_topics.append({
                "content_subtype": "conversation_starter",
                "topic": f"Tell me about {keyword} traditions in your family",
                "cultural_connection": f"heritage_{keyword}",
                "conversation_guide": {
                    "opening": f"I'd love to hear about {keyword} traditions",
                    "follow_up_questions": [
                        f"What {keyword} celebrations do you remember?",
                        f"Did your family have special {keyword} foods?",
                        f"What {keyword} music or songs were popular?"
                    ],
                    "active_listening": "Encourage stories, ask for details, validate memories"
                },
                "caregiver_guidance": {
                    "approach": "Open-ended questions, patient listening",
                    "validation": "All memories are valuable, even if details vary",
                    "engagement": "Show genuine interest in their experiences"
                }
            })
        
        # Generate era-based conversation topics
        for decade in decades_lived[-3:]:  # Recent decades for memory accessibility
            conversation_topics.append({
                "content_subtype": "era_conversation",
                "topic": f"What do you remember about the {decade}?",
                "cultural_connection": f"era_{decade}",
                "conversation_guide": {
                    "opening": f"The {decade} must have been an interesting time",
                    "follow_up_questions": [
                        f"What was popular music in the {decade}?",
                        f"What were people wearing in the {decade}?",
                        f"What big events happened in the {decade}?"
                    ],
                    "memory_triggers": f"Music, fashion, news, technology from {decade}"
                },
                "caregiver_guidance": {
                    "approach": "Use decade as starting point for personal memories",
                    "flexibility": "Let conversation flow naturally to personal experiences",
                    "support": "Provide gentle prompts if they get stuck"
                }
            })
        
        return conversation_topics
    
    def _generate_ambient_sound_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate ambient sound suggestions for calming environments."""
        
        ambient_sounds = []
        
        # Seasonal ambient sounds based on cultural profile
        seasonal_context = sensory_strategy.get("cultural_elements", {}).get("seasonal_context", {})
        birth_season = seasonal_context.get("birth_season")
        
        seasonal_sounds = {
            "spring": ["gentle rain", "birds chirping", "flowing water"],
            "summer": ["ocean waves", "gentle breeze", "cricket sounds"],
            "fall": ["rustling leaves", "crackling fireplace", "gentle wind"],
            "winter": ["soft snow falling", "crackling fire", "peaceful silence"]
        }
        
        if birth_season and birth_season in seasonal_sounds:
            for sound in seasonal_sounds[birth_season]:
                ambient_sounds.append({
                    "content_subtype": "ambient_sound",
                    "sound_type": sound,
                    "seasonal_connection": birth_season,
                    "caregiver_guidance": {
                        "implementation": f"Play {sound} sounds during quiet times",
                        "volume": "Keep very low as background",
                        "duration": "Can play continuously for ambiance"
                    },
                    "therapeutic_benefits": {
                        "relaxation": "May reduce anxiety and promote calm",
                        "memory": f"May trigger positive {birth_season} memories",
                        "focus": "Can help with concentration and peace"
                    }
                })
        
        return ambient_sounds
    
    async def _generate_visual_content(self, 
                                      sensory_strategy: Dict[str, Any],
                                      cultural_recommendations: Dict[str, Any],
                                      blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content (videos, images, visual activities)."""
        
        visual_content = {
            "available": True,
            "content_type": "visual",
            "elements": []
        }
        
        # Check for video recommendations from Qloo
        video_entities = []
        for entity_type in ["urn:entity:movie", "urn:entity:tv_show"]:
            if entity_type in cultural_recommendations:
                recommendation = cultural_recommendations[entity_type]
                if recommendation.get("available"):
                    video_entities.extend(recommendation.get("entities", []))
        
        # Generate YouTube video content
        if video_entities and not self._is_content_blocked("video", blocked_content):
            try:
                youtube_videos = await self._generate_youtube_video_content(video_entities[:3])
                visual_content["elements"].extend(youtube_videos)
            except Exception as e:
                logger.warning(f"YouTube video generation failed: {str(e)}")
        
        # Generate visual activities based on cultural elements
        visual_activities = self._generate_visual_activities(sensory_strategy)
        visual_content["elements"].extend(visual_activities)
        
        # Generate photo viewing suggestions
        photo_suggestions = self._generate_photo_viewing_suggestions(sensory_strategy)
        visual_content["elements"].extend(photo_suggestions)
        
        return visual_content
    
    async def _generate_youtube_video_content(self, video_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate YouTube video content from Qloo video entities."""
        
        youtube_content = []
        
        for entity in video_entities:
            content_name = entity.get("name", "")
            if not content_name:
                continue
            
            try:
                # Search for content on YouTube
                search_results = await self.youtube_tool.search_videos(
                    query=f"{content_name} classic scenes highlights",
                    max_results=2
                )
                
                if search_results and search_results.get("items"):
                    for video in search_results["items"]:
                        youtube_content.append({
                            "content_subtype": "youtube_video",
                            "title": video.get("snippet", {}).get("title", ""),
                            "video_id": video.get("id", {}).get("videoId", ""),
                            "original_content": content_name,
                            "cultural_connection": entity.get("cultural_context", {}),
                            "youtube_url": f"https://www.youtube.com/watch?v={video.get('id', {}).get('videoId', '')}",
                            "caregiver_guidance": {
                                "implementation": f"Watch {content_name} content together",
                                "engagement": "Comment on scenes, ask about memories",
                                "attention": "Watch for attention span, pause if needed"
                            },
                            "viewing_notes": {
                                "duration": "Start with short clips (5-15 minutes)",
                                "interaction": "Encourage comments and reactions",
                                "comfort": "Ensure comfortable seating and lighting"
                            }
                        })
                
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"YouTube video search failed for {content_name}: {str(e)}")
        
        return youtube_content
    
    def _generate_visual_activities(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate visual activities based on cultural elements."""
        
        visual_activities = []
        
        cultural_elements = sensory_strategy.get("cultural_elements", {})
        heritage_keywords = cultural_elements.get("heritage_keywords", [])
        
        # Heritage-based visual activities
        for keyword in heritage_keywords[:2]:
            visual_activities.append({
                "content_subtype": "cultural_visual_activity",
                "activity": f"Look at {keyword} cultural photos online",
                "cultural_connection": f"heritage_{keyword}",
                "implementation": {
                    "setup": f"Search for '{keyword} culture photos' on tablet or computer",
                    "engagement": "Point out interesting details, ask about similarities to their experience",
                    "discussion": f"Talk about {keyword} traditions, foods, celebrations"
                },
                "caregiver_guidance": {
                    "approach": "Use images as conversation starters",
                    "flexibility": "Let them guide which images interest them most",
                    "validation": "All reactions and memories are valuable"
                }
            })
        
        # Era-based visual activities
        decades_lived = cultural_elements.get("decades_lived", [])
        for decade in decades_lived[-2:]:
            visual_activities.append({
                "content_subtype": "era_visual_activity", 
                "activity": f"Browse {decade} photo collections",
                "cultural_connection": f"era_{decade}",
                "implementation": {
                    "setup": f"Find {decade} photo collections online or in books",
                    "focus": "Fashion, cars, homes, technology from that era",
                    "interaction": "Ask 'Do you remember when...?' questions"
                },
                "caregiver_guidance": {
                    "memory_support": "Use images to trigger personal memories",
                    "patience": "Allow time for memories to surface",
                    "encouragement": "Celebrate any memories that come up"
                }
            })
        
        return visual_activities
    
    def _generate_photo_viewing_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate photo viewing suggestions for memory engagement."""
        
        photo_suggestions = [
            {
                "content_subtype": "family_photo_viewing",
                "activity": "Look through family photo albums",
                "purpose": "Memory stimulation and family connection",
                "implementation": {
                    "setup": "Gather family photo albums or digital photos",
                    "approach": "Go slowly, one photo at a time",
                    "interaction": "Ask who, what, when, where questions gently"
                },
                "caregiver_guidance": {
                    "emotional_support": "Be prepared for emotional reactions",
                    "validation": "Accept whatever they remember or don't remember",
                    "connection": "Share your own memories of people in photos"
                }
            },
            {
                "content_subtype": "nature_photo_viewing",
                "activity": "Browse beautiful nature photography",
                "purpose": "Calming visual stimulation",
                "implementation": {
                    "setup": "Use nature photography books or websites",
                    "focus": "Peaceful scenes - gardens, landscapes, animals",
                    "interaction": "Comment on colors, beauty, peaceful feelings"
                },
                "caregiver_guidance": {
                    "relaxation": "Use for calming during agitated moments",
                    "sensory": "Point out colors, textures, lighting",
                    "mindfulness": "Focus on present moment appreciation"
                }
            }
        ]
        
        return photo_suggestions
    
    async def _generate_gustatory_content(self, 
                                         sensory_strategy: Dict[str, Any],
                                         cultural_recommendations: Dict[str, Any],
                                         blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate gustatory content (recipes, food experiences)."""
        
        gustatory_content = {
            "available": True,
            "content_type": "gustatory",
            "elements": []
        }
        
        if self._is_content_blocked("food", blocked_content):
            gustatory_content["available"] = False
            gustatory_content["blocked_reason"] = "food_content_blocked_by_user"
            return gustatory_content
        
        # Extract cultural food elements
        cultural_elements = sensory_strategy.get("cultural_elements", {})
        heritage_keywords = cultural_elements.get("heritage_keywords", [])
        birth_year = cultural_elements.get("birth_year")
        
        # Generate recipes using Gemini
        try:
            recipes = await self._generate_cultural_recipes(heritage_keywords, birth_year)
            gustatory_content["elements"].extend(recipes)
        except Exception as e:
            logger.warning(f"Recipe generation failed: {str(e)}")
        
        # Generate food memory activities
        food_activities = self._generate_food_memory_activities(cultural_elements)
        gustatory_content["elements"].extend(food_activities)
        
        # Generate taste exploration suggestions
        taste_explorations = self._generate_taste_explorations(cultural_elements)
        gustatory_content["elements"].extend(taste_explorations)
        
        return gustatory_content
    
    async def _generate_cultural_recipes(self, 
                                        heritage_keywords: List[str],
                                        birth_year: Optional[int]) -> List[Dict[str, Any]]:
        """Generate recipes using individual heritage sharing (ANTI-BIAS approach)."""
        
        recipes = []
        
        # ANTI-BIAS APPROACH: Use heritage keywords for open-ended recipe exploration
        # No predetermined cultural food assumptions
        
        if heritage_keywords:
            try:
                # Generate recipe based on open-ended heritage exploration
                heritage_recipe_prompt = f"""
                Generate a simple, comforting recipe for someone whose family has shared these heritage elements: {', '.join(heritage_keywords[:3])}.
                
                IMPORTANT ANTI-BIAS REQUIREMENTS:
                - DO NOT make assumptions about specific cuisines based on heritage keywords
                - DO NOT create stereotypical cultural food combinations
                - Focus on comfort, simplicity, and adaptability
                - Ask caregiver to customize based on individual preferences
                
                Create a recipe that:
                - Uses common, accessible ingredients
                - Can be adapted for different dietary needs
                - Provides opportunities for sensory engagement (smells, textures)
                - Includes space for individual customization
                
                Include a note that caregivers should adapt this based on the individual's actual food preferences and memories, not heritage assumptions.
                
                Format as JSON with: name, ingredients, instructions, caregiver_customization_notes, dietary_alternatives, sensory_engagement_tips
                """
                
                recipe_response = await self.gemini_tool.generate_recipe(heritage_recipe_prompt)
                
                if recipe_response:
                    recipes.append({
                        "content_subtype": "heritage_inspired_recipe",
                        "heritage_keywords": heritage_keywords,
                        "recipe_data": recipe_response,
                        "anti_bias_approach": "individual_customization_required",
                        "caregiver_guidance": {
                            "customization": "Adapt this recipe based on their individual food preferences and stories",
                            "no_assumptions": f"Don't assume food preferences based on heritage keywords: {', '.join(heritage_keywords[:3])}",
                            "individual_focus": "Ask them about foods they actually enjoyed or cooked",
                            "sensory_experience": "Focus on smells, textures, colors they personally enjoy",
                            "memory_connection": "Use their specific food memories, not cultural stereotypes"
                        },
                        "safety_considerations": {
                            "kitchen_safety": "Supervise any knife or heat use",
                            "dietary_restrictions": "Check for actual dietary restrictions and preferences",
                            "simplification": "Break recipe into smaller steps based on current abilities",
                            "flexibility": "Adapt based on their current abilities and interests"
                        }
                    })
                
                await asyncio.sleep(0.2)  # Rate limiting for Gemini
                
            except Exception as e:
                logger.warning(f"Heritage-inspired recipe generation failed: {str(e)}")
        
        # Generate era-appropriate comfort food (factual, not assumptive)
        if birth_year:
            try:
                era_recipe_prompt = f"""
                Generate a simple comfort food recipe that would have been commonly available and popular during the formative years of someone born in {birth_year}.
                
                Focus on:
                - Simple, accessible ingredients that were common in that era
                - Comfort food that was widely enjoyed across different backgrounds
                - Easy preparation suitable for caregiver-assisted cooking
                - Sensory engagement opportunities (familiar smells, textures)
                
                AVOID:
                - Cultural or ethnic food assumptions
                - Complex preparations
                - Ingredients that may not have been widely available
                
                Include notes about why this was a common comfort food of that era and how to adapt for current dietary needs.
                
                Format as JSON with: name, ingredients, instructions, era_context, adaptation_notes, sensory_highlights
                """
                
                era_recipe = await self.gemini_tool.generate_recipe(era_recipe_prompt)
                
                if era_recipe:
                    recipes.append({
                        "content_subtype": "era_comfort_food",
                        "birth_year_connection": birth_year,
                        "recipe_data": era_recipe,
                        "approach": "factual_era_context_no_assumptions",
                        "caregiver_guidance": {
                            "era_connection": f"This was a common comfort food for people born around {birth_year}",
                            "individual_verification": "Ask if they remember eating similar foods",
                            "adaptation": "Modify based on their actual food memories and preferences",
                            "nostalgia_factor": "Use recipe to explore their individual food memories",
                            "storytelling": "Ask about foods their family actually made"
                        }
                    })
                    
            except Exception as e:
                logger.warning(f"Era recipe generation failed for {birth_year}: {str(e)}")
        
        # Generate universally appealing comfort food option
        try:
            universal_recipe_prompt = """
            Generate a simple, universally comforting recipe that:
            - Uses basic, familiar ingredients
            - Is easy to prepare with assistance
            - Provides rich sensory experiences (aromas, textures)
            - Can be customized based on individual preferences
            - Is suitable for people with varying dietary needs
            
            Focus on creating positive sensory experiences and opportunities for shared cooking activities.
            
            Format as JSON with: name, ingredients, instructions, customization_options, sensory_benefits, caregiver_tips
            """
            
            universal_recipe = await self.gemini_tool.generate_recipe(universal_recipe_prompt)
            
            if universal_recipe:
                recipes.append({
                    "content_subtype": "universal_comfort_recipe",
                    "approach": "broad_appeal_individual_customization",
                    "recipe_data": universal_recipe,
                    "caregiver_guidance": {
                        "universal_appeal": "This recipe is designed to be widely comforting",
                        "customization": "Adapt based on their individual taste preferences",
                        "sensory_focus": "Emphasize the smells, textures, and visual appeal",
                        "shared_experience": "Cook together for maximum benefit"
                    }
                })
                
        except Exception as e:
            logger.warning(f"Universal recipe generation failed: {str(e)}")
        
        return recipes
    
    def _generate_food_memory_activities(self, cultural_elements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate food-related memory activities."""
        
        food_activities = [
            {
                "content_subtype": "food_memory_conversation",
                "activity": "Talk about favorite family recipes",
                "implementation": {
                    "starter": "What was your favorite dish that your mother/grandmother made?",
                    "follow_up": "Do you remember any special ingredients or cooking methods?",
                    "engagement": "Ask about holiday foods, celebration meals, everyday favorites"
                },
                "caregiver_guidance": {
                    "approach": "Use food as gateway to family memories",
                    "validation": "All food memories are valuable, even if details vary",
                    "extension": "Consider recreating dishes they mention"
                }
            },
            {
                "content_subtype": "spice_exploration",
                "activity": "Smell and identify familiar spices",
                "implementation": {
                    "setup": "Gather common spices in small bowls",
                    "interaction": "Let them smell each spice, ask about recognition",
                    "discussion": "Talk about dishes that use each spice"
                },
                "caregiver_guidance": {
                    "sensory_safety": "Ensure no allergies or sensitivities",
                    "memory_trigger": "Spices can trigger powerful food memories",
                    "storytelling": "Encourage stories about cooking and kitchens"
                }
            }
        ]
        
        return food_activities
    
    def _generate_taste_explorations(self, cultural_elements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate safe taste exploration activities."""
        
        taste_explorations = [
            {
                "content_subtype": "familiar_taste_sampling",
                "activity": "Sample familiar flavors",
                "implementation": {
                    "setup": "Prepare small samples of familiar foods",
                    "examples": "Cookies, fruits, simple snacks they've enjoyed",
                    "interaction": "Discuss flavors, textures, memories"
                },
                "caregiver_guidance": {
                    "safety": "Check for dietary restrictions and swallowing ability",
                    "portions": "Use very small samples",
                    "observation": "Watch for enjoyment and positive reactions"
                }
            }
        ]
        
        return taste_explorations
    
    async def _generate_olfactory_content(self, 
                                         sensory_strategy: Dict[str, Any],
                                         cultural_recommendations: Dict[str, Any],
                                         blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate olfactory content (scents, aromatherapy)."""
        
        olfactory_content = {
            "available": True,
            "content_type": "olfactory",
            "elements": []
        }
        
        # Generate cultural scent connections
        cultural_scents = self._generate_cultural_scent_suggestions(sensory_strategy)
        olfactory_content["elements"].extend(cultural_scents)
        
        # Generate cooking scent experiences
        cooking_scents = self._generate_cooking_scent_experiences(sensory_strategy)
        olfactory_content["elements"].extend(cooking_scents)
        
        # Generate therapeutic aromatherapy suggestions
        aromatherapy = self._generate_aromatherapy_suggestions(sensory_strategy)
        olfactory_content["elements"].extend(aromatherapy)
        
        return olfactory_content
    
    def _generate_cultural_scent_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate scent suggestions based on individual cultural sharing (NO stereotypes)."""
        
        cultural_scents = []
        
        cultural_elements = sensory_strategy.get("cultural_elements", {})
        heritage_keywords = cultural_elements.get("heritage_keywords", [])
        
        # ANTI-BIAS APPROACH: Generate broad scent exploration opportunities
        # Use cultural keywords for open-ended discovery, not predetermined assumptions
        
        if heritage_keywords:
            # Suggest general scent exploration related to heritage without assumptions
            cultural_scents.append({
                "content_subtype": "heritage_scent_exploration",
                "activity": "Explore scents that might connect to their heritage",
                "approach": "caregiver_guided_discovery",
                "implementation": {
                    "method": "Ask caregiver about scents from family cooking, traditions, or places",
                    "examples": "Herbs, spices, flowers, or foods they've mentioned enjoying",
                    "customization": "Focus on individual preferences, not cultural assumptions"
                },
                "caregiver_guidance": {
                    "individual_first": "Use their specific stories and preferences",
                    "no_assumptions": f"Don't assume preferences based on heritage keywords: {', '.join(heritage_keywords[:3])}",
                    "discovery": "Ask: 'What scents bring back good memories for you?'",
                    "observation": "Watch for positive responses to guide future selections"
                },
                "anti_bias_note": "This suggestion avoids cultural stereotypes and focuses on individual discovery"
            })
        
        # Generate broad, universally appealing scent categories for exploration
        universal_scent_categories = [
            {
                "category": "cooking_herbs",
                "examples": ["herbs they've mentioned", "spices from cooking stories"],
                "discovery_approach": "Based on their individual cooking memories"
            },
            {
                "category": "garden_flowers", 
                "examples": ["flowers from their garden", "blooms they've mentioned loving"],
                "discovery_approach": "Based on their individual garden or nature experiences"
            },
            {
                "category": "comfort_scents",
                "examples": ["scents from happy memories", "aromas they find comforting"],
                "discovery_approach": "Based on their individual comfort associations"
            }
        ]
        
        for category in universal_scent_categories:
            cultural_scents.append({
                "content_subtype": "individualized_scent_exploration",
                "category": category["category"],
                "examples": category["examples"],
                "approach": category["discovery_approach"],
                "implementation": {
                    "method": "Work with caregiver to identify specific scents based on individual stories",
                    "intensity": "Very mild - just enough to notice",
                    "duration": "5-10 minutes initially"
                },
                "caregiver_guidance": {
                    "personalization": "Use their specific memories and preferences",
                    "safety": "Check for allergies to any specific scents",
                    "observation": "Watch for positive or negative reactions",
                    "no_assumptions": "Don't assume preferences based on background"
                }
            })
        
        return cultural_scents
    
    def _generate_cooking_scent_experiences(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cooking scent experiences for memory stimulation."""
        
        cooking_scents = [
            {
                "content_subtype": "baking_scents",
                "activity": "Baking bread or cookies for the aroma",
                "implementation": {
                    "method": "Use simple baking mixes or bread machine",
                    "focus": "Enjoy the baking smells together",
                    "interaction": "Talk about memories of home baking"
                },
                "caregiver_guidance": {
                    "memory_connection": "Baking scents often trigger childhood memories",
                    "participation": "Let them help with simple tasks if able",
                    "enjoyment": "Focus on the sensory pleasure, not perfect results"
                }
            },
            {
                "content_subtype": "coffee_tea_aromas",
                "activity": "Brewing familiar coffee or tea",
                "implementation": {
                    "method": "Brew their preferred coffee or tea",
                    "focus": "Enjoy the brewing aromas",
                    "ritual": "Create a peaceful morning or afternoon ritual"
                },
                "caregiver_guidance": {
                    "routine": "Can become part of daily routine",
                    "social": "Share the drinking experience together",
                    "comfort": "Familiar scents provide comfort and routine"
                }
            }
        ]
        
        return cooking_scents
    
    def _generate_aromatherapy_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate therapeutic aromatherapy suggestions."""
        
        aromatherapy = [
            {
                "content_subtype": "calming_aromatherapy",
                "scents": ["lavender", "chamomile", "vanilla"],
                "purpose": "Relaxation and anxiety reduction",
                "implementation": {
                    "method": "Essential oil diffuser on lowest setting",
                    "timing": "During quiet times or before sleep",
                    "duration": "15-20 minutes maximum"
                },
                "caregiver_guidance": {
                    "safety": "Use only pure essential oils, check for allergies",
                    "observation": "Monitor for any respiratory irritation",
                    "effectiveness": "May help with sleep and anxiety"
                }
            },
            {
                "content_subtype": "energizing_aromatherapy",
                "scents": ["citrus", "peppermint", "rosemary"],
                "purpose": "Gentle alertness and mood lifting",
                "implementation": {
                    "method": "Fresh citrus peels or very mild essential oils",
                    "timing": "Morning or when they seem sluggish",
                    "intensity": "Very subtle - overpowering scents can be agitating"
                },
                "caregiver_guidance": {
                    "moderation": "Less is more with dementia care",
                    "individual_response": "Each person responds differently",
                    "discontinue": "Stop immediately if any negative reaction"
                }
            }
        ]
        
        return aromatherapy
    
    async def _generate_tactile_content(self, 
                                       sensory_strategy: Dict[str, Any],
                                       cultural_recommendations: Dict[str, Any],
                                       blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tactile content (textures, objects, activities)."""
        
        tactile_content = {
            "available": True,
            "content_type": "tactile",
            "elements": []
        }
        
        # Generate cultural tactile objects
        cultural_objects = self._generate_cultural_tactile_objects(sensory_strategy)
        tactile_content["elements"].extend(cultural_objects)
        
        # Generate texture exploration activities
        texture_activities = self._generate_texture_exploration_activities()
        tactile_content["elements"].extend(texture_activities)
        
        # Generate comfort object suggestions
        comfort_objects = self._generate_comfort_object_suggestions()
        tactile_content["elements"].extend(comfort_objects)
        
        return tactile_content
    
    def _generate_cultural_tactile_objects(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate tactile objects for exploration (ANTI-BIAS: individual-focused)."""
        
        cultural_objects = []
        
        cultural_elements = sensory_strategy.get("cultural_elements", {})
        heritage_keywords = cultural_elements.get("heritage_keywords", [])
        
        # ANTI-BIAS APPROACH: Generate broad tactile exploration based on individual sharing
        # No predetermined cultural object categories or assumptions
        
        if heritage_keywords:
            # Suggest open-ended tactile exploration based on their individual heritage sharing
            cultural_objects.append({
                "content_subtype": "heritage_tactile_exploration",
                "activity": "Explore textures connected to their heritage stories",
                "approach": "individual_story_based",
                "implementation": {
                    "method": "Ask caregiver about objects from their heritage stories",
                    "examples": "Items they've mentioned: fabrics, tools, kitchen items, crafts",
                    "safety": "Ensure all objects are safe for handling",
                    "customization": "Use their specific memories, not cultural assumptions"
                },
                "caregiver_guidance": {
                    "individual_focus": f"Base on their stories about: {', '.join(heritage_keywords[:3])}",
                    "no_stereotypes": "Don't assume objects based on heritage - use their specific experiences",
                    "discovery_questions": [
                        "What objects were important in your family?",
                        "What did you like to touch or work with?",
                        "What textures bring back good memories?"
                    ],
                    "safety": "All objects should be safe to handle and explore"
                },
                "anti_bias_note": "Focuses on individual experiences rather than cultural stereotypes"
            })
        
        # Generate broad, universally appealing tactile categories for exploration
        universal_tactile_categories = [
            {
                "category": "familiar_textures",
                "description": "Textures from their individual life experiences",
                "examples": "Based on their stories about work, hobbies, or family life"
            },
            {
                "category": "comfort_objects",
                "description": "Objects that provide personal comfort and familiarity", 
                "examples": "Based on their individual preferences and memories"
            },
            {
                "category": "memory_objects",
                "description": "Objects similar to those from their personal stories",
                "examples": "Based on items they've mentioned or shown interest in"
            }
        ]
        
        for category in universal_tactile_categories:
            cultural_objects.append({
                "content_subtype": "individualized_tactile_exploration",
                "category": category["category"],
                "description": category["description"],
                "examples": category["examples"],
                "implementation": {
                    "approach": "Work with caregiver to identify specific objects from individual stories",
                    "interaction": "Let them explore texture, weight, temperature at their own pace",
                    "discussion": "Talk about their personal memories connected to similar objects"
                },
                "caregiver_guidance": {
                    "personalization": "Use their specific life experiences and stories",
                    "safety": "Ensure all objects are safe to handle and explore",
                    "encouragement": "Allow extended exploration time",
                    "memory_connection": "Connect to their individual memories, not cultural assumptions",
                    "observation": "Note which textures and objects they prefer"
                }
            })
        
        return cultural_objects
    
    def _generate_texture_exploration_activities(self) -> List[Dict[str, Any]]:
        """Generate texture exploration activities."""
        
        texture_activities = [
            {
                "content_subtype": "texture_exploration_box",
                "activity": "Explore different textures in a sensory box",
                "materials": ["soft fabrics", "smooth stones", "textured papers", "soft brushes"],
                "implementation": {
                    "setup": "Create a box with various safe textures",
                    "interaction": "Let them explore each texture",
                    "discussion": "Talk about how each texture feels"
                },
                "caregiver_guidance": {
                    "safety": "All items should be large enough to avoid choking hazards",
                    "cleanliness": "Keep items clean and washable",
                    "enjoyment": "Focus on pleasure of exploration"
                }
            },
            {
                "content_subtype": "hand_massage",
                "activity": "Gentle hand massage with lotion",
                "implementation": {
                    "setup": "Use unscented, hypoallergenic lotion",
                    "technique": "Gentle, slow movements",
                    "focus": "Comfort and human connection"
                },
                "caregiver_guidance": {
                    "permission": "Always ask permission before touching",
                    "gentleness": "Very light pressure, watch for comfort level",
                    "connection": "Maintain eye contact and conversation"
                }
            }
        ]
        
        return texture_activities
    
    def _generate_comfort_object_suggestions(self) -> List[Dict[str, Any]]:
        """Generate comfort object suggestions."""
        
        comfort_objects = [
            {
                "content_subtype": "comfort_blanket",
                "object": "Soft, weighted blanket or throw",
                "purpose": "Comfort and security",
                "implementation": {
                    "selection": "Choose soft, washable material",
                    "weight": "Light weight for comfort, not restriction",
                    "use": "Available for them to hold or wrap around"
                },
                "caregiver_guidance": {
                    "availability": "Keep accessible for times of anxiety",
                    "cleanliness": "Wash regularly",
                    "personal_choice": "Let them decide when to use it"
                }
            },
            {
                "content_subtype": "fidget_objects",
                "objects": ["stress ball", "worry stones", "textured fabric squares"],
                "purpose": "Hand occupation and anxiety relief",
                "implementation": {
                    "variety": "Provide several different textures and weights",
                    "accessibility": "Keep within easy reach",
                    "rotation": "Change objects to maintain interest"
                },
                "caregiver_guidance": {
                    "observation": "Notice which textures they prefer",
                    "safety": "Ensure objects are safe if put in mouth",
                    "purpose": "Help with restlessness and anxiety"
                }
            }
        ]
        
        return comfort_objects
    
    def _is_content_blocked(self, content_type: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if a content type is blocked."""
        
        blocked_categories = blocked_content.get("categories", [])
        blocked_types = blocked_content.get("types", [])
        
        return content_type in blocked_categories or content_type in blocked_types
    
    def _create_cross_sensory_experiences(self, 
                                         sensory_content: Dict[str, Any],
                                         cross_domain_connections: Dict[str, Any],
                                         request_type: str) -> List[Dict[str, Any]]:
        """Create combined multi-sensory experiences."""
        
        cross_sensory_experiences = []
        
        # Create thematic multi-sensory packages
        if request_type == "meal":
            cooking_experience = self._create_cooking_experience(sensory_content)
            if cooking_experience:
                cross_sensory_experiences.append(cooking_experience)
        
        elif request_type == "music":
            musical_experience = self._create_musical_experience(sensory_content)
            if musical_experience:
                cross_sensory_experiences.append(musical_experience)
        
        # Create general multi-sensory experiences for dashboard
        if request_type == "dashboard":
            cultural_exploration = self._create_cultural_exploration_experience(sensory_content)
            if cultural_exploration:
                cross_sensory_experiences.append(cultural_exploration)
            
            comfort_experience = self._create_comfort_experience(sensory_content)
            if comfort_experience:
                cross_sensory_experiences.append(comfort_experience)
        
        return cross_sensory_experiences
    
    def _create_cooking_experience(self, sensory_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a multi-sensory cooking experience."""
        
        gustatory = sensory_content.get("gustatory", {})
        olfactory = sensory_content.get("olfactory", {})
        tactile = sensory_content.get("tactile", {})
        auditory = sensory_content.get("auditory", {})
        
        if not (gustatory.get("available") and gustatory.get("elements")):
            return None
        
        return {
            "experience_name": "Cultural Cooking Experience",
            "description": "Multi-sensory cooking activity combining taste, smell, touch, and conversation",
            "sensory_components": {
                "gustatory": "Cook a cultural recipe together",
                "olfactory": "Enjoy cooking aromas and spices",
                "tactile": "Handle ingredients and cooking utensils",
                "auditory": "Play cultural music while cooking, share cooking stories"
            },
            "implementation_guide": {
                "preparation": "Choose simple recipe, gather ingredients",
                "process": "Cook together, focusing on sensory experiences",
                "engagement": "Share memories about food and cooking",
                "completion": "Enjoy the meal together"
            },
            "caregiver_guidance": {
                "safety": "Supervise all cooking activities",
                "flexibility": "Adapt tasks to current abilities",
                "enjoyment": "Focus on the process, not perfect results",
                "memory": "Use cooking as opportunity for storytelling"
            }
        }
    
    def _create_musical_experience(self, sensory_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a multi-sensory musical experience."""
        
        auditory = sensory_content.get("auditory", {})
        tactile = sensory_content.get("tactile", {})
        visual = sensory_content.get("visual", {})
        
        if not (auditory.get("available") and auditory.get("elements")):
            return None
        
        return {
            "experience_name": "Cultural Musical Journey",
            "description": "Multi-sensory musical experience combining sound, movement, and memory",
            "sensory_components": {
                "auditory": "Play culturally relevant music",
                "tactile": "Use rhythm instruments or tap along",
                "visual": "Watch related videos or look at era photos",
                "kinesthetic": "Gentle movement or dancing to music"
            },
            "implementation_guide": {
                "setup": "Choose comfortable seating, moderate volume",
                "engagement": "Start with familiar songs, watch for reactions",
                "interaction": "Encourage singing, humming, or movement",
                "discussion": "Talk about memories the music brings up"
            },
            "caregiver_guidance": {
                "volume": "Keep at comfortable level",
                "variety": "Try different musical styles",
                "response": "Follow their energy and interest level",
                "memory": "Use music to access emotional memories"
            }
        }
    
    def _create_cultural_exploration_experience(self, sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive cultural exploration experience."""
        
        return {
            "experience_name": "Cultural Heritage Exploration",
            "description": "Multi-sensory journey through cultural heritage and memories",
            "sensory_components": {
                "visual": "Look at cultural photos and videos",
                "auditory": "Listen to cultural music and share stories",
                "olfactory": "Experience cultural scents and cooking aromas",
                "gustatory": "Taste cultural foods and flavors",
                "tactile": "Handle cultural objects and textures"
            },
            "implementation_guide": {
                "duration": "1-2 hours, with breaks as needed",
                "progression": "Start with one sense, add others gradually",
                "customization": "Focus on elements that generate positive response",
                "documentation": "Note which elements work best"
            },
            "caregiver_guidance": {
                "pacing": "Go slowly, allow time for processing",
                "observation": "Watch for signs of enjoyment or overstimulation",
                "flexibility": "Adapt based on their current mood and energy",
                "validation": "Celebrate all responses and memories"
            }
        }
    
    def _create_comfort_experience(self, sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create a multi-sensory comfort experience."""
        
        return {
            "experience_name": "Comfort and Calm Experience",
            "description": "Gentle multi-sensory experience for relaxation and comfort",
            "sensory_components": {
                "auditory": "Soft music or nature sounds",
                "tactile": "Comfort objects and gentle textures", 
                "olfactory": "Calming scents like lavender",
                "visual": "Peaceful images or familiar photos",
                "kinesthetic": "Gentle hand massage or light stretching"
            },
            "implementation_guide": {
                "timing": "Use during agitated or anxious periods",
                "environment": "Create calm, dimly lit space",
                "approach": "Very gentle, non-demanding activities",
                "duration": "15-30 minutes or as needed"
            },
            "caregiver_guidance": {
                "gentleness": "All activities should be very gentle",
                "choice": "Let them choose which elements to engage with",
                "presence": "Your calm presence is the most important element",
                "adaptation": "Adjust based on their response"
            }
        }
    
    def _generate_implementation_guidance(self, 
                                         sensory_content: Dict[str, Any],
                                         cross_sensory_experiences: List[Dict[str, Any]],
                                         request_type: str) -> Dict[str, Any]:
        """Generate comprehensive implementation guidance for caregivers."""
        
        return {
            "getting_started": {
                "first_steps": "Start with one sensory element they seem to enjoy",
                "observation": "Watch their facial expressions and body language for positive responses",
                "timing": "Choose times when they are alert but not overstimulated",
                "environment": "Create a calm, comfortable space"
            },
            "building_experiences": {
                "layering": "Add sensory elements gradually based on positive responses",
                "customization": "Focus on elements that generate the most engagement",
                "routine": "Consider incorporating successful elements into daily routines",
                "documentation": "Keep notes on what works best"
            },
            "safety_considerations": {
                "allergies": "Check for any allergies before introducing scents or foods",
                "choking": "Ensure all tactile objects are safe and appropriate size",
                "overstimulation": "Watch for signs of overwhelm and reduce stimulation",
                "hygiene": "Keep all objects clean and sanitized"
            },
            "troubleshooting": {
                "no_response": "Try different elements or come back to it later",
                "negative_response": "Stop immediately and try something else",
                "agitation": "Use calming elements like gentle music or comfortable textures",
                "fatigue": "Shorter sessions, focus on comfort elements"
            },
            "maximizing_benefits": {
                "consistency": "Regular engagement often works better than long sessions",
                "personalization": "Adapt everything to their specific preferences and history",
                "social_connection": "Share the experiences together for maximum benefit",
                "memory_making": "Focus on creating positive moments in the present"
            }
        }
    
    def _assess_cultural_coherence(self, 
                                  sensory_content: Dict[str, Any],
                                  cultural_profile: Dict[str, Any]) -> Dict[str, str]:
        """Assess how well sensory content maintains cultural coherence."""
        
        cultural_elements = cultural_profile.get("cultural_elements", {})
        heritage_keywords = cultural_elements.get("heritage_keywords", [])
        
        coherence_assessment = {
            "heritage_integration": "medium",
            "era_consistency": "medium", 
            "cross_sensory_themes": "medium",
            "individual_focus": "high"
        }
        
        # Count heritage connections across senses
        heritage_connections = 0
        for sense_data in sensory_content.values():
            if sense_data.get("available"):
                for element in sense_data.get("elements", []):
                    if any(keyword in str(element.get("cultural_connection", "")) for keyword in heritage_keywords):
                        heritage_connections += 1
        
        if heritage_connections >= 3:
            coherence_assessment["heritage_integration"] = "high"
        elif heritage_connections >= 1:
            coherence_assessment["heritage_integration"] = "medium"
        else:
            coherence_assessment["heritage_integration"] = "low"
        
        return coherence_assessment
    
    def _validate_anti_bias_compliance(self, sensory_package: Dict[str, Any]) -> None:
        """Validate that no cultural stereotypes or biases were introduced."""
        
        sensory_content = sensory_package.get("sensory_content", {})
        
        # Check for stereotypical cultural assumptions
        bias_indicators = [
            "italian basil", "mexican cinnamon", "irish lavender", 
            "cultural_scent", "heritage_object_mapping",
            "traditional", "typical", "authentic", "classic cultural"
        ]
        
        content_text = str(sensory_content).lower()
        
        detected_bias = []
        for indicator in bias_indicators:
            if indicator in content_text:
                detected_bias.append(indicator)
        
        if detected_bias:
            logger.warning(f"Potential cultural bias detected: {detected_bias}")
        
        # Verify individual-first approach
        individual_indicators = [
            "individual", "personal", "their specific", "caregiver_guided",
            "no_assumptions", "anti_bias", "customization"
        ]
        
        individual_count = sum(1 for indicator in individual_indicators if indicator in content_text)
        
        if individual_count < 3:
            logger.warning("Insufficient individual-first language in sensory content")
        
        # Check for cultural stereotype mappings (should be none)
        for sense_data in sensory_content.values():
            if isinstance(sense_data, dict):
                for element in sense_data.get("elements", []):
                    if isinstance(element, dict):
                        cultural_connection = element.get("cultural_connection", "")
                        if any(bias in str(cultural_connection).lower() for bias in ["_heritage", "culture_", "traditional_"]):
                            logger.warning(f"Potential cultural stereotype in element: {element.get('content_subtype', 'unknown')}")
        
        logger.info("Anti-bias compliance validation completed")
    
    def _validate_sensory_content_quality(self, sensory_package: Dict[str, Any]) -> None:
    
        """Validate the quality and safety of generated sensory content."""
        
        sensory_content = sensory_package.get("sensory_content", {})
        
        # Check that all senses have content
        expected_senses = ["auditory", "visual", "gustatory", "olfactory", "tactile"]
        missing_senses = []
        
        for sense in expected_senses:
            if sense not in sensory_content or not sensory_content[sense].get("available"):
                missing_senses.append(sense)
        
        if missing_senses:
            logger.info(f"Some senses missing content: {missing_senses}")
        
        # Check for caregiver guidance
        implementation_guidance = sensory_package.get("implementation_guidance", {})
        if not implementation_guidance.get("safety_considerations"):
            logger.warning("Safety considerations missing from implementation guidance")
        
        # Validate cross-sensory experiences
        cross_sensory = sensory_package.get("cross_sensory_experiences", [])
        if not cross_sensory:
            logger.info("No cross-sensory experiences generated")
        
        logger.info("Sensory content quality validation completed")
    
    def _create_fallback_sensory_content(self, 
                                        consolidated_info: Dict[str, Any],
                                        cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails."""
        
        request_type = consolidated_info.get("request_context", {}).get("request_type", "dashboard")
        
        fallback_content = {
            "sensory_content": {
                "generation_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "mode": "fallback_safe_defaults",
                    "blocked_content_respected": True
                },
                "sensory_content": {
                    "auditory": {
                        "available": True,
                        "elements": [{
                            "content_subtype": "gentle_music",
                            "activity": "Play familiar, gentle music",
                            "caregiver_guidance": {
                                "implementation": "Choose music from their era",
                                "observation": "Watch for positive responses"
                            }
                        }]
                    },
                    "visual": {
                        "available": True, 
                        "elements": [{
                            "content_subtype": "family_photos",
                            "activity": "Look at family photos together",
                            "caregiver_guidance": {
                                "implementation": "Go slowly, one photo at a time",
                                "interaction": "Ask gentle questions about people and places"
                            }
                        }]
                    }
                },
                "cross_sensory_experiences": [],
                "implementation_guidance": {
                    "getting_started": {
                        "first_steps": "Start with simple, familiar activities",
                        "safety": "Ensure comfortable, safe environment"
                    }
                },
                "caregiver_notes": {
                    "approach": "use_fallback_content_as_starting_point",
                    "flexibility": "adapt_based_on_individual_response"
                }
            }
        }
        
        return fallback_content