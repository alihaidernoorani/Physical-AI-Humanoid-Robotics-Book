# Data Model: RAG Chatbot Architecture Migration

## Entities

### 1. ChatSession
**Description**: Represents a user's chat session with the RAG system
- **Fields**:
  - id: UUID (primary key)
  - user_id: Optional[str] - Identifier for authenticated users
  - created_at: datetime - Timestamp of session creation
  - updated_at: datetime - Timestamp of last activity
  - metadata: Dict[str, Any] - Additional session-specific data
- **Relationships**: Contains multiple UserQuery entities
- **Validation**: Session must have valid timestamps and optional user_id format

### 2. UserQuery
**Description**: Represents a single query from a user within a chat session
- **Fields**:
  - id: UUID (primary key)
  - session_id: UUID - Reference to parent ChatSession
  - query_text: str - The original user query
  - selected_text: Optional[str] - Text selected by user for selected-text mode
  - query_mode: ChatMode - Enum indicating full_text or selected_text mode
  - timestamp: datetime - When the query was submitted
- **Relationships**: Belongs to one ChatSession, generates one GeneratedResponse
- **Validation**: query_text must be non-empty, query_mode must be valid enum value

### 3. GeneratedResponse
**Description**: Represents the AI-generated response to a user query
- **Fields**:
  - id: UUID (primary key)
  - session_id: UUID - Reference to parent ChatSession
  - query_id: UUID - Reference to the corresponding UserQuery
  - response_text: str - The generated response text
  - citations: List[str] - Paths to sources used in the response
  - grounding_confidence: float - Confidence score for response grounding (0.0-1.0)
  - generated_at: datetime - When the response was generated
  - response_metadata: Dict[str, Any] - Additional metadata about the response
- **Relationships**: Belongs to one ChatSession and one UserQuery
- **Validation**: grounding_confidence must be between 0.0 and 1.0, citations must be valid paths

### 4. RetrievedContext
**Description**: Represents the contextual information retrieved from the textbook for response generation
- **Fields**:
  - id: str - Unique identifier for the context chunk
  - content: str - The actual text content retrieved
  - module_name: str - Name of the textbook module
  - chapter_title: str - Title of the chapter containing the content
  - section_path: str - Full path to the content section
  - token_count: int - Number of tokens in the content
  - similarity_score: float - Similarity score from embedding search
  - metadata: Dict[str, Any] - Additional context metadata
- **Relationships**: Used by GeneratedResponse during response generation
- **Validation**: similarity_score must be between 0.0 and 1.0, content must be non-empty

### 5. TextChunk
**Description**: Represents a chunk of textbook content stored in the vector database
- **Fields**:
  - id: str - Unique identifier for the chunk
  - content: str - The text content of the chunk
  - module_name: str - Name of the textbook module
  - chapter_title: str - Title of the chapter
  - section_path: str - Full path to the section
  - token_count: int - Number of tokens in the chunk
  - embedding_vector: List[float] - Numerical representation of the content
  - metadata: Dict[str, Any] - Additional chunk metadata
- **Relationships**: Stored in Qdrant vector database
- **Validation**: content must be within 300-500 token range, embedding_vector must have correct dimensions

### 6. ChatMode
**Description**: Enumeration representing different chat modes
- **Values**:
  - full_text: Search across entire textbook
  - selected_text: Use only selected text as context
- **Usage**: Determines how context is retrieved for response generation

## State Transitions

### ChatSession State Transitions
- ACTIVE: Session is active and accepting new queries
- INACTIVE: Session has been idle for a period
- ARCHIVED: Session is preserved for history but not active

### UserQuery Processing Flow
1. RECEIVED: Query is received from user
2. EMBEDDING_GENERATED: Embedding is created for the query
3. CONTEXT_RETRIEVED: Relevant context is retrieved from vector database
4. RESPONSE_GENERATING: AI is generating the response
5. RESPONSE_GENERATED: Response is ready for the user

## Relationships

- ChatSession (1) ←→ (Many) UserQuery: One session contains many queries
- UserQuery (1) ←→ (1) GeneratedResponse: One query generates one response
- UserQuery (Many) ←→ (Many) RetrievedContext: Queries use multiple context chunks
- RetrievedContext (Many) ←→ (Many) TextChunk: Retrieved contexts come from text chunks

## Validation Rules

### Content Validation
- All text content must be original and properly sourced per constitution
- No hallucinated references or fabricated information
- Textbook content must maintain academic accuracy

### Grounding Validation
- Responses must be grounded in retrieved context
- If insufficient context exists, system must refuse to answer
- Citation paths must be valid and accessible

### Safety Validation
- All responses must comply with safety constraints
- Refusal mechanisms must be preserved
- No generation of unsafe or inappropriate content