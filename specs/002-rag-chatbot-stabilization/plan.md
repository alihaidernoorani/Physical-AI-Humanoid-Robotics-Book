# Implementation Plan: RAG Chatbot Stabilization and Modernization

**Branch**: `002-rag-chatbot-stabilization` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-rag-chatbot-stabilization/spec.md`

## Summary

Stabilize and modernize the RAG chatbot by implementing optimistic UI updates for instant message display, fixing Cohere embedding API calls with correct `input_type` parameters, adding database connection retry logic with graceful degradation, applying modern "Claude-like" CSS styling, and creating a batch ingestion script for Qdrant population.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**: FastAPI, Cohere SDK, Qdrant Client, SQLAlchemy, React, Docusaurus
**Storage**: Qdrant (vectors), Neon Postgres (sessions), Local state (messages)
**Testing**: pytest (backend), manual verification (frontend)
**Target Platform**: Web (GitHub Pages frontend, cloud backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <100ms UI response, <3s API response, 0.7 relevance threshold
**Constraints**: 2000 char message limit, 500-1000 token chunks, 3 retry attempts
**Scale/Scope**: Single-user sessions, ~21 MDX files to ingest

## Constitution Check

*GATE: PASS - All principles satisfied*

- Scientific Accuracy: RAG grounding ensures responses from verified textbook content only
- Academic Clarity: No content changes; infrastructure improvements only
- Reproducibility & Transparency: Quickstart guide documents all setup steps
- Ethical & Safety Awareness: No ethical concerns for infrastructure changes
- Module Structure Compliance: Ingestion preserves module metadata (4 locked modules)
- Frontend Architecture: Enhances existing Docusaurus-based chat component
- Backend Architecture: Improves existing FastAPI + Qdrant + Neon stack
- Personalization & Translation: Not modified by this feature
- Change Control: No module structure changes; only infrastructure stabilization

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot-stabilization/
├── plan.md              # This file
├── research.md          # Phase 0: Technical decisions
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Setup guide
├── contracts/           # Phase 1: API contracts
│   └── chat-api.yaml    # OpenAPI specification
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py              # FastAPI app (existing)
│   ├── config.py            # Settings (existing)
│   ├── rag.py               # RAG service (MODIFY: add input_type)
│   ├── chat.py              # Chat endpoints (MODIFY: validation)
│   ├── agent.py             # AI agent (existing)
│   └── services/
│       └── db_manager.py    # NEW: Connection pooling + retry
├── scripts/
│   └── ingest_textbook.py   # NEW: Batch ingestion script
└── tests/
    ├── test_rag.py          # NEW: RAG service tests
    └── test_db_manager.py   # NEW: DB retry tests

frontend/
├── src/
│   ├── components/
│   │   └── ChatInterface/
│   │       ├── ChatWindow.jsx    # MODIFY: Optimistic updates
│   │       └── ChatWindow.css    # MODIFY: Modern styling
│   └── services/
│       └── chatApi.js            # MODIFY: Request field alignment
└── docs/                         # Content to ingest (21 MDX files)
```

**Structure Decision**: Web application with existing backend/frontend separation. Changes focus on stabilization within existing structure; no new directories except `backend/app/services/` for database manager.

## Complexity Tracking

No constitution violations requiring justification.

## Implementation Phases

### Phase 1: Infrastructure (Backend Stabilization)

**Goal**: Fix Cohere API errors and database reliability

#### 1.1 Cohere input_type Fix
- Modify `CohereEmbeddingService.generate_single_embedding()` to accept `input_type` parameter
- Modify `CohereEmbeddingService.generate_batch_embeddings()` to accept `input_type` parameter
- Update `RAGService.retrieve_context()` to pass `input_type="search_query"`
- Add relevance score filtering (threshold: 0.7)

#### 1.2 Database Connection Manager
- Create `backend/app/services/db_manager.py`
- Implement SQLAlchemy engine with connection pooling
- Add retry decorator with exponential backoff (3 retries: 1s, 2s, 4s)
- Implement graceful degradation flag for RAG-only mode
- Add structured logging for connection failures

#### 1.3 Input Validation
- Add message length validation (1-2000 characters)
- Add empty/whitespace message rejection
- Return user-friendly error messages

### Phase 2: UI/UX (Frontend Modernization)

**Goal**: Implement optimistic updates and modern styling

#### 2.1 Optimistic Updates
- Modify `ChatWindow.jsx` state management
- Add user message to state immediately on submit
- Show loading indicator during API call
- Append bot response on API completion
- Handle errors gracefully with retry option

#### 2.2 Modern CSS Theme
- Define CSS variables for design tokens
- Update message bubble styling (16px border-radius)
- Implement color scheme (user: #2563eb, bot: #f3f4f6)
- Add smooth typing animation
- Ensure responsive design

#### 2.3 API Field Alignment
- Update `chatApi.js` to send `message` field (not `query`)
- Ensure request/response field names match backend contract

### Phase 3: Data Ingestion

**Goal**: Populate Qdrant with textbook content

#### 3.1 Ingestion Script
- Create `backend/scripts/ingest_textbook.py`
- Implement markdown-aware text splitting (500-1000 tokens)
- Extract metadata from file paths and frontmatter
- Generate embeddings with `input_type="search_document"`
- Batch upload to Qdrant with metadata

#### 3.2 Metadata Extraction
- Parse module from directory name
- Parse chapter from filename
- Extract subsection from markdown headers
- Store source file path as page_reference

## Testing Strategy

### Unit Tests
- `test_rag.py`: Verify `input_type` parameter passed correctly
- `test_db_manager.py`: Verify retry logic and degradation

### Integration Tests
- Send chat message, verify Qdrant returns relevant chunks
- Simulate DB disconnect, verify auto-reconnect within 30s
- Run ingestion, query Qdrant for known content

### Manual Verification
- UI: Send message, verify appears within 100ms (use DevTools)
- UI: Verify visual distinction between user/bot messages
- UI: Verify typing animation during loading

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Cohere API rate limits | Implement backoff, batch embeddings in ingestion |
| Qdrant collection corruption | Create backup before re-ingestion |
| Breaking existing chat flow | Test with existing sessions before deploy |
| CSS conflicts with Docusaurus | Scope styles to chat component |

## Dependencies

```
# Backend (add to requirements.txt)
tenacity>=8.2.0        # Retry logic
sqlalchemy>=2.0.0      # Connection pooling (likely already present)

# Frontend (no new dependencies)
# Uses existing React, existing chatApi service
```

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chunking | Markdown-aware | Preserves semantic boundaries |
| State management | Local React state | Simpler, sufficient for single-session |
| DB connection | SQLAlchemy pooling | Built-in retry support, efficient |
| Relevance threshold | 0.7 | Balances recall and precision |
| CSS approach | CSS variables | Matches Docusaurus patterns |

## Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Message appearance | <100ms | Browser DevTools timing |
| API success rate | >95% | No page refresh needed |
| DB recovery time | <30s | Simulated disconnect test |
| Citation accuracy | >90% | Manual spot checks |
| Ingestion coverage | 100% | Count indexed vs source files |

## Next Steps

Run `/sp.tasks` to generate the detailed task breakdown with acceptance criteria for each implementation item.
