# Tasks: RAG Chatbot Stabilization and Modernization

**Feature**: 002-rag-chatbot-stabilization
**Branch**: `002-rag-chatbot-stabilization`
**Generated**: 2025-12-27
**Source**: [spec.md](./spec.md) | [plan.md](./plan.md)

## User Stories Summary

| Story | Priority | Description | Tasks |
|-------|----------|-------------|-------|
| US1 | P1 | Real-Time Chat Responsiveness | T007-T012 |
| US2 | P1 | Accurate RAG Context Retrieval | T013-T018 |
| US3 | P2 | Resilient Database Connections | T019-T024 |
| US4 | P2 | Modern Chat UI Aesthetics | T025-T030 |
| US5 | P3 | Successful Content Ingestion | T031-T037 |

---

## Phase 1: Setup

**Goal**: Project initialization and dependency setup

- [ ] T001 Add tenacity>=8.2.0 to backend/requirements.txt for retry logic
- [ ] T002 Create backend/app/services/ directory for new service modules
- [ ] T003 Create backend/scripts/ directory for ingestion scripts
- [ ] T004 Verify Cohere API key is configured in backend/.env
- [ ] T005 Verify Qdrant URL and API key are configured in backend/.env
- [ ] T006 Verify Neon DATABASE_URL with sslmode=require in backend/.env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Shared infrastructure that blocks multiple user stories

- [ ] T007 [P] Create backend/app/services/__init__.py with empty exports
- [ ] T008 Update backend/app/config.py to add RELEVANCE_THRESHOLD=0.7 setting
- [ ] T009 Update backend/app/config.py to add MAX_MESSAGE_LENGTH=2000 setting

---

## Phase 3: User Story 1 - Real-Time Chat Responsiveness (P1)

**Story Goal**: User messages appear instantly (<100ms) with loading indicator; bot responses appear without refresh

**Independent Test**: Send message → verify user message appears before API completes → verify bot response appends seamlessly

**Acceptance Criteria**:
- AC1.1: User message appears within 100ms of clicking Send
- AC1.2: Loading indicator shows while awaiting response
- AC1.3: Bot response appears without page refresh
- AC1.4: Error messages are user-friendly and allow retry

### Tasks

- [ ] T010 [US1] Refactor frontend/src/components/ChatInterface/ChatWindow.jsx to add user message to state immediately in handleSubmit before API call
- [ ] T011 [US1] Add isLoading state and loading indicator JSX in frontend/src/components/ChatInterface/ChatWindow.jsx
- [ ] T012 [US1] Add useRef scroll anchor and useEffect auto-scroll in frontend/src/components/ChatInterface/ChatWindow.jsx
- [ ] T013 [US1] Update error handling in handleSubmit to show user-friendly message with retry option in frontend/src/components/ChatInterface/ChatWindow.jsx
- [ ] T014 [US1] Update frontend/src/services/chatApi.js to send "message" field instead of "query" to match API contract
- [ ] T015 [US1] Add input validation in frontend/src/components/ChatInterface/ChatWindow.jsx to reject empty/whitespace and messages >2000 chars

---

## Phase 4: User Story 2 - Accurate RAG Context Retrieval (P1)

**Story Goal**: Cohere embeddings use correct input_type; retrieval filters by 0.7 relevance; citations displayed

**Independent Test**: Ask "What is a ROS 2 topic?" → verify relevant chunks retrieved → verify citations in response

**Acceptance Criteria**:
- AC2.1: Cohere embed() called with input_type="search_query" for queries
- AC2.2: Results filtered by 0.7 relevance threshold
- AC2.3: Response includes citations from retrieved chunks
- AC2.4: System responds honestly when no relevant context found

### Tasks

