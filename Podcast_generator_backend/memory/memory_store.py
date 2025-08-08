"""
Simple in-memory memory store for podcast generation history.
"""

import time
from typing import Dict, List, Optional
from collections import OrderedDict
from models.request_models import MemoryEntry, Tone, Voice


class MemoryStore:
    """Simple in-memory store with TTL and capacity management."""
    
    def __init__(self, max_entries: int = 100, ttl_hours: int = 24):
        """
        Initialize the memory store.
        
        Args:
            max_entries: Maximum number of entries to store
            ttl_hours: Time to live for entries in hours
        """
        self.max_entries = max_entries
        self.ttl_seconds = ttl_hours * 3600
        self._store: OrderedDict[str, MemoryEntry] = OrderedDict()
    
    def add_entry(self, entry: MemoryEntry) -> None:
        """
        Add a new memory entry.
        
        Args:
            entry: The memory entry to add
        """
        # Clean expired entries first
        self._cleanup_expired()
        
        # Create a unique key for the entry
        key = f"{entry.topic}_{entry.tone}_{entry.voice}_{entry.timestamp}"
        
        # Add to store
        self._store[key] = entry
        
        # Remove oldest entry if we exceed max_entries
        if len(self._store) > self.max_entries:
            self._store.popitem(last=False)
    
    def get_recent_entries(self, limit: int = 10) -> List[MemoryEntry]:
        """
        Get recent memory entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of recent memory entries
        """
        self._cleanup_expired()
        return list(self._store.values())[-limit:]
    
    def get_entries_by_topic(self, topic: str) -> List[MemoryEntry]:
        """
        Get entries that match a specific topic.
        
        Args:
            topic: The topic to search for
            
        Returns:
            List of matching memory entries
        """
        self._cleanup_expired()
        return [entry for entry in self._store.values() if topic.lower() in entry.topic.lower()]
    
    def get_entries_by_voice(self, voice: Voice) -> List[MemoryEntry]:
        """
        Get entries that used a specific voice.
        
        Args:
            voice: The voice to search for
            
        Returns:
            List of matching memory entries
        """
        self._cleanup_expired()
        return [entry for entry in self._store.values() if entry.voice == voice]
    
    def get_user_preferences(self) -> Dict[str, any]:
        """
        Analyze user preferences based on memory entries.
        
        Returns:
            Dictionary with user preferences
        """
        self._cleanup_expired()
        
        if not self._store:
            return {}
        
        # Count preferences
        voice_counts = {}
        tone_counts = {}
        success_rate = 0
        total_entries = len(self._store)
        
        for entry in self._store.values():
            voice_counts[entry.voice] = voice_counts.get(entry.voice, 0) + 1
            tone_counts[entry.tone] = tone_counts.get(entry.tone, 0) + 1
            if entry.success:
                success_rate += 1
        
        # Calculate percentages
        success_rate = (success_rate / total_entries) * 100 if total_entries > 0 else 0
        
        return {
            "preferred_voice": max(voice_counts.items(), key=lambda x: x[1])[0] if voice_counts else None,
            "preferred_tone": max(tone_counts.items(), key=lambda x: x[1])[0] if tone_counts else None,
            "success_rate": round(success_rate, 2),
            "total_generations": total_entries,
            "voice_distribution": voice_counts,
            "tone_distribution": tone_counts
        }
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries from the store."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._store.items()
            if current_time - entry.timestamp > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self._store[key]
    
    def clear(self) -> None:
        """Clear all entries from the store."""
        self._store.clear()
    
    def size(self) -> int:
        """Get the current number of entries in the store."""
        self._cleanup_expired()
        return len(self._store)


# Global memory store instance
memory_store = MemoryStore() 