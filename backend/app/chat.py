from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, List
import logging
from datetime import datetime
import asyncio

from .agent import agent_config
from .rag import rag_service
from .config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest:
    def __init__(self, message: str, selected_text: str = None, user_preferences: Dict = None):
        self.message = message
        self.selected_text = selected_text
        self.user_preferences = user_preferences or {}

class TranslateRequest:
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language

class PersonalizeRequest:
    def __init__(self, text: str, learning_level: str = "intermediate"):
        self.text = text
        self.learning_level = learning_level

@router.post("/chat")
async def chat_endpoint(request: Dict[str, Any]):
    """
    Main chat endpoint with RAG functionality
    """
    start_time = datetime.utcnow()

    try:
        message = request.get("message", "")
        selected_text = request.get("selected_text", "")
        user_preferences = request.get("user_preferences", {})

        if not message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is required"
            )

        logger.info(f"Processing chat request: {message[:50]}...")

        # Retrieve context from RAG system
        retrieval_mode = request.get("retrieval_mode", "full-book")
        metadata_filters = request.get("metadata_filters", None)

        context_chunks = rag_service.retrieve_context(
            query=message,
            retrieval_mode=retrieval_mode,
            selected_text=selected_text if selected_text else None,
            metadata_filters=metadata_filters
        )

        logger.info(f"Retrieved {len(context_chunks)} context chunks")

        # Process with agent using context
        response_text = await agent_config.process_with_context(
            query=message,
            context_chunks=context_chunks,
            selected_text=selected_text if selected_text else None
        )

        # Add message to conversation
        session_id = request.get("session_id")
        if not session_id:
            session_id = agent_config.create_conversation()
        else:
            # Ensure conversation exists
            existing_conversation = agent_config.get_conversation(session_id)
            if not existing_conversation:
                session_id = agent_config.create_conversation(session_id)

        # Add user message to conversation
        agent_config.add_message_to_conversation(session_id, {
            "role": "user",
            "content": message,
            "citations": [chunk["chunk_id"] for chunk in context_chunks],
            "selected_text": selected_text
        })

        # Add assistant response to conversation
        agent_config.add_message_to_conversation(session_id, {
            "role": "assistant",
            "content": response_text,
            "citations": [chunk["chunk_id"] for chunk in context_chunks],
            "selected_text": ""
        })

        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        logger.info(f"Chat request processed in {response_time:.2f}ms")

        return {
            "response": response_text,
            "session_id": session_id,
            "citations": [chunk["chunk_id"] for chunk in context_chunks],
            "response_time_ms": response_time,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/translate")
async def translate_endpoint(request: Dict[str, Any]):
    """
    Translation endpoint using textbook content
    """
    try:
        text = request.get("text", "")
        target_language = request.get("target_language", "ur")  # Default to Urdu

        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required"
            )

        logger.info(f"Translating text to {target_language}")

        # For now, we'll use a simple approach - in a real implementation,
        # this would use Cohere's translation capabilities or a translation model
        # Since we're using the agent with textbook context, we'll ask the agent to translate

        translation_prompt = f"Translate the following text to {target_language}: {text}"

        # Retrieve relevant context for better translation
        context_chunks = rag_service.retrieve_context(
            query=text,
            retrieval_mode="full-book"
        )

        # Process with agent using context
        translated_text = await agent_config.process_with_context(
            query=translation_prompt,
            context_chunks=context_chunks
        )

        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in translate endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/personalize")
async def personalize_endpoint(request: Dict[str, Any]):
    """
    Personalization endpoint using textbook content
    """
    try:
        text = request.get("text", "")
        learning_level = request.get("learning_level", "intermediate")
        user_preferences = request.get("user_preferences", {})

        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required"
            )

        logger.info(f"Personalizing content for level: {learning_level}")

        # Create a prompt that adapts the content based on learning level
        level_descriptions = {
            "beginner": "simple terms with basic explanations and analogies",
            "intermediate": "moderate detail with technical terms explained",
            "advanced": "detailed technical explanation with advanced terminology"
        }

        level_description = level_descriptions.get(learning_level, level_descriptions["intermediate"])

        personalization_prompt = f"""
        Adapt the following content for a {learning_level} level learner ({level_description}):

        {text}
        """

        # Retrieve relevant context for better personalization
        context_chunks = rag_service.retrieve_context(
            query=text,
            retrieval_mode="full-book"
        )

        # Process with agent using context
        personalized_text = await agent_config.process_with_context(
            query=personalization_prompt,
            context_chunks=context_chunks
        )

        return {
            "original_text": text,
            "personalized_text": personalized_text,
            "learning_level": learning_level,
            "user_preferences": user_preferences,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in personalize endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/health")
def health_check():
    """
    Health check endpoint
    """
    try:
        # Check each service
        agent_healthy = True  # Agent service is initialized at startup
        rag_healthy = rag_service.health_check()

        all_healthy = all([agent_healthy, rag_healthy])

        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "services": {
                "agent": agent_healthy,
                "rag": rag_healthy,
                "neon_db": True  # Assuming DB is healthy if we can reach this endpoint
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "services": {
                "agent": False,
                "rag": False,
                "neon_db": False
            },
            "timestamp": datetime.utcnow().isoformat()
        }