- [ ] T016 [US2] Update CohereEmbeddingService.generate_single_embedding() in backend/app/rag.py to accept input_type parameter defaulting to "search_query"
- [ ] T017 [US2] Update CohereEmbeddingService.generate_batch_embeddings() in backend/app/rag.py to accept input_type parameter
- [ ] T018 [US2] Update co.embed() calls in backend/app/rag.py to pass input_type parameter explicitly
- [ ] T019 [US2] Add relevance score filtering in QdrantRetrievalService.search_chunks_full_book() in backend/app/rag.py to filter results below 0.7 threshold
- [ ] T020 [US2] Add relevance score filtering in QdrantRetrievalService.search_chunks_per_page() in backend/app/rag.py to filter results below 0.7 threshold
- [ ] T021 [US2] Update RAGService.retrieve_context() in backend/app/rag.py to handle empty results gracefully and return appropriate message

---

## Phase 5: User Story 3 - Resilient Database Connections (P2)

**Story Goal**: Database connections retry with exponential backoff; system operates in degraded mode when DB unavailable

**Independent Test**: Simulate DB disconnect → verify retry attempts → verify graceful degradation to RAG-only

**Acceptance Criteria**:
- AC3.1: Connection retries 3 times with exponential backoff (1s, 2s, 4s)
- AC3.2: Connection failures logged with error type and timestamp
- AC3.3: System operates in degraded mode (RAG-only) when DB unavailable
- AC3.4: User-friendly error message on persistent failure

### Tasks

- [ ] T022 [US3] Create backend/app/services/db_manager.py with DatabaseManager class
- [ ] T023 [US3] Implement SQLAlchemy engine with pool_pre_ping=True and pool_recycle=3600 in backend/app/services/db_manager.py
- [ ] T024 [US3] Add @retry decorator from tenacity with exponential backoff (wait=1,2,4s, stop=3 attempts) in backend/app/services/db_manager.py
- [ ] T025 [US3] Implement is_database_available() method with graceful degradation flag in backend/app/services/db_manager.py
- [ ] T026 [US3] Add structured logging for connection failures (error type, timestamp, sanitized params) in backend/app/services/db_manager.py
- [ ] T027 [US3] Update backend/app/chat.py to use DatabaseManager and handle degraded mode (skip session persistence if DB unavailable)

---

## Phase 6: User Story 4 - Modern Chat UI Aesthetics (P2)

**Story Goal**: Chat interface has modern "Claude-like" design with distinct user/bot bubbles and typing animation

**Independent Test**: Visual inspection → verify user bubbles right-aligned blue, bot bubbles left-aligned gray, typing animation smooth

**Acceptance Criteria**:
- AC4.1: User messages: #2563eb background, white text, right-aligned
- AC4.2: Bot messages: #f3f4f6 background, #1f2937 text, left-aligned
- AC4.3: Message bubbles have 16px border-radius
- AC4.4: Smooth typing/thinking animation during loading

### Tasks

- [ ] T028 [P] [US4] Add CSS variables for design tokens at top of frontend/src/components/ChatInterface/ChatWindow.css
- [ ] T029 [US4] Update .chat-messages container in frontend/src/components/ChatInterface/ChatWindow.css to use Flexbox column layout with 1.25rem gap
- [ ] T030 [US4] Update .user-message styling in frontend/src/components/ChatInterface/ChatWindow.css: background #2563eb, color white, align-self flex-end, border-radius 16px, padding 0.75rem
- [ ] T031 [US4] Update .bot-message styling in frontend/src/components/ChatInterface/ChatWindow.css: background #f3f4f6, color #1f2937, align-self flex-start, border-radius 16px, padding 0.75rem
- [ ] T032 [US4] Update .typing-indicator animation in frontend/src/components/ChatInterface/ChatWindow.css for smoother pulse effect
- [ ] T033 [US4] Update font-family in frontend/src/components/ChatInterface/ChatWindow.css to Inter, -apple-system, system-ui, sans-serif

---

## Phase 7: User Story 5 - Successful Content Ingestion (P3)

**Story Goal**: Ingestion script processes all MDX files, creates 500-1000 token chunks with metadata, uploads to Qdrant

**Independent Test**: Run ingestion script → query Qdrant → verify all 21 MDX files indexed with correct metadata

