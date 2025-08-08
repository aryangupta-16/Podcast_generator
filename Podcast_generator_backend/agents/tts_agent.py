"""
Text-to-Speech agent using OpenAI's TTS-1-HD model.
"""

import os
from typing import Optional
from openai import AsyncOpenAI
from models.request_models import Voice


class TTSAgent:
    """Agent for converting text to speech using OpenAI TTS."""
    
    def __init__(self):
        """Initialize the TTS agent."""
        self.model = "tts-1-hd"
        self._client = None
    
    @property
    def client(self):
        """Lazy-load the OpenAI client."""
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "your_openai_api_key_here":
                raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
            self._client = AsyncOpenAI(api_key=api_key)
        return self._client
    
    def _validate_voice(self, voice: Voice) -> str:
        """
        Validate and return the voice parameter.
        
        Args:
            voice: The voice to validate
            
        Returns:
            Validated voice string
        """
        valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        voice_str = voice.value if hasattr(voice, 'value') else str(voice)
        
        if voice_str not in valid_voices:
            raise ValueError(f"Invalid voice: {voice_str}. Valid voices are: {valid_voices}")
        
        return voice_str
    
    def _preprocess_script(self, script: str) -> str:
        """
        Preprocess the script for better TTS quality.
        
        Args:
            script: The raw script
            
        Returns:
            Preprocessed script
        """
        # Remove any markdown formatting
        script = script.replace("*", "").replace("_", "").replace("**", "")
        
        # Clean up extra whitespace
        script = " ".join(script.split())
        
        # Add natural pauses for better flow
        # Replace common punctuation with pause indicators
        script = script.replace("...", " [pause] ")
        script = script.replace("--", " [pause] ")
        
        # Add pauses after sentences for better pacing
        script = script.replace(". ", ". [pause] ")
        script = script.replace("! ", "! [pause] ")
        script = script.replace("? ", "? [pause] ")
        
        # Clean up multiple pauses
        script = script.replace("[pause] [pause]", "[pause]")
        
        return script.strip()
    
    async def generate_audio(
        self, 
        script: str, 
        voice: Voice,
        output_format: str = "mp3"
    ) -> bytes:
        """
        Generate audio from script using OpenAI TTS.
        
        Args:
            script: The podcast script
            voice: The TTS voice to use
            output_format: Output format (mp3, opus, aac, flac)
            
        Returns:
            Audio data as bytes
        """
        try:
            # Validate voice
            voice_str = self._validate_voice(voice)
            
            # Preprocess script
            processed_script = self._preprocess_script(script)
            
            # Validate script length (OpenAI TTS has limits)
            if len(processed_script) > 4096:
                raise ValueError("Script is too long for TTS. Maximum 4096 characters allowed.")
            
            if len(processed_script) < 10:
                raise ValueError("Script is too short for TTS.")
            
            # Generate audio
            response = await self.client.audio.speech.create(
                model=self.model,
                voice=voice_str,
                input=processed_script,
                response_format=output_format
            )
            
            # Get audio data
            audio_data = response.content
            
            if not audio_data:
                raise ValueError("No audio data received from TTS service")
            
            return audio_data
            
        except Exception as e:
            raise Exception(f"Failed to generate audio: {str(e)}")
    
    def estimate_audio_duration(self, script: str) -> float:
        """
        Estimate the duration of the generated audio in seconds.
        
        Args:
            script: The podcast script
            
        Returns:
            Estimated duration in seconds
        """
        # Count words
        words = len(script.split())
        
        # Average speaking rate: 155 words per minute
        words_per_minute = 155
        minutes = words / words_per_minute
        
        return minutes * 60  # Convert to seconds
    
    def get_voice_characteristics(self, voice: Voice) -> dict:
        """
        Get characteristics of a specific voice.
        
        Args:
            voice: The voice to get characteristics for
            
        Returns:
            Dictionary with voice characteristics
        """
        voice_characteristics = {
            Voice.ALLOY: {
                "description": "A balanced, neutral voice suitable for most content",
                "best_for": ["Educational content", "Professional presentations", "News"],
                "personality": "Professional and trustworthy"
            },
            Voice.ECHO: {
                "description": "A warm, friendly voice with natural intonation",
                "best_for": ["Conversational content", "Storytelling", "Casual podcasts"],
                "personality": "Friendly and approachable"
            },
            Voice.FABLE: {
                "description": "A clear, expressive voice with good pacing",
                "best_for": ["Storytelling", "Narrative content", "Entertainment"],
                "personality": "Engaging and expressive"
            },
            Voice.ONYX: {
                "description": "A deep, authoritative voice with gravitas",
                "best_for": ["Serious topics", "Documentaries", "Professional content"],
                "personality": "Authoritative and serious"
            },
            Voice.NOVA: {
                "description": "A bright, energetic voice with enthusiasm",
                "best_for": ["Entertainment", "Motivational content", "Youth-oriented content"],
                "personality": "Energetic and enthusiastic"
            },
            Voice.SHIMMER: {
                "description": "A smooth, melodic voice with natural flow",
                "best_for": ["Relaxing content", "Meditation", "Smooth narration"],
                "personality": "Calm and soothing"
            }
        }
        
        return voice_characteristics.get(voice, voice_characteristics[Voice.FABLE]) 