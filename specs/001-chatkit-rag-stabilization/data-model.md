# Data Model: ChatKit + Docusaurus RAG Stabilization

**Date**: 2025-12-28
**Feature**: 001-chatkit-rag-stabilization
**Model Type**: Domain entities and API contracts

## Entity Definitions

### Chat Message
**Description**: A unit of conversation containing text content, sender type, and metadata

**Fields**:
- `id` (string): Unique identifier for the message
- `text` (string): The message content
- `sender` (enum): Message sender type (user|assistant|system)
- `timestamp` (string): ISO 8601 formatted timestamp
- `citations` (array): Optional array of source citations
- `status` (string): Message status (sent|delivered|error)

**Validation Rules**:
- `text` must be non-empty
- `sender` must be one of allowed values
- `timestamp` must be valid ISO 8601 format

### Session
**Description**: A conversation thread identified by session_id that maintains context between messages

**Fields**:
- `session_id` (string): Unique identifier for the conversation session
- `created_at` (string): Session creation timestamp
- `updated_at` (string): Last activity timestamp
- `metadata` (object): Optional session metadata

**Validation Rules**:
- `session_id` must be unique and non-empty
- `created_at` must be valid timestamp

### RAG Response
**Description**: A structured response containing the assistant's answer and relevant citations

**Fields**:
- `response` (string): The assistant's response text
- `session_id` (string): Associated session identifier
- `citations` (array): Array of source citations
- `response_time_ms` (number): Time taken to generate response
- `timestamp` (string): Response creation timestamp

**Validation Rules**:
- `response` must be non-empty
- `session_id` must exist
- `response_time_ms` must be positive number

## API Contracts

### POST /api/v1/chat
**Description**: Main chat endpoint for sending messages and receiving responses

**Request Body**:
```json
{
  "message": "string (required)",
  "session_id": "string (optional)",
  "retrieval_mode": "string (optional, default: full-book)",
  "metadata_filters": "object (optional)"
}
```

**Response Body (Success - 200)**:
```json
{
  "response": "string",
  "session_id": "string",
  "citations": "array of strings",
  "response_time_ms": "number",
  "timestamp": "string"
}
```

**Response Codes**:
- `200`: Success - message processed and response returned
- `400`: Client error - invalid request parameters
- `500`: Server error - unexpected internal error

**Validation**:
- `message` is required and non-empty
- `message` must be string type
- `message` length must be within configured limits

### GET /api/v1/health
**Description**: Health check endpoint for backend services

**Response Body (Success - 200)**:
```json
{
  "status": "string",
  "services": {
    "agent": "boolean",
    "rag": "boolean",
    "neon_db": "boolean"
  },
  "database": {
    "healthy": "boolean",
    "message": "string",
    "pool_status": "string"
  },
  "timestamp": "string"
}
```

## State Transitions

### Message State Flow
```
Initial → Sent → Delivered → Read
        ↓
      Error → Retry → Delivered
```

### Session State Flow
```
Created → Active → Inactive → Closed
```

## Payload Contracts

### Frontend to Backend
**Request Contract**:
- Field name: "message" (required)
- Field name: "session_id" (optional)
- Must follow { message: string, session_id: string } structure

### Backend to Frontend
**Response Contract**:
- Field name: "response" (assistant response text)
- Field name: "session_id" (session identifier)
- Field name: "citations" (source references)

## Validation Rules Summary

1. **Message Validation**:
   - Content length within configured limits (max_message_length)
   - Non-empty text content
   - Valid sender type

2. **Session Validation**:
   - Valid session_id format
   - Session exists before processing

3. **Error Handling**:
   - 400 errors must remain 400 (not converted to 500)
   - HTTPException must be re-thrown, not wrapped

## Data Flow

### Message Processing Flow
1. Frontend sends { message, session_id } to backend
2. Backend validates message content and structure
3. RAG service retrieves context from Qdrant
4. Agent processes query with context
5. Response returned to frontend
6. Frontend appends response to message state via setMessages(prev => [...prev, assistantMessage])

### Error Flow
1. Validation errors return appropriate HTTP status (400)
2. Unexpected errors return 500 status
3. No conversion of 4xx to 500 status

## Constraints

- No architectural rewrites
- Maintain existing data models
- Preserve existing Qdrant collection structure
- Keep current Cohere embedding model (embed-multilingual-v3.0)
- Maintain relevance threshold (0.35)