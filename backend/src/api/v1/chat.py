from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum
from src.models.chat_session import ChatMode, UserQuery, GeneratedResponse
from src.services.chat_service import ChatService


router = APIRouter()

# Initialize the chat service
chat_service = ChatService()


class ChatRequest(BaseModel):
    query: str
    mode: ChatMode = ChatMode.full_text
    selected_text: Optional[str] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    citations: List[str] = Field(default_factory=list)
    grounding_confidence: float = Field(ge=0.0, le=1.0)
    generated_at: datetime


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class RetrieveResponse(BaseModel):
    contexts: List[dict]
    query: str
    retrieved_at: datetime


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that handles both full-text and selected-text modes.
    """
    # Generate a new session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    # Validate the request based on mode
    if request.mode == ChatMode.selected_text and not request.selected_text:
        raise HTTPException(
            status_code=400,
            detail="selected_text is required when mode is 'selected_text'"
        )

    # Process the query using the chat service
    response = chat_service.process_query(
        query_text=request.query,
        session_id=session_id,
        mode=request.mode,
        selected_text=request.selected_text
    )

    return ChatResponse(
        response=response.response_text,
        session_id=response.session_id,
        citations=response.citations,
        grounding_confidence=response.grounding_confidence,
        generated_at=response.generated_at
    )


@router.post("/chat/retrieve", response_model=RetrieveResponse)
async def retrieve_context(request: RetrieveRequest):
    """
    Endpoint to retrieve relevant contexts from the textbook without generating a response.
    """
    # Placeholder response - in a real implementation, this would call the retrieval service
    contexts = [
        {
            "id": f"context_{i}",
            "content": f"Placeholder context chunk {i} related to '{request.query}'",
            "source_module": "The Robotic Nervous System (ROS 2)",
            "source_chapter": f"Chapter {i+1}",
            "source_section": f"Section {i+1}.{i+1}",
            "similarity_score": 0.85 - (i * 0.05)
        }
        for i in range(request.top_k)
    ]

    return RetrieveResponse(
        contexts=contexts,
        query=request.query,
        retrieved_at=datetime.now()
    )