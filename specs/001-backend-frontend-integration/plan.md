# Implementation Plan: Backend-Frontend Integration

**Branch**: `001-backend-frontend-integration` | **Date**: 2025-12-20 | **Spec**: [specs/001-backend-frontend-integration/spec.md](specs/001-backend-frontend-integration/spec.md)
**Input**: Feature specification from `/specs/001-backend-frontend-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan addresses the safe cleanup of legacy backend files while integrating a ChatKit UI frontend. The approach involves first removing legacy files identified in the audit report, preserving core backend functionality, then implementing the ChatKit UI and connecting it to backend API endpoints for chat, translation, and personalization features.

## Technical Context

**Language/Version**: Python 3.11, Node.js 20+
**Primary Dependencies**: FastAPI, Docusaurus, Qdrant, OpenAI Agents, ChatKit
**Storage**: Qdrant vector database, Neon Postgres
**Testing**: pytest, Jest
**Target Platform**: Linux server, Web-based application
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <200ms p95 latency for API responses, 95%+ success rate on API endpoints
**Constraints**: Core backend files must remain unchanged, no new backend features allowed in this phase
**Scale/Scope**: Single textbook application with RAG chatbot, translation, and personalization features

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
specs/001-backend-frontend-integration/
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
│   ├── main.py          # Core backend file (untouched)
│   ├── agent.py         # Core backend file (untouched)
│   ├── rag.py           # Core backend file (untouched)
│   ├── chat.py          # Core backend file (untouched)
│   └── config.py        # Core backend file (untouched)
├── src/                 # Legacy directory to be removed
│   ├── models/
│   ├── services/
│   └── api/
├── tests/               # Legacy directory to be removed
├── main.py              # Legacy file to be removed
├── src/config.py        # Legacy file to be removed
├── CONFIGURATION.md     # Legacy file to be removed
├── venv/                # Legacy directory to be removed
├── requirements.txt
└── Dockerfile

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface/
│   │   ├── ChatKit/
│   │   └── RAGModeSelector/
│   ├── pages/
│   └── services/
├── package.json
└── docusaurus.config.js

# Files to archive
index_textbook.py
README.md
=1.24.3
```

**Structure Decision**: Web application structure with separate backend and frontend directories. The backend contains the core 5-file structure that must remain unchanged, with legacy files to be removed. The frontend will be enhanced with ChatKit UI components and API integration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Legacy file removal | Codebase cleanup required for maintainability | Keeping legacy files would create confusion and potential conflicts |
