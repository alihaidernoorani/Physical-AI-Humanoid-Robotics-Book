# Data Model: Fix Chat API Field Mismatch

**Feature Branch**: `001-fix-chat-field-mismatch`
**Date**: 2025-12-27

## Entities

### ChatMessageRequest

The payload sent from frontend to backend for chat messages.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | The user's question or input text |
| session_id | string | No | Session identifier for conversation continuity |
| selected_text | string | No | Optional selected text from page for context |
| user_preferences | object | No | User personalization preferences |
| retrieval_mode | string | No | RAG retrieval mode ("full-book" default) |
| metadata_filters | object | No | Optional filters for RAG retrieval |

**Validation Rules**:
- `message` cannot be empty or whitespace-only
- `session_id` should be a valid UUID or null (backend will create one)

### ChatMessageResponse

The response returned from the chat endpoint.

| Field | Type | Description |
|-------|------|-------------|
| response | string | AI-generated response text |
| session_id | string | Session ID (created if not provided) |
| citations | array[string] | List of chunk IDs used for context |
| response_time_ms | number | Processing time in milliseconds |
| timestamp | string | ISO 8601 timestamp |

### ErrorResponse

The error payload returned when requests fail.

| Field | Type | Description |
|-------|------|-------------|
| detail | string | Human-readable error description |

**HTTP Status Code Mapping**:
- 400: Validation errors (empty message, invalid format)
- 401: Authentication errors
- 403: Authorization errors
- 500: Internal server errors (genuine exceptions)

## State Transitions

This is a stateless request-response pattern. No state machine required.

## Relationships

```
ChatMessageRequest → Backend Processing → ChatMessageResponse
                         ↓ (on error)
                    ErrorResponse
```

## Field Name Alignment

### Before (Bug)

Frontend sends:
```json
{
  "query": "What is ROS 2?",
  "session_id": "abc-123"
}
```

Backend expects:
```json
{
  "message": "What is ROS 2?",
  "session_id": "abc-123"
}
```

### After (Fix)

Frontend sends (aligned with backend):
```json
{
  "message": "What is ROS 2?",
  "session_id": "abc-123"
}
```
