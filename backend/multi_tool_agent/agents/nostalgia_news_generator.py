"""
Agent 5: Nostalgia News Generator - Enhanced with Theme-Based Fallbacks
File: backend/multi_tool_agent/agents/nostalgia_news_generator.py

ENHANCED:
- Uses simple_gemini_tools for consistency
- Extensive theme-based fallbacks from JSON
- Always works even when Gemini fails
- Personalized content without dates in fallbacks
- Comprehensive error handling
- FIXED: Slice error in _extract_cultural_data method
"""

import logging
import json
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class NostalgiaNewsGenerator:
    """
    Agent 5: Enhanced Nostalgia News Generator
    
    Creates personalized cultural "newspaper" using Gemini AI with extensive
    theme-based fallbacks that ensure the feature always works beautifully.
    """
    
    def __init__(self, gemini_tool=None):
        # Use simple_gemini_tools for consistency
        self.gemini_tool = gemini_tool
        
        # Load theme-based fallback content
        self.theme_fallbacks = self._load_theme_fallbacks()
        
        # Load additional fallback content for when everything fails
        self.emergency_fallback = self._load_emergency_fallback()
        
        logger.info("📰 Agent 5: Enhanced Nostalgia News Generator initialized")
        logger.info(f"🧠 Gemini tool available: {self.gemini_tool is not None}")
        logger.info(f"🎯 Theme fallbacks loaded: {len(self.theme_fallbacks)} themes")
        logger.info("✅ Extensive fallbacks ensure this feature ALWAYS works")
    
    def _load_theme_fallbacks(self) -> Dict[str, Any]:
        """Load theme-based fallback content from JSON"""
        
        try:
            # Try multiple paths for the fallback JSON file
            possible_paths = [
                Path(__file__).parent.parent.parent / "config" / "nostalgia_news_fallbacks.json",
                Path(__file__).parent.parent / "config" / "nostalgia_news_fallbacks.json", 
                Path(__file__).parent / "nostalgia_news_fallbacks.json",
                Path("config/nostalgia_news_fallbacks.json"),
                Path("nostalgia_news_fallbacks.json")
            ]
            
            for path in possible_paths:
                if path.exists():
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        logger.info(f"✅ Loaded theme fallbacks from {path}")
                        return data.get("theme_fallbacks", {})
            
            logger.warning("⚠️ Nostalgia news fallbacks JSON not found, using built-in fallbacks")
            
        except Exception as e:
            logger.error(f"❌ Error loading theme fallbacks: {e}")
        
        # Return built-in fallbacks if file loading fails
        return self._get_builtin_theme_fallbacks()
    
    def _load_emergency_fallback(self) -> Dict[str, Any]:
        """Load emergency fallback content"""
        
        try:
            # Try to get from the same JSON file
            possible_paths = [
                Path(__file__).parent.parent.parent / "config" / "nostalgia_news_fallbacks.json",
                Path(__file__).parent.parent / "config" / "nostalgia_news_fallbacks.json",
            ]
            
            for path in possible_paths:
                if path.exists():
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return data.get("emergency_fallback", {})
                        
        except Exception as e:
            logger.error(f"❌ Error loading emergency fallback: {e}")
        
        # Return built-in emergency fallback
        return self._get_builtin_emergency_fallback()
    
    def _get_builtin_theme_fallbacks(self) -> Dict[str, Any]:
        """Built-in theme fallbacks if JSON file is unavailable"""
        
        return {
            "birthday": {
                "on_this_day": {
                    "content": "Birthdays have always been special celebrations that bring families together! Throughout history, people have marked these precious days with joy, love, and treasured memories.",
                    "generic_facts": ["Birthday celebrations date back thousands of years", "Making birthday wishes is a tradition found worldwide"]
                },
                "era_spotlight": {
                    "content": "Throughout the decades, families have celebrated birthdays with homemade cakes, music, and gathered loved ones creating beautiful memories together.",
                    "generic_facts": ["Birthday parties often featured family sing-alongs", "Homemade birthday cakes were labors of love"]
                },
                "heritage_traditions": {
                    "content": "Every culture has beautiful birthday traditions that honor the special person, from sharing favorite foods to creating lasting memories with loved ones.",
                    "generic_facts": ["Many cultures have special birthday foods", "Birthday songs exist in nearly every culture"]
                },
                "conversation_questions": [
                    "What was your most memorable birthday celebration?",
                    "Did your family have special birthday traditions?", 
                    "What's your favorite birthday memory?"
                ]
            },
            "family": {
                "on_this_day": {
                    "content": "Family gatherings have always been the heart of happy memories! Families have come together to share stories, laughter, and bonds that make life meaningful.",
                    "generic_facts": ["Family traditions preserve cultural heritage", "Family gatherings strengthen emotional bonds"]
                },
                "era_spotlight": {
                    "content": "Families often gathered around dinner tables for conversations, shared photo albums, and created traditions that brought everyone together.",
                    "generic_facts": ["Sunday dinners were family tradition highlights", "Photo albums were treasured family keepsakes"]
                },
                "heritage_traditions": {
                    "content": "Each family heritage brings unique traditions, from special recipes passed down through generations to cultural celebrations that connect us to our roots.",
                    "generic_facts": ["Family recipes often carry cultural history", "Heritage traditions strengthen family identity"]
                },
                "conversation_questions": [
                    "What family traditions do you remember most fondly?",
                    "Tell me about your favorite family gathering",
                    "What made your family special?"
                ]
            },
            "memory_lane": {
                "on_this_day": {
                    "content": "Walking down memory lane reminds us of all the beautiful moments that have shaped our lives! Every memory is a treasure that connects us to joy, love, and meaningful experiences.",
                    "generic_facts": ["Memories help us appreciate life's journey", "Sharing memories strengthens relationships"]
                },
                "era_spotlight": {
                    "content": "Each era brought its own special moments and memories, from music and dancing to simple pleasures that made life beautiful and meaningful.",
                    "generic_facts": ["Every generation creates unique memories", "Music often triggers the strongest memories"]
                },
                "heritage_traditions": {
                    "content": "Our heritage gives us rich memories and traditions that connect us to our families and cultural roots, creating a beautiful tapestry of experiences.",
                    "generic_facts": ["Cultural memories span generations", "Heritage traditions create lasting memories"]
                },
                "conversation_questions": [
                    "What's one of your happiest memories?",
                    "What always makes you smile when you think about it?",
                    "Tell me about a perfect day from your past"
                ]
            }
        }
    
    def _get_builtin_emergency_fallback(self) -> Dict[str, Any]:
        """Built-in emergency fallback when everything fails"""
        
        return {
            "on_this_day": {
                "content": "Today is a special day to celebrate the wonderful person you are! Every day brings new opportunities for joy, connection, and beautiful moments.",
                "generic_facts": ["Every day is an opportunity for joy", "Human connections make life meaningful"]
            },
            "era_spotlight": {
                "content": "Throughout all the years, the most important things remain the same: kindness, love, and the connections we make with others.",
                "generic_facts": ["Love and kindness are timeless", "Human connections transcend all eras"]
            },
            "heritage_traditions": {
                "content": "No matter where we come from, we all share the universal values of family, kindness, and caring for one another.",
                "generic_facts": ["Kindness and care are universal human values", "Every person has unique experiences to share"]
            },
            "conversation_questions": [
                "What brings you joy today?",
                "Tell me about something that makes you smile",
                "What are you grateful for?"
            ]
        }
    
    def _extract_profile_data(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Safely extract profile data with defaults"""
        
        try:
            patient_info = agent1_output.get("patient_info", {})
            theme_info = agent1_output.get("theme_info", {})
            
            first_name = patient_info.get("first_name", "Friend")
            age = patient_info.get("current_age", 80)
            heritage = patient_info.get("cultural_heritage", "american")
            birth_year = patient_info.get("birth_year", 1945)
            theme = theme_info.get("name", "memory_lane")
            theme_display = theme_info.get("display_name", "Memory Lane")
            
            # Calculate era based on birth year
            if birth_year <= 1945:
                era = "1940s"
            elif birth_year <= 1955:
                era = "1950s"
            elif birth_year <= 1965:
                era = "1960s"
            else:
                era = "1970s"
            
            return {
                "first_name": first_name,
                "age": age,
                "heritage": heritage.lower(), 
                "theme": theme,
                "theme_display": theme_display,
                "current_date": datetime.now().strftime("%B %d"),
                "full_date": datetime.now().strftime("%B %d, %Y"),
                "era": era,
                "birth_year": birth_year
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Error extracting profile data: {e}")
            return {
                "first_name": "Friend",
                "age": 80,
                "heritage": "american", 
                "theme": "memory_lane",
                "theme_display": "Memory Lane",
                "current_date": datetime.now().strftime("%B %d"),
                "full_date": datetime.now().strftime("%B %d, %Y"),
                "era": "1940s"
            }
    
    def _extract_cultural_data(self, agent3_output: Dict[str, Any]) -> Dict[str, Any]:
        """Safely extract cultural intelligence with defaults - FIXED SLICE ERROR"""
        
        try:
            qloo_data = agent3_output.get("qloo_intelligence", {})
            cultural_recs = qloo_data.get("cultural_recommendations", {})
            
            # CRITICAL FIX: Safe extraction with type checking before slicing
            artists_data = cultural_recs.get("artists", {})
            if isinstance(artists_data, dict):
                artists = artists_data.get("entities", [])
            else:
                artists = []
                
            # CRITICAL FIX: Ensure artists is a list before slicing
            if not isinstance(artists, list):
                artists = []
            
            return {
                "preferred_artists": [artist.get("name", "") for artist in artists[:3] if isinstance(artist, dict) and artist.get("name")],
                "cultural_insights": qloo_data.get("cultural_insights", {}),
                "heritage_connections": qloo_data.get("heritage_connections", [])
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Error extracting cultural data: {e}")
            return {
                "preferred_artists": ["Classical Music"],
                "cultural_insights": {},
                "heritage_connections": []
            }
    
    def _extract_content_data(self, agent4a_output: Dict[str, Any], 
                             agent4b_output: Dict[str, Any],
                             agent4c_output: Dict[str, Any]) -> Dict[str, Any]:
        """Safely extract selected content with defaults"""
        
        try:
            music_content = agent4a_output.get("music_content", {})
            recipe_content = agent4b_output.get("recipe_content", {})
            photo_content = agent4c_output.get("photo_content", {})
            
            return {
                "selected_artist": music_content.get("artist", "Classical music"),
                "selected_piece": music_content.get("piece_title", "beautiful melodies"),
                "selected_recipe": recipe_content.get("name", "comfort food"),
                "recipe_heritage": recipe_content.get("heritage_tags", []),
                "photo_description": photo_content.get("description", "cherished memories"),
                "photo_theme": photo_content.get("theme", "special moments")
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Error extracting content data: {e}")
            return {
                "selected_artist": "Classical music",
                "selected_piece": "beautiful melodies", 
                "selected_recipe": "comfort food",
                "recipe_heritage": [],
                "photo_description": "cherished memories",
                "photo_theme": "special moments"
            }
    
    async def _generate_with_gemini(self, profile_data: Dict[str, Any],
                                   cultural_data: Dict[str, Any], 
                                   content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate nostalgia news using Gemini AI with error handling"""
    
        try:
            # Create comprehensive prompt
            prompt = self._create_gemini_prompt(profile_data, cultural_data, content_data)
            
            # Call Gemini using simple_gemini_tools (returns string directly)
            if hasattr(self.gemini_tool, 'generate_content'):
                gemini_content = await self.gemini_tool.generate_content(prompt)
            else:
                logger.warning("⚠️ Gemini tool missing generate_content method")
                return {"success": False}
            
            # Parse and validate response (simple_gemini_tools returns string directly)
            if gemini_content and isinstance(gemini_content, str):
                parsed_result = self._parse_gemini_response(gemini_content, profile_data)
                if parsed_result:
                    parsed_result["success"] = True
                    return parsed_result
            
            logger.warning("⚠️ Gemini response validation failed")
            return {"success": False}
                
        except Exception as e:
            logger.warning(f"⚠️ Gemini generation exception: {e}")
            return {"success": False}
    
    def _create_gemini_prompt(self, profile_data: Dict[str, Any],
                             cultural_data: Dict[str, Any],
                             content_data: Dict[str, Any]) -> str:
        """Create optimized prompt for Gemini"""
        
        prompt = f"""
Create warm, positive "Nostalgia News" for {profile_data['first_name']}, a {profile_data['age']}-year-old {profile_data['heritage']} person.

CONTEXT:
- Today: {profile_data['full_date']}
- Theme: {profile_data['theme_display']}
- Era: {profile_data['era']} (born {profile_data.get('birth_year', 'unknown')})
- Heritage: {profile_data['heritage']}
- Music: {content_data['selected_artist']} - {content_data['selected_piece']}
- Food: {content_data['selected_recipe']}

Create exactly 4 sections in JSON format:

1. "on_this_day": Positive historical event from {profile_data['current_date']} connecting to their era. 2-3 sentences using their name.

2. "era_spotlight": How {profile_data['theme_display']} was celebrated in the {profile_data['era']}. Connect to today's music. 2-3 sentences using their name.

3. "heritage_traditions": How {profile_data['heritage']} families celebrated {profile_data['theme_display']}. Connect to today's recipe. 2-3 sentences using their name.

4. "conversation_questions": 3 gentle questions about their {profile_data['theme_display']} experiences using their name.

REQUIREMENTS:
- Use {profile_data['first_name']}'s name in each section
- Keep positive, warm, encouraging tone
- Focus on family, traditions, happy memories
- No illness, loss, or negative events
- 2-3 sentences maximum per section
- Return valid JSON only

JSON format:
{{
    "on_this_day": "Content here with {profile_data['first_name']}'s name...",
    "era_spotlight": "Content here with {profile_data['first_name']}'s name...",
    "heritage_traditions": "Content here with {profile_data['first_name']}'s name...",
    "conversation_questions": ["Question 1 for {profile_data['first_name']}?", "Question 2 for {profile_data['first_name']}?", "Question 3 for {profile_data['first_name']}?"]
}}
"""
        
        return prompt
    
    def _parse_gemini_response(self, gemini_content: str, profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse and validate Gemini response with extensive error handling"""
        
        try:
            # Extract JSON from response (simple_gemini_tools returns string directly)
            if "{" in gemini_content and "}" in gemini_content:
                start = gemini_content.find("{")
                end = gemini_content.rfind("}") + 1
                json_str = gemini_content[start:end]
                
                parsed_content = json.loads(json_str)
                
                # Validate required fields
                required_fields = ["on_this_day", "era_spotlight", "heritage_traditions", "conversation_questions"]
                if not all(field in parsed_content for field in required_fields):
                    logger.warning("⚠️ Gemini response missing required fields")
                    return None
                
                # Validate conversation_questions is a list
                if not isinstance(parsed_content.get("conversation_questions"), list):
                    logger.warning("⚠️ Gemini response conversation_questions not a list")
                    return None
                
                # Structure the final response
                return {
                    "title": f"{profile_data['first_name']}'s Nostalgia News for {profile_data['current_date']}",
                    "subtitle": f"{profile_data['heritage'].title()} Heritage Edition",
                    "date": profile_data['full_date'],
                    "personalized_for": profile_data['first_name'],
                    
                    "sections": {
                        "on_this_day": {
                            "headline": "🌟 On This Day in History",
                            "content": parsed_content["on_this_day"],
                            "era_connection": profile_data['era']
                        },
                        "era_spotlight": {
                            "headline": "🎵 Your Era Spotlight",
                            "content": parsed_content["era_spotlight"],
                            "era": profile_data['era']
                        },
                        "heritage_traditions": {
                            "headline": "🍽️ Heritage Traditions",
                            "content": parsed_content["heritage_traditions"],
                            "heritage": profile_data['heritage'].title()
                        },
                        "conversation_corner": {
                            "headline": "💭 Conversation Corner",
                            "questions": parsed_content["conversation_questions"]
                        }
                    },
                    
                    "metadata": {
                        "generated_by": "gemini",
                        "generation_timestamp": datetime.now().isoformat(),
                        "theme_integrated": profile_data['theme_display'],
                        "heritage_featured": profile_data['heritage'],
                        "era_highlighted": profile_data['era'],
                        "safety_level": "dementia_friendly"
                    }
                }
                
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ Gemini response JSON parsing failed: {e}")
        except Exception as e:
            logger.warning(f"⚠️ Gemini response parsing error: {e}")
        
        return None
    
    def _generate_theme_fallback(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate theme-based fallback content that always works"""
        
        logger.info(f"📰 Generating theme-based fallback for: {profile_data['theme']}")
        
        # Get theme-specific fallback content
        theme_content = self.theme_fallbacks.get(profile_data['theme'], 
                                                 self.theme_fallbacks.get('memory_lane',
                                                                         self.emergency_fallback))
        
        if not theme_content:
            theme_content = self.emergency_fallback
        
        # Personalize the content with the user's name
        first_name = profile_data['first_name']
        
        return {
            "title": f"{first_name}'s Nostalgia News",  # No date in fallback
            "subtitle": f"Special Edition for {first_name}",
            "personalized_for": first_name,
            
            "sections": {
                "on_this_day": {
                    "headline": "🌟 On This Day",
                    "content": self._personalize_content(theme_content["on_this_day"]["content"], first_name),
                    "fun_fact": random.choice(theme_content["on_this_day"].get("generic_facts", ["Every day is special!"]))
                },
                "era_spotlight": {
                    "headline": "🎵 Through the Years",
                    "content": self._personalize_content(theme_content["era_spotlight"]["content"], first_name),
                    "fun_fact": random.choice(theme_content["era_spotlight"].get("generic_facts", ["Music brings joy to every era!"]))
                },
                "heritage_traditions": {
                    "headline": "🍽️ Cherished Traditions",
                    "content": self._personalize_content(theme_content["heritage_traditions"]["content"], first_name),
                    "fun_fact": random.choice(theme_content["heritage_traditions"].get("generic_facts", ["Traditions connect us to our heritage!"]))
                },
                "conversation_corner": {
                    "headline": "💭 Let's Talk",
                    "questions": [self._personalize_question(q, first_name) for q in random.sample(
                        theme_content["conversation_questions"], 
                        min(3, len(theme_content["conversation_questions"]))
                    )]
                }
            },
            
            "metadata": {
                "generated_by": "theme_fallback",
                "generation_timestamp": datetime.now().isoformat(),
                "theme_used": profile_data['theme'],
                "theme_display": profile_data['theme_display'],
                "safety_level": "dementia_friendly",
                "fallback_type": "theme_based"
            }
        }
    
    def _generate_emergency_fallback(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Generate emergency fallback when everything else fails"""
        
        logger.warning("🚨 Using emergency fallback for Nostalgia News")
        
        # Extract name safely
        try:
            first_name = agent1_output.get("patient_info", {}).get("first_name", "Friend")
        except:
            first_name = "Friend"
        
        emergency_content = self.emergency_fallback
        
        return {
            "title": f"{first_name}'s Special News",
            "subtitle": "Daily Edition",
            "personalized_for": first_name,
            
            "sections": {
                "on_this_day": {
                    "headline": "✨ Today's Message",
                    "content": self._personalize_content(emergency_content["on_this_day"]["content"], first_name),
                    "fun_fact": random.choice(emergency_content["on_this_day"].get("generic_facts", ["Every day is a gift!"]))
                },
                "era_spotlight": {
                    "headline": "🎵 Timeless Joy",
                    "content": self._personalize_content(emergency_content["era_spotlight"]["content"], first_name),
                    "fun_fact": random.choice(emergency_content["era_spotlight"].get("generic_facts", ["Joy is timeless!"]))
                },
                "heritage_traditions": {
                    "headline": "🤝 Human Connection", 
                    "content": self._personalize_content(emergency_content["heritage_traditions"]["content"], first_name),
                    "fun_fact": random.choice(emergency_content["heritage_traditions"].get("generic_facts", ["We are all connected!"]))
                },
                "conversation_corner": {
                    "headline": "💭 Share With Us",
                    "questions": [self._personalize_question(q, first_name) for q in emergency_content["conversation_questions"]]
                }
            },
            
            "metadata": {
                "generated_by": "emergency_fallback",
                "generation_timestamp": datetime.now().isoformat(),
                "safety_level": "dementia_friendly",
                "fallback_type": "emergency"
            }
        }
    
    def _personalize_content(self, content: str, first_name: str) -> str:
        """Add personalization to content by inserting the person's name"""
        
        if not first_name or first_name == "Friend":
            return content
        
        # Add name at the end if not already present
        if first_name.lower() not in content.lower():
            # Add name naturally to the content
            if content.endswith("!") or content.endswith("."):
                return content[:-1] + f", {first_name}!"
            else:
                return content + f", {first_name}!"
        
        return content
    
    def _personalize_question(self, question: str, first_name: str) -> str:
        """Personalize a question with the person's name"""
        
        if not first_name or first_name == "Friend":
            return question
        
        # If the question doesn't already contain the name, add it
        if first_name.lower() not in question.lower():
            if question.endswith("?"):
                return question[:-1] + f", {first_name}?"
            else:
                return f"{question}, {first_name}?"
        
        return question

    async def run(self,
                  agent1_output: Dict[str, Any],
                  agent2_output: Dict[str, Any], 
                  agent3_output: Dict[str, Any],
                  agent4a_output: Dict[str, Any],
                  agent4b_output: Dict[str, Any],
                  agent4c_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized Nostalgia News with extensive fallback support
        
        This method ALWAYS succeeds and returns properly formatted content.
        """
        
        logger.info("📰 Agent 5: Generating Nostalgia News with extensive fallbacks")
        
        try:
            # Extract profile data (always works)
            profile_data = self._extract_profile_data(agent1_output)
            
            logger.info(f"📋 Generating news for: {profile_data['first_name']} - Theme: {profile_data['theme']}")
            
            # Try Gemini first if available
            if self.gemini_tool:
                logger.info("🧠 Attempting Gemini generation...")
                try:
                    cultural_data = self._extract_cultural_data(agent3_output)
                    content_data = self._extract_content_data(agent4a_output, agent4b_output, agent4c_output)
                    
                    gemini_result = await self._generate_with_gemini(profile_data, cultural_data, content_data)
                    
                    if gemini_result and gemini_result.get("success"):
                        logger.info("✅ Gemini generation successful!")
                        return {"nostalgia_news": gemini_result}
                    else:
                        logger.info("⚠️ Gemini generation failed, using theme fallback")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Gemini generation error: {e}")
            
            # If Gemini failed or unavailable, use theme-based fallback
            logger.info("📰 Using theme-based fallback generation")
            theme_fallback = self._generate_theme_fallback(profile_data)
            return {"nostalgia_news": theme_fallback}
            
        except Exception as e:
            # Last resort: emergency fallback
            logger.error(f"❌ All fallbacks failed, using emergency mode: {e}")
            emergency_fallback = self._generate_emergency_fallback(agent1_output)
            return {"nostalgia_news": emergency_fallback}

# Export the main class
__all__ = ["NostalgiaNewsGenerator"]