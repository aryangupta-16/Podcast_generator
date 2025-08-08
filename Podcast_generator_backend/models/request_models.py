"""
Pydantic models for request and response validation.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator


class Tone(str, Enum):
    """Available podcast tones."""
    STORYTELLING = "storytelling"
    CONVERSATIONAL = "conversational"
    EDUCATIONAL = "educational"
    ENTERTAINING = "entertaining"
    PROFESSIONAL = "professional"
    CASUAL = "casual"


class Voice(str, Enum):
    """Available OpenAI TTS voices."""
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


class PodcastRequest(BaseModel):
    """Request model for podcast generation."""
    topic: str = Field(..., min_length=1, max_length=500, description="The podcast topic")
    tone: Tone = Field(default=Tone.CONVERSATIONAL, description="The desired tone of the podcast")
    voice: Voice = Field(default=Voice.FABLE, description="The TTS voice to use")
    duration_minutes: Optional[int] = Field(default=5, ge=1, le=30, description="Target duration in minutes")

    @validator('topic')
    def validate_topic(cls, v):
        """Validate topic is not empty and contains meaningful content."""
        if not v.strip():
            raise ValueError('Topic cannot be empty')
        return v.strip()


class PodcastResponse(BaseModel):
    """Response model for podcast generation."""
    success: bool = Field(..., description="Whether the generation was successful")
    audio_file_path: Optional[str] = Field(None, description="Path to the generated audio file")
    duration_seconds: Optional[float] = Field(None, description="Actual duration of the generated audio")
    error_message: Optional[str] = Field(None, description="Error message if generation failed")
    topic: Optional[str] = Field(None, description="The processed topic")
    voice_used: Optional[str] = Field(None, description="The voice that was used")


class MemoryEntry(BaseModel):
    """Model for memory entries."""
    topic: str
    tone: Tone
    voice: Voice
    timestamp: float
    duration_seconds: float
    success: bool 