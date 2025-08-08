"""
FastAPI endpoints for podcast generation.
"""

import os
from pathlib import Path
from typing import List
from fastapi import APIRouter, HTTPException, Response, BackgroundTasks
from fastapi.responses import FileResponse
from models.request_models import PodcastRequest, PodcastResponse, Tone, Voice
from workflows.podcast_workflow import podcast_workflow
from memory.memory_store import memory_store
from utils.audio_utils import audio_utils
from agents.tts_agent import TTSAgent

router = APIRouter(prefix="/api/v1", tags=["podcast"])


@router.post("/generate-podcast", response_model=PodcastResponse)
async def generate_podcast(request: PodcastRequest, background_tasks: BackgroundTasks):
    """
    Generate a podcast episode from a topic.
    
    Args:
        request: The podcast generation request
        background_tasks: FastAPI background tasks
        
    Returns:
        Podcast generation response
    """
    try:
        # Validate OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured"
            )
        
        # Generate podcast using workflow
        response = await podcast_workflow.generate_podcast(request)
        
        print(response)
        if not response.success:
            raise HTTPException(
                status_code=500,
                detail=response.error_message or "Failed to generate podcast"
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/download/{filename}")
async def download_audio(filename: str):
    """
    Download a generated audio file.
    
    Args:
        filename: The audio file filename
        
    Returns:
        Audio file response
    """
    try:

        file_path = audio_utils.get_file_path(filename)
        
        print("file_path")
        print(file_path)
        if not audio_utils.validate_audio_file(file_path):
            raise HTTPException(
                status_code=404,
                detail="Audio file not found or invalid"
            )
        
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to serve audio file: {str(e)}"
        )


@router.get("/voices", response_model=List[dict])
async def get_available_voices():
    """
    Get information about available TTS voices.
    
    Returns:
        List of available voices with characteristics
    """
    try:
        tts_agent = TTSAgent()
        voices = []
        
        for voice in Voice:
            characteristics = tts_agent.get_voice_characteristics(voice)
            voices.append({
                "id": voice.value,
                "name": voice.value.title(),
                **characteristics
            })
        
        return voices
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get voice information: {str(e)}"
        )


@router.get("/tones", response_model=List[dict])
async def get_available_tones():
    """
    Get information about available podcast tones.
    
    Returns:
        List of available tones with descriptions
    """
    tone_descriptions = {
        Tone.STORYTELLING: {
            "description": "Compelling narrative style with engaging stories",
            "best_for": ["Personal stories", "Historical content", "Entertainment"]
        },
        Tone.CONVERSATIONAL: {
            "description": "Friendly, chatty style like talking to a friend",
            "best_for": ["Casual topics", "Q&A sessions", "Personal content"]
        },
        Tone.EDUCATIONAL: {
            "description": "Informative and instructional content",
            "best_for": ["How-to guides", "Educational content", "Tutorials"]
        },
        Tone.ENTERTAINING: {
            "description": "Fun and engaging with humor and energy",
            "best_for": ["Entertainment", "Comedy", "Light-hearted topics"]
        },
        Tone.PROFESSIONAL: {
            "description": "Formal and authoritative business style",
            "best_for": ["Business content", "Professional topics", "News"]
        },
        Tone.CASUAL: {
            "description": "Relaxed and informal approach",
            "best_for": ["Lifestyle content", "Personal opinions", "Relaxed topics"]
        }
    }
    
    tones = []
    for tone in Tone:
        description = tone_descriptions.get(tone, {})
        tones.append({
            "id": tone.value,
            "name": tone.value.title(),
            **description
        })
    
    return tones


@router.get("/memory/stats")
async def get_memory_stats():
    """
    Get memory statistics and user preferences.
    
    Returns:
        Memory statistics and user preferences
    """
    try:
        preferences = memory_store.get_user_preferences()
        storage_info = audio_utils.get_storage_info()
        
        return {
            "memory_entries": memory_store.size(),
            "user_preferences": preferences,
            "storage_info": storage_info
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get memory stats: {str(e)}"
        )


@router.delete("/memory/clear")
async def clear_memory():
    """
    Clear all memory entries.
    
    Returns:
        Success message
    """
    try:
        memory_store.clear()
        return {"message": "Memory cleared successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear memory: {str(e)}"
        )


@router.delete("/audio/cleanup")
async def cleanup_old_audio_files(background_tasks: BackgroundTasks):
    """
    Clean up old audio files.
    
    Returns:
        Cleanup results
    """
    try:
        deleted_count = audio_utils.cleanup_old_files()
        return {
            "message": f"Cleaned up {deleted_count} old audio files",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup audio files: {str(e)}"
        ) 