# Feature Specification: RAG Backend Fix & Frontend Integration

**Feature Branch**: `001-rag-backend-integration`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "Ensure the backend services are fully functional, fix all existing issues, and properly integrate the frontend with the backend for the RAG chatbot. All environment variables must be correctly used and secured in the project."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAG Chatbot Query (Priority: P1)

As a user, I want to ask questions about the Physical AI textbook content and receive accurate, contextually relevant responses that are grounded in the source material.

**Why this priority**: This is the core functionality of the RAG system - users need to be able to query the textbook and get reliable answers to support their learning.

**Independent Test**: Can be fully tested by asking questions about specific textbook content and verifying that responses reference the correct source material with citations.

**Acceptance Scenarios**:

1. **Given** I am on the textbook website, **When** I type a question about the content and submit it, **Then** I receive a response that is accurate and includes citations to the relevant source material.
2. **Given** I have selected specific text on a page, **When** I ask a question related to that text in per-page mode, **Then** the response is grounded only in the selected text and not the entire book.

---

### User Story 2 - Environment Configuration (Priority: P1)

As a developer, I want the system to securely use environment variables for all sensitive configuration, so that no hardcoded credentials exist in the codebase.

**Why this priority**: Security is critical - hardcoded credentials would create significant vulnerabilities and deployment issues.

**Independent Test**: Can be fully tested by verifying that all sensitive configuration values are loaded from environment variables and no credentials appear in the source code.

**Acceptance Scenarios**:

1. **Given** the application is deployed, **When** I examine the source code, **Then** I find no hardcoded API keys or sensitive credentials.
2. **Given** environment variables are properly set, **When** the application starts, **Then** it successfully connects to all required services (Qdrant, Cohere, Gemini, Neon DB).

---

### User Story 3 - Dual Retrieval Modes (Priority: P2)

As a user, I want to switch between full-book retrieval and per-page selected-text retrieval modes, so that I can get either comprehensive answers or focused responses based on specific content I'm reading.

**Why this priority**: This provides flexibility for different learning scenarios - comprehensive study vs focused reading.

**Independent Test**: Can be fully tested by using both retrieval modes and verifying that responses are appropriately scoped to the selected mode.

**Acceptance Scenarios**:

1. **Given** I am in full-book mode, **When** I ask a question, **Then** the response can reference any part of the entire textbook.
2. **Given** I am in per-page mode with selected text, **When** I ask a question, **Then** the response is grounded only in the selected text.

---

### Edge Cases

- What happens when the Qdrant vector database is temporarily unavailable?
- How does the system handle queries when no relevant content is found in the vector store?
- What occurs when environment variables are missing or invalid during startup?
- How does the system behave when the Cohere or Gemini APIs are rate-limited or unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST generate semantic embeddings for content indexing using an external AI service
- **FR-002**: The system MUST provide chat completion functionality through an AI service
- **FR-003**: The system MUST store and retrieve content in a vector database for semantic search
- **FR-004**: The system MUST support dual retrieval modes: full-book and per-page selected-text only
- **FR-005**: The system MUST add metadata to all indexed content: module, chapter, subsection, source_type, source_origin
- **FR-006**: The system MUST securely load all sensitive configuration from environment variables
- **FR-007**: The frontend MUST capture selected text and send it to backend when in per-page mode
- **FR-008**: The frontend MUST display citations based on returned content metadata
- **FR-009**: The system MUST handle errors gracefully with appropriate logging
- **FR-010**: The system MUST integrate with a database for personalization and translation endpoints
- **FR-011**: The system MUST ensure all environment variables are used securely without hardcoding keys in the codebase
- **FR-012**: The system MUST maintain backward compatibility with existing frontend components during integration

### Key Entities

- **RAG Query**: A user's question that requires contextual response based on textbook content, including query text, retrieval mode, and optional selected text
- **Knowledge Chunk**: A segment of textbook content stored in vector database with metadata (module, chapter, subsection, source_type, source_origin)
- **Chat Response**: The system's answer to a user query with citations to source material and confidence indicators
- **Environment Configuration**: Securely stored API keys and service endpoints loaded from environment variables

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Backend endpoints respond correctly without errors or warnings during full test suite execution
- **SC-002**: Embeddings generated via Cohere are correctly stored in Qdrant vector database with 99% success rate
- **SC-003**: OpenAI Agents SDK integration with Gemini model returns chat completions with 95% success rate
- **SC-004**: Per-page selected-text retrieval functions correctly, returning results only from the selected text 98% of the time
- **SC-005**: Frontend successfully communicates with backend services with 99% API call success rate
- **SC-006**: All environment variables are securely used without any hardcoded keys in the codebase (0% hardcoded credentials)
- **SC-007**: End-to-end tests pass with 95% success rate, confirming accurate and grounded responses
- **SC-008**: Project passes all tests and is deployable to production environment without issues
