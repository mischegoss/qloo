"""
Enhanced Mobile Synthesizer Agent with Places as Memory Anchors
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

Agent 6: Transforms places into memory anchors and conversation starters
rather than destination suggestions for dementia care.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class MobileSynthesizerAgent:
    """
    Agent 6: Mobile Synthesizer with Memory-Focused Places Usage
    
    Transforms all content into mobile-friendly experiences with places used
    as memory anchors and recipe inspiration rather than visit suggestions.
    """
    
    def __init__(self):
        logger.info("Mobile Synthesizer initialized with memory-focused places approach")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize all content into mobile experience with places as memory anchors.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            qloo_intelligence: Output from Agent 3
            sensory_content: Output from Agent 4
            photo_analysis: Output from Agent 5
            
        Returns:
            Mobile-ready experience with memory-focused places usage
        """
        
        try:
            logger.info("📱 Agent 6: Starting mobile synthesis with memory anchors")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            patient_name = patient_profile.get("first_name", "").split()[0] if patient_profile.get("first_name") else "Patient"
            heritage = patient_profile.get("cultural_heritage", "American")
            
            # Create memory-focused dashboard content
            mobile_experience = {
                "dashboard_content": self._create_memory_focused_dashboard(
                    consolidated_info, cultural_profile, qloo_intelligence, sensory_content
                ),
                "places_as_memory_anchors": self._transform_places_to_memory_content(
                    qloo_intelligence, heritage, patient_name
                ),
                "conversation_starters": self._create_places_based_conversations(
                    qloo_intelligence, heritage, patient_name
                ),
                "recipe_inspiration_notes": self._extract_recipe_inspiration_from_places(
                    qloo_intelligence, sensory_content
                ),
                "caregiver_guidance": self._create_caregiver_guidance_for_places(heritage),
                "mobile_structure": self._define_mobile_structure()
            }
            
            return {
                "mobile_experience": mobile_experience
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            return self._create_fallback_mobile_experience(consolidated_info)
    
    def _create_memory_focused_dashboard(self,
                                       consolidated_info: Dict[str, Any],
                                       cultural_profile: Dict[str, Any],
                                       qloo_intelligence: Dict[str, Any],
                                       sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create dashboard with places used as memory triggers."""
        
        patient_profile = consolidated_info.get("patient_profile", {})
        patient_name = patient_profile.get("first_name", "").split()[0] if patient_profile.get("first_name") else "Patient"
        
        # Extract recipe from sensory content
        recipe_content = sensory_content.get("content_by_sense", {}).get("taste", {})
        recipe = recipe_content.get("elements", [{}])[0] if recipe_content.get("available") else {}
        
        # Extract music from sensory content
        music_content = sensory_content.get("content_by_sense", {}).get("sound", {})
        music = music_content.get("elements", [{}])[0] if music_content.get("available") else {}
        
        dashboard = {
            "today_highlights": [
                {
                    "type": "recipe_activity",
                    "title": recipe.get("name", "Simple Comfort Recipe"),
                    "subtitle": "Cooking together",
                    "duration": recipe.get("total_time", "25 minutes"),
                    "description": recipe.get("description", "A simple, comforting recipe"),
                    "cultural_inspiration": recipe.get("recipe_inspiration_source", "Traditional family cooking"),
                    "engagement_focus": "Recipe inspired by family restaurant memories"
                },
                {
                    "type": "music_activity", 
                    "title": music.get("title", "Era-Appropriate Music"),
                    "subtitle": "Listening together",
                    "duration": "15-30 minutes",
                    "description": "Music from their formative years",
                    "cultural_connection": f"Music that connects to their {patient_profile.get('cultural_heritage', 'cultural')} background"
                }
            ],
            "memory_conversation_section": self._create_memory_conversation_section(
                qloo_intelligence, patient_name
            )
        }
        
        return dashboard
    
    def _transform_places_to_memory_content(self,
                                          qloo_intelligence: Dict[str, Any],
                                          heritage: str,
                                          patient_name: str) -> Dict[str, Any]:
        """Transform places into memory anchor content."""
        
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        places_data = cultural_recommendations.get("places", {})
        
        memory_anchors = []
        
        if places_data.get("available") and places_data.get("entities"):
            for place_entity in places_data["entities"][:3]:  # Limit to 3 for mobile
                
                # Check if this is already a memory anchor from our enhanced system
                if place_entity.get("memory_anchor_name"):
                    memory_anchor = {
                        "type": "memory_anchor",
                        "title": f"Family Restaurant Memories",
                        "subtitle": f"Inspired by {place_entity.get('memory_anchor_name')}",
                        "usage": "conversation_starter_and_recipe_inspiration",
                        "conversation_prompts": place_entity.get("conversation_prompts", []),
                        "recipe_inspiration": place_entity.get("recipe_inspiration", {}),
                        "memory_focus": f"Think about family restaurants from the {heritage} community",
                        "not_a_destination": True
                    }
                else:
                    # Transform regular place into memory anchor
                    place_name = place_entity.get("name", "Family Restaurant")
                    memory_anchor = {
                        "type": "memory_anchor",
                        "title": f"Family Dining Memories",
                        "subtitle": f"Style of {place_name}",
                        "usage": "conversation_starter_and_recipe_inspiration",
                        "conversation_prompts": [
                            f"Did you have a favorite family restaurant?",
                            f"What do you remember about dining out with family?",
                            f"Tell me about the food at places like this"
                        ],
                        "memory_focus": f"Think about family restaurants and special meals",
                        "not_a_destination": True
                    }
                
                memory_anchors.append(memory_anchor)
        
        return {
            "memory_anchors": memory_anchors,
            "usage_note": "These are for memories and conversations, not actual visits",
            "caregiver_instruction": f"Use these to help {patient_name} remember family dining experiences"
        }
    
    def _create_places_based_conversations(self,
                                         qloo_intelligence: Dict[str, Any],
                                         heritage: str,
                                         patient_name: str) -> Dict[str, Any]:
        """Create conversation starters based on places as memory anchors."""
        
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        places_data = cultural_recommendations.get("places", {})
        
        conversation_starters = []
        
        # Era-based restaurant memory conversations
        era_context = qloo_intelligence.get("metadata", {}).get("formative_decades", [])
        
        for decade in era_context[:2]:  # Use top 2 decades
            conversation_starters.extend([
                {
                    "category": "family_dining_memories",
                    "starter": f"What was your favorite family restaurant in the {decade}s?",
                    "follow_ups": [
                        "Who did you go there with?",
                        "What did you usually order?",
                        "What made it special?"
                    ],
                    "context": f"Family restaurants were important social spaces in the {decade}s",
                    "memory_trigger": "family dining experiences",
                    "decade_focus": decade
                },
                {
                    "category": "food_traditions",
                    "starter": f"Tell me about how families cooked {heritage} food in the {decade}s",
                    "follow_ups": [
                        "Did your family have special recipes?",
                        "Who taught you to cook?",
                        "What smells remind you of home cooking?"
                    ],
                    "context": f"Traditional cooking methods from the {decade}s",
                    "memory_trigger": "cooking and food preparation",
                    "decade_focus": decade
                }
            ])
        
        # Add heritage-specific restaurant conversations
        conversation_starters.append({
            "category": "cultural_food_memories",
            "starter": f"What {heritage} restaurants did you love when you were younger?",
            "follow_ups": [
                "What made the food special there?",
                "Did you have regular dishes you'd order?",
                "Who introduced you to these places?"
            ],
            "context": f"Cultural food experiences and {heritage} community dining",
            "memory_trigger": "cultural food identity",
            "heritage_focus": heritage
        })
        
        return {
            "conversation_starters": conversation_starters,
            "usage_guidance": "Use these to explore food and family memories, not to plan visits",
            "caregiver_note": f"Let {patient_name} lead the conversation and share what they remember"
        }
    
    def _extract_recipe_inspiration_from_places(self,
                                              qloo_intelligence: Dict[str, Any],
                                              sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract how places inspired the recipe creation."""
        
        # Get recipe from sensory content
        recipe_content = sensory_content.get("content_by_sense", {}).get("taste", {})
        recipe = recipe_content.get("elements", [{}])[0] if recipe_content.get("available") else {}
        
        # Get places data
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        places_data = cultural_recommendations.get("places", {})
        
        inspiration_notes = {
            "recipe_name": recipe.get("name", "Simple Comfort Recipe"),
            "inspiration_source": recipe.get("recipe_inspiration_source", "Traditional family cooking"),
            "cooking_style": "Family restaurant style from their formative years",
            "flavor_profile": "Comfort food flavors that would remind them of dining out with family",
            "preparation_approach": "Simple, traditional methods used in family restaurants",
            "memory_connection": "Designed to evoke positive memories of family dining experiences"
        }
        
        if places_data.get("available") and places_data.get("entities"):
            first_place = places_data["entities"][0]
            if first_place.get("recipe_inspiration"):
                inspiration_notes.update({
                    "specific_inspiration": first_place.get("recipe_inspiration"),
                    "place_style": first_place.get("memory_anchor_name", "Family restaurant style")
                })
        
        return inspiration_notes
    
    def _create_memory_conversation_section(self,
                                          qloo_intelligence: Dict[str, Any],
                                          patient_name: str) -> Dict[str, Any]:
        """Create conversation section focused on memory exploration."""
        
        return {
            "section_title": f"Exploring {patient_name}'s Memories",
            "conversation_approach": "memory_focused_not_destination_focused",
            "conversation_categories": [
                {
                    "category": "family_restaurants",
                    "icon": "🍽️",
                    "title": "Family Dining Memories",
                    "description": "Explore memories of favorite family restaurants and special meals",
                    "sample_questions": [
                        "Where did your family go for special occasions?",
                        "What restaurant did you visit most often?",
                        "Tell me about a memorable meal you had"
                    ]
                },
                {
                    "category": "cooking_memories", 
                    "icon": "👨‍🍳",
                    "title": "Cooking & Food Traditions",
                    "description": "Discuss family recipes and cooking traditions",
                    "sample_questions": [
                        "Who was the best cook in your family?",
                        "What smells remind you of home cooking?",
                        "Did you have any special family recipes?"
                    ]
                },
                {
                    "category": "community_dining",
                    "icon": "🏘️", 
                    "title": "Neighborhood Food Places",
                    "description": "Remember local delis, bakeries, and community gathering spots",
                    "sample_questions": [
                        "What shops did you visit in your neighborhood?",
                        "Where did families in your community gather?",
                        "Tell me about the local bakery or deli"
                    ]
                }
            ],
            "caregiver_guidance": f"Use these topics to help {patient_name} share food-related memories. Focus on their stories, not on planning any visits."
        }
    
    def _create_caregiver_guidance_for_places(self, heritage: str) -> Dict[str, Any]:
        """Create specific guidance for caregivers about using places as memory anchors."""
        
        return {
            "approach": "memory_anchors_not_destinations",
            "key_principles": [
                "Use places to trigger memories, not plan visits",
                "Focus on the past, not future activities",
                "Let them lead the conversation about their experiences",
                "Don't assume they want to visit anywhere new"
            ],
            "conversation_techniques": [
                {
                    "technique": "memory_bridging",
                    "description": "Use place names to bridge to personal memories",
                    "example": "This reminds me of Italian restaurants - did you have a favorite one?"
                },
                {
                    "technique": "sensory_connection",
                    "description": "Connect places to sensory memories",
                    "example": "What did it smell like in your favorite restaurant?"
                },
                {
                    "technique": "family_connection",
                    "description": "Connect places to family memories",
                    "example": "Who did you go to restaurants with when you were younger?"
                }
            ],
            "what_to_avoid": [
                "Don't suggest actually visiting any places",
                "Don't assume they want to go out to eat",
                "Don't make plans based on place recommendations",
                "Don't use places as activity suggestions"
            ],
            "safety_considerations": [
                "Many people with dementia prefer familiar environments",
                "New places can be overwhelming and confusing",
                "Focus on memory and comfort, not exploration",
                "Use places for cooking inspiration and conversation only"
            ]
        }
    
    def _define_mobile_structure(self) -> Dict[str, Any]:
        """Define mobile app structure with memory-focused places usage."""
        
        return {
            "structure_type": "memory_focused_dashboard", 
            "layout": "vertical_scrolling_cards",
            "primary_sections": [
                "today_highlights",
                "memory_conversation_starters", 
                "recipe_inspiration_notes",
                "places_as_memory_anchors",
                "family_food_memories"
            ],
            "interaction_pattern": "tap_to_explore_memories",
            "places_usage": "memory_anchors_and_recipe_inspiration_only",
            "caregiver_controls": "visible_throughout_with_memory_guidance"
        }
    
    def _create_fallback_mobile_experience(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback mobile experience when synthesis fails."""
        
        patient_profile = consolidated_info.get("patient_profile", {})
        heritage = patient_profile.get("cultural_heritage", "American")
        
        return {
            "mobile_experience": {
                "dashboard_content": {
                    "today_highlights": [
                        {
                            "type": "memory_conversation",
                            "title": "Family Food Memories",
                            "description": f"Talk about {heritage} family food traditions",
                            "duration": "15-30 minutes"
                        }
                    ]
                },
                "places_as_memory_anchors": {
                    "memory_anchors": [
                        {
                            "type": "memory_anchor",
                            "title": "Family Restaurant Memories",
                            "usage": "conversation_starter_only",
                            "not_a_destination": True
                        }
                    ],
                    "usage_note": "These are for memories only, not visits"
                },
                "fallback_used": True
            }
        }

# Test function
async def test_memory_focused_synthesis():
    """Test the memory-focused places synthesis."""
    
    agent = MobileSynthesizerAgent()
    
    # Test data with places as memory anchors
    consolidated_info = {
        "patient_profile": {
            "first_name": "Maria",
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "location": "Brooklyn, New York"
        }
    }
    
    cultural_profile = {
        "era_context": {
            "formative_decades": [1950, 1960, 1970]
        }
    }
    
    qloo_intelligence = {
        "cultural_recommendations": {
            "places": {
                "available": True,
                "memory_anchors": True,
                "entities": [
                    {
                        "name": "Larcomar",
                        "memory_anchor_name": "1960s-style Larcomar",
                        "conversation_prompts": [
                            "Did you have a favorite restaurant in the 1960s?",
                            "What do you remember about restaurants from that time?"
                        ],
                        "recipe_inspiration": {
                            "cuisine_style": "1960s family-style cooking",
                            "flavor_profile": "comfort food flavors"
                        },
                        "not_a_destination": True
                    }
                ]
            }
        },
        "metadata": {
            "formative_decades": [1950, 1960, 1970]
        }
    }
    
    sensory_content = {
        "content_by_sense": {
            "taste": {
                "available": True,
                "elements": [
                    {
                        "name": "Simple Italian Comfort Bread",
                        "description": "A comforting recipe inspired by family restaurants",
                        "recipe_inspiration_source": "Inspired by 1960s-style family restaurants"
                    }
                ]
            }
        }
    }
    
    photo_analysis = {"status": "skipped"}
    
    # Run the agent
    print("Testing memory-focused places synthesis...")
    result = await agent.run(
        consolidated_info, cultural_profile, qloo_intelligence, 
        sensory_content, photo_analysis
    )
    
    # Display results
    mobile_exp = result.get("mobile_experience", {})
    places_anchors = mobile_exp.get("places_as_memory_anchors", {})
    
    print(f"\nMemory Anchors Generated:")
    print(f"Count: {len(places_anchors.get('memory_anchors', []))}")
    print(f"Usage note: {places_anchors.get('usage_note')}")
    
    conversation_starters = mobile_exp.get("conversation_starters", {})
    print(f"\nConversation Starters: {len(conversation_starters.get('conversation_starters', []))}")
    
    caregiver_guidance = mobile_exp.get("caregiver_guidance", {})
    print(f"Caregiver approach: {caregiver_guidance.get('approach')}")
    
    # Show first memory anchor
    if places_anchors.get("memory_anchors"):
        first_anchor = places_anchors["memory_anchors"][0]
        print(f"\nFirst Memory Anchor:")
        print(f"Title: {first_anchor.get('title')}")
        print(f"Usage: {first_anchor.get('usage')}")
        print(f"Not a destination: {first_anchor.get('not_a_destination')}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_memory_focused_synthesis())