from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class ChatMode(str, Enum):
    full_text = "full_text"
    selected_text = "selected_text"


class ChatSession(BaseModel):
    id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    mode: ChatMode
    metadata: Optional[Dict] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class RetrievedContext(BaseModel):
    id: str
    session_id: str
    chunk_text: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    source_module: str
    source_chapter: str
    source_section: str
    source_page: Optional[str] = None
    retrieved_at: datetime


class UserQuery(BaseModel):
    id: str
    session_id: str
    query_text: str
    selected_text: Optional[str] = None
    query_mode: ChatMode
    timestamp: datetime

    class Config:
        use_enum_values = True


class GeneratedResponse(BaseModel):
    id: str
    session_id: str
    query_id: str
    response_text: str
    citations: List[str] = Field(default_factory=list)
    grounding_confidence: float = Field(ge=0.0, le=1.0)
    generated_at: datetime
    response_metadata: Optional[Dict] = Field(default_factory=dict)