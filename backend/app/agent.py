from agents import Agent, Runner, ModelSettings
from agents.extensions.models.litellm_model import LitellmModel
from typing import Dict, Any, List, Optional
import json
import logging
from psycopg2.extras import RealDictCursor
import uuid
from datetime import datetime
import asyncio

from .config import settings

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

        # Initialize Neon Postgres connection for conversation storage
        self.db_connection = None
        self._init_db_connection()

    def _init_db_connection(self):
        """
        Initialize connection to Neon Postgres
        """
        try:
            import psycopg2
            self.db_connection = psycopg2.connect(
                settings.database_url,
                cursor_factory=RealDictCursor
            )
            logger.info("Connected to Neon Postgres successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Neon Postgres: {str(e)}")
            # For development, we can continue without DB connection
            pass

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
        Create a new conversation thread in Neon Postgres following ChatKit protocol
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        if self.db_connection:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO conversations (id, created_at, updated_at, metadata)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (session_id, datetime.utcnow(), datetime.utcnow(), json.dumps({}))
                    )
                    self.db_connection.commit()
                    logger.info(f"Created conversation: {session_id}")
            except Exception as e:
                logger.error(f"Failed to create conversation in DB: {str(e)}")
                self.db_connection.rollback()
                raise

        return session_id

    def get_conversation(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve conversation thread from Neon Postgres following ChatKit protocol
        """
        if not self.db_connection:
            return None

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM conversations WHERE id = %s", (session_id,)
                )
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get conversation from DB: {str(e)}")
            return None

    def add_message_to_conversation(self, session_id: str, message: Dict[str, Any]):
        """
        Add a message to the conversation thread in Neon Postgres following ChatKit protocol
        """
        if not self.db_connection:
            return

        try:
            # Validate message fields
            role = message.get("role", "user")
            if role not in ["user", "assistant", "system"]:
                role = "user"  # Default to user if invalid role

            content = message.get("content", "")
            citations = message.get("citations", [])
            selected_text = message.get("selected_text", "")

            message_id = str(uuid.uuid4())
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO messages (id, session_id, role, content, timestamp, citations, selected_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        message_id,
                        session_id,
                        role,
                        content,
                        datetime.utcnow(),
                        json.dumps(citations),  # Serialize JSON field
                        selected_text
                    )
                )
                self.db_connection.commit()
                logger.debug(f"Added message to conversation {session_id}")
        except Exception as e:
            logger.error(f"Failed to add message to conversation in DB: {str(e)}")
            if self.db_connection:
                self.db_connection.rollback()

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