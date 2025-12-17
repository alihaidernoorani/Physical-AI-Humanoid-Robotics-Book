# Data Model: RAG Backend & Frontend Integration

## Entity: RAG Query
**Description**: A user's question that requires contextual response based on textbook content
**Fields**:
- `query_text` (string): The user's question text
- `retrieval_mode` (enum): "full-book" or "per-page"
- `selected_text` (string, optional): Text selected by user in per-page mode
- `user_id` (string, optional): Identifier for personalization
- `metadata_filters` (object): Filters for module/chapter/subsection if specified

## Entity: Knowledge Chunk
**Description**: A segment of textbook content stored in vector database with metadata
**Fields**:
- `chunk_id` (string): Unique identifier for the chunk
- `content` (string): The actual text content of the chunk
- `embedding` (array): Vector embedding representation of the content
- `module` (string): Module name (The Robotic Nervous System (ROS 2), etc.)
- `chapter` (string): Chapter name within the module
- `subsection` (string): Subsection name within the chapter
- `source_type` (string): Type of source (e.g., "textbook", "diagram", "exercise")
- `source_origin` (string): Original source location
- `page_reference` (string): Page or section reference for citation
- `created_at` (datetime): Timestamp when chunk was created
- `updated_at` (datetime): Timestamp when chunk was last updated

## Entity: Chat Response
**Description**: The system's answer to a user query with citations to source material
**Fields**:
- `response_id` (string): Unique identifier for the response
- `query_id` (string): Reference to the original query
- `response_text` (string): The AI-generated response text
- `citations` (array): List of source citations used in response
- `confidence_score` (float): Confidence level of the response (0.0-1.0)
- `grounded_chunks` (array): IDs of chunks that grounded this response
- `created_at` (datetime): Timestamp when response was generated
- `is_fallback` (boolean): Whether this is a fallback response due to insufficient grounding

## Entity: Environment Configuration
**Description**: Securely stored API keys and service endpoints
**Fields**:
- `cohere_api_key` (string): API key for Cohere embedding service
- `gemini_api_key` (string): API key for Gemini model access
- `qdrant_url` (string): URL for Qdrant vector database
- `qdrant_api_key` (string): API key for Qdrant access
- `neon_db_url` (string): Connection string for Neon Postgres
- `debug_mode` (boolean): Whether to enable debug logging

## Entity: Personalization Settings
**Description**: User-specific settings for content delivery
**Fields**:
- `user_id` (string): Unique identifier for the user
- `learning_level` (enum): "beginner", "intermediate", "advanced"
- `preferred_language` (string): Default language preference
- `last_accessed_module` (string): Most recently accessed module
- `custom_preferences` (object): Additional user preferences

## Entity: Translation Cache
**Description**: Cached translations for performance optimization
**Fields**:
- `cache_id` (string): Unique identifier for the cache entry
- `original_text` (string): Original English text
- `translated_text` (string): Translated text (e.g., Urdu)
- `source_language` (string): Language of original text
- `target_language` (string): Language of translated text
- `content_hash` (string): Hash to detect content changes
- `created_at` (datetime): Timestamp when cached
- `expires_at` (datetime): Expiration timestamp for cache entry

## Relationships

### RAG Query → Knowledge Chunk
- A RAG query retrieves multiple Knowledge Chunks based on semantic similarity
- Relationship: One-to-Many (query can reference multiple chunks)

### Knowledge Chunk → Chat Response
- Multiple Knowledge Chunks may contribute to a single Chat Response
- Relationship: Many-to-Many (chunks can be used in multiple responses)

### User → Personalization Settings
- Each User has one set of Personalization Settings
- Relationship: One-to-One

### Chat Response → Translation Cache
- A Chat Response may have cached translations
- Relationship: One-to-Many (one response can have multiple language translations)

## Validation Rules

### RAG Query Validation
- `query_text` must be 1-1000 characters
- `retrieval_mode` must be either "full-book" or "per-page"
- If `retrieval_mode` is "per-page", `selected_text` must be provided

### Knowledge Chunk Validation
- `content` must be 50-2000 characters (per constitution chunk size requirements)
- All metadata fields (module, chapter, subsection) must be non-empty
- `embedding` must be a valid vector array

### Chat Response Validation
- `confidence_score` must be between 0.0 and 1.0
- `citations` must reference valid Knowledge Chunk IDs
- `response_text` must not exceed 5000 characters

### Environment Configuration Validation
- All API keys must be properly formatted
- URLs must be valid and accessible
- No sensitive information should be logged

## State Transitions

### RAG Query States
- `pending` → `processing` → `completed` | `failed`
- Status tracking for query lifecycle

### Chat Response States
- `generating` → `validated` → `delivered` | `rejected`
- Quality validation before delivery

### Translation Cache States
- `requested` → `generating` → `cached` | `expired`
- Cache lifecycle management