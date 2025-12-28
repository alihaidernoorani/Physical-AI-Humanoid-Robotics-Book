# Implementation Plan: ChatKit + Docusaurus RAG Stabilization

**Branch**: `001-chatkit-rag-stabilization` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-chatkit-rag-stabilization/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Stabilize ChatKit + Docusaurus RAG integration focusing on: 1) reliable message display without refresh, 2) correct HTTP status codes (no 4xx→500 conversion), 3) proper RAG retrieval from existing Qdrant data. Implementation will align frontend payload contract, fix backend exception handling, and ensure React state updates work correctly.

## Technical Context

**Language/Version**: Python 3.11, Node.js 20+, React 18
**Primary Dependencies**: FastAPI, React, Cohere SDK, Qdrant client, Docusaurus
**Storage**: Qdrant vector database, Neon Postgres
**Testing**: Manual testing with DevTools, backend logs, UI verification
**Target Platform**: Docusaurus static site with ChatKit widget, Hugging Face Spaces backend
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <200ms response time, immediate message display
**Constraints**: No architectural rewrites, maintain existing contracts, focus on stability fixes
**Scale/Scope**: Single textbook content with RAG functionality

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
specs/001-chatkit-rag-stabilization/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── chat.py          # Chat endpoint (needs HTTP status fixes)
│   ├── rag.py           # RAG service (needs model/threshold alignment)
│   ├── agent.py         # Agent configuration (may need updates)
│   ├── config.py        # Configuration (has relevance threshold)
│   └── services/
│       └── db_manager.py # Database manager (from previous work)
└── scripts/
    └── ingest_textbook.py # Ingestion script (from previous work)

frontend/
├── src/
│   ├── components/
│   │   └── ChatKit/     # ChatKit widget components
│   │       ├── ChatKit.tsx
│   │       ├── ChatWindow/
│   │       ├── Message/
│   │       ├── MessageInput/
│   │       └── MessageList/
│   └── services/
│       └── api.js       # API service (needs payload alignment)
```

**Structure Decision**: Web application with separate frontend (Docusaurus/React) and backend (FastAPI) components. Backend handles RAG and chat logic, frontend provides ChatKit widget for Docusaurus integration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations detected] | [N/A] |
