"""
LangGraph workflow for podcast generation with memory and tool calling.
"""

import time
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from agents.script_agent import ScriptAgent
from agents.tts_agent import TTSAgent
from memory.memory_store import memory_store
from utils.audio_utils import audio_utils
from models.request_models import PodcastRequest, PodcastResponse, MemoryEntry, Tone, Voice


class WorkflowState(TypedDict):
    """State for the podcast generation workflow."""
    request: PodcastRequest
    script: str
    audio_data: bytes
    audio_file_path: str
    duration_seconds: float
    success: bool
    error_message: str
    user_preferences: Dict[str, Any]
    timestamp: float


class PodcastWorkflow:
    """LangGraph workflow for podcast generation."""
    
    def __init__(self):
        """Initialize the workflow."""
        self.script_agent = ScriptAgent()
        self.tts_agent = TTSAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the state graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("get_user_preferences", self._get_user_preferences)
        workflow.add_node("generate_script", self._generate_script)
        workflow.add_node("generate_audio", self._generate_audio)
        workflow.add_node("save_audio", self._save_audio)
        workflow.add_node("update_memory", self._update_memory)
        workflow.add_node("handle_error", self._handle_error)
        
        # Define the workflow
        workflow.set_entry_point("get_user_preferences")
        
        # Add edges
        workflow.add_edge("get_user_preferences", "generate_script")
        workflow.add_edge("generate_script", "generate_audio")
        workflow.add_edge("generate_audio", "save_audio")
        workflow.add_edge("save_audio", "update_memory")
        workflow.add_edge("update_memory", END)
        
        # Add conditional edges for error handling
        workflow.add_conditional_edges(
            "generate_script",
            self._should_continue,
            {
                "continue": "generate_audio",
                "error": "handle_error"
            }
        )
        
        workflow.add_conditional_edges(
            "generate_audio",
            self._should_continue,
            {
                "continue": "save_audio",
                "error": "handle_error"
            }
        )
        
        workflow.add_conditional_edges(
            "save_audio",
            self._should_continue,
            {
                "continue": "update_memory",
                "error": "handle_error"
            }
        )
        
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def _get_user_preferences(self, state: WorkflowState) -> WorkflowState:
        """Get user preferences from memory."""
        try:
            user_preferences = memory_store.get_user_preferences()
            state["user_preferences"] = user_preferences
            state["timestamp"] = time.time()
            state["success"] = True
            state["error_message"] = ""
            return state
        except Exception as e:
            state["success"] = False
            state["error_message"] = f"Failed to get user preferences: {str(e)}"
            return state
    
    def _generate_script(self, state: WorkflowState) -> WorkflowState:
        """Generate the podcast script."""
        try:
            request = state["request"]
            user_preferences = state.get("user_preferences", {})
            
            import asyncio
            script = None
            try:
                script = asyncio.run(self.script_agent.generate_script(
                    topic=request.topic,
                    tone=request.tone,
                    duration_minutes=request.duration_minutes,
                    user_preferences=user_preferences
                ))
            except Exception as e:
                state["success"] = False
                state["error_message"] = f"Failed to generate script: {str(e)}"
                return state
            state["script"] = script
            state["success"] = True
            state["error_message"] = ""
            return state
            
        except Exception as e:
            state["success"] = False
            state["error_message"] = f"Failed to generate script: {str(e)}"
            return state
    
    def _generate_audio(self, state: WorkflowState) -> WorkflowState:
        """Generate audio from the script."""
        try:
            request = state["request"]
            script = state["script"]
            
            import asyncio
            audio_data = None
            try:
                audio_data = asyncio.run(self.tts_agent.generate_audio(
                    script=script,
                    voice=request.voice,
                    output_format="mp3"
                ))
            except Exception as e:
                state["success"] = False
                state["error_message"] = f"Failed to generate audio: {str(e)}"
                return state
            state["audio_data"] = audio_data
            state["success"] = True
            state["error_message"] = ""
            return state
            
        except Exception as e:
            state["success"] = False
            state["error_message"] = f"Failed to generate audio: {str(e)}"
            return state
    
    def _save_audio(self, state: WorkflowState) -> WorkflowState:
        """Save the audio file."""
        try:
            request = state["request"]
            audio_data = state["audio_data"]
            timestamp = state["timestamp"]
            
            # Generate filename
            filename = audio_utils.generate_filename(
                topic=request.topic,
                voice=request.voice.value,
                timestamp=timestamp
            )
            file_path = audio_utils.get_file_path(filename)
            # print(file_path)
            file_path.parent.mkdir(exist_ok=True)
            # Write the actual audio data to the file
            with open(file_path, "wb") as f:
                f.write(audio_data)
            # Calculate duration
            duration_seconds = self.tts_agent.estimate_audio_duration(state["script"])

            state["audio_file_path"] = str(filename)
            state["duration_seconds"] = duration_seconds
            state["success"] = True
            state["error_message"] = ""
            return state
            
        except Exception as e:
            state["success"] = False
            state["error_message"] = f"Failed to save audio: {str(e)}"
            return state
    
    def _update_memory(self, state: WorkflowState) -> WorkflowState:
        """Update memory with the generation result."""
        try:
            request = state["request"]
            timestamp = state["timestamp"]
            duration_seconds = state["duration_seconds"]
            success = state["success"]
            
            # Create memory entry
            memory_entry = MemoryEntry(
                topic=request.topic,
                tone=request.tone,
                voice=request.voice,
                timestamp=timestamp,
                duration_seconds=duration_seconds,
                success=success
            )
            
            # Add to memory
            memory_store.add_entry(memory_entry)
            
            return state
            
        except Exception as e:
            # Don't fail the workflow for memory errors
            state["error_message"] = f"Warning: Failed to update memory: {str(e)}"
            return state
    
    def _handle_error(self, state: WorkflowState) -> WorkflowState:
        """Handle errors in the workflow."""
        # Update memory with failed attempt
        try:
            request = state["request"]
            timestamp = state["timestamp"]
            
            memory_entry = MemoryEntry(
                topic=request.topic,
                tone=request.tone,
                voice=request.voice,
                timestamp=timestamp,
                duration_seconds=0.0,
                success=False
            )
            
            memory_store.add_entry(memory_entry)
        except:
            pass  # Ignore memory errors in error handling
        
        return state
    
    def _should_continue(self, state: WorkflowState) -> str:
        """Determine if the workflow should continue or handle error."""
        return "continue" if state["success"] else "error"
    
    async def generate_podcast(self, request: PodcastRequest) -> PodcastResponse:
        """
        Generate a podcast using the workflow.
        
        Args:
            request: The podcast generation request
            
        Returns:
            Podcast generation response
        """
        try:
            # Initialize state
            initial_state = WorkflowState(
                request=request,
                script="",
                audio_data=b"",
                audio_file_path="",
                duration_seconds=0.0,
                success=False,
                error_message="",
                user_preferences={},
                timestamp=time.time()
            )
            
            # Run the workflow
            final_state = await self.graph.ainvoke(initial_state)
            
            # Create response
            response = PodcastResponse(
                success=final_state["success"],
                audio_file_path=final_state.get("audio_file_path"),
                duration_seconds=final_state.get("duration_seconds"),
                error_message=final_state.get("error_message"),
                topic=request.topic,
                voice_used=request.voice.value
            )
            
            return response
            
        except Exception as e:
            return PodcastResponse(
                success=False,
                error_message=f"Workflow execution failed: {str(e)}",
                topic=request.topic,
                voice_used=request.voice.value
            )


# Global workflow instance
podcast_workflow = PodcastWorkflow() 