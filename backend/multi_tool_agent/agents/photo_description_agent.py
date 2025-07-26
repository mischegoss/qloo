"""
Agent 4C: Cultural Photo Description Agent
File: backend/multi_tool_agent/agents/photo_description_agent.py

APPROACH:
- Loads pre-analyzed photos from photo_analysis.json
- Maps today's theme to appropriate photo
- Uses Qloo cultural profile to enhance photo interactions
- Uses Gemini AI to create culturally-relevant conversation starters
- Comprehensive fallbacks ensure it always works
- Perfect for dementia patients: culturally sensitive, gentle questions
"""

import logging
import json
import random
from typing import Dict, Any, List, Optional
from pathlib import Path

# Configure logger
logger = logging.getLogger(__name__)

# Import Gemini tool with proper fallback handling
try:
    # Try importing through the fixed __init__.py
    from ..tools import SimpleGeminiTool
    logger.debug("✅ Imported SimpleGeminiTool via __init__.py")
except ImportError as e1:
    # Fallback to direct imports
    try:
        from ..tools.simple_gemini_tools import SimpleGeminiTool
        logger.debug("✅ Imported SimpleGeminiTool directly")
    except ImportError as e2:
        # Try absolute imports (for when running tests)
        try:
            from multi_tool_agent.tools.simple_gemini_tools import SimpleGeminiTool
            logger.debug("✅ Imported SimpleGeminiTool via absolute imports")
        except ImportError as e3:
            # Final fallback - no Gemini available
            SimpleGeminiTool = None
            logger.warning(f"⚠️ Could not import SimpleGeminiTool: {e1}, {e2}, {e3} - running in fallback mode")

