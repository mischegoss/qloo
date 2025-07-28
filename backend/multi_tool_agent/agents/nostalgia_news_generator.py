"""
Agent 5: Nostalgia News Generator - FIXED NEWSLETTER TONE
File: backend/multi_tool_agent/agents/nostalgia_news_generator.py

CRITICAL FIX:
- Always returns sections format that Agent 6 expects
- Uses generate_nostalgia_newsletter with proper tone guidance
- Newsletter-style content appropriate for caregivers to read aloud
- No more format mismatches
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
    Agent 5: FIXED Nostalgia News Generator - Newsletter Tone Restored
    """
    
    def __init__(self, gemini_tool=None):
        self.gemini_tool = gemini_tool
        self.theme_fallbacks = self._load_theme_fallbacks()
        
        logger.info("📰 Agent 5: FIXED Nostalgia News Generator initialized")
        logger.info(f"🧠 Gemini tool available: {self.gemini_tool is not None}")
        logger.info("✅ SECTIONS format with NEWSLETTER TONE guaranteed")
    
    def _load_theme_fallbacks(self) -> Dict[str, Any]:
        """Load theme fallbacks with guaranteed newsletter-style structure"""
        
        try:
            config_path = Path(__file__).parent.parent.parent / "config" / "nostalgia_news_fallbacks.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    theme_fallbacks = data.get("theme_fallbacks", {})
                    if theme_fallbacks:
                        logger.info(f"✅ Loaded {len(theme_fallbacks)} theme fallbacks from JSON")
                        return theme_fallbacks
        except Exception as e:
            logger.warning(f"⚠️ Error loading JSON fallbacks: {e}")
        
        # Guaranteed fallbacks with newsletter-style content
        return {
            "travel": {
                "memory_spotlight": "Remember those wonderful family road trips? Back in the 1950s, families would pack their cars and set off to explore America's highways, stopping at roadside diners and scenic overlooks. Travel has always opened hearts to new experiences and created lasting memories that connect us to the wider world.",
                "era_highlights": "In past decades, travel was a grand family adventure filled with discovery and wonder. Picture those classic family station wagons from the 1960s, loaded with suitcases and excitement for the journey ahead. Every trip was an opportunity to see something new and create stories that would be shared for years to come.",
                "heritage_traditions": "Every culture has its own special travel traditions, from family pilgrimages to seasonal journeys that honor heritage. Many families would visit relatives during holidays, creating beautiful connections across generations and sharing the joy of being together in different places.",
                "conversation_starters": [
                    "What was your favorite place to visit with your family?",
                    "Tell me about a memorable family trip you took",
                    "What did you enjoy most about traveling in those days?"
                ]
            },
            "food": {
                "memory_spotlight": "Remember those wonderful Sunday dinners when the whole family gathered around the table? Back in the 1940s and 50s, the aroma of home-cooked meals would fill the house, bringing everyone together. Food has always been at the heart of family life, creating moments of connection and love.",
                "era_highlights": "Those were the days when meals were prepared from scratch with care and attention. Picture Grandma's kitchen in the 1950s, with fresh bread rising and soup simmering on the stove. Every meal was a celebration of family togetherness and the simple pleasure of sharing good food.",
                "heritage_traditions": "Every family brought their own special food traditions to America, creating unique recipes that told the story of their heritage. These cherished recipes were passed down through generations, connecting families to their roots while creating new memories around the dinner table.",
                "conversation_starters": [
                    "What was your favorite family recipe growing up?",
                    "Tell me about special meals you remember from your childhood",
                    "What food traditions were most important to your family?"
                ]
            },
            "family": {
                "memory_spotlight": "Remember those wonderful family gatherings when everyone came together? Back in those days, families would gather for holidays, birthdays, and Sunday dinners, filling the house with laughter and stories. Family bonds have always been the foundation of life's most meaningful moments.",
                "era_highlights": "In the 1940s and 50s, family gatherings were grand affairs with multiple generations sharing the same table. Picture those holiday celebrations with children playing, adults sharing stories, and everyone feeling the warmth of being surrounded by loved ones. Every gathering created memories that would last a lifetime.",
                "heritage_traditions": "Every family brought their own special traditions to celebrations, whether it was singing songs, playing games, or sharing stories from the old country. These beautiful customs connected generations and preserved the wisdom and love that made each family unique.",
                "conversation_starters": [
                    "Tell me about your favorite family tradition growing up",
                    "What family gatherings do you remember most fondly?",
                    "Who was the best storyteller in your family?"
                ]
            },
            "birthday": {
                "memory_spotlight": "Remember those magical birthday celebrations when the whole family would come together? Back in the 1950s, birthdays were special occasions marked by homemade cakes, family sing-alongs, and cherished traditions. Every birthday was a celebration of life and the joy of being surrounded by loved ones.",
                "era_highlights": "In those days, birthday cakes were lovingly made from scratch, and the whole family would gather to sing and celebrate. Picture those wonderful moments when everyone would crowd around the birthday person, sharing hugs and making wishes. Every celebration created precious memories that would be treasured for years.",
                "heritage_traditions": "Every culture brought beautiful birthday traditions to America, with special foods, songs, and customs that made each celebration unique. These meaningful traditions connected families to their heritage while creating new memories that would be passed down through generations.",
                "conversation_starters": [
                    "What made birthday celebrations special in your family?",
                    "Do you remember a particularly wonderful birthday from your younger days?",
                    "What was your favorite birthday cake or special treat?"
                ]
            }
        }
    
    def _extract_profile_data(self, agent1_output: Dict[str, Any]) -> Dict[str, Any]:
        """Extract profile data with safe defaults"""
        
        try:
            patient_info = agent1_output.get("patient_info", {})
            theme_info = agent1_output.get("theme_info", {})
            
            return {
                "first_name": patient_info.get("first_name", "Friend"),
                "heritage": patient_info.get("cultural_heritage", "American").lower(),
                "theme_id": theme_info.get("id", "travel"),
                "theme_name": theme_info.get("name", "Travel"),
                "current_date": datetime.now().strftime("%B %d"),
                "birth_year": patient_info.get("birth_year", 1945)
            }
        except Exception as e:
            logger.warning(f"⚠️ Error extracting profile data: {e}")
            return {
                "first_name": "Friend",
                "heritage": "american",
                "theme_id": "travel", 
                "theme_name": "Travel",
                "current_date": datetime.now().strftime("%B %d"),
                "birth_year": 1945
            }
    
    def _extract_content_data(self, agent4a_output: Dict[str, Any], 
                             agent4b_output: Dict[str, Any],
                             agent4c_output: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content data with safe defaults"""
        
        try:
            music_content = agent4a_output.get("music_content", {})
            recipe_content = agent4b_output.get("recipe_content", {})
            
            return {
                "music_artist": music_content.get("artist", "Classical Music"),
                "music_piece": music_content.get("piece_title", "Beautiful Melodies"),
                "recipe_name": recipe_content.get("name", "Comfort Food")
            }
        except Exception as e:
            logger.warning(f"⚠️ Error extracting content data: {e}")
            return {
                "music_artist": "Classical Music",
                "music_piece": "Beautiful Melodies",
                "recipe_name": "Comfort Food"
            }
    
    async def _generate_with_gemini(self, profile_data: Dict[str, Any], content_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate using Gemini with NEWSLETTER TONE guidance"""
        
        # Check if Gemini tool has the newsletter method
        if not self.gemini_tool:
            logger.info("🤖 No Gemini tool available")
            return None
        
        # Try the new newsletter method first
        if hasattr(self.gemini_tool, 'generate_nostalgia_newsletter'):
            try:
                logger.info("🧠 Using Gemini generate_nostalgia_newsletter method")
                
                # Create comprehensive newsletter prompt
                prompt = f"""
                Create warm, positive nostalgia newsletter content focusing on {profile_data['theme_name']} for dementia care.
                
                Context:
                - Theme: {profile_data['theme_name']} (THIS IS THE MAIN FOCUS)
                - Heritage: {profile_data['heritage']} background
                - Era: 1940s-1950s
                - Today's music: {content_data['music_artist']} - {content_data['music_piece']}
                - Today's recipe: {content_data['recipe_name']}
                
                Create newsletter-style content that caregivers can read aloud to patients. Use warm, conversational tone with historical details and cultural context appropriate for the {profile_data['heritage']} heritage and {profile_data['theme_name']} theme.
                """
                
                # Define EXACT JSON structure
                json_schema = {
                    "memory_spotlight": "string",
                    "era_highlights": "string", 
                    "heritage_traditions": "string",
                    "conversation_starters": ["string", "string", "string"]
                }
                
                gemini_result = await self.gemini_tool.generate_nostalgia_newsletter(prompt, json_schema)
                
                if gemini_result and self._validate_gemini_result(gemini_result):
                    logger.info("✅ Gemini newsletter generation successful!")
                    return gemini_result
                else:
                    logger.warning("⚠️ Gemini newsletter result validation failed")
                    
            except Exception as e:
                logger.warning(f"⚠️ Gemini newsletter generation exception: {e}")
        
        # Fallback to regular structured JSON method
        if hasattr(self.gemini_tool, 'generate_structured_json'):
            try:
                logger.info("🧠 Falling back to Gemini generate_structured_json")
                
                # Create comprehensive prompt with newsletter tone guidance
                prompt = f"""
                Create warm, positive nostalgia content in NEWSLETTER STYLE focusing heavily on {profile_data['theme_name']} for dementia care.
                
                Context:
                - Theme: {profile_data['theme_name']} (THIS IS THE MAIN FOCUS)
                - Heritage: {profile_data['heritage']} background
                - Era: 1940s-1950s
                - Today's music: {content_data['music_artist']} - {content_data['music_piece']}
                - Today's recipe: {content_data['recipe_name']}
                
                NEWSLETTER TONE REQUIREMENTS:
                - Write for caregivers to read aloud to patients
                - NEVER use patient names in the content
                - Use simple, warm language that flows naturally when spoken
                - Include phrases like "Remember when..." or "Back in [year]..." 
                - Include specific historical details with years when appropriate
                - Make it sound like friendly news from the past
                - Focus on positive cultural memories and traditions
                - Each section should be 2-3 sentences that sound conversational
                
                EXAMPLE TONE: "Remember those wonderful Sunday drives? Back in the 1950s, families would pile into their cars just to see the countryside and stop for ice cream along the way."
                """
                
                # Define EXACT JSON structure
                json_schema = {
                    "memory_spotlight": "string",
                    "era_highlights": "string", 
                    "heritage_traditions": "string",
                    "conversation_starters": ["string", "string", "string"]
                }
                
                gemini_result = await self.gemini_tool.generate_structured_json(prompt, json_schema)
                
                if gemini_result and self._validate_gemini_result(gemini_result):
                    logger.info("✅ Gemini structured generation successful!")
                    return gemini_result
                else:
                    logger.warning("⚠️ Gemini structured result validation failed")
                    
            except Exception as e:
                logger.warning(f"⚠️ Gemini structured generation exception: {e}")
        
        logger.info("🤖 No suitable Gemini methods available")
        return None
    
    def _validate_gemini_result(self, result: Dict[str, Any]) -> bool:
        """Validate Gemini generated content has all required sections"""
        
        required_sections = ["memory_spotlight", "era_highlights", "heritage_traditions", "conversation_starters"]
        
        for section in required_sections:
            if section not in result:
                logger.warning(f"⚠️ Missing section: {section}")
                return False
            
            if section == "conversation_starters":
                if not isinstance(result[section], list) or len(result[section]) < 3:
                    logger.warning(f"⚠️ Invalid conversation_starters: {type(result[section])}, length: {len(result[section]) if isinstance(result[section], list) else 'N/A'}")
                    return False
            else:
                content = result[section]
                if not content or len(content.split()) < 10:
                    logger.warning(f"⚠️ Section {section} too short: {len(content.split()) if content else 0} words")
                    return False
        
        return True
    
    def _create_guaranteed_fallback(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create guaranteed fallback content with newsletter-style tone"""
        
        theme_id = profile_data['theme_id']
        theme_name = profile_data['theme_name']
        heritage = profile_data['heritage']
        
        # Get theme-specific content or create it
        theme_content = self.theme_fallbacks.get(theme_id)
        
        if not theme_content:
            # Create newsletter-style content for any theme
            heritage_title = heritage.title()
            theme_content = {
                "memory_spotlight": f"Remember when {theme_name.lower()} brought families together in such special ways? Back in the 1940s and 50s, {theme_name.lower()} was an important part of creating meaningful connections and cherished memories. Every moment was an opportunity to celebrate what mattered most in life.",
                "era_highlights": f"In those wonderful days, {theme_name.lower()} was celebrated with family gatherings, community events, and traditions that brought people together in joy. Picture those times when everyone would come together, sharing stories and creating memories that would last a lifetime. Every celebration was a testament to the simple pleasures that made life so rich.",
                "heritage_traditions": f"{heritage_title} families brought their own beautiful traditions to {theme_name.lower()}, creating unique cultural experiences that honored their heritage. These special customs connected generations and preserved the wisdom and love that made each family's story unique. Every tradition was a bridge between the past and the present.",
                "conversation_starters": [
                    f"What memories about {theme_name.lower()} are most special to you?",
                    f"How did your family celebrate {theme_name.lower()} in those days?",
                    "What traditions were most important to your family?"
                ]
            }
        
        logger.info(f"📝 Created newsletter-style fallback for {theme_name} theme")
        return theme_content
    
    def _format_final_response(self, content: Dict[str, Any], profile_data: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Format content into GUARANTEED sections structure for Agent 6"""
        
        logger.info(f"🎨 Formatting newsletter-style final response from {source}")
        
        # CRITICAL: This is the EXACT structure Agent 6 expects
        final_response = {
            "title": f"Nostalgia News – {profile_data['current_date']}",
            "subtitle": f"{profile_data['theme_name']} Edition",
            "date": datetime.now().strftime("%B %d, %Y"),
            "personalized_for": profile_data['first_name'],
            
            # THIS IS THE KEY - Agent 6 looks for "sections" with this exact structure
            "sections": {
                "memory_spotlight": {
                    "headline": "📚 Memory Spotlight",
                    "content": content.get("memory_spotlight", "Remember those wonderful times when families came together? Every day brought opportunities for meaningful moments and beautiful memories that would last a lifetime."),
                    "fun_fact": "Historical moments create our most treasured memories."
                },
                "era_highlights": {
                    "headline": "🎵 Era Highlights", 
                    "content": content.get("era_highlights", "Back in the 1940s and 50s, every era brought its own special joys and celebrations. Those were the days when simple pleasures created the most lasting happiness."),
                    "fun_fact": "Music has always been central to life's celebrations."
                },
                "heritage_traditions": {
                    "headline": "🏛️ Heritage Traditions",
                    "content": content.get("heritage_traditions", "Every family brought their own beautiful traditions to America, creating cultural experiences that honored their heritage. These special customs connected generations and preserved wisdom through time."),
                    "fun_fact": "Cultural traditions connect us to our roots."
                },
                "conversation_starters": {
                    "headline": "💬 Conversation Starters",
                    "questions": content.get("conversation_starters", [
                        "What brings you joy when you think about those days?",
                        "Tell me about a happy memory from your younger years",
                        "What traditions were most important to your family?"
                    ])[:3]  # Ensure exactly 3 questions
                }
            },
            
            "themes": [profile_data['theme_name'], "Heritage", "Memories"],
            
            "metadata": {
                "generated_by": source,
                "generation_timestamp": datetime.now().isoformat(),
                "theme_integrated": profile_data['theme_name'],
                "heritage_featured": profile_data['heritage'],
                "safety_level": "dementia_friendly",
                "structure_verified": True,
                "sections_count": 4,
                "newsletter_tone": True
            }
        }
        
        # Log the structure we're creating
        logger.info(f"✅ Newsletter-style final response structure created:")
        logger.info(f"   - Title: {final_response['title']}")
        logger.info(f"   - Sections: {list(final_response['sections'].keys())}")
        logger.info(f"   - Conversation starters: {len(final_response['sections']['conversation_starters']['questions'])}")
        logger.info(f"   - Newsletter tone: {final_response['metadata']['newsletter_tone']}")
        
        return final_response

    async def run(self,
                  agent1_output: Dict[str, Any],
                  agent2_output: Dict[str, Any], 
                  agent3_output: Dict[str, Any],
                  agent4a_output: Dict[str, Any],
                  agent4b_output: Dict[str, Any],
                  agent4c_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate nostalgia news with GUARANTEED sections format and NEWSLETTER TONE
        """
        
        logger.info("📰 Agent 5: Generating NEWSLETTER-STYLE SECTIONS FORMAT Nostalgia News")
        
        try:
            # Extract data with safe defaults
            profile_data = self._extract_profile_data(agent1_output)
            content_data = self._extract_content_data(agent4a_output, agent4b_output, agent4c_output)
            
            logger.info(f"📋 Profile: {profile_data['first_name']} | Theme: {profile_data['theme_name']} | Heritage: {profile_data['heritage']}")
            
            # Try Gemini first with newsletter tone guidance
            generated_content = None
            source = "fallback"
            
            if self.gemini_tool:
                logger.info("🧠 Attempting Gemini newsletter generation...")
                
                generated_content = await self._generate_with_gemini(profile_data, content_data)
                
                if generated_content:
                    source = "gemini_newsletter"
                    logger.info("✅ Gemini newsletter generation successful!")
                else:
                    logger.info("⚠️ Gemini newsletter generation failed, using guaranteed fallback")
            else:
                logger.info("🤖 No Gemini tool, using guaranteed newsletter fallback")
            
            # Use fallback if Gemini failed or unavailable
            if not generated_content:
                generated_content = self._create_guaranteed_fallback(profile_data)
                source = "guaranteed_newsletter_fallback"
                logger.info("✅ Guaranteed newsletter fallback content created")
            
            # Format the final response with GUARANTEED sections structure
            final_response = self._format_final_response(generated_content, profile_data, source)
            
            logger.info("✅ NEWSLETTER-STYLE SECTIONS FORMAT nostalgia news generated!")
            logger.info(f"📊 Response structure: {list(final_response.keys())}")
            logger.info(f"📊 Sections structure: {list(final_response['sections'].keys())}")
            
            return {"nostalgia_news": final_response}
            
        except Exception as e:
            logger.error(f"❌ All methods failed, using emergency newsletter fallback: {e}")
            
            # Emergency fallback with newsletter tone and guaranteed structure
            emergency_profile = {
                "first_name": "Friend",
                "theme_name": "Beautiful Moments",
                "current_date": datetime.now().strftime("%B %d"),
                "heritage": "universal",
                "theme_id": "universal"
            }
            
            emergency_content = {
                "memory_spotlight": "Remember those wonderful times when life was filled with simple pleasures? Back in the 1940s and 50s, every day brought opportunities for meaningful moments and beautiful memories that would warm the heart for years to come.",
                "era_highlights": "In those special days, families and communities came together in celebration and joy. Picture those times when people found happiness in the simplest things - sharing a meal, listening to music, or just spending time with loved ones.",
                "heritage_traditions": "Every family brought their own beautiful traditions to America, creating a rich tapestry of cultural experiences. These special customs connected generations and preserved the wisdom and love that made each family's story unique.",
                "conversation_starters": [
                    "What brings you joy when you think about those wonderful days?",
                    "Tell me about a happy memory from your younger years",
                    "What traditions were most important to your family?"
                ]
            }
            
            emergency_response = self._format_final_response(emergency_content, emergency_profile, "emergency_newsletter_fallback")
            
            return {"nostalgia_news": emergency_response}

# Export the main class
__all__ = ["NostalgiaNewsGenerator"]