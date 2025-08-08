# test_get_path.py

from utils.audio_utils import audio_utils

def main():
    filename = "give-agentic-ai-project-ideas_fable_20250807_161942.mp3 "
    path = audio_utils.get_file_path(filename)
    print("Generated file path:", path)

if __name__ == "__main__":
    main()