class PhotoDescriptionAgent:
    """
    Agent 4C: Cultural Photo Description with Gemini enhancement.
    
    Takes today's theme and patient cultural profile, selects appropriate photo
    and uses Gemini AI to create culturally-relevant conversation starters.
    """
    
    def __init__(self, gemini_tool=None):
        self.gemini_tool = gemini_tool
        
        # Load pre-analyzed photos from JSON file
        self.photo_database = self._load_photo_database()
        
        logger.info("📷 Agent 4C: Cultural Photo Description initialized")
        logger.info(f"📊 Loaded {len(self.photo_database)} pre-analyzed photos")
        if self.gemini_tool:
            logger.info("🤖 Gemini AI enabled for cultural enhancement")
        else:
            logger.info("📝 Using pre-written conversation starters (fallback mode)")
    
    def _load_photo_database(self) -> List[Dict[str, Any]]:
        """Load photo analyses from the photo_analysis.json file"""
        
        try:
            # Find the photo_analysis.json file (relative to this file)
            photo_file = Path(__file__).parent.parent.parent / "config" / "photo_analysis.json"
            
            if photo_file.exists():
                with open(photo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    photos = data.get("photo_analyses", [])
                    logger.info(f"✅ Loaded {len(photos)} photos from {photo_file}")
                    return photos
            else:
                logger.warning(f"⚠️ Photo analysis file not found: {photo_file}")
                return self._get_fallback_photos()
                
        except Exception as e:
            logger.error(f"❌ Error loading photo database: {e}")
            return self._get_fallback_photos()
    
    def _get_fallback_photos(self) -> List[Dict[str, Any]]:
        """Provide emergency fallback photos if JSON loading fails"""
        
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
            }
        ]
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select and culturally enhance a photo based on patient profile and theme.
        
        Args:
            enhanced_profile: Profile from previous agents containing patient_info, theme_info, qloo_intelligence
            
        Returns:
            Dict containing selected photo with culturally-enhanced conversation starters
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
            
            # Step 1: Find photo that matches today's theme
            selected_photo = self._find_photo_by_theme(theme_id)
            
            if not selected_photo:
                logger.warning(f"⚠️ No photo found for theme '{theme_id}', using fallback")
                selected_photo = self._get_fallback_photos()[0]
            
            photo_name = selected_photo.get("image_name", "unknown.png")
            logger.info(f"✅ Selected photo: {photo_name}")
            
            # Step 2: Enhance with cultural context using Gemini if available
            enhanced_photo = await self._enhance_with_cultural_context(
                selected_photo, patient_info, theme_info, qloo_intelligence
            )
            
            # Step 3: Format final output
            return self._format_photo_output(enhanced_photo, heritage, theme_id)
            
        except Exception as e:
            logger.error(f"❌ Photo description failed: {e}")
            return await self._get_emergency_fallback(enhanced_profile)
    
    def _find_photo_by_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Find photo that matches the given theme"""
        
        for photo in self.photo_database:
            if photo.get("theme", "").lower() == theme_id.lower():
                logger.debug(f"🔍 Found photo for theme '{theme_id}': {photo.get('image_name')}")
                return photo
        
        logger.warning(f"⚠️ No photo found for theme '{theme_id}'")
        return None
    
    async def _enhance_with_cultural_context(self, photo: Dict[str, Any], patient_info: Dict[str, Any], 
                                           theme_info: Dict[str, Any], qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini AI to enhance photo conversation with cultural context"""
        
        if not self.gemini_tool:
            logger.info("🤖 No Gemini tool available, using original conversation starters")
            return photo
        
        try:
            # Extract cultural context from patient info and Qloo data
            patient_name = patient_info.get("first_name", "Friend")
            heritage = patient_info.get("cultural_heritage", "American")
            birth_year = patient_info.get("birth_year", 1945)
            current_age = 2024 - birth_year
            theme_name = theme_info.get("name", "Memory")
            
            # Get photo details
            photo_description = photo.get("google_vision_description", "A meaningful photo")
            original_starters = photo.get("conversation_starters", [])
            photo_theme = photo.get("theme", "general")
            
            # Extract any relevant Qloo cultural insights
            qloo_artists = self._extract_qloo_artists(qloo_intelligence)
            cultural_context = f"Heritage: {heritage}, interested in {', '.join(qloo_artists[:2]) if qloo_artists else 'classical music'}"
            
            # Create Gemini prompt for cultural enhancement
            gemini_prompt = f"""
            Photo Description: {photo_description}
            
            Patient Context:
            - Name: {patient_name}
            - Heritage: {heritage}
            - Born: {birth_year} (age {current_age})
            - Cultural interests: {cultural_context}
            - Today's theme: {theme_name}
            
            Original conversation starters:
            {chr(10).join(f"- {starter}" for starter in original_starters)}
            
            Create 3 culturally-enhanced conversation starters that:
            1. Connect this photo to their {heritage} heritage and cultural background
            2. Reference experiences someone born in {birth_year} might have had
            3. Stay gentle, positive, and appropriate for dementia care
            4. Feel personally relevant and culturally meaningful
            5. Use simple, warm language
            
            Make each question specific to their cultural background while staying connected to what's shown in the photo.
            
            Format as a simple list of 3 questions, one per line, without bullet points.
            """
            
            enhanced_starters = await self.gemini_tool.generate_content(gemini_prompt, max_tokens=300)
            
            if enhanced_starters and enhanced_starters.strip():
                # Parse Gemini response into list
                starter_lines = [line.strip() for line in enhanced_starters.split('\n') if line.strip()]
                if len(starter_lines) >= 3:
                    # Create enhanced photo copy
                    enhanced_photo = photo.copy()
                    enhanced_photo["enhanced_conversation_starters"] = starter_lines[:3]
                    enhanced_photo["cultural_enhancement"] = True
                    enhanced_photo["heritage_context"] = heritage
                    logger.info(f"🤖 ✅ Gemini enhanced photo for {heritage} heritage")
                    return enhanced_photo
                else:
                    logger.info("🤖 ⚠️ Gemini response too short, using original starters")
            else:
                logger.info("🤖 ⚠️ Gemini returned empty response, using original starters")
                
        except Exception as e:
            logger.warning(f"🤖 ⚠️ Gemini enhancement failed: {e}, using original starters")
        
        # Return original photo if enhancement fails
        return photo
    
    def _extract_qloo_artists(self, qloo_intelligence: Dict[str, Any]) -> List[str]:
        """Extract artist names from Qloo intelligence for cultural context"""
        
        try:
            cultural_recs = qloo_intelligence.get("cultural_recommendations", {})
            artists_data = cultural_recs.get("artists", {})
            
            if artists_data.get("success"):
                entities = artists_data.get("entities", [])
                artist_names = [entity.get("name", "") for entity in entities if entity.get("name")]
                return artist_names[:3]  # Limit to 3 artists
                
        except Exception as e:
            logger.debug(f"Could not extract Qloo artists: {e}")
        
        return []
    
    def _format_photo_output(self, photo: Dict[str, Any], heritage: str, theme_id: str) -> Dict[str, Any]:
        """Format the final photo output for the dashboard"""
        
        # Use enhanced starters if available, otherwise use original
        conversation_starters = photo.get("enhanced_conversation_starters", photo.get("conversation_starters", []))
        is_enhanced = photo.get("cultural_enhancement", False)
        
        return {
            "photo_content": {
                "image_name": photo.get("image_name", "unknown.png"),
                "theme": photo.get("theme", theme_id),
                "description": photo.get("google_vision_description", "A meaningful photograph"),
                "conversation_starters": conversation_starters[:3],  # Limit to 3 starters
                "emotional_tone": photo.get("emotional_tone", "warm, meaningful"),
                "key_elements": photo.get("key_elements", []),
                "heritage_connection": f"Enhanced for {heritage} heritage" if is_enhanced else "General photo description",
                "theme_connection": f"Selected for {theme_id} theme",
                "cultural_connection_summary": photo.get("cultural_connection_summary", ""),
                "generation_context": photo.get("generation_context", "")
            },
            "metadata": {
                "theme_match": True,
                "cultural_enhancement": is_enhanced,
                "heritage_context": photo.get("heritage_context", heritage),
                "selection_method": "theme_based_with_cultural_enhancement" if self.gemini_tool else "theme_based_fallback",
                "conversation_source": "gemini_enhanced" if is_enhanced else "pre_written",
                "agent": "photo_description_agent_4c",
                "analysis_source": "google_vision_pre_analyzed",
                "total_photos_available": len(self.photo_database),
                "enhancement_quality": "structured_cultural_context" if is_enhanced else "original_content"
            }
        }
    
    async def _get_emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback if everything fails"""
        
        logger.warning("🚨 Using emergency photo fallback")
        
        patient_info = enhanced_profile.get("patient_info", {})
        heritage = patient_info.get("cultural_heritage", "American")
        
        emergency_photo = {
            "image_name": "family.png",
            "theme": "family",
            "description": "A warm family gathering bringing people together",
            "conversation_starters": [
                "Tell me about your family",
                "What memories make you smile?",
                "Do you remember gatherings with loved ones?"
            ]
        }
        
        return {
            "photo_content": {
                "image_name": emergency_photo["image_name"],
                "theme": emergency_photo["theme"],
                "description": emergency_photo["description"],
                "conversation_starters": emergency_photo["conversation_starters"],
                "emotional_tone": "warm, comforting",
                "key_elements": ["family", "togetherness"],
                "heritage_connection": "Universal family themes",
                "theme_connection": "Always appropriate"
            },
            "metadata": {
                "theme_match": False,
                "cultural_enhancement": False,
                "heritage_context": heritage,
                "selection_method": "emergency_fallback",
                "conversation_source": "emergency_fallback",
                "agent": "photo_description_agent_4c",
                "analysis_source": "emergency_fallback",
                "total_photos_available": 0
            }
        }

# Simple test function for development
async def test_photo_agent():
    """Test the photo description agent with sample data"""
    
    logger.info("🧪 Testing Photo Description Agent...")
    
    # Mock enhanced profile from previous agents
    mock_profile = {
        "patient_info": {
            "first_name": "Maria",
            "cultural_heritage": "Italian-American",
            "birth_year": 1945
        },
        "theme_info": {
            "id": "birthday",
            "name": "Birthday",
            "description": "Celebrating special occasions and joyful milestones"
        },
        "qloo_intelligence": {
            "cultural_recommendations": {
                "artists": {
                    "success": True,
                    "entities": [
                        {"name": "Vivaldi"},
                        {"name": "Puccini"}
                    ]
                }
            }
        }
    }
    
    # Test with no Gemini tool (pure fallback)
    logger.info("🧪 Testing without Gemini tool...")
    agent_fallback = PhotoDescriptionAgent()
    result_fallback = await agent_fallback.run(mock_profile)
    
    print(f"✅ Result: {result['photo_content']['image_name']}")
    print(f"   Cultural Enhancement: {result['metadata']['cultural_enhancement']}")
    print(f"   Conversation Source: {result['metadata']['conversation_source']}")
    print(f"   Enhancement Quality: {result['metadata']['enhancement_quality']}")
    print(f"   Conversation Starters: {result['photo_content']['conversation_starters'][:2]}")
    
    # Test with Gemini tool (in real usage, you'd initialize with API key)
    # gemini_tool = SimpleGeminiTool("YOUR_GEMINI_API_KEY") 
    # agent_with_gemini = PhotoDescriptionAgent(gemini_tool)
    # result_with_gemini = await agent_with_gemini.run(mock_profile)
    # 
    # print(f"✅ Enhanced Result: {result_with_gemini['photo_content']['cultural_connection_summary']}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_photo_agent())