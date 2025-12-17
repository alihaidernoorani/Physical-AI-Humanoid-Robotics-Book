from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
import os

Base = declarative_base()

class PersonalizationSettings(Base):
    """
    Database model for user personalization settings
    """
    __tablename__ = "personalization_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    learning_level = Column(String(20), default="intermediate")  # beginner, intermediate, advanced
    preferred_language = Column(String(10), default="en")
    last_accessed_module = Column(String(200))
    custom_preferences = Column(Text)  # JSON string for additional preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TranslationCache(Base):
    """
    Database model for cached translations
    """
    __tablename__ = "translation_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_id = Column(String(100), unique=True, index=True, nullable=False)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), default="en")
    target_language = Column(String(10), nullable=False)
    content_hash = Column(String(64), index=True, nullable=False)  # SHA-256 hash
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    hit_count = Column(Integer, default=1)  # Track how often this translation is used

class UserSession(Base):
    """
    Database model for user sessions (for tracking usage and preferences)
    """
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(String(100), index=True)
    module_accessed = Column(String(200))
    chapter_accessed = Column(String(200))
    last_activity = Column(DateTime, default=datetime.utcnow)
    preferences = Column(Text)  # JSON string for session-specific preferences
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatHistory(Base):
    """
    Database model for storing chat history
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True)
    session_id = Column(String(100), index=True)
    query_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    citations = Column(Text)  # JSON string of citations
    confidence_score = Column(Float, default=0.0)
    grounded_chunks = Column(Text)  # JSON string of chunk IDs
    is_fallback = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_database_url():
    """
    Get database URL from environment or default to SQLite for development
    """
    database_url = os.getenv("NEON_DB_URL")
    if not database_url:
        # Fallback to SQLite for development
        database_url = "sqlite:///./rag_backend.db"
    return database_url

def create_database_engine():
    """
    Create database engine with the appropriate URL
    """
    database_url = get_database_url()
    return create_engine(database_url)

def create_database_tables():
    """
    Create all database tables
    """
    engine = create_database_engine()
    Base.metadata.create_all(bind=engine)
    return engine

# Create session factory
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Additional Pydantic models for API validation (if needed)
from pydantic import BaseModel
from typing import Optional, Dict, Any

class PersonalizationSettingsCreate(BaseModel):
    user_id: str
    learning_level: Optional[str] = "intermediate"
    preferred_language: Optional[str] = "en"
    last_accessed_module: Optional[str] = None
    custom_preferences: Optional[Dict[str, Any]] = None

class PersonalizationSettingsUpdate(BaseModel):
    learning_level: Optional[str] = None
    preferred_language: Optional[str] = None
    last_accessed_module: Optional[str] = None
    custom_preferences: Optional[Dict[str, Any]] = None

class TranslationCacheCreate(BaseModel):
    original_text: str
    target_language: str
    source_language: Optional[str] = "en"
    expires_at: Optional[datetime] = None

class TranslationCacheResponse(BaseModel):
    cache_id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    from_cache: bool
    created_at: datetime