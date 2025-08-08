"""
Basic test to verify the setup works correctly.
"""

import asyncio
import os
from models.request_models import PodcastRequest, Tone, Voice
from memory.memory_store import memory_store
from utils.audio_utils import audio_utils


def test_imports():
    """Test that all modules can be imported correctly."""
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
    
    return True


def test_environment():
    """Test environment configuration."""
    print("\n🔧 Environment Check:")
    
    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  OpenAI API key not configured (set OPENAI_API_KEY in .env)")
    
    # Check debug mode
    debug = os.getenv("DEBUG", "False").lower() == "true"
    print(f"✅ Debug mode: {debug}")
    
    return True


async def test_workflow_components():
    """Test workflow components (without making API calls)."""
    print("\n🔄 Workflow Components Check:")
    
    try:
        from workflows.podcast_workflow import podcast_workflow
        print("✅ LangGraph workflow initialized")
        
        from agents.script_agent import ScriptAgent
        from agents.tts_agent import TTSAgent
        
        script_agent = ScriptAgent()
        tts_agent = TTSAgent()
        
        print("✅ Agents initialized")
        
        # Test voice characteristics
        characteristics = tts_agent.get_voice_characteristics(Voice.FABLE)
        print(f"✅ Voice characteristics: {characteristics['personality']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Running AI Podcast Generator Tests\n")
    
    # Test imports
    test_imports()
    
    # Test environment
    test_environment()
    
    # Test workflow components
    asyncio.run(test_workflow_components())
    
    print("\n🎉 All tests completed!")
    print("\n📚 Next steps:")
    print("1. Set your OpenAI API key in .env file")
    print("2. Run: uv run python main.py")
    print("3. Visit: http://localhost:8000/docs")


if __name__ == "__main__":
    main() 