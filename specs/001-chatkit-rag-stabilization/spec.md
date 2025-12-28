# Feature Specification: ChatKit + Docusaurus RAG Stabilization

**Feature Branch**: `001-chatkit-rag-stabilization`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "ChatKit + Docusaurus RAG stabilization and UI correctness

Target system:
- Docusaurus static site (frontend)
- ChatKit widget (React)
- FastAPI backend deployed on Hugging Face Spaces
- RAG stack: Cohere embeddings + Qdrant vector DB

Primary goals:
1. Chat messages must send and display correctly without refresh
2. RAG must return answers from existing Qdrant data
3. Backend must return correct HTTP status codes (no false 500s)
4. Frontend-backend payload contract must be aligned and stable

Success criteria:
- Sending a message displays user message immediately
- Assistant response appears without minimizing or refreshing widget
- POST /api/v1/chat returns 200 for valid requests
- Backend never converts 4xx errors into 500 errors
- Asking: "What is the title of the first chapter?" returns a correct answer
- RAG retrieves results from Qdrant using existing collection

System contracts (must not change):
- Frontend payload field name: "message"
- Backend expects: { message: string, session_id: string }
- Embedding model: embed-multilingual-v3.0
- Qdrant collection name: textbook_rag
- Retrieval relevance threshold: 0.35
- Cohere embeddings use input_type="search_query"

Frontend requirements:
- Assistant response must be appended to React state via:
  setMessages(prev => [...prev, assistantMessage])
- No reliance on page refresh, remount, or widget toggle

Backend requirements:
- HTTPException must be re-thrown, not wrapped
- 400 errors must remain 400
- Only unexpected failures return 500

Constraints:
- No architectural rewrites
- No model changes beyond specified values
- No UI redesign beyond functional fixes
- Hugging Face Space restart is manual and out of scope

Not building:
- New RAG pipeline
- New database schema
- New UI theme or styling system
- Authentication, streaming, or typing indicators"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Stable Chat Message Display (Priority: P1)

As a user, I need to see my messages and the assistant responses immediately without needing to refresh or minimize/restore the chat widget, so that I can have a smooth conversational experience.

**Why this priority**: This is the core user experience - if messages don't appear reliably, the chat is unusable.

**Independent Test**: Can be fully tested by sending a message and verifying both user and assistant messages appear in the chat window without any page refresh or widget state changes.

**Acceptance Scenarios**:
1. **Given** I type a message and click send, **When** I submit the message, **Then** my message appears immediately in the chat window
2. **Given** I have sent a message, **When** the assistant responds, **Then** the response appears in the chat window without minimizing or refreshing the widget
3. **Given** a conversation is in progress, **When** I continue chatting, **Then** all messages remain visible and properly ordered

---

### User Story 2 - Reliable RAG Response Retrieval (Priority: P2)

As a user, I need the assistant to return accurate answers from the existing textbook content, so that I can learn from the material that has been indexed in the vector database.

**Why this priority**: This is the core value proposition - if the RAG system doesn't return relevant content, the chat is not useful for learning.

**Independent Test**: Can be tested by asking specific questions about textbook content and verifying the responses contain accurate information from the indexed materials.

**Acceptance Scenarios**:
1. **Given** I ask "What is the title of the first chapter?", **When** the RAG system processes my query, **Then** it returns the correct title from the textbook content
2. **Given** I ask a question about textbook content, **When** the system searches Qdrant, **Then** it retrieves relevant results from the existing collection
3. **Given** a question with clear textbook answers, **When** I submit it, **Then** the response contains accurate information from indexed materials

---

### User Story 3 - Correct HTTP Status Handling (Priority: P3)

As a developer, I need the backend to return appropriate HTTP status codes for different error conditions, so that frontend error handling works correctly and users see appropriate feedback.

**Why this priority**: Proper error handling is essential for debugging and user experience, but secondary to core functionality.

**Independent Test**: Can be tested by sending various invalid requests and verifying the backend returns the correct HTTP status codes without converting 4xx errors to 500s.

**Acceptance Scenarios**:
1. **Given** I send a valid chat request, **When** processing completes successfully, **Then** the backend returns HTTP 200
2. **Given** I send a request with missing required fields, **When** validation runs, **Then** the backend returns HTTP 400 (not 500)
3. **Given** an unexpected server error occurs, **When** the error is handled, **Then** the backend returns HTTP 500

---

### Edge Cases

- What happens when Qdrant is temporarily unavailable? System should return appropriate error message without crashing.
- What happens when Cohere API is rate-limited? System should handle gracefully with user-friendly message.
- What happens when session_id is invalid? System should handle gracefully and potentially create new session.
- What happens when React state becomes inconsistent? System should recover without requiring page refresh.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Chat frontend MUST display user messages immediately upon send (optimistic update)
- **FR-002**: Chat frontend MUST append assistant responses to existing message state via setMessages(prev => [...prev, assistantMessage])
- **FR-003**: Frontend payload MUST use "message" field name as specified in contract
- **FR-004**: Backend MUST expect payload with { message: string, session_id: string } structure
- **FR-005**: Backend MUST return HTTP 200 for successful chat requests
- **FR-006**: Backend MUST preserve HTTP 4xx status codes without converting to 500
- **FR-007**: HTTPException MUST be re-thrown, not wrapped in 500 errors
- **FR-008**: RAG system MUST use embed-multilingual-v3.0 model for embeddings
- **FR-009**: RAG system MUST use input_type="search_query" for Cohere embeddings
- **FR-010**: RAG system MUST query Qdrant collection named "textbook_rag"
- **FR-011**: RAG system MUST use relevance threshold of 0.35 for filtering results
- **FR-012**: RAG system MUST retrieve context from existing Qdrant collection data
- **FR-013**: System MUST NOT require page refresh, widget remount, or toggle for message display
- **FR-014**: Only unexpected server failures MAY return HTTP 500 status

### Key Entities

- **Chat Message**: A unit of conversation containing text content, sender type (user/assistant), timestamp, and optional metadata like citations
- **Session**: A conversation thread identified by session_id that maintains context between messages
- **RAG Response**: A structured response containing the assistant's answer and relevant citations from the textbook content

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of user messages appear immediately in chat window upon sending (no delay or refresh required)
- **SC-002**: 100% of assistant responses appear in chat window without widget minimization or page refresh
- **SC-003**: 100% of valid chat requests return HTTP 200 status from backend
- **SC-004**: 0% of 4xx errors are converted to 500 errors in backend
- **SC-005**: Questions like "What is the title of the first chapter?" return correct textbook content answers
- **SC-006**: RAG system successfully retrieves results from existing Qdrant collection 95% of the time

## Assumptions

- Qdrant vector database contains properly indexed textbook content
- Cohere API is accessible and properly configured with embed-multilingual-v3.0 model
- Frontend and backend are properly connected via API endpoints
- Network connectivity is stable between components
- Existing data models and contracts can be maintained without breaking changes

## Out of Scope

- New RAG pipeline implementation
- New database schema or migrations
- New UI theme or styling system
- Authentication or user management features
- Streaming responses or typing indicators
- Hugging Face Space deployment configuration
- Performance optimization beyond stability fixes
