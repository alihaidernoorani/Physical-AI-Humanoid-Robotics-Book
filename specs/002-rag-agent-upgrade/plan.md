# Implementation Plan: RAG Agent Upgrade

**Branch**: `002-rag-agent-upgrade` | **Date**: 2025-12-17 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/002-rag-agent-upgrade/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Surgical refactor and upgrade of the existing FastAPI and Docusaurus codebase to implement a production-ready RAG system using the OpenAI Agents SDK with Gemini-2.5-flash, Cohere embeddings, Qdrant Cloud, and Neon Serverless Postgres. The implementation involves a comprehensive code audit to remove redundant files and circular imports, followed by migration of chat logic to use OpenAI Agents SDK with OpenAIChatCompletionsModel pointing to Gemini, ensuring feature parity for Selected Text RAG, Translation, and Personalization endpoints.

## Technical Context

**Language/Version**: Python 3.11, Node.js 20+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Cohere, Qdrant, Neon Postgres
**Storage**: Qdrant Cloud vector database, Neon Serverless Postgres
**Testing**: pytest, Jest
**Target Platform**: Linux server (Docker container)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <3 seconds response time for 95% of RAG queries, maintain 99% uptime for endpoints
**Constraints**: Must maintain compatibility with existing Docusaurus frontend, ensure no relative import errors, FastAPI app must launch with uvicorn
**Scale/Scope**: Support multiple concurrent users, handle textbook-sized knowledge base with efficient retrieval

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Scientific Accuracy: All technical claims must be verifiable and traceable to reputable sources ✓
- Academic Clarity: Content must be written for undergraduate-level audience with proper terminology definitions ✓
- Reproducibility & Transparency: All methods and algorithms must be presented with sufficient detail for reproduction ✓
- Ethical & Safety Awareness: All content must address ethical implications and safety constraints ✓
- Module Structure Compliance: All content must follow the fixed 4-module structure (The Robotic Nervous System (ROS 2), The Digital Twin (Gazebo & Unity), The AI-Robot Brain (NVIDIA Isaac™), Vision-Language-Action (VLA)) ✓
- Frontend Architecture: Must implement Docusaurus-based frontend with interactive module cards, glossary, quizzes, and reusable MDX components ✓
- Backend Architecture: Must implement FastAPI backend with RAG chatbot, Qdrant vector database, and translation/personalization endpoints ✓
- Personalization & Translation: Urdu toggle and personalization must function on every chapter ✓
- Change Control: Module names, structure, and hierarchy are immutable - no autonomous scope expansion allowed ✓

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-agent-upgrade/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

backend/
├── main.py              # Entry point and router mounting
├── src/
│   ├── config/          # Configuration and environment management
│   ├── api/             # API endpoints and routing
│   │   ├── v1/          # Version 1 API endpoints (chat, health)
│   │   └── rag.py       # RAG-specific logic and endpoints
│   ├── services/        # Business logic services (chat, embedding, retrieval)
│   ├── models/          # Data models and database models
│   └── middleware/      # Request/response middleware
└── tests/               # Backend tests

frontend/
├── src/
│   ├── components/      # React components (ChatInterface, etc.)
│   ├── pages/           # Docusaurus pages
│   ├── theme/           # Docusaurus theme customization
│   └── services/        # Frontend API services
└── tests/               # Frontend tests

**Structure Decision**: Web application structure with FastAPI backend and Docusaurus frontend. Backend follows 5-file target structure: main.py (entry point), agent.py (Agent SDK config), rag.py (embedding and retrieval), chat.py (endpoints), config.py (env management).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|