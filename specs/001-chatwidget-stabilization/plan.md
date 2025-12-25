# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Docusaurus theme wrapper using Root.tsx to host the global ChatWidget while ensuring SSG (Static Site Generation) build success. Remove the @theme/Layout override and replace it with a ChatLoader component that uses useState and useEffect to lazily load ChatKit code only after browser hydration, preventing the "RangeError: Maximum call stack size exceeded" during SSG builds.

## Technical Context

**Language/Version**: TypeScript 5.0+ (frontend), Python 3.11+ (backend)
**Primary Dependencies**: React 18+, Docusaurus 3.9+, FastAPI 0.104+, Qdrant vector database
**Storage**: Qdrant vector database for RAG, Neon Postgres for metadata
**Testing**: Jest for frontend, pytest for backend
**Target Platform**: Web application (GitHub Pages frontend, Hugging Face Space backend)
**Project Type**: Web application (frontend/backend architecture)
**Performance Goals**: <10s response time for 90% of chat queries, sub-200ms UI interactions
**Constraints**: GitHub Pages deployment (static hosting), CORS restrictions, cross-origin requests, SSG build compatibility
**Scale/Scope**: Single textbook website with global ChatWidget, multiple concurrent users

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
specs/001-chatwidget-stabilization/
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
│   ├── main.py          # FastAPI app with CORS configuration
│   ├── chat.py          # Chat API endpoints
│   └── agent.py         # RAG agent implementation
└── requirements.txt

frontend/
├── src/
│   ├── theme/
│   │   └── Root.tsx     # ChatWidget hosting location (theme wrapper)
│   ├── components/
│   │   ├── ChatLoader/  # SSG-safe ChatKit loader component
│   │   └── ChatKit/     # ChatWidget components
│   │       ├── ChatKit.tsx
│   │       ├── ChatWindow/
│   │       └── ChatKit.css
│   └── services/
│       └── api.js       # API service with backend URL configuration
└── docusaurus.config.ts # Docusaurus configuration
```

**Structure Decision**: This is a web application with frontend (Docusaurus/React) and backend (FastAPI) components. The ChatKit component will be hosted in Root.tsx instead of Layout.tsx to prevent circular dependencies. A ChatLoader component will be created to handle lazy loading of ChatKit with proper SSG safety using useState and useEffect hooks. The API service needs to be configured with the correct backend URL for production deployment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
