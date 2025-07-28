"""
Agent 4C: Cultural Photo Description Agent - WITH DEMENTIA-FRIENDLY DESCRIPTIONS
File: backend/multi_tool_agent/agents/photo_description_agent.py

CORRECT FIXES APPLIED:
- ✅ Fixed JSON file name (photo_analyses.json not photo_analysis.json)
- ✅ Fixed JSON structure (photo_analyses array not photo_analysis_data dict)
- ✅ Fixed theme matching logic for array structure
- ✅ Fixed Gemini response handling (string not dict)
- ✅ Improved error handling and fallbacks

NEW FEATURE:
- ✅ Added dementia-friendly photo descriptions using Gemini
- ✅ Replaces technical descriptions with simple, warm language

PURPOSE:
Takes today's theme and patient cultural profile, selects appropriate photo
and uses Gemini AI to create culturally-relevant conversation starters
AND generate simple, warm, dementia-friendly photo descriptions.
"""

import asyncio
import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class PhotoDescriptionAgent:
    """
    Agent 4C: Cultural Photo Description Agent - WITH DEMENTIA-FRIENDLY DESCRIPTIONS
    
    CORRECT FIXES:
    - Fixed JSON file path (photo_analyses.json)
    - Fixed JSON structure handling (array not dict)
    - Fixed theme-based photo selection
    - Fixed Gemini response handling
    - Improved fallback mechanisms
    
    NEW FEATURE:
    - Generates simple, warm photo descriptions for dementia care
    """
    
    def __init__(self, gemini_tool=None):
        self.gemini_tool = gemini_tool
        
        # Load pre-analyzed photos from JSON file
        self.photo_database = self._load_photo_database()
        
        logger.info("📷 Agent 4C: Cultural Photo Description initialized")
        logger.info(f"📊 Loaded {len(self.photo_database)} pre-analyzed photos")
        if self.gemini_tool:
            logger.info("🤖 Gemini AI enabled for cultural enhancement AND dementia-friendly descriptions")
        else:
            logger.info("📝 Using pre-written conversation starters (fallback mode)")
    
    def _load_photo_database(self) -> List[Dict[str, Any]]:
        """Load photo analyses from the photo_analyses.json file - CORRECTLY FIXED"""
        
        try:
            # CORRECT: Look for photo_analyses.json (with 's')
            photo_file = Path(__file__).parent.parent.parent / "config" / "photo_analyses.json"
            
            if photo_file.exists():
                with open(photo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # CORRECT: Use photo_analyses key (array structure)
                    photos_list = data.get("photo_analyses", [])
                    logger.info(f"✅ Loaded {len(photos_list)} photos from {photo_file}")
                    return photos_list
            else:
                logger.warning(f"⚠️ Photo analysis file not found: {photo_file}")
                return self._get_fallback_photos()
                
        except Exception as e:
            logger.error(f"❌ Error loading photo database: {e}")
            return self._get_fallback_photos()
    
    def _get_fallback_photos(self) -> List[Dict[str, Any]]:
        """Provide emergency fallback photos if JSON loading fails - CORRECTLY FIXED"""
        
        return [
            {
                "image_name": "family.png",
                "theme": "family",
                "google_vision_description": "A warm family gathering with multiple generations sitting together",
                "conversation_starters": [
                    "Tell me about your family",
                    "What family traditions were special to you?",
                    "Do you remember family gatherings like this?"
                ],
                "emotional_tone": "warm, familial",
                "key_elements": ["family", "gathering", "togetherness"]
            },
            {
                "image_name": "birthday.png",
                "theme": "birthday",
                "google_vision_description": "Children celebrating a birthday party with cake and candles",
                "conversation_starters": [
                    "How did you celebrate birthdays when you were young?",
                    "What was your favorite birthday cake?",
                    "Do you remember blowing out birthday candles?"
                ],
                "emotional_tone": "joyful, celebratory",
                "key_elements": ["birthday", "cake", "celebration"]
            },
            {
                "image_name": "music.png",
                "theme": "music",
                "google_vision_description": "A young person playing piano with sheet music",
                "conversation_starters": [
                    "Did you play piano or another instrument?",
                    "What music did you enjoy when you were young?",
                    "Do you remember music lessons?"
                ],
                "emotional_tone": "joyful, musical, talented",
                "key_elements": ["piano", "young musician", "sheet music", "performance"]
            }
        ]
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select and culturally enhance a photo based on patient profile and theme.
        
        Args:
            enhanced_profile: Profile from previous agents containing patient_info, theme_info, qloo_intelligence
            
        Returns:
            Dict containing selected photo with culturally-enhanced conversation starters
            AND dementia-friendly description
        """
        
        logger.info("📷 Agent 4C: Starting culturally-aware photo description")
        
        try:
            # Extract patient and theme information
            patient_info = enhanced_profile.get("patient_info", {})
            theme_info = enhanced_profile.get("theme_info", {})
            qloo_intelligence = enhanced_profile.get("qloo_intelligence", {})
            
            heritage = patient_info.get("cultural_heritage", "American").lower()
            birth_year = patient_info.get("birth_year", 1945)
            patient_name = patient_info.get("first_name", "Friend")
            theme_id = theme_info.get("id", "family")
            theme_name = theme_info.get("name", "Family")
            
            logger.info(f"🎯 Selecting photo for {patient_name} (Heritage: {heritage}, Theme: {theme_name})")
            
            # Step 1: Find photo that matches today's theme - CORRECTLY FIXED
            selected_photo = self._find_photo_by_theme(theme_id)
            
            if not selected_photo:
                logger.warning(f"⚠️ No photo found for theme '{theme_id}', using fallback")
                # Use first available photo as fallback
                fallback_photos = self._get_fallback_photos()
                selected_photo = fallback_photos[0]
            
            photo_name = selected_photo.get("image_name", "unknown.png")
            logger.info(f"✅ Selected photo: {photo_name}")
            
            # Step 2: Enhance with cultural context AND generate dementia-friendly description
            enhanced_photo_data = await self._enhance_with_cultural_context(
                selected_photo, patient_info, theme_info, qloo_intelligence
            )
            
            # Step 3: Format final output
            return self._format_photo_output(enhanced_photo_data, heritage, theme_id)
            
        except Exception as e:
            logger.error(f"❌ Photo description failed: {e}")
            return await self._get_emergency_fallback(enhanced_profile)
    
    def _find_photo_by_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Find photo that matches the given theme - CORRECTLY FIXED for array structure"""
        
        # Search through photo array for theme matches
        for photo in self.photo_database:
            # Direct theme match
            if photo.get("theme", "").lower() == theme_id.lower():
                logger.debug(f"🔍 Direct theme match for '{theme_id}': {photo.get('image_name')}")
                return photo
            
            # Check image name for theme match
            image_name = photo.get("image_name", "")
            if theme_id.lower() in image_name.lower():
                logger.debug(f"🔍 Image name match for '{theme_id}': {image_name}")
                return photo
        
        logger.warning(f"⚠️ No photo found for theme '{theme_id}'")
        return None
    
    async def _enhance_with_cultural_context(self, photo_data: Dict[str, Any], patient_info: Dict[str, Any], 
                                           theme_info: Dict[str, Any], qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini AI to enhance photo conversation with cultural context AND generate dementia-friendly description"""
        
        heritage = patient_info.get("cultural_heritage", "American")
        patient_name = patient_info.get("first_name", "Friend")
        birth_year = patient_info.get("birth_year", 1945)
        
        # Get original conversation starters and description
        original_starters = photo_data.get("conversation_starters", [])
        original_description = photo_data.get("google_vision_description", "A meaningful photograph")
        
        # Process results
        enhanced_data = photo_data.copy()
        
        if not self.gemini_tool:
            logger.info("🤖 No Gemini tool available, using JSON fallback descriptions")
            # Use JSON fallback description
            enhanced_data["dementia_friendly_description"] = self._get_fallback_description(photo_data)
            enhanced_data["description_enhanced"] = False
            enhanced_data["cultural_enhancement"] = False
            return enhanced_data
        
        try:
            # Get Qloo artists for additional context
            qloo_artists = self._extract_qloo_artists(qloo_intelligence)
            
            # Step 1: Generate dementia-friendly photo description using Gemini
            logger.info("🤖 Generating dementia-friendly photo description...")
            dementia_friendly_description = await self.gemini_tool.generate_dementia_friendly_description(
                original_description, patient_name, heritage
            )
            
            # Step 2: Create culturally-aware prompt for conversation starters
            cultural_prompt = self._create_cultural_enhancement_prompt(
                heritage, original_description, original_starters, qloo_artists, birth_year
            )
            
            # Step 3: Get enhanced conversation starters from Gemini
            gemini_content = await self.gemini_tool.generate_content(cultural_prompt)
            
            # Use dementia-friendly description if generated successfully, otherwise use JSON fallback
            if dementia_friendly_description:
                enhanced_data["dementia_friendly_description"] = dementia_friendly_description
                enhanced_data["description_enhanced"] = True
                enhanced_data["description_source"] = "gemini_generated"
                logger.info("✅ Generated dementia-friendly description with Gemini")
            else:
                enhanced_data["dementia_friendly_description"] = self._get_fallback_description(photo_data)
                enhanced_data["description_enhanced"] = False
                enhanced_data["description_source"] = "json_fallback"
                logger.warning("⚠️ Using JSON fallback description")
            
            # Use enhanced conversation starters if available
            if gemini_content:
                enhanced_starters = self._parse_gemini_conversation_starters(gemini_content)
                
                if enhanced_starters:
                    enhanced_data["enhanced_conversation_starters"] = enhanced_starters
                    enhanced_data["cultural_enhancement"] = True
                    enhanced_data["enhancement_heritage"] = heritage
                    logger.info(f"🤖 ✅ Gemini enhanced conversation starters for {heritage} heritage")
                else:
                    enhanced_data["cultural_enhancement"] = False
                    logger.warning("⚠️ Could not parse Gemini conversation starters")
            else:
                enhanced_data["cultural_enhancement"] = False
                logger.warning("⚠️ Gemini conversation enhancement failed")
            
            return enhanced_data
            
        except Exception as e:
            logger.warning(f"⚠️ Cultural enhancement failed: {e}")
            # Use JSON fallback description when Gemini fails
            enhanced_data["dementia_friendly_description"] = self._get_fallback_description(photo_data)
            enhanced_data["description_enhanced"] = False
            enhanced_data["description_source"] = "json_fallback"
            enhanced_data["cultural_enhancement"] = False
            return enhanced_data
    
    def _get_fallback_description(self, photo_data: Dict[str, Any]) -> str:
        """Get dementia-friendly description from JSON data, with emergency fallback"""
        
        # First try: Use pre-written dementia-friendly description from JSON
        json_description = photo_data.get("dementia_friendly_description")
        if json_description:
            logger.info("📝 Using pre-written dementia-friendly description from JSON")
            return json_description
        
        # Second try: Use basic text simplification
        original_description = photo_data.get("google_vision_description", "A meaningful photograph")
        simplified = self._create_simple_fallback_description(original_description)
        logger.info("📝 Using basic text simplification fallback")
        return simplified
    
    def _create_simple_fallback_description(self, original_description: str) -> str:
        """Create a simple fallback description when Gemini and JSON fallbacks are not available"""
        
        # Basic simplification rules
        simple_words = {
            "photograph": "picture",
            "captures": "shows",
            "featuring": "with",
            "individual": "person",
            "composition": "picture",
            "backdrop": "background",
            "appears to be": "looks like",
            "demonstrates": "shows"
        }
        
        # Start with original and simplify
        simplified = original_description.lower()
        
        for complex_word, simple_word in simple_words.items():
            simplified = simplified.replace(complex_word, simple_word)
        
        # Make it warmer and shorter
        if "family" in simplified:
            return "Here's a lovely picture of a happy family together. Everyone looks so joyful and peaceful."
        elif "child" in simplified or "young" in simplified:
            return "This picture shows a happy child. It looks like such a wonderful, peaceful moment."
        elif "music" in simplified or "piano" in simplified:
            return "Here's a beautiful picture of someone making music. How lovely and peaceful it looks."
        else:
            return "This is a beautiful, peaceful picture that brings back happy memories."
    
    def _create_cultural_enhancement_prompt(self, heritage: str, visual_description: str, 
                                          original_starters: List[str], qloo_artists: List[str], 
                                          birth_year: int) -> str:
        """Create culturally-sensitive prompt for Gemini"""
        
        age_context = f"born in {birth_year}" if birth_year else "senior"
        
        prompt = f"""
        You are helping create conversation starters for a dementia care patient.
        
        Patient Background:
        - Heritage: {heritage}
        - Age context: {age_context}
        - Cultural artists they might know: {', '.join(qloo_artists[:3]) if qloo_artists else 'None available'}
        
        Photo Description: {visual_description}
        
        Original conversation starters: {', '.join(original_starters)}
        
        Please create 1-3 new conversation starters that:
        1. Are culturally sensitive to {heritage} heritage
        2. Are appropriate for someone with dementia (simple, positive, memory-focused)
        3. Connect to the photo content
        4. Avoid complex questions or negative themes
        5. Use warm, friendly language
        
        Format as a simple list, one starter per line.
        """
        
        return prompt
    
    def _parse_gemini_conversation_starters(self, gemini_content: str) -> List[str]:
        """Parse conversation starters from Gemini response"""
        
        try:
            lines = gemini_content.strip().split('\n')
            starters = []
            
            for line in lines:
                # Clean up the line
                cleaned = line.strip()
                # Remove bullet points, numbers, etc.
                cleaned = cleaned.lstrip('•-*1234567890. ')
                
                if cleaned and len(cleaned) > 10:  # Valid starter
                    # Ensure it ends with appropriate punctuation
                    if not cleaned.endswith(('?', '.', '!')):
                        cleaned += '?'
                    starters.append(cleaned)
            
            return starters[:3]  # Limit to 3 starters
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse Gemini starters: {e}")
            return []
    
    def _extract_qloo_artists(self, qloo_intelligence: Dict[str, Any]) -> List[str]:
        """Extract artist names from Qloo intelligence for context"""
        
        try:
            artists_data = qloo_intelligence.get("qloo_results", {})
            
            if artists_data.get("success"):
                entities = artists_data.get("entities", [])
                artist_names = [entity.get("name", "") for entity in entities if entity.get("name")]
                return artist_names[:3]  # Limit to 3 artists
                
        except Exception as e:
            logger.debug(f"Could not extract Qloo artists: {e}")
        
        return []
    
    def _format_photo_output(self, photo_data: Dict[str, Any], heritage: str, theme_id: str) -> Dict[str, Any]:
        """Format the final photo output for the dashboard with dementia-friendly description"""
        
        # Use enhanced starters if available, otherwise use original
        conversation_starters = photo_data.get("enhanced_conversation_starters", 
                                              photo_data.get("conversation_starters", []))
        is_enhanced = photo_data.get("cultural_enhancement", False)
        
        # Use dementia-friendly description if available, otherwise use original
        description = photo_data.get("dementia_friendly_description",
                                   photo_data.get("google_vision_description", "A meaningful photograph"))
        is_description_enhanced = photo_data.get("description_enhanced", False)
        description_source = photo_data.get("description_source", "unknown")
        
        return {
            "photo_content": {
                "image_name": photo_data.get("image_name", "unknown.png"),
                "theme": photo_data.get("theme", theme_id),
                "description": description,  # NOW USES DEMENTIA-FRIENDLY DESCRIPTION
                "conversation_starters": conversation_starters[:3],  # Limit to 3 starters
                "emotional_tone": photo_data.get("emotional_tone", "warm, meaningful"),
                "key_elements": photo_data.get("key_elements", []),
                "heritage_connection": f"Enhanced for {heritage} heritage" if is_enhanced else "General photo description",
                "theme_connection": f"Selected for {theme_id} theme"
            },
            "metadata": {
                "agent": "4C_photo_description",
                "selection_method": "gemini_enhanced" if is_enhanced else "theme_based_fallback",
                "theme_match": True,
                "cultural_enhancement": is_enhanced,
                "description_simplified": is_description_enhanced,
                "description_source": description_source,
                "heritage_target": heritage,
                "safety_level": "positive_memories",
                "dementia_friendly": True
            }
        }
    
    async def _get_emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback when everything else fails"""
        
        logger.warning("⚠️ Using emergency fallback for photo description")
        
        patient_info = enhanced_profile.get("patient_info", {})
        theme_info = enhanced_profile.get("theme_info", {})
        heritage = patient_info.get("cultural_heritage", "American")
        theme_id = theme_info.get("id", "family")
        
        fallback_photo_data = {
            "image_name": "family.png",
            "theme": theme_id,
            "google_vision_description": "A warm, meaningful photograph",
            "dementia_friendly_description": "Here's a lovely family enjoying time together outdoors! A little girl with curly hair is having her picture taken on a beautiful grassy hill. Someone is taking her photo while a man sits nearby watching with a smile. The golden grass and green trees make such a peaceful, happy scene. What a wonderful family moment!",
            "conversation_starters": [
                "This picture brings back memories",
                "Tell me what you see here",
                "What does this remind you of?"
            ],
            "emotional_tone": "warm, comforting",
            "key_elements": ["memories", "meaningful moments"],
            "description_enhanced": False,
            "description_source": "emergency_fallback",
            "cultural_enhancement": False
        }
        
        return self._format_photo_output(fallback_photo_data, heritage, theme_id)