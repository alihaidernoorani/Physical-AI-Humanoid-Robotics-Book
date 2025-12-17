# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the migration of the existing integrated RAG chatbot to a revised architecture that reorganizes frontend code, replaces the embedding provider with Cohere, and replaces the OpenAI Chat API with the OpenAI Agents SDK using a Gemini model. The migration will proceed in controlled phases: first, frontend files will be identified and relocated into a `/frontend` directory with all imports and build scripts updated; second, the embedding layer will be refactored to use Cohere instead of Sentence Transformers, including environment configuration and compatibility with Qdrant; third, the inference layer will be replaced by the OpenAI Agents SDK with Gemini-2.5-flash as the model, while preserving existing RAG grounding, selected-text mode, refusal logic, and API contracts. The approach maintains zero functional regression while improving the architectural clarity and updating the technology stack as specified.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript for frontend components
**Primary Dependencies**: FastAPI (backend), Docusaurus (frontend), Qdrant (vector database), Sentence Transformers (current embeddings), OpenAI (current inference), Cohere (new embeddings), OpenAI Agents SDK (new inference framework), Gemini-2.5-flash (new model)
**Storage**: Qdrant vector database for embeddings, Neon Postgres for metadata, Docusaurus static files for frontend
**Testing**: pytest for backend, Jest/Cypress for frontend, integration tests for RAG functionality
**Target Platform**: Linux server deployment with GitHub Pages for frontend
**Project Type**: Web application with separate frontend (Docusaurus) and backend (FastAPI) components
**Performance Goals**: Maintain current response times (<200ms p95), preserve retrieval accuracy, maintain grounding behavior
**Constraints**: Zero functional regression in chatbot behavior, maintain safety and refusal mechanisms, preserve API contracts, ensure backward compatibility
**Scale/Scope**: Single textbook with 4 modules, multiple chapters per module, RAG chatbot with full-text and selected-text modes

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
The project currently has a mixed structure where Docusaurus frontend files are in the root directory, but the migration will reorganize them into a dedicated frontend directory as specified in the feature requirements.

Current structure (to be migrated):
```text
. (root)
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   └── chat_session.py
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── textbook_content_extractor.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── chat.py
│   │       ├── health.py
│   │       └── textbook.py
│   │   └── config/
│   │       └── settings.py
│   ├── tests/
│   ├── requirements.txt
│   ├── main.py
│   └── index_textbook.py
├── docs/ (Docusaurus content)
│   ├── module-1/
│   ├── module-2/
│   ├── module-3/
│   └── module-4/
├── frontend/ (new directory for frontend code)
│   └── src/
│       ├── components/
│       │   ├── ChatInterface/
│       │   │   ├── ChatWindow.jsx
│       │   │   ├── CitationDisplay.jsx
│       │   │   └── TextSelectionHandler.jsx
│       │   └── common/
│       └── services/
│           └── chatApi.js
├── docusaurus.config.ts (Docusaurus config - to be moved to frontend/)
├── package.json (Docusaurus package.json - to be moved to frontend/)
├── sidebars.ts (Docusaurus sidebar config - to be moved to frontend/)
├── tsconfig.json (Docusaurus tsconfig - to be moved to frontend/)
└── specs/
    └── 001-rag-architecture-migration/
        ├── spec.md
        ├── plan.md
        └── research.md
```

Target structure after migration:
```text
. (root)
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   └── chat_session.py
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── textbook_content_extractor.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── chat.py
│   │       ├── health.py
│   │       └── textbook.py
│   │   └── config/
│   │       └── settings.py
│   ├── tests/
│   ├── requirements.txt
│   ├── main.py
│   └── index_textbook.py
├── frontend/ (all Docusaurus files moved here)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface/
│   │   │   │   ├── ChatWindow.jsx
│   │   │   │   ├── CitationDisplay.jsx
│   │   │   │   └── TextSelectionHandler.jsx
│   │   │   └── common/
│   │   └── services/
│   │       └── chatApi.js
│   ├── docs/
│   │   ├── module-1/
│   │   ├── module-2/
│   │   ├── module-3/
│   │   └── module-4/
│   ├── docusaurus.config.ts
│   ├── package.json
│   ├── sidebars.ts
│   └── tsconfig.json
└── specs/
    └── 001-rag-architecture-migration/
        ├── spec.md
        ├── plan.md
        └── research.md
```

**Structure Decision**: The migration will reorganize the project to have a clear separation between frontend and backend. All Docusaurus-related files (docusaurus.config.ts, package.json, sidebars.ts, tsconfig.json, docs/, and frontend/src/) will be moved into the dedicated `/frontend` directory. The backend files will remain in the `/backend` directory. This will create a cleaner architecture that separates concerns between the frontend (Docusaurus) and backend (FastAPI) components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
