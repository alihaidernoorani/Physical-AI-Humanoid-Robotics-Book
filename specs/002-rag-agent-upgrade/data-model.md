# Data Model: RAG Agent Upgrade

## Entity Definitions

### Chat Session
- **Purpose**: Represents a user's interaction with the RAG system, containing conversation history and context
- **Fields**:
  - `id`: UUID (primary key)
  - `user_id`: UUID (optional, for registered users)
  - `session_token`: String (for anonymous users)
  - `created_at`: DateTime (timestamp)
  - `updated_at`: DateTime (timestamp)
  - `messages`: List of Message objects
  - `metadata`: JSON (additional session data)

### Message
- **Purpose**: Represents a single message in a chat conversation
- **Fields**:
  - `id`: UUID (primary key)
  - `session_id`: UUID (foreign key to ChatSession)
  - `role`: String (user/assistant/system)
  - `content`: String (message text)
  - `timestamp`: DateTime
  - `citations`: List of Citation objects (for RAG responses)
  - `selected_text`: String (optional, text selected from frontend)

### Vector Embedding
- **Purpose**: Mathematical representation of text content used for similarity search in the RAG system
- **Fields**:
  - `id`: UUID (primary key)
  - `text_content`: String (original text)
  - `embedding_vector`: List of Float (vector representation)
  - `model_name`: String (e.g., "cohere/embed-multilingual-v3.0")
  - `created_at`: DateTime
  - `metadata`: JSON (source information, module, chapter, etc.)

### Knowledge Base Chunk
- **Purpose**: Collection of textbook content and related materials stored in Qdrant vector database
- **Fields**:
  - `id`: UUID (primary key in Qdrant)
  - `content`: String (text chunk)
  - `module`: String (e.g., "The Robotic Nervous System (ROS 2)")
  - `chapter`: String (chapter name)
  - `subsection`: String (subsection name)
  - `source_type`: String (e.g., "textbook", "diagram_description", "exercise")
  - `source_origin`: String (file path or URL)
  - `embedding_id`: UUID (foreign key to VectorEmbedding)
  - `metadata`: JSON (additional context)

### User Preferences
- **Purpose**: Settings that control personalization and translation preferences for individual users
- **Fields**:
  - `id`: UUID (primary key)
  - `user_id`: UUID (optional, for registered users)
  - `session_token`: String (for anonymous users)
  - `language_preference`: String (e.g., "en", "ur")
  - `learning_level`: String (e.g., "beginner", "intermediate", "advanced")
  - `personalization_enabled`: Boolean
  - `created_at`: DateTime
  - `updated_at`: DateTime

## Validation Rules

### Chat Session Validation
- Session must have either user_id or session_token (not both null)
- Messages list cannot exceed 1000 items
- Session must be updated within 24 hours or be considered expired

### Message Validation
- Content must be between 1 and 10,000 characters
- Role must be one of: "user", "assistant", "system"
- Must have valid session_id reference

### Vector Embedding Validation
- embedding_vector must have consistent dimensions (based on model)
- model_name must be one of supported embedding models
- text_content must not be empty

### Knowledge Base Chunk Validation
- content must be between 50 and 2000 tokens
- module must be one of the 4 fixed textbook modules
- metadata must include required source information

### User Preferences Validation
- language_preference must be one of supported languages
- learning_level must be one of: "beginner", "intermediate", "advanced"
- Only one of user_id or session_token should be set

## State Transitions

### Chat Session States
- `active`: New session, ready for messages
- `in-progress`: Session has messages, still active
- `completed`: Session completed naturally
- `expired`: Session timed out (24+ hours since last activity)
- `archived`: Session data archived for storage optimization

## Relationships

### Chat Session ↔ Message
- One-to-Many: One ChatSession can have many Messages
- Cascade delete: Messages deleted when parent ChatSession is deleted

### Vector Embedding ↔ Knowledge Base Chunk
- One-to-One: Each Knowledge Base Chunk has one Vector Embedding
- Foreign key: knowledge_base_chunk.embedding_id → vector_embedding.id

### User Preferences ↔ Chat Session
- One-to-Many: One UserPreference can be associated with many ChatSessions
- Optional relationship: Anonymous sessions may not have UserPreferences