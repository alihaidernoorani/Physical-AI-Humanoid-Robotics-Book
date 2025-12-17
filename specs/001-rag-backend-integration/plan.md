# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This implementation plan addresses the RAG Backend Fix & Frontend Integration feature, focusing on migrating from OpenAI to OpenAI Agents SDK with Gemini-2.5-flash for chat completions and Cohere for embeddings generation. The backend architecture implements FastAPI with Qdrant vector database and Neon Postgres for personalization, supporting dual retrieval modes (full-book and per-page selected-text). The frontend integrates with backend services through secure API communication with proper environment variable handling for all sensitive configuration. The system ensures proper grounding in source material with comprehensive metadata tracking (module, chapter, subsection, source_type, source_origin) as required by the project constitution.

## Technical Context

**Language/Version**: Python 3.11, Node.js 20+
**Primary Dependencies**: FastAPI (backend), Docusaurus v3.9 (frontend), OpenAI Agents SDK, Cohere, Qdrant, Neon Postgres
**Storage**: Qdrant vector database for embeddings, Neon Postgres for metadata and personalization
**Testing**: pytest for backend, Jest for frontend, integration tests for RAG functionality
**Target Platform**: Linux server (backend), Web browser (frontend), GitHub Pages deployment
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <500ms p95 response time for RAG queries, 95%+ API success rate
**Constraints**: Secure handling of API keys via environment variables, proper grounding in source material, 90%+ accuracy on seeded test questions
**Scale/Scope**: Single textbook with 4 modules, multiple chapters per module, supporting per-page and full-book retrieval modes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Scientific Accuracy: All technical claims must be verifiable and traceable to reputable sources
- ✅ Academic Clarity: Content must be written for undergraduate-level audience with proper terminology definitions
- ✅ Reproducibility & Transparency: All methods and algorithms must be presented with sufficient detail for reproduction
- ✅ Ethical & Safety Awareness: All content must address ethical implications and safety constraints
- ✅ Module Structure Compliance: All content must follow the fixed 4-module structure (The Robotic Nervous System (ROS 2), The Digital Twin (Gazebo & Unity), The AI-Robot Brain (NVIDIA Isaac™), Vision-Language-Action (VLA))
- ✅ Frontend Architecture: Must implement Docusaurus-based frontend with interactive module cards, glossary, quizzes, and reusable MDX components
- ✅ Backend Architecture: Must implement FastAPI backend with RAG chatbot using OpenAI Agents SDK and Gemini-2.5-flash, Qdrant vector database, Cohere embeddings, and translation/personalization endpoints
- ✅ Personalization & Translation: Urdu toggle and personalization must function on every chapter
- ✅ Change Control: Module names, structure, and hierarchy are immutable - no autonomous scope expansion allowed
- ✅ RAG Grounding Enforcement: All RAG responses must be properly grounded in source material with metadata tracking; if grounding is insufficient, respond with uncertainty rather than hallucinating
- ✅ Environment Security: All API keys and sensitive configuration must be loaded securely from environment variables with no hardcoded credentials
- ✅ Metadata Requirements: All indexed chunks must include proper metadata: module, chapter, subsection, source_type, source_origin

### Post-Design Verification:
- All API contracts support required metadata fields for proper grounding
- Environment configuration is handled securely through .env files
- Dual retrieval modes (full-book and per-page) are supported in the data model
- Personalization and translation endpoints are defined in API contracts
- RAG grounding enforcement is built into the response model with confidence scoring
- No hardcoded credentials in any of the defined components

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-backend-integration/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-contracts.md # API specifications
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI application entry point
├── src/
│   ├── models/          # Data models (Pydantic)
│   ├── services/        # Business logic and RAG services
│   ├── api/             # API route definitions
│   │   ├── rag.py       # RAG endpoints
│   │   ├── embeddings.py # Embedding generation endpoints
│   │   ├── user.py      # User and personalization endpoints
│   │   └── translate.py # Translation endpoints
│   └── utils/           # Utility functions
├── requirements.txt     # Python dependencies
└── tests/               # Backend tests
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/      # React components
│   │   ├── ChatInterface/ # RAG chat interface
│   │   ├── RAGModeSelector/ # Dual mode selector
│   │   └── CitationDisplay/ # Citation display components
│   ├── services/        # API service layer
│   │   └── api.js       # API client for backend communication
│   └── pages/           # Page components
├── docs/                # Docusaurus documentation pages
├── docusaurus.config.js # Docusaurus configuration
├── package.json         # Frontend dependencies
└── tests/               # Frontend tests

.env                    # Environment variables (git-ignored)
.env.example            # Example environment variables
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend (Docusaurus React) components. Backend handles RAG processing, embeddings, and API services. Frontend provides user interface with chat functionality and dual retrieval modes.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | | No violations identified |
