# Data Model: ChatWidget Stabilization

## Overview
This document defines the data models for the ChatWidget stabilization feature, focusing on the entities involved in frontend-backend communication and UI state management.

## 1. Core Entities

### ChatMessage
Represents a single message in the chat conversation

**Fields:**
- `id` (string|number): Unique identifier for the message
- `text` (string): The content of the message
- `sender` (enum): Message sender ('user' | 'bot' | 'system')
- `timestamp` (string): ISO 8601 formatted timestamp
- `citations` (string[], optional): Array of source citations for bot responses

**Validation Rules:**
- `id` must be unique within the conversation
- `text` must not be empty
- `sender` must be one of the allowed values
- `timestamp` must be a valid ISO 8601 string

**State Transitions:**
- Created when message is sent/received
- Immutable once created

### ChatSession
Represents a user's chat session with the RAG backend

**Fields:**
- `sessionId` (string): Unique identifier for the session
- `timestamp` (string): ISO 8601 formatted creation time
- `metadata` (object): Additional session metadata
  - `type` (string): Session type ('global-chat', etc.)
  - `userAgent` (string, optional): Client information
  - `pageContext` (string, optional): Context of the current page

**Validation Rules:**
- `sessionId` must be unique
- `timestamp` must be a valid ISO 8601 string
- `metadata.type` must be specified

**State Transitions:**
- Created when user first opens chat
- Active while user is interacting
- May be persisted across page navigation

### ChatState
Represents the UI state of the ChatWidget

**Fields:**
- `isVisible` (boolean): Whether the chat window is visible
- `isLoading` (boolean): Whether a message request is in progress
- `error` (string|null): Error message if any
- `messages` (ChatMessage[]): Array of messages in the conversation
- `currentSessionId` (string|null): ID of the current chat session

**Validation Rules:**
- `isLoading` and error state should be mutually exclusive in UI
- `messages` should maintain chronological order
- `currentSessionId` should be consistent with backend session

**State Transitions:**
- `isVisible`: toggled by user interaction
- `isLoading`: set true when sending/receiving, false when complete
- `error`: set when error occurs, cleared when resolved
- `messages`: appended when new messages arrive
- `currentSessionId`: set when session is created

## 2. API Request/Response Models

### SendMessageRequest
Model for sending messages to the backend

**Fields:**
- `query` (string): The user's query message
- `session_id` (string): The current session ID
- `context` (object, optional): Additional context information
  - `current_page` (string): Current page URL or identifier
  - `referrer` (string): Referring page if applicable

**Validation Rules:**
- `query` must not be empty
- `session_id` must be valid
- `context` fields are optional but should be meaningful if provided

### SendMessageResponse
Model for responses from the backend

**Fields:**
- `response` (string, optional): The response text (deprecated)
- `answer` (string): The response text
- `citations` (string[], optional): Array of source citations
- `session_id` (string, optional): Session ID confirmation
- `metadata` (object, optional): Additional response metadata

**Validation Rules:**
- Either `response` or `answer` must be present (prefer `answer`)
- `citations` should be valid source references
- `session_id` should match the request if provided

### CreateSessionRequest
Model for creating a new chat session

**Fields:**
- `timestamp` (string): ISO 8601 formatted creation time
- `metadata` (object): Session metadata
  - `type` (string): Session type ('global-chat')
  - `pageContext` (string, optional): Context of the page where session started

**Validation Rules:**
- `timestamp` must be a valid ISO 8601 string
- `metadata.type` must be specified

### CreateSessionResponse
Model for session creation response

**Fields:**
- `session_id` (string): The created session ID
- `timestamp` (string): Session creation time
- `status` (string): Creation status ('success' | 'error')

**Validation Rules:**
- `session_id` must be provided and valid
- `status` must be 'success' for successful creation

## 3. Relationships

### ChatSession → ChatMessage (1 to many)
- One chat session contains many messages
- Messages are associated with a specific session via session_id

### ChatState → ChatSession (1 to 1)
- One chat state corresponds to one active session
- Chat state manages the UI representation of the session

## 4. Constraints

### Data Integrity
- Message ordering must be preserved (chronological)
- Session IDs must be unique and consistent between frontend and backend
- User data must not be stored without consent

### Performance
- Message history should be paginated for large conversations
- Session data should be efficiently stored and retrieved
- Response times should meet performance goals (<10s for 90% of queries)

### Security
- Session IDs should be treated as sensitive information
- No PII should be transmitted in messages without explicit user consent
- API requests should include appropriate authentication if required