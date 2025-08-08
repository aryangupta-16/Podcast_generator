"""
Example usage of the AI Podcast Generator API.
"""

import asyncio
import aiohttp
import json
from models.request_models import PodcastRequest, Tone, Voice


async def generate_podcast_example():
    """Example of generating a podcast using the API."""
    
    # API base URL
    base_url = "http://localhost:8000"
    
    # Example request
    request_data = {
        "topic": "The Future of Artificial Intelligence in Healthcare",
        "tone": "educational",
        "voice": "alloy",
        "duration_minutes": 3
    }
    
    print("🎙️ Generating podcast...")
    print(f"Topic: {request_data['topic']}")
    print(f"Tone: {request_data['tone']}")
    print(f"Voice: {request_data['voice']}")
    print(f"Duration: {request_data['duration_minutes']} minutes")
    print("-" * 50)
    
    async with aiohttp.ClientSession() as session:
        try:
            # Generate podcast
            async with session.post(
                f"{base_url}/api/v1/generate-podcast",
                json=request_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Podcast generated successfully!")
                    print(f"Audio file: {result['audio_file_path']}")
                    print(f"Duration: {result['duration_seconds']:.1f} seconds")
                    
                    # Download the audio file
                    filename = result['audio_file_path'].split('/')[-1]
                    download_url = f"{base_url}/api/v1/download/{filename}"
                    
                    print(f"\n📥 Downloading audio file...")
                    async with session.get(download_url) as download_response:
                        if download_response.status == 200:
                            # Save the audio file
                            with open(filename, 'wb') as f:
                                f.write(await download_response.read())
                            print(f"✅ Audio file saved as: {filename}")
                        else:
                            print(f"❌ Failed to download audio: {download_response.status}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to generate podcast: {response.status}")
                    print(f"Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")


async def get_available_voices():
    """Get information about available voices."""
    
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/api/v1/voices") as response:
                if response.status == 200:
                    voices = await response.json()
                    print("\n🎙️ Available Voices:")
                    for voice in voices:
                        print(f"  • {voice['name']} ({voice['id']})")
                        print(f"    {voice['description']}")
                        print(f"    Best for: {', '.join(voice['best_for'])}")
                        print()
                else:
                    print(f"❌ Failed to get voices: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")


async def get_available_tones():
    """Get information about available tones."""
    
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/api/v1/tones") as response:
                if response.status == 200:
                    tones = await response.json()
                    print("\n🎭 Available Tones:")
                    for tone in tones:
                        print(f"  • {tone['name']} ({tone['id']})")
                        print(f"    {tone['description']}")
                        print(f"    Best for: {', '.join(tone['best_for'])}")
                        print()
                else:
                    print(f"❌ Failed to get tones: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")


async def get_memory_stats():
    """Get memory statistics."""
    
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/api/v1/memory/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    print("\n🧠 Memory Statistics:")
                    print(f"  • Total entries: {stats['memory_entries']}")
                    print(f"  • Storage info: {stats['storage_info']}")
                    
                    if stats['user_preferences']:
                        prefs = stats['user_preferences']
                        print(f"  • Preferred voice: {prefs.get('preferred_voice', 'None')}")
                        print(f"  • Preferred tone: {prefs.get('preferred_tone', 'None')}")
                        print(f"  • Success rate: {prefs.get('success_rate', 0)}%")
                    else:
                        print("  • No user preferences yet")
                        
                else:
                    print(f"❌ Failed to get memory stats: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    """Run the example."""
    print("🎙️ AI Podcast Generator - Example Usage")
    print("=" * 50)
    
    # Check if server is running
    base_url = "http://localhost:8000"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    print("✅ Server is running!")
                else:
                    print("❌ Server is not responding properly")
                    return
        except Exception as e:
            print("❌ Cannot connect to server. Make sure it's running on http://localhost:8000")
            print("   Start the server with: uv run python main.py")
            return
    
    # Get available options
    await get_available_voices()
    await get_available_tones()
    
    # Get memory stats
    await get_memory_stats()
    
    # Generate a podcast
    await generate_podcast_example()
    
    print("\n🎉 Example completed!")
    print("\n📚 API Documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(main()) 