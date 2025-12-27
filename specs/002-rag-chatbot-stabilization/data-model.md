# Data Model: RAG Chatbot Stabilization

**Feature**: 002-rag-chatbot-stabilization
**Date**: 2025-12-27

## Entities

### ChatMessage

Represents a single message in a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string | UUID, unique | Message identifier |
| session_id | string | UUID, required | Parent session reference |
| role | enum | "user" \| "assistant" | Message sender type |
| content | string | max 10000 chars | Message text content |
| citations | string[] | optional | Array of chunk IDs used for response |
| confidence | float | 0.0-1.0, optional | Grounding confidence score |
| created_at | datetime | auto-generated | Message timestamp |
| error | boolean | default false | Indicates error response |

**Validation Rules**:
- User messages: content length 1-2000 characters
- Assistant messages: content length 1-10000 characters
- Citations only present for assistant messages

### ContextChunk

A segment of textbook content stored in Qdrant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| chunk_id | string | UUID, unique | Chunk identifier |
| content | string | 500-1000 tokens | Text content |
| embedding | float[] | 1024 dimensions | Cohere embedding vector |
| metadata.module | string | required | Module name (locked list) |
| metadata.chapter | string | required | Chapter title |
| metadata.subsection | string | optional | Subsection title |
| metadata.page_reference | string | optional | Source file path |
| metadata.source_type | string | "textbook" | Content source type |
| created_at | datetime | auto-generated | Ingestion timestamp |

**Validation Rules**:
- Module must be one of: "ros2-nervous-system", "digital-twin", "ai-robot-brain", "vla"
- Content must be non-empty
- Embedding dimension must match model (1024 for Cohere v3)

### ChatSession

A conversation context.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| session_id | string | UUID, unique | Session identifier |
| created_at | datetime | auto-generated | Session start time |
| updated_at | datetime | auto-updated | Last activity time |
| message_count | integer | >= 0 | Total messages in session |

**State Transitions**:
- Created → Active (on first message)
- Active → Active (on subsequent messages)
- Active → Expired (after 24h inactivity, handled by cleanup job)

### EmbeddingRequest

Internal request structure for Cohere API.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| texts | string[] | 1-96 items | Texts to embed |
| model | string | "embed-english-v3.0" | Embedding model |
| input_type | enum | "search_query" \| "search_document" | Query vs document embedding |

## Relationships

```
ChatSession 1───* ChatMessage
    │
    └── session_id

ContextChunk *───* ChatMessage (via citations)
    │
    └── chunk_id referenced in citations[]
```

## Indexes

### Qdrant Collection: textbook_rag

- Vector index: HNSW on embedding field (cosine distance)
- Payload index: metadata.module (keyword)
- Payload index: metadata.chapter (keyword)

### Postgres (if conversation persistence enabled)

- Primary: chat_sessions(session_id)
- Primary: chat_messages(id)
- Foreign key: chat_messages(session_id) → chat_sessions(session_id)
- Index: chat_messages(session_id, created_at)
