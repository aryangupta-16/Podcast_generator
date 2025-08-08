"""
Simple test to verify basic functionality.
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test basic imports."""
    print("🧪 Testing imports...")
    
    try:
        from models.request_models import PodcastRequest, Tone, Voice
        print("✅ Models imported successfully")
        
        from memory.memory_store import memory_store
        print("✅ Memory store imported successfully")
        
        from utils.audio_utils import audio_utils
        print("✅ Audio utils imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_models():
    """Test model creation."""
    print("\n🧪 Testing models...")
    
    try:
        from models.request_models import PodcastRequest, Tone, Voice
        
        request = PodcastRequest(
            topic="Test topic",
            tone=Tone.CONVERSATIONAL,
            voice=Voice.FABLE
        )
        
        print(f"✅ Created request: {request.topic}")
        print(f"✅ Tone: {request.tone}")
        print(f"✅ Voice: {request.voice}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False


def test_memory():
    """Test memory store."""
    print("\n🧪 Testing memory store...")
    
    try:
        from memory.memory_store import memory_store
        from models.request_models import MemoryEntry, Tone, Voice
        import time
        
        # Test memory operations
        entry = MemoryEntry(
            topic="Test topic",
            tone=Tone.CONVERSATIONAL,
            voice=Voice.FABLE,
            timestamp=time.time(),
            duration_seconds=120.0,
            success=True
        )
        
        memory_store.add_entry(entry)
        print(f"✅ Added memory entry")
        print(f"✅ Memory size: {memory_store.size()}")
        
        preferences = memory_store.get_user_preferences()
        print(f"✅ User preferences: {preferences}")
        
        return True
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        return False


def test_audio_utils():
    """Test audio utilities."""
    print("\n🧪 Testing audio utils...")
    
    try:
        from utils.audio_utils import audio_utils
        
        # Test filename generation
        filename = audio_utils.generate_filename("Test Topic", "fable")
        print(f"✅ Generated filename: {filename}")
        
        # Test file path
        file_path = audio_utils.get_file_path(filename)
        print(f"✅ File path: {file_path}")
        
        # Test storage info
        storage_info = audio_utils.get_storage_info()
        print(f"✅ Storage info: {storage_info}")
        
        return True
    except Exception as e:
        print(f"❌ Audio utils test failed: {e}")
        return False


def test_environment():
    """Test environment setup."""
    print("\n🧪 Testing environment...")
    
    try:
        # Check if .env file exists
        env_file = Path(".env")
        if env_file.exists():
            print("✅ .env file exists")
        else:
            print("⚠️  .env file not found")
            return False
        
        # Try to load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ Environment variables loaded")
        except Exception as e:
            print(f"⚠️  Could not load .env file: {e}")
            # Continue with default values
        
        # Check OpenAI key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not configured")
        
        # Check debug mode
        debug = os.getenv("DEBUG", "False").lower() == "true"
        print(f"✅ Debug mode: {debug}")
        
        return True
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🎙️ AI Podcast Generator - Simple Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_models,
        test_memory,
        test_audio_utils,
        test_environment
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        print("\n📚 Next steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: uv run python main.py")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("Please check the errors above and fix them.")


if __name__ == "__main__":
    main() 