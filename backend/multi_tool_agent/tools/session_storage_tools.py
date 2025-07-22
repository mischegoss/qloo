"""
Session Storage Tools
File: backend/multi_tool_agent/tools/session_storage_tools.py

Provides in-memory session storage for user preferences and feedback learning
"""

import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class UserPreference:
    """User preference data structure."""
    preference_id: str
    category: str
    item_name: str
    preference_type: str  # "positive", "negative", "blocked"
    timestamp: str
    context: Dict[str, Any]
    feedback_source: str  # "emoji_feedback", "manual_block", "caregiver_input"

@dataclass
class SessionData:
    """Session data structure."""
    session_id: str
    patient_id: str
    created_timestamp: str
    last_updated: str
    preferences: List[UserPreference]
    blocked_content: Dict[str, List[str]]
    positive_patterns: Dict[str, List[str]]
    session_metadata: Dict[str, Any]

class SessionStorageManager:
    """
    Session storage manager for user preferences and feedback learning.
    Used by Agent 7: Feedback Learning System Agent
    """
    
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
        self.session_timeout = timedelta(hours=24)  # Sessions expire after 24 hours
        
    async def create_session(self, patient_id: str, session_id: Optional[str] = None) -> str:
        """
        Create a new session for a patient.
        
        Args:
            patient_id: Patient identifier
            session_id: Optional session ID (auto-generated if not provided)
            
        Returns:
            Session ID
        """
        
        if not session_id:
            session_id = f"session_{patient_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        session_data = SessionData(
            session_id=session_id,
            patient_id=patient_id,
            created_timestamp=datetime.utcnow().isoformat(),
            last_updated=datetime.utcnow().isoformat(),
            preferences=[],
            blocked_content={
                "categories": [],
                "types": [],
                "specific_items": []
            },
            positive_patterns={
                "music_genres": [],
                "food_types": [],
                "conversation_topics": [],
                "video_content": [],
                "cultural_connections": []
            },
            session_metadata={
                "total_interactions": 0,
                "positive_feedback_count": 0,
                "negative_feedback_count": 0,
                "blocked_items_count": 0
            }
        )
        
        self.sessions[session_id] = session_data
        logger.info(f"Created new session: {session_id} for patient: {patient_id}")
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Retrieve session data.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found
        """
        
        if session_id not in self.sessions:
            logger.warning(f"Session not found: {session_id}")
            return None
        
        session = self.sessions[session_id]
        
        # Check if session has expired
        created_time = datetime.fromisoformat(session.created_timestamp)
        if datetime.utcnow() - created_time > self.session_timeout:
            logger.info(f"Session expired: {session_id}")
            del self.sessions[session_id]
            return None
        
        return session
    
    async def update_session(self, session_id: str, session_data: SessionData) -> bool:
        """
        Update session data.
        
        Args:
            session_id: Session identifier
            session_data: Updated session data
            
        Returns:
            True if successful, False otherwise
        """
        
        try:
            session_data.last_updated = datetime.utcnow().isoformat()
            self.sessions[session_id] = session_data
            logger.info(f"Updated session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {str(e)}")
            return False
    
    async def add_preference(self, 
                           session_id: str, 
                           category: str,
                           item_name: str,
                           preference_type: str,
                           context: Dict[str, Any],
                           feedback_source: str = "emoji_feedback") -> bool:
        """
        Add a user preference to the session.
        
        Args:
            session_id: Session identifier
            category: Preference category (music, food, conversation, etc.)
            item_name: Name of the item/content
            preference_type: "positive", "negative", or "blocked"
            context: Additional context about the preference
            feedback_source: Source of the feedback
            
        Returns:
            True if successful, False otherwise
        """
        
        try:
            session = await self.get_session(session_id)
            if not session:
                return False
            
            preference = UserPreference(
                preference_id=f"pref_{len(session.preferences)}_{datetime.utcnow().strftime('%H%M%S')}",
                category=category,
                item_name=item_name,
                preference_type=preference_type,
                timestamp=datetime.utcnow().isoformat(),
                context=context,
                feedback_source=feedback_source
            )
            
            session.preferences.append(preference)
            
            # Update session metadata
            session.session_metadata["total_interactions"] += 1
            if preference_type == "positive":
                session.session_metadata["positive_feedback_count"] += 1
            elif preference_type == "negative":
                session.session_metadata["negative_feedback_count"] += 1
            elif preference_type == "blocked":
                session.session_metadata["blocked_items_count"] += 1
            
            await self.update_session(session_id, session)
            logger.info(f"Added preference: {preference_type} for {item_name} in {category}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding preference: {str(e)}")
            return False
    
    async def add_blocked_content(self, 
                                session_id: str,
                                block_type: str,
                                content_identifier: str,
                                context: Dict[str, Any]) -> bool:
        """
        Add blocked content to the session.
        
        Args:
            session_id: Session identifier
            block_type: "category", "type", or "specific_item"
            content_identifier: The content to block
            context: Context about why it was blocked
            
        Returns:
            True if successful, False otherwise
        """
        
        try:
            session = await self.get_session(session_id)
            if not session:
                return False
            
            # Add to appropriate blocked content list
            if block_type == "category":
                if content_identifier not in session.blocked_content["categories"]:
                    session.blocked_content["categories"].append(content_identifier)
            elif block_type == "type":
                if content_identifier not in session.blocked_content["types"]:
                    session.blocked_content["types"].append(content_identifier)
            elif block_type == "specific_item":
                if content_identifier not in session.blocked_content["specific_items"]:
                    session.blocked_content["specific_items"].append(content_identifier)
            
            # Also add as a blocked preference
            await self.add_preference(
                session_id,
                context.get("category", "general"),
                content_identifier,
                "blocked",
                context,
                "manual_block"
            )
            
            logger.info(f"Blocked {block_type}: {content_identifier}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding blocked content: {str(e)}")
            return False
    
    async def get_blocked_content(self, session_id: str) -> Dict[str, List[str]]:
        """
        Get all blocked content for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary of blocked content by type
        """
        
        session = await self.get_session(session_id)
        if not session:
            return {"categories": [], "types": [], "specific_items": []}
        
        return session.blocked_content
    
    async def get_positive_patterns(self, session_id: str) -> Dict[str, List[str]]:
        """
        Get positive patterns learned from feedback.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary of positive patterns by category
        """
        
        session = await self.get_session(session_id)
        if not session:
            return {"music_genres": [], "food_types": [], "conversation_topics": [], "video_content": [], "cultural_connections": []}
        
        # Extract positive patterns from preferences
        patterns = defaultdict(list)
        
        for pref in session.preferences:
            if pref.preference_type == "positive":
                category_key = f"{pref.category}_preferences"
                if pref.item_name not in patterns[category_key]:
                    patterns[category_key].append(pref.item_name)
        
        return dict(patterns)
    
    async def is_content_blocked(self, 
                               session_id: str,
                               content_name: str,
                               content_category: str,
                               content_type: str) -> bool:
        """
        Check if content is blocked for this session.
        
        Args:
            session_id: Session identifier
            content_name: Name of the content
            content_category: Category of the content
            content_type: Type of the content
            
        Returns:
            True if content is blocked, False otherwise
        """
        
        blocked_content = await self.get_blocked_content(session_id)
        
        # Check specific items
        if content_name.lower() in [item.lower() for item in blocked_content["specific_items"]]:
            return True
        
        # Check categories
        if content_category.lower() in [cat.lower() for cat in blocked_content["categories"]]:
            return True
        
        # Check types
        if content_type.lower() in [typ.lower() for typ in blocked_content["types"]]:
            return True
        
        return False
    
    async def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a summary of the session for analytics.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary or None if session not found
        """
        
        session = await self.get_session(session_id)
        if not session:
            return None
        
        # Calculate preference distributions
        preference_counts = defaultdict(int)
        category_counts = defaultdict(int)
        
        for pref in session.preferences:
            preference_counts[pref.preference_type] += 1
            category_counts[pref.category] += 1
        
        return {
            "session_id": session.session_id,
            "patient_id": session.patient_id,
            "session_duration": str(datetime.utcnow() - datetime.fromisoformat(session.created_timestamp)),
            "total_preferences": len(session.preferences),
            "preference_breakdown": dict(preference_counts),
            "category_breakdown": dict(category_counts),
            "blocked_content_counts": {
                "categories": len(session.blocked_content["categories"]),
                "types": len(session.blocked_content["types"]),
                "specific_items": len(session.blocked_content["specific_items"])
            },
            "session_metadata": session.session_metadata
        }
    
    async def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions from memory.
        
        Returns:
            Number of sessions cleaned up
        """
        
        expired_sessions = []
        current_time = datetime.utcnow()
        
        for session_id, session in self.sessions.items():
            created_time = datetime.fromisoformat(session.created_timestamp)
            if current_time - created_time > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    async def export_session_data(self, session_id: str) -> Optional[str]:
        """
        Export session data as JSON string.
        
        Args:
            session_id: Session identifier
            
        Returns:
            JSON string of session data or None if session not found
        """
        
        session = await self.get_session(session_id)
        if not session:
            return None
        
        try:
            # Convert session data to dictionary
            session_dict = asdict(session)
            return json.dumps(session_dict, indent=2)
        except Exception as e:
            logger.error(f"Error exporting session data: {str(e)}")
            return None
    
    async def import_session_data(self, session_data_json: str) -> Optional[str]:
        """
        Import session data from JSON string.
        
        Args:
            session_data_json: JSON string containing session data
            
        Returns:
            Session ID if successful, None otherwise
        """
        
        try:
            session_dict = json.loads(session_data_json)
            
            # Convert preferences back to UserPreference objects
            preferences = [
                UserPreference(**pref) for pref in session_dict["preferences"]
            ]
            
            session_data = SessionData(
                session_id=session_dict["session_id"],
                patient_id=session_dict["patient_id"],
                created_timestamp=session_dict["created_timestamp"],
                last_updated=session_dict["last_updated"],
                preferences=preferences,
                blocked_content=session_dict["blocked_content"],
                positive_patterns=session_dict["positive_patterns"],
                session_metadata=session_dict["session_metadata"]
            )
            
            self.sessions[session_data.session_id] = session_data
            logger.info(f"Imported session data: {session_data.session_id}")
            
            return session_data.session_id
            
        except Exception as e:
            logger.error(f"Error importing session data: {str(e)}")
            return None
    
    def get_active_session_count(self) -> int:
        """Get the number of active sessions."""
        return len(self.sessions)
    
    def get_all_session_ids(self) -> List[str]:
        """Get all active session IDs."""
        return list(self.sessions.keys())