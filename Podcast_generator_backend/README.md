# AI Podcast Generator

A production-grade backend for generating high-quality podcast episodes using GPT-4 and OpenAI TTS. Built with FastAPI, LangGraph, and modern Python practices.

## 🎯 Features

- **AI-Powered Script Generation**: Uses GPT-4 to create engaging podcast scripts
- **High-Quality TTS**: Converts scripts to natural audio using OpenAI's `tts-1-hd` model
- **Multiple Voices**: Support for 6 different TTS voices (alloy, echo, fable, onyx, nova, shimmer)
- **Multiple Tones**: 6 different podcast tones (storytelling, conversational, educational, entertaining, professional, casual)
- **LangGraph Workflow**: Orchestrated workflow with memory and tool calling
- **Memory System**: Tracks user preferences and generation history
- **Production Ready**: FastAPI with proper error handling, validation, and documentation

## 🏗️ Architecture

```
ai-podcast-generator/
├── main.py                 # FastAPI app entrypoint
├── api/
│   └── podcast.py         # REST API endpoints
├── agents/
│   ├── script_agent.py    # GPT-4 script generator
│   └── tts_agent.py       # OpenAI TTS converter
├── workflows/
│   └── podcast_workflow.py # LangGraph orchestration
├── memory/
│   └── memory_store.py    # In-memory store with TTL
├── models/
│   └── request_models.py  # Pydantic models
├── utils/
│   └── audio_utils.py     # Audio file management
└── pyproject.toml         # Project configuration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key
- uv (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Podcast_generator
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DEBUG=True
   ```

4. **Run the application**
   ```bash
   uv run python main.py
   ```

   Or with uvicorn directly:
   ```bash
   uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📚 API Documentation

### Generate Podcast

**POST** `/api/v1/generate-podcast`

Generate a podcast episode from a topic.

**Request Body:**
```json
{
  "topic": "How AI will change travel",
  "tone": "storytelling",
  "voice": "fable",
  "duration_minutes": 5
}
```

**Response:**
```json
{
  "success": true,
  "audio_file_path": "how-ai-will-change-travel_fable_20241206_143022.mp3",
  "duration_seconds": 312.5,
  "topic": "How AI will change travel",
  "voice_used": "fable"
}
```

### Download Audio

**GET** `/api/v1/download/{filename}`

Download a generated audio file.

### Get Available Voices

**GET** `/api/v1/voices`

Get information about available TTS voices.

### Get Available Tones

**GET** `/api/v1/tones`

Get information about available podcast tones.

### Memory Statistics

**GET** `/api/v1/memory/stats`

Get memory statistics and user preferences.

## 🎙️ Available Voices

| Voice | Description | Best For |
|-------|-------------|----------|
| **alloy** | Balanced, neutral voice | Educational content, Professional presentations |
| **echo** | Warm, friendly voice | Conversational content, Storytelling |
| **fable** | Clear, expressive voice | Storytelling, Narrative content |
| **onyx** | Deep, authoritative voice | Serious topics, Documentaries |
| **nova** | Bright, energetic voice | Entertainment, Motivational content |
| **shimmer** | Smooth, melodic voice | Relaxing content, Meditation |

## 🎭 Available Tones

| Tone | Description | Best For |
|------|-------------|----------|
| **storytelling** | Compelling narrative style | Personal stories, Historical content |
| **conversational** | Friendly, chatty style | Casual topics, Q&A sessions |
| **educational** | Informative and instructional | How-to guides, Educational content |
| **entertaining** | Fun and engaging | Entertainment, Comedy |
| **professional** | Formal and authoritative | Business content, Professional topics |
| **casual** | Relaxed and informal | Lifestyle content, Personal opinions |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DEBUG` | Enable debug mode | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `AUDIO_OUTPUT_DIR` | Audio files directory | `./audio_output` |
| `MEMORY_MAX_ENTRIES` | Max memory entries | `100` |
| `MEMORY_TTL_HOURS` | Memory TTL in hours | `24` |

### LangGraph Workflow

The application uses LangGraph to orchestrate the podcast generation process:

1. **Get User Preferences**: Retrieve user preferences from memory
2. **Generate Script**: Use GPT-4 to create podcast script
3. **Generate Audio**: Convert script to audio using OpenAI TTS
4. **Save Audio**: Save audio file to disk
5. **Update Memory**: Store generation result in memory

## 🧠 Memory System

The application includes a sophisticated memory system that:

- Tracks user preferences (preferred voices, tones)
- Stores generation history with TTL
- Analyzes success rates and patterns
- Provides insights for personalization

## 📁 File Structure

Generated audio files are stored in the `audio_output/` directory with the naming convention:
```
{clean-topic}_{voice}_{timestamp}.mp3
```

Example: `how-ai-will-change-travel_fable_20241206_143022.mp3`

## 🛠️ Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black .
uv run isort .
```

### Linting

```bash
uv run flake8
```

## 🚀 Production Deployment

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

For production, ensure:
- Set `DEBUG=False`
- Configure proper CORS origins
- Set up proper logging
- Use environment-specific OpenAI API keys
- Configure proper file storage (consider cloud storage)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the health endpoint at `/health`
- Check the memory statistics at `/api/v1/memory/stats`

## 🔮 Future Enhancements

- [ ] Background music integration
- [ ] Multiple speaker support
- [ ] Podcast episode series
- [ ] Advanced audio editing
- [ ] Cloud storage integration
- [ ] User authentication
- [ ] Analytics dashboard