**Acceptance Criteria**:
- AC5.1: Script recursively reads all .md/.mdx files from frontend/docs/
- AC5.2: Chunks are 500-1000 tokens with 100 token overlap
- AC5.3: Metadata includes module, chapter, subsection, page_reference
- AC5.4: Embeddings created with input_type="search_document"
- AC5.5: 100% of valid files successfully indexed

### Tasks

- [ ] T034 [US5] Create backend/scripts/ingest_textbook.py with main() entry point and argparse for --docs-path
- [ ] T035 [US5] Implement recursive MDX file discovery in backend/scripts/ingest_textbook.py using pathlib glob("**/*.mdx")
- [ ] T036 [US5] Implement markdown-aware text splitter in backend/scripts/ingest_textbook.py with chunk_size=800, overlap=100 chars
- [ ] T037 [US5] Implement metadata extraction in backend/scripts/ingest_textbook.py: module from parent dir, chapter from filename, subsection from headers
- [ ] T038 [US5] Implement batch embedding generation in backend/scripts/ingest_textbook.py using input_type="search_document"
- [ ] T039 [US5] Implement Qdrant upsert in backend/scripts/ingest_textbook.py with payload containing content and metadata
- [ ] T040 [US5] Add progress logging and summary report (files processed, chunks created, errors) in backend/scripts/ingest_textbook.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Input validation, error handling, and final integration

- [ ] T041 Add message length validation (1-2000 chars) in backend/app/chat.py chat_endpoint()
- [ ] T042 Add empty/whitespace message rejection in backend/app/chat.py chat_endpoint()
- [ ] T043 Update error responses in backend/app/chat.py to return user-friendly messages without stack traces
- [ ] T044 Update /health endpoint in backend/app/chat.py to return "degraded" status when DB unavailable but RAG working
- [ ] T045 Run backend server and verify /api/chat accepts both "message" and "query" fields for backwards compatibility

---

## Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
┌───────────────────────────────────────────────────────┐
│  Phase 3 (US1)  │  Phase 4 (US2)  │  Phase 5 (US3)   │  ← Can run in parallel
│  Responsiveness │  RAG Accuracy   │  DB Resilience   │
└───────────────────────────────────────────────────────┘
    ↓                   ↓                   ↓
┌───────────────────────────────────────────────────────┐
│        Phase 6 (US4) Modern UI                        │  ← Depends on US1 for state
└───────────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────────┐
│        Phase 7 (US5) Content Ingestion                │  ← Depends on US2 for input_type
└───────────────────────────────────────────────────────┘
    ↓
Phase 8 (Polish)
```

## Parallel Execution Opportunities

### Within Phase 3 (US1)
```
T010, T011, T012 can run in parallel (different concerns in same file)
T014 (chatApi.js) parallel with T010-T013 (ChatWindow.jsx)
```

### Within Phase 4 (US2)
```
T016, T017 can run in parallel (different methods)
T019, T020 can run in parallel (different search methods)
```

### Within Phase 6 (US4)
```
T028 must complete first (CSS variables)
T029-T033 can run in parallel after T028
```

### Within Phase 7 (US5)
```
T034, T035 must complete first (file structure)
T036, T037 can run in parallel (splitting vs metadata)
T038, T039 sequential (embed then upload)
```

### Cross-Phase Parallelism
```
US1 (frontend) || US2 (backend RAG) || US3 (backend DB)
```

## Implementation Strategy

### MVP Scope (Recommended First Delivery)
Complete **Phase 1-4 (US1 + US2)** for minimum viable chatbot:
- Optimistic UI updates working
- Cohere input_type fixed
- Basic chat functional

### Incremental Delivery
1. **Sprint 1**: US1 + US2 (core functionality)
2. **Sprint 2**: US3 + US4 (reliability + aesthetics)
3. **Sprint 3**: US5 + Polish (data population + refinement)

## Validation Checklist

- [ ] All 45 tasks have checkbox format
- [ ] All tasks have sequential IDs (T001-T045)
- [ ] User story tasks have [US#] labels
- [ ] Parallelizable tasks have [P] marker
- [ ] All tasks specify exact file paths
- [ ] Each user story has independent test criteria
- [ ] Dependencies clearly documented
