"""
Step 1: Simple Feedback Handler
File: backend/utils/feedback_handler.py

SIMPLE FEEDBACK MECHANISM:
- Handle likes and dislikes from UI
- Track content preferences
- Provide simple insights for personalization
- Clean data structure for pipeline
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SimpleFeedbackHandler:
    """
    Step 1: Simple Feedback Handler for Pipeline
    
    PURPOSE:
    - Process likes/dislikes from UI
    - Track content type preferences
    - Provide simple personalization insights
    - Clean feedback data for pipeline
    """
    
    def __init__(self):
        logger.info("✅ Simple Feedback Handler initialized")
    
    def process_feedback(self, feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process feedback data into clean structure
        
        Args:
            feedback_data: Raw feedback from UI/session
            
        Returns:
            Clean feedback summary for pipeline
        """
        
        if not feedback_data:
            return self._create_empty_feedback()
        
        try:
            # Extract likes and dislikes
            likes = self._extract_likes(feedback_data)
            dislikes = self._extract_dislikes(feedback_data)
            
            # Generate insights
            insights = self._generate_insights(likes, dislikes)
            
            feedback_summary = {
                "likes": likes,
                "dislikes": dislikes,
                "insights": insights,
                "metadata": {
                    "total_feedback": len(likes) + len(dislikes),
                    "feedback_available": len(likes) + len(dislikes) > 0,
                    "processed_at": datetime.now().isoformat()
                }
            }
            
            logger.info(f"🔄 Feedback processed: {len(likes)} likes, {len(dislikes)} dislikes")
            return feedback_summary
            
        except Exception as e:
            logger.error(f"❌ Feedback processing failed: {e}")
            return self._create_empty_feedback()
    
    def _extract_likes(self, feedback_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and validate likes"""
        
        likes = feedback_data.get("likes", [])
        
        # Ensure it's a list
        if not isinstance(likes, list):
            likes = []
        
        # Clean and validate each like
        clean_likes = []
        for like in likes:
            if isinstance(like, dict):
                clean_like = {
                    "type": like.get("type", "unknown"),
                    "name": like.get("name", "Unknown Content"),
                    "timestamp": like.get("timestamp", datetime.now().isoformat()),
                    "session_id": like.get("session_id", "unknown")
                }
                clean_likes.append(clean_like)
            elif isinstance(like, str):
                # Handle simple string likes
                clean_like = {
                    "type": "content",
                    "name": like,
                    "timestamp": datetime.now().isoformat(),
                    "session_id": "current"
                }
                clean_likes.append(clean_like)
        
        return clean_likes
    
    def _extract_dislikes(self, feedback_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and validate dislikes"""
        
        dislikes = feedback_data.get("dislikes", [])
        
        # Ensure it's a list
        if not isinstance(dislikes, list):
            dislikes = []
        
        # Clean and validate each dislike
        clean_dislikes = []
        for dislike in dislikes:
            if isinstance(dislike, dict):
                clean_dislike = {
                    "type": dislike.get("type", "unknown"),
                    "name": dislike.get("name", "Unknown Content"),
                    "timestamp": dislike.get("timestamp", datetime.now().isoformat()),
                    "session_id": dislike.get("session_id", "unknown"),
                    "reason": dislike.get("reason", "not_specified")
                }
                clean_dislikes.append(clean_dislike)
            elif isinstance(dislike, str):
                # Handle simple string dislikes
                clean_dislike = {
                    "type": "content",
                    "name": dislike,
                    "timestamp": datetime.now().isoformat(),
                    "session_id": "current",
                    "reason": "not_specified"
                }
                clean_dislikes.append(clean_dislike)
        
        return clean_dislikes
    
    def _generate_insights(self, likes: List[Dict[str, Any]], 
                          dislikes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate simple insights from feedback"""
        
        # Count preferences by type
        liked_types = {}
        disliked_types = {}
        
        for like in likes:
            content_type = like.get("type", "unknown")
            liked_types[content_type] = liked_types.get(content_type, 0) + 1
        
        for dislike in dislikes:
            content_type = dislike.get("type", "unknown")
            disliked_types[content_type] = disliked_types.get(content_type, 0) + 1
        
        # Determine preferred and avoided types
        preferred_types = sorted(liked_types.items(), key=lambda x: x[1], reverse=True)
        avoided_types = sorted(disliked_types.items(), key=lambda x: x[1], reverse=True)
        
        insights = {
            "preferred_types": [t[0] for t in preferred_types[:3]],  # Top 3
            "avoided_types": [t[0] for t in avoided_types[:3]],      # Top 3
            "type_counts": {
                "likes": liked_types,
                "dislikes": disliked_types
            },
            "engagement_level": self._calculate_engagement_level(likes, dislikes),
            "personalization_ready": len(likes) + len(dislikes) >= 3
        }
        
        return insights
    
    def _calculate_engagement_level(self, likes: List[Dict[str, Any]], 
                                   dislikes: List[Dict[str, Any]]) -> str:
        """Calculate user engagement level"""
        
        total_feedback = len(likes) + len(dislikes)
        
        if total_feedback == 0:
            return "new_user"
        elif total_feedback <= 2:
            return "exploring"
        elif total_feedback <= 5:
            return "engaged"
        else:
            return "highly_engaged"
    
    def _create_empty_feedback(self) -> Dict[str, Any]:
        """Create empty feedback structure"""
        
        return {
            "likes": [],
            "dislikes": [],
            "insights": {
                "preferred_types": [],
                "avoided_types": [],
                "type_counts": {"likes": {}, "dislikes": {}},
                "engagement_level": "new_user",
                "personalization_ready": False
            },
            "metadata": {
                "total_feedback": 0,
                "feedback_available": False,
                "processed_at": datetime.now().isoformat()
            }
        }
    
    def add_like(self, content_type: str, content_name: str, 
                 session_id: str = "current") -> Dict[str, Any]:
        """
        Add a new like (for real-time feedback)
        
        Args:
            content_type: Type of content (music, recipe, photo, etc.)
            content_name: Name of the content
            session_id: Current session ID
            
        Returns:
            Like record
        """
        
        like_record = {
            "type": content_type,
            "name": content_name,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
        
        logger.info(f"👍 Like added: {content_type} - {content_name}")
        return like_record
    
    def add_dislike(self, content_type: str, content_name: str, 
                    reason: str = "not_specified", 
                    session_id: str = "current") -> Dict[str, Any]:
        """
        Add a new dislike (for real-time feedback)
        
        Args:
            content_type: Type of content
            content_name: Name of the content
            reason: Reason for dislike
            session_id: Current session ID
            
        Returns:
            Dislike record
        """
        
        dislike_record = {
            "type": content_type,
            "name": content_name,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "reason": reason
        }
        
        logger.info(f"👎 Dislike added: {content_type} - {content_name} (reason: {reason})")
        return dislike_record
    
    def should_avoid_content_type(self, content_type: str, 
                                  feedback_summary: Dict[str, Any]) -> bool:
        """
        Check if a content type should be avoided based on feedback
        
        Args:
            content_type: Type to check
            feedback_summary: Processed feedback summary
            
        Returns:
            True if content type should be avoided
        """
        
        insights = feedback_summary.get("insights", {})
        avoided_types = insights.get("avoided_types", [])
        
        return content_type in avoided_types
    
    def get_preferred_content_types(self, feedback_summary: Dict[str, Any]) -> List[str]:
        """Get list of preferred content types"""
        
        insights = feedback_summary.get("insights", {})
        return insights.get("preferred_types", [])

# Global instance for easy import
simple_feedback_handler = SimpleFeedbackHandler()

# Export
__all__ = ["SimpleFeedbackHandler", "simple_feedback_handler"]