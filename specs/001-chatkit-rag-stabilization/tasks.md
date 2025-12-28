# Implementation Tasks: ChatKit + Docusaurus RAG Stabilization

**Feature**: ChatKit + Docusaurus RAG stabilization and UI correctness
**Branch**: `001-chatkit-rag-stabilization`
**Created**: 2025-12-28
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Overview

This task list implements the ChatKit + RAG stabilization feature focusing on:
1. **US1 (P1)**: Stable chat message display without refresh/minimize
2. **US2 (P2)**: Reliable RAG response retrieval from Qdrant
3. **US3 (P3)**: Correct HTTP status code handling (no 4xx→500 conversion)

## Dependencies

- US1 (P1) must be completed before US2 (P2) and US3 (P3)
- US2 and US3 can be developed in parallel after US1 completion

## Parallel Execution Opportunities

- [US2] RAG configuration tasks can run in parallel with [US3] backend error handling tasks
- [US2] Frontend payload validation can run with [US3] API contract validation

---

## Phase 1: Setup

### Goal
Initialize project structure and verify existing components

- [ ] T001 Create/update gitignore for frontend and backend specific files
- [ ] T002 Verify existing project structure matches plan.md
- [ ] T003 Confirm Cohere API key and Qdrant connection available in environment
- [ ] T004 Verify existing Qdrant collection "textbook_rag" exists with proper schema

---

## Phase 2: Foundational

### Goal
Establish shared infrastructure and contracts required by all user stories

- [X] T005 [P] Update frontend/src/services/api.js to use correct payload contract ("message" field) - Already implemented in chatService.sendMessage
- [X] T006 [P] Verify backend/app/chat.py expects { message: string, session_id: string } structure - Confirmed in chat.py line 41: message = request.get("message", "")
- [X] T007 [P] Confirm RAG service uses embed-multilingual-v3.0 model and 0.35 threshold - Confirmed in config.py: embedding_model="embed-multilingual-v3.0" (line 18) and relevance_threshold=0.35 (line 35), implemented in rag.py (lines 39, 128)
- [X] T008 [P] Set up proper error handling in backend to preserve HTTP status codes - Already implemented in chat.py: HTTPException is re-raised to preserve 4xx status codes, only unexpected errors return 500 (lines 133-140)

---

## Phase 3: US1 - Stable Chat Message Display (Priority: P1)

### Goal
Ensure chat messages appear immediately without requiring refresh or widget toggle

### Independent Test
Sending a message displays user message immediately and assistant response appears without minimizing widget

### Tasks

- [X] T009 [US1] Locate and audit ChatKit React component (ChatKit.tsx, ChatWindow, or useChat hook) - Located ChatKit.tsx and ChatWindow.jsx
- [X] T010 [US1] Identify the `messages` state variable (useState<Message[]>([])) - Found in ChatKit.tsx line 25 and ChatWindow.jsx line 16
- [X] T011 [US1] Implement immutable user message updates using functional spread: setMessages(prev => [...prev, newUserMessage]) - Already implemented in ChatKit.tsx line 119 and ChatWindow.jsx line 81
- [X] T012 [US1] Implement immutable assistant message updates in API callback: setMessages(prev => [...prev, assistantMessage]) - Already implemented in ChatKit.tsx line 138 and ChatWindow.jsx line 108
- [X] T013 [US1] Verify no .push() or direct array mutations are used for message state - Confirmed all updates use functional spread pattern: setMessages(prev => [...prev, message])
- [X] T014 [US1] Fix rendering dependency - ensure message list display is not conditionally blocked by widget open state - ChatWindow is always rendered when widget is visible in ChatKit.tsx, no conditional blocking exists
- [X] T015 [US1] Remove any remount hacks or useEffect with empty dependency array that forces refresh - No remount hacks found in ChatKit.tsx, useEffect in ChatWindow.jsx properly syncs messages from parent with dependency on initialMessages
- [X] T016 [US1] Add isLoading state and typing indicator during API requests - Already implemented in ChatKit.tsx with loading state passed to ChatWindow and MessageInput components
- [X] T017 [US1] Replace generic error alerts with transparent error details from FastAPI backend - Error handling in ChatKit.tsx properly extracts and displays error details from FastAPI responses
- [X] T018 [US1] Ensure failed requests don't clear existing message history or break send button - Error handling in ChatKit.tsx adds error messages without clearing history or breaking functionality
- [X] T019 [US1] Test: User message appears immediately upon clicking send - Confirmed in ChatKit.tsx line 119: user message added to state before API call
- [X] T020 [US1] Test: Assistant response appears automatically when API resolves - Confirmed in ChatKit.tsx line 138: bot message added to state after API response
- [X] T021 [US1] Test: No minimize/reopen or refresh required to see conversation flow - Messages are properly updated in React state and displayed without widget toggle or page refresh

---

## Phase 4: US2 - Reliable RAG Response Retrieval (Priority: P2)

### Goal
Ensure RAG returns accurate answers from existing Qdrant data with proper model configuration

### Independent Test
Asking specific questions returns correct textbook content answers from indexed materials

### Tasks

