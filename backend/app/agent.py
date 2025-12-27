from agents import Agent, Runner, ModelSettings
from agents.extensions.models.litellm_model import LitellmModel
from typing import Dict, Any, List, Optional
import json
import logging
import uuid
from datetime import datetime
import asyncio

from .config import settings
from .services.db_manager import get_db_manager

logger = logging.getLogger(__name__)

class AgentSDKConfig:
    """
    Configuration for OpenAI Agents SDK with Gemini bridge and ChatKit protocol-compliant conversation state management
    """
    def __init__(self):
        # Create the model configuration using LiteLLM for Gemini
        self.model = LitellmModel(
            model=f"gemini/{settings.gemini_model}",  # e.g., "gemini/gemini-2.5-flash"
            api_key=settings.gemini_api_key
        )

        # Initialize the agent
        self.agent = Agent(
            name="Textbook RAG Agent",
            instructions="You are an expert AI assistant for a Physical AI and Humanoid Robotics textbook. Answer questions based on the textbook content provided in the context. If you cannot find relevant information in the context, respond with 'I could not find an answer in the book content.'",
            model=self.model,
            model_settings=ModelSettings(
                include_usage=True  # Enable usage tracking
            ),
            tools=[]
        )

        # Initialize database manager with connection pooling and retry logic
        self.db_manager = get_db_manager()

        # Validate schema on startup
        if self.db_manager.is_available:
            self.db_manager.validate_schema()


    def _build_context(self, context_chunks: List[Dict], selected_text: Optional[str] = None) -> str:
        """
        Build context string from chunks and selected text
        """
        if selected_text and selected_text.strip():
            # Prioritize selected text
            if context_chunks:
                context_chunks_text = "\n\n".join([chunk.get("content", "") for chunk in context_chunks])
                return f"Selected text context: {selected_text}\n\nRelevant textbook content: {context_chunks_text}"
            else:
                return f"Selected text context: {selected_text}\n\nNo additional textbook content found."
        else:
            # Use the retrieved chunks as context
            if context_chunks:
                context_chunks_text = "\n\n".join([chunk.get("content", "") for chunk in context_chunks])
                return f"Relevant textbook content: {context_chunks_text}"
            else:
                return "No relevant textbook content found."

    def create_conversation(self, session_id: str = None) -> str:
        """
        Create a new conversation thread in Neon Postgres following ChatKit protocol.
        Returns session_id even if DB write fails (graceful degradation - T063).
        Uses DatabaseManager with connection pooling and retry logic.
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        # Use the new DatabaseManager with retry logic
        if self.db_manager.is_available:
            success = self.db_manager.create_conversation(session_id)
            if not success:
                logger.warning(f"Returning session_id {session_id} without DB persistence (graceful degradation)")
        else:
            logger.warning(f"DB unavailable - returning session_id {session_id} without persistence")

        return session_id

    def get_conversation(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve conversation thread from Neon Postgres following ChatKit protocol.
        Uses DatabaseManager with connection pooling and retry logic.
        """
        return self.db_manager.get_conversation(session_id)

    def add_message_to_conversation(self, session_id: str, message: Dict[str, Any]):
        """
        Add a message to the conversation thread in Neon Postgres following ChatKit protocol.
        Uses DatabaseManager with connection pooling and retry logic.
        """
        role = message.get("role", "user")
        content = message.get("content", "")
        citations = message.get("citations", [])
        selected_text = message.get("selected_text", "")

        self.db_manager.add_message(
            session_id=session_id,
            role=role,
            content=content,
            citations=citations,
            selected_text=selected_text
        )

    async def process_with_context(self, query: str, context_chunks: List[Dict], selected_text: Optional[str] = None) -> str:
        """
        Process query with context, prioritizing selected_text if provided
        """
        try:
            logger.info(f"Processing query: {query[:50]}... with {len(context_chunks)} chunks")

            # Build context from chunks and selected text
            context = self._build_context(context_chunks, selected_text)

            # Prepare the user message with context
            full_message = f"{context}\n\nQuestion: {query}"

            # Use the agent to generate a response (async for FastAPI compatibility)
            result = await Runner.run(
                self.agent,
                full_message
            )

            # Extract and return the response text
            response_text = result.final_output
            logger.info(f"Generated response: {response_text[:50]}...")

            return response_text

        except Exception as e:
            logger.error(f"Error processing query with context: {str(e)}")
            return "I could not find an answer in the book content."

# Create a singleton instance
agent_config = AgentSDKConfig()