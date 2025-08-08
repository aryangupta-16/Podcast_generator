#!/usr/bin/env python3
"""
Setup script for AI Podcast Generator.
"""

import os
import sys
from pathlib import Path


def create_env_file():
    """Create .env file if it doesn't exist."""
    env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
APP_NAME=AI Podcast Generator
APP_VERSION=0.1.0
DEBUG=True

# Audio Configuration
AUDIO_OUTPUT_DIR=./audio_output
MAX_AUDIO_DURATION=300

# Available TTS Voices
AVAILABLE_VOICES=alloy,echo,fable,onyx,nova,shimmer

# Memory Configuration
MEMORY_MAX_ENTRIES=100
MEMORY_TTL_HOURS=24
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        try:
            with open(env_file, "w", encoding="utf-8") as f:
                f.write(env_content)
            print("✅ Created .env file")
            print("⚠️  Please update OPENAI_API_KEY in .env file")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import openai
        import langgraph
        import pydantic
        import aiofiles
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: uv sync")
        return False


def check_openai_key():
    """Check if OpenAI API key is configured."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            print("✅ OpenAI API key is configured")
            return True
        else:
            print("⚠️  OpenAI API key not configured")
            print("Please update OPENAI_API_KEY in .env file")
            return False
    except Exception as e:
        print(f"❌ Error checking OpenAI key: {e}")
        return False


def run_tests():
    """Run basic tests."""
    print("\n🧪 Running basic tests...")
    try:
        # Test imports
        from models.request_models import PodcastRequest, Tone, Voice
        from memory.memory_store import memory_store
        from utils.audio_utils import audio_utils
        
        print("✅ All modules imported successfully")
        
        # Test models
        request = PodcastRequest(
            topic="Test topic",
            tone=Tone.CONVERSATIONAL,
            voice=Voice.FABLE
        )
        print(f"✅ Models working: {request.topic}")
        
        # Test memory store
        print(f"✅ Memory store working: {memory_store.size()} entries")
        
        # Test audio utils
        print(f"✅ Audio utils working: {audio_utils.output_dir}")
        
        # Test workflow components
        from workflows.podcast_workflow import podcast_workflow
        from agents.script_agent import ScriptAgent
        from agents.tts_agent import TTSAgent
        
        print("✅ LangGraph workflow initialized")
        
        script_agent = ScriptAgent()
        tts_agent = TTSAgent()
        
        print("✅ Agents initialized")
        
        # Test voice characteristics
        characteristics = tts_agent.get_voice_characteristics(Voice.FABLE)
        print(f"✅ Voice characteristics: {characteristics['personality']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🎙️ AI Podcast Generator Setup")
    print("=" * 40)
    
    # Create .env file
    if not create_env_file():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check OpenAI key
    check_openai_key()
    
    # Run tests
    if run_tests():
        print("\n🎉 Setup completed successfully!")
        print("\n📚 Next steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: uv run python main.py")
        print("3. Visit: http://localhost:8000/docs")
        print("4. Try the example: uv run python example_usage.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")


if __name__ == "__main__":
    main() 