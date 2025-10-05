"""
Main FastAPI application for AI Podcast Generator.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from api.podcast import router as podcast_router
from api.order import router as order_router
from utils.audio_utils import audio_utils
from memory.memory_store import memory_store
from db import init_db
from api import auth
# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 Starting AI Podcast Generator...")
    
    # Create audio output directory
    audio_utils.output_dir.mkdir(exist_ok=True)
    
    # Clean up old files on startup
    deleted_count = audio_utils.cleanup_old_files()
    if deleted_count > 0:
        print(f"🧹 Cleaned up {deleted_count} old audio files")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down AI Podcast Generator...")


# Create FastAPI app
app = FastAPI(
    title="AI Podcast Generator",
    description="Generate high-quality podcast episodes using GPT-4 and OpenAI TTS",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Include routers
app.include_router(podcast_router)
app.include_router(order_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Podcast Generator API",
        "version": "0.1.0",
        "description": "Generate high-quality podcast episodes using GPT-4 and OpenAI TTS",
        "endpoints": {
            "generate_podcast": "POST /api/v1/generate-podcast",
            "download_audio": "GET /api/v1/download/{filename}",
            "get_voices": "GET /api/v1/voices",
            "get_tones": "GET /api/v1/tones",
            "memory_stats": "GET /api/v1/memory/stats",
            "clear_memory": "DELETE /api/v1/memory/clear",
            "cleanup_audio": "DELETE /api/v1/audio/cleanup"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "error": "OpenAI API key not configured"
                }
            )
        
        # Check audio directory
        if not audio_utils.output_dir.exists():
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "error": "Audio output directory not accessible"
                }
            )
        
        return {
            "status": "healthy",
            "openai_configured": bool(openai_key),
            "audio_directory": str(audio_utils.output_dir.absolute()),
            "memory_entries": memory_store.size()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🎙️ Starting AI Podcast Generator on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔧 Debug mode: {reload}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
