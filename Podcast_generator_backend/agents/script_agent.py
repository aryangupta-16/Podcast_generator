"""
Script generation agent using GPT-4 to create podcast scripts.
"""

import os
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from models.request_models import Tone, Voice


class ScriptAgent:
    """Agent for generating podcast scripts using GPT-4."""
    
    def __init__(self):
        """Initialize the script agent."""
        self.model = "gpt-4"
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
    
    def _get_tone_instructions(self, tone: Tone) -> str:
        """
        Get specific instructions for the requested tone.
        
        Args:
            tone: The desired tone
            
        Returns:
            Tone-specific instructions
        """
        tone_instructions = {
            Tone.STORYTELLING: """
            Write in a compelling storytelling style with:
            - Engaging narrative structure with clear beginning, middle, and end
            - Vivid descriptions and emotional hooks
            - Personal anecdotes or relatable examples
            - Suspenseful elements and cliffhangers
            - Conversational flow that draws listeners in
            """,
            
            Tone.CONVERSATIONAL: """
            Write in a friendly, conversational style with:
            - Natural speech patterns and contractions
            - Direct address to the listener ("you")
            - Casual language and relatable examples
            - Questions to engage the audience
            - Warm and approachable tone
            """,
            
            Tone.EDUCATIONAL: """
            Write in an educational, informative style with:
            - Clear structure with main points and subpoints
            - Definitions and explanations of complex concepts
            - Real-world examples and case studies
            - Step-by-step breakdowns where appropriate
            - Professional but accessible language
            """,
            
            Tone.ENTERTAINING: """
            Write in an entertaining, engaging style with:
            - Humor and wit throughout the content
            - Pop culture references and current trends
            - Interactive elements and audience engagement
            - Dynamic pacing and varied sentence structures
            - Fun facts and surprising revelations
            """,
            
            Tone.PROFESSIONAL: """
            Write in a professional, authoritative style with:
            - Formal language and industry terminology
            - Data-driven insights and statistics
            - Expert opinions and credible sources
            - Structured arguments and logical flow
            - Balanced and objective perspective
            """,
            
            Tone.CASUAL: """
            Write in a casual, relaxed style with:
            - Informal language and slang (appropriate)
            - Personal opinions and experiences
            - Light-hearted approach to serious topics
            - Easy-to-follow structure
            - Friendly and relatable tone
            """
        }
        
        return tone_instructions.get(tone, tone_instructions[Tone.CONVERSATIONAL])
    
    def _get_script_template(self, duration_minutes: int) -> str:
        """
        Get a script template based on target duration.
        
        Args:
            duration_minutes: Target duration in minutes
            
        Returns:
            Script template
        """
        # Estimate words per minute (average speaking rate is 150-160 WPM)
        words_per_minute = 155
        target_words = duration_minutes * words_per_minute
        
        return f"""
        Create a podcast script that is approximately {target_words} words long 
        (targeting {duration_minutes} minutes of audio).
        
        Structure the script with:
        1. Engaging introduction (hook the listener in 30 seconds)
        2. Main content (3-4 key points with examples)
        3. Conclusion (summarize and call to action)
        
        Include natural speech patterns:
        - Use contractions (you're, we're, it's)
        - Include filler words and pauses naturally
        - Vary sentence length for rhythm
        - Add emphasis markers where needed
        - Include audience engagement phrases
        """
    
    async def generate_script(
        self, 
        topic: str, 
        tone: Tone, 
        duration_minutes: int = 5,
        user_preferences: Optional[Dict] = None
    ) -> str:
        """
        Generate a podcast script using GPT-4.
        
        Args:
            topic: The podcast topic
            tone: The desired tone
            duration_minutes: Target duration in minutes
            user_preferences: Optional user preferences from memory
            
        Returns:
            Generated podcast script
        """
        # Build the prompt
        tone_instructions = self._get_tone_instructions(tone)
        script_template = self._get_script_template(duration_minutes)
        
        # Add user preferences if available
        preference_context = ""
        if user_preferences:
            preferred_voice = user_preferences.get("preferred_voice")
            preferred_tone = user_preferences.get("preferred_tone")
            
            if preferred_tone and preferred_tone != tone:
                preference_context = f"""
                Note: The user typically prefers {preferred_tone} tone, but has requested {tone} for this episode.
                Adapt the style accordingly while maintaining the requested tone.
                """
        
        system_prompt = f"""You are an expert podcast script writer. Your task is to create engaging, 
        high-quality podcast scripts that are ready for text-to-speech conversion.
        
        {tone_instructions}
        
        {script_template}
        
        {preference_context}
        
        Important guidelines:
        - Write for audio consumption (not reading)
        - Use natural speech patterns and conversational flow
        - Include appropriate pauses and emphasis markers
        - Make it engaging from the first sentence
        - Ensure logical flow and clear structure
        - Avoid complex jargon unless necessary
        - Include audience engagement elements
        - End with a strong conclusion or call to action
        
        Return only the script text, no additional formatting or explanations.
        """
        
        user_prompt = f"Create a podcast script about: {topic}"
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                top_p=0.9
            )
            print(response)
            script = response.choices[0].message.content.strip()
            
            # Basic validation
            if not script or len(script) < 100:
                raise ValueError("Generated script is too short or empty")
            
            return script
            
        except Exception as e:
            raise Exception(f"Failed to generate script: {str(e)}")
    
    def estimate_duration(self, script: str) -> float:
        """
        Estimate the duration of a script in seconds.
        
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