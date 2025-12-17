from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RetrievalMode(str, Enum):
    full_book = "full-book"
    per_page = "per-page"

class RAGQuery(BaseModel):
    """
    A user's question that requires contextual response based on textbook content
    """
    query_text: str = Field(..., min_length=1, max_length=1000, description="The user's question text")
    retrieval_mode: RetrievalMode = Field(default=RetrievalMode.full_book, description="Retrieval mode: full-book or per-page")
    selected_text: Optional[str] = Field(None, description="Text selected by user in per-page mode")
    user_id: Optional[str] = Field(None, description="Identifier for personalization")
    metadata_filters: Optional[Dict[str, str]] = Field(default_factory=dict, description="Filters for module/chapter/subsection if specified")

    class Config:
        use_enum_values = True

class KnowledgeChunk(BaseModel):
    """
    A segment of textbook content stored in vector database with metadata
    """
    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    content: str = Field(..., min_length=50, max_length=2000, description="The actual text content of the chunk")
    embedding: List[float] = Field(..., description="Vector embedding representation of the content")
    module: str = Field(..., description="Module name (The Robotic Nervous System (ROS 2), etc.)")
    chapter: str = Field(..., description="Chapter name within the module")
    subsection: str = Field(..., description="Subsection name within the chapter")
    source_type: str = Field(..., description="Type of source (e.g., 'textbook', 'diagram', 'exercise')")
    source_origin: str = Field(..., description="Original source location")
    page_reference: str = Field(..., description="Page or section reference for citation")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when chunk was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when chunk was last updated")

class ChatResponse(BaseModel):
    """
    The system's answer to a user query with citations to source material
    """
    response_id: str = Field(..., description="Unique identifier for the response")
    query_id: Optional[str] = Field(None, description="Reference to the original query")
    response_text: str = Field(..., max_length=5000, description="The AI-generated response text")
    citations: List[Dict[str, Any]] = Field(default_factory=list, description="List of source citations used in response")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the response (0.0-1.0)")
    grounded_chunks: List[str] = Field(default_factory=list, description="IDs of chunks that grounded this response")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when response was generated")
    is_fallback: bool = Field(default=False, description="Whether this is a fallback response due to insufficient grounding")

class Citation(BaseModel):
    """
    Citation model for referencing source material
    """
    chunk_id: str
    module: str
    chapter: str
    subsection: str
    page_reference: str

class RAGResponse(BaseModel):
    """
    Complete response model for the RAG endpoint
    """
    response_id: str
    response_text: str
    citations: List[Citation] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)
    grounded_chunks: List[str] = Field(default_factory=list)
    is_fallback: bool = Field(default=False)