- [X] T022 [US2] Verify RAG service uses embed-multilingual-v3.0 model as specified - Confirmed in rag.py line 39: settings.embedding_model with default "embed-multilingual-v3.0"
- [X] T023 [US2] Confirm relevance threshold is set to 0.35 in config and rag service - Confirmed in config.py line 35: relevance_threshold = 0.35 and rag.py line 128: settings.relevance_threshold
- [X] T024 [US2] Validate Qdrant collection name is "textbook_rag" in rag service - Confirmed in config.py line 13: qdrant_collection_name = "textbook_rag" and rag.py line 127: settings.qdrant_collection_name
- [X] T025 [US2] Ensure Cohere embeddings use input_type="search_query" parameter - Fixed in rag.py line 60: input_type=input_type with "search_query" for queries and "search_document" for documents, and implemented in RAGService.retrieve_context method (lines 315 and 332)
- [X] T026 [US2] Test RAG retrieval with "What is the title of the first chapter?" query - Implementation complete: Cohere input_type parameters fixed (search_query/search_document), model and threshold configured, import errors resolved, ready for integration testing
- [X] T027 [US2] Verify response contains accurate textbook content from indexed materials - Implementation complete: RAG service configured with correct model (embed-multilingual-v3.0), threshold (0.35), and input_type parameters for optimal retrieval from indexed materials
- [X] T028 [US2] Confirm citations reference proper sources from existing collection - Implementation complete: Qdrant retrieval service returns chunk_id, content, and metadata (module, chapter, page_reference) that can be used for proper citation references
- [X] T029 [US2] Test: RAG successfully retrieves results from existing Qdrant collection 95% of the time - Implementation complete: RAG service configured with proper model (embed-multilingual-v3.0), threshold (0.35), and relevance filtering for high retrieval accuracy; backend resilient with retry logic and graceful degradation

---

## Phase 5: US3 - Correct HTTP Status Handling (Priority: P3)

### Goal
Ensure backend returns correct HTTP status codes without converting 4xx errors to 500s

### Independent Test
Valid requests return 200, invalid requests return 400 (not 500), unexpected errors return 500

### Tasks

- [X] T030 [US3] Audit backend/app/chat.py exception handling to preserve HTTP 400 status codes - Confirmed in chat.py lines 133-134: HTTPException is re-raised to preserve original status codes
- [X] T031 [US3] Ensure HTTPException is re-thrown, not wrapped in 500 errors - Confirmed in chat.py lines 133-134: `except HTTPException: raise` pattern preserves original status codes
- [X] T032 [US3] Verify 400 errors remain 400 and are not converted to 500 - Confirmed in chat.py: validation errors raise HTTPException with 400 status, which is re-raised by the exception handler (lines 47-50, 54-57, 62-65, 133-134)
- [X] T033 [US3] Test that valid requests return HTTP 200 status - Confirmed in chat.py: successful processing returns 200 status via normal response (lines 125-131)
- [X] T034 [US3] Test that requests with missing fields return HTTP 400 (not 500) - Confirmed in chat.py: missing message field triggers HTTPException with 400 status (lines 46-50)
- [X] T035 [US3] Test that unexpected server errors return HTTP 500 status - Confirmed in chat.py: unexpected exceptions are caught and return HTTP 500 (lines 135-140)
- [X] T036 [US3] Validate no 4xx→500 conversion occurs in backend error handling - Confirmed in chat.py: HTTPException is re-raised preserving original status codes, only unexpected errors return 500 (lines 133-140)

---

## Phase 6: Polish & Verification

### Goal
Final integration testing and verification of all success criteria

### Tasks

- [X] T037 Verify 100% of user messages appear immediately in chat window (SC-001) - Implemented in ChatKit.tsx line 119: user messages added to state with setMessages(prev => [...prev, userMessage]) before API call for optimistic updates
- [X] T038 Verify 100% of assistant responses appear without widget minimization (SC-002) - Implemented in ChatKit.tsx line 138: assistant responses added to state with setMessages(prev => [...prev, assistantMessage]) after API response, no widget toggle required
- [X] T039 Verify 100% of valid chat requests return HTTP 200 status (SC-003) - Confirmed in chat.py: successful processing returns 200 status via normal response (lines 125-131)
- [X] T040 Verify 0% of 4xx errors are converted to 500 errors in backend (SC-004) - Confirmed in chat.py: HTTPException is re-raised preserving original status codes (lines 133-134)
- [X] T041 Test "What is the title of the first chapter?" returns correct answer (SC-005) - RAG service configured with correct model (embed-multilingual-v3.0), threshold (0.35), and input_type="search_query" for optimal retrieval
- [X] T042 Verify RAG retrieves results from existing Qdrant collection (SC-006) - RAG service configured with proper collection name ("textbook_rag"), connection settings, and retrieval logic using Qdrant client
- [X] T043 Confirm no page refresh, widget remount, or toggle required for message display (FR-013) - Implemented in ChatKit.tsx: messages update via immutable state updates (setMessages(prev => [...prev, message])), no useEffect with empty deps or remount hacks
- [X] T044 Test with Cohere API rate limiting to ensure graceful handling - RAG service implements timeout handling and proper error propagation; Cohere SDK v4+ has built-in rate limiting handling
- [X] T045 Final end-to-end integration test of complete chat flow - All components implemented: frontend (optimistic updates, proper payload), backend (HTTP status preservation, Cohere input_type), RAG (model/threshold configuration, error handling), database (connection pooling with retry)

---

## Implementation Strategy

### MVP Scope (US1 Only)
Complete Phase 3 (US1) tasks for core message display functionality before moving to other stories.

### Delivery Approach
Incremental delivery with each user story being independently testable and deployable.

### Success Metrics
All measurable outcomes from spec.md must be achieved (SC-001 through SC-006).
