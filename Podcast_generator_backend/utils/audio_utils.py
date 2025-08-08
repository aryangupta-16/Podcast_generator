"""
Audio utility functions for file management and validation.
"""

import os
import re
import time
from pathlib import Path
from typing import Optional
import aiofiles


class AudioUtils:
    """Utility class for audio file operations."""
    
    def __init__(self, output_dir: str = "./audio_output"):
        """
        Initialize audio utilities.
        
        Args:
            output_dir: Directory to store audio files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_filename(self, topic: str, voice: str, timestamp: Optional[float] = None) -> str:
        """
        Generate a unique filename for the audio file.
        
        Args:
            topic: The podcast topic
            voice: The TTS voice used
            timestamp: Optional timestamp (uses current time if not provided)
            
        Returns:
            Generated filename
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Clean topic for filename
        clean_topic = re.sub(r'[^\w\s-]', '', topic.lower())
        clean_topic = re.sub(r'[-\s]+', '-', clean_topic)
        clean_topic = clean_topic[:50]  # Limit length
        
        # Format timestamp
        date_str = time.strftime("%Y%m%d_%H%M%S", time.localtime(timestamp))
        
        return f"{clean_topic}_{voice}_{date_str}.mp3"
    
    def get_file_path(self, filename: str) -> Path:
        """
        Get the full path for a filename.
        
        Args:
            filename: The filename
            
        Returns:
            Full path to the file
        """

        return self.output_dir / filename
    
    async def save_audio_file(self, audio_data: bytes, filename: str) -> Path:
        """
        Save audio data to a file.
        
        Args:
            audio_data: The audio data as bytes
            filename: The filename to save as
            
        Returns:
            Path to the saved file
        """
        file_path = self.get_file_path(filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(audio_data)
        
        return file_path
    
    def validate_audio_file(self, file_path: Path) -> bool:
        """
        Validate that an audio file exists and is readable.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if file is valid, False otherwise
        """

        print("file_path")
        print(file_path)
        if not file_path.exists():
            print(1)
            return False
        
        if not file_path.is_file():
            print(2)
            return False
        
        # Check file size (should be > 0)
        if file_path.stat().st_size == 0:
            print(3)
            return False
        
        # Check file extension
        # if file_path.suffix.lower() != '.mp3':
        #     print(f"Expected .mp3, got {file_path.suffix.lower()}")
        #     print(4)
        #     return False
        
        return True
    
    def get_file_size_mb(self, file_path: Path) -> float:
        """
        Get file size in megabytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in MB
        """
        if not file_path.exists():
            return 0.0
        
        return file_path.stat().st_size / (1024 * 1024)
    
    def cleanup_old_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up old audio files.
        
        Args:
            max_age_hours: Maximum age of files to keep in hours
            
        Returns:
            Number of files deleted
        """
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        deleted_count = 0
        
        for file_path in self.output_dir.glob("*.mp3"):
            file_age = current_time - file_path.stat().st_mtime
            
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except OSError:
                    # File might be in use, skip it
                    continue
        
        return deleted_count
    
    def get_storage_info(self) -> dict:
        """
        Get information about audio storage.
        
        Returns:
            Dictionary with storage information
        """
        total_files = 0
        total_size_mb = 0.0
        
        for file_path in self.output_dir.glob("*.mp3"):
            total_files += 1
            total_size_mb += self.get_file_size_mb(file_path)
        
        return {
            "total_files": total_files,
            "total_size_mb": round(total_size_mb, 2),
            "output_directory": str(self.output_dir.absolute())
        }


# Global audio utils instance
audio_utils = AudioUtils() 