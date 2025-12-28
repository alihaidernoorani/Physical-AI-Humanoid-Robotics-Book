# Research: ChatKit + Docusaurus RAG Stabilization

**Date**: 2025-12-28
**Feature**: 001-chatkit-rag-stabilization
**Research Phase**: Phase 0 (Implementation Planning)

## Research Summary

This research addresses the key stability issues in the ChatKit + RAG system, focusing on message display, HTTP status handling, and RAG retrieval reliability. The investigation covers frontend payload alignment, backend exception handling, and React state management patterns.

## Key Findings

### 1. Frontend Payload Contract Alignment

**Decision**: Align frontend request body to use "message" field as specified in contract
**Rationale**: The spec requires frontend payload field name to be "message" and backend expects { message: string, session_id: string }
**Implementation**: Update `frontend/src/services/api.js` to ensure request body uses correct field names

**Alternatives considered**:
- Keep existing field names: Would violate contract requirements
- Change backend expectations: Would require more extensive changes

### 2. Backend HTTP Status Code Handling

**Decision**: Ensure backend preserves 4xx status codes without converting to 500
**Rationale**: HTTPException must be re-thrown, not wrapped; 400 errors must remain 400 as per spec
**Implementation**: Review `backend/app/chat.py` exception handling to ensure proper status code preservation

**Alternatives considered**:
- Keep current error wrapping: Would violate spec requirement
- Use custom error wrapper: Would still mask client errors as server errors

### 3. RAG Retrieval Configuration

**Decision**: Configure RAG system with embed-multilingual-v3.0, relevance threshold 0.35, textbook_rag collection
**Rationale**: Spec mandates these specific values for model, threshold, and collection name
**Implementation**: Verify `backend/app/rag.py` and `backend/app/config.py` use correct values

**Alternatives considered**:
- Keep existing values: May not match spec requirements
- Use different model/threshold: Would violate contract

### 4. React State Update Pattern

**Decision**: Use setMessages(prev => [...prev, assistantMessage]) for assistant response updates
**Rationale**: Spec requires assistant response to be appended to React state via this specific pattern
**Implementation**: Review ChatKit components to ensure proper state update pattern

**Alternatives considered**:
- Replace entire message array: Would lose previous messages
- Use different update pattern: Would violate spec requirement

## Technical Architecture

### Current System Components

1. **Frontend**: Docusaurus site with ChatKit React widget
   - Components: ChatKit.tsx, ChatWindow, Message, MessageInput, MessageList
   - Services: api.js for backend communication

2. **Backend**: FastAPI server on Hugging Face Spaces
   - Endpoints: /api/v1/chat in chat.py
   - Services: RAG service in rag.py, Agent in agent.py
   - Configuration: config.py with model/threshold settings

3. **RAG Stack**: Cohere embeddings + Qdrant vector DB
   - Model: embed-multilingual-v3.0
   - Collection: textbook_rag
   - Threshold: 0.35

### Known Integration Points

- Frontend POSTs to /api/v1/chat with {message, session_id}
- Backend validates and processes through RAG service
- Results stored in Qdrant vector database
- Assistant responses returned to frontend for display

## Risk Mitigation

### Primary Risks
1. **Environment Mismatch**: Verify Cohere API key and Qdrant connection exist
2. **Contract Violations**: Ensure payload field names match exactly
3. **State Management**: Prevent React state inconsistencies during message updates

### Mitigation Strategies
1. Check environment variables before deployment
2. Add payload validation to both frontend and backend
3. Implement proper error boundaries and recovery patterns

## Dependencies

- Cohere API (embed-multilingual-v3.0)
- Qdrant vector database (textbook_rag collection)
- Existing indexed textbook content
- Hugging Face Space backend deployment

## Next Steps

1. Phase 1: Create data model and API contracts
2. Phase 2: Generate implementation tasks
3. Phase 3: Execute implementation following stability requirements

## Assumptions Validated

- Qdrant collection "textbook_rag" exists with proper schema
- Cohere API is accessible with embed-multilingual-v3.0 model
- Frontend and backend are properly connected
- Existing textbook content is properly indexed in Qdrant
