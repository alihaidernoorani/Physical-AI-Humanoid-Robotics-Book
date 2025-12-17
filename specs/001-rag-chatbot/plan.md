# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) chatbot integrated within the Physical AI & Humanoid Robotics textbook. The system will allow students to ask questions about textbook content and receive responses grounded only in the book's content, with support for both full-book retrieval and selected-text-only modes. The architecture uses FastAPI backend with Qdrant vector database for content retrieval, OpenAI Agents SDK for response generation, and seamless Docusaurus frontend integration.

## Technical Context

**Language/Version**: Python 3.11+ (for FastAPI backend), JavaScript/TypeScript (for Docusaurus frontend)
**Primary Dependencies**: FastAPI, Qdrant vector database, OpenAI Agents SDK / ChatKit, Neon Serverless Postgres, Docusaurus v3.9
**Storage**: Qdrant vector database (for embeddings), Neon Serverless Postgres (for metadata and conversation state)
**Testing**: pytest (backend), Jest/Cypress (frontend integration), RAG-specific validation tests
**Target Platform**: Linux server (backend deployment), Web browser (frontend)
**Project Type**: Web application (frontend + backend architecture)
**Performance Goals**: <5 seconds response time for typical queries, 95% accuracy on seeded test questions
**Constraints**: <10% impact on textbook load times, RAG grounding enforcement (no hallucinations), 98% accuracy in selected text mode
**Scale/Scope**: Single textbook with 20-30 chapters, multiple concurrent users, serverless-friendly for scalability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Scientific Accuracy: All technical claims must be verifiable and traceable to reputable sources
- Academic Clarity: Content must be written for undergraduate-level audience with proper terminology definitions
- Reproducibility & Transparency: All methods and algorithms must be presented with sufficient detail for reproduction
- Ethical & Safety Awareness: All content must address ethical implications and safety constraints
- Module Structure Compliance: All content must follow the fixed 4-module structure (The Robotic Nervous System (ROS 2), The Digital Twin (Gazebo & Unity), The AI-Robot Brain (NVIDIA Isaac™), Vision-Language-Action (VLA))
- Frontend Architecture: Must implement Docusaurus-based frontend with interactive module cards, glossary, quizzes, and reusable MDX components
- Backend Architecture: Must implement FastAPI backend with RAG chatbot, Qdrant vector database, and translation/personalization endpoints
- Personalization & Translation: Urdu toggle and personalization must function on every chapter
- Change Control: Module names, structure, and hierarchy are immutable - no autonomous scope expansion allowed

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Current Docusaurus frontend (to be moved to frontend/ directory)
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── Message.jsx
│   │   │   └── InputArea.jsx
│   │   └── RAG/
│   │       ├── TextSelectionHandler.jsx
│   │       └── CitationDisplay.jsx
│   ├── pages/
│   │   └── ChatPage.jsx
│   └── services/
│       ├── chatApi.js
│       └── textSelection.js
├── docs/
│   ├── module-1-the-robotic-nervous-system-ros-2/
│   ├── module-2-the-digital-twin-gazebo-unity/
│   ├── module-3-the-ai-robot-brain-nvidia-isaac/
│   ├── module-4-vision-language-action/
│   └── ...
├── static/
├── docusaurus.config.ts
├── sidebars.ts
├── package.json
├── tsconfig.json
└── .docusaurus/
└── tests/
    ├── unit/
    │   └── test_chat_components.js
    └── integration/
        └── test_chat_integration.js

# New backend API for RAG functionality
backend/
├── src/
│   ├── models/
│   │   ├── chat_session.py
│   │   ├── retrieved_context.py
│   │   └── user_query.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   │   └── chat_service.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py
│   │   │   ├── embeddings.py
│   │   │   └── health.py
│   │   └── main.py
│   ├── config/
│   │   ├── settings.py
│   │   └── database.py
│   └── utils/
│       ├── text_chunker.py
│       └── validation.py
└── tests/
    ├── unit/
    │   ├── test_rag_service.py
    │   └── test_chat_service.py
    ├── integration/
    │   └── test_chat_api.py
    └── contract/
        └── test_rag_contracts.py

# Shared configuration and documentation
docs/
└── rag-architecture.md
```

**Structure Decision**: Web application structure with clear separation of concerns. The existing Docusaurus frontend will be moved to the frontend/ directory to house all textbook content, UI components, and client-side chat integration. The new backend/ directory will contain the FastAPI application handling RAG processing, embeddings, and chat logic. This structure maintains the existing textbook functionality while cleanly separating the new RAG backend services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
