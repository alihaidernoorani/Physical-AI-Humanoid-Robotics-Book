---
id: 2
title: "rag-agent-upgrade-planning"
stage: "plan"
date_iso: "2025-12-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "rag-agent-upgrade"
branch: "002-rag-agent-upgrade"
user: "user"
command: "/sp.plan Surgical Refactor & RAG Integration"
labels: ["plan", "rag", "upgrade", "ai", "agents", "architecture"]
links:
  spec: "specs/002-rag-agent-upgrade/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - specs/002-rag-agent-upgrade/plan.md
  - specs/002-rag-agent-upgrade/research.md
  - specs/002-rag-agent-upgrade/data-model.md
  - specs/002-rag-agent-upgrade/quickstart.md
  - specs/002-rag-agent-upgrade/contracts/chat-api.yaml
  - specs/002-rag-agent-upgrade/contracts/rag-api.yaml
tests_yaml: |
  - "constitution check validation"
  - "data model validation"
  - "api contract validation"
---

# PHR: rag-agent-upgrade-planning

## Prompt

```
Surgical Refactor & RAG Integration
Architecture Overview: Refine the existing project by consolidating the FastAPI backend and Docusaurus frontend. The system must transition to a structured OpenAI Agents SDK implementation using Gemini-2.5-flash

Tech Stack Decisions:

- Backend: FastAPI (Refine existing /backend).

- Agent SDK: OpenAI Agents SDK (Bridge to Gemini via OpenAI-compatible base URL).

- Model: gemini-2.5-flash.

- Embeddings: Cohere

- Vector DB: Qdrant Cloud.

- Relational DB: Neon Postgres


Refinement Strategy:

Inventory & Audit (Constraint 1): Execute a full scan of backend/ and frontend/. Identify circular imports and verify which files align with the target 5-file backend structure:

1) app/main.py: Entry point and router mounting.

2) app/agent.py: Agent SDK configuration and Gemini bridge.

3) app/rag.py: Cohere embedding logic and Qdrant retrieval.

4) app/chat.py: Endpoints (/chat, /translate, /personalize).

5) app/config.py: Environment variable management.


- Consolidation Pass: Merge overlapping chatbot logic into the established 5-file backend structure (main, agent, rag, chat, config).

- Selected-Text Logic: Implement a high-priority context handler that overrides general RAG when selected_text is passed from the Docusaurus frontend.


Constraints:

- Inventory First: Do not write new code until a list of "files to keep" and "files to delete" is generated and verified.

- Minimal Diff: Prefer editing existing files over creating new ones.

- Task Limit: Aim for a minimum of tasks with the last few tasks dedicated to quality checks and that the build properly works
```

## Response

Completed comprehensive planning for the RAG Agent Upgrade feature. Key deliverables include:

1. **Implementation Plan** (plan.md): Detailed architecture plan with technical context, constitution check, and project structure aligned with the 5-file backend target structure.

2. **Research Document** (research.md): Comprehensive audit of current backend structure with files to keep, consolidate, and delete. Identified circular imports and recommended implementation approach.

3. **Data Model** (data-model.md): Complete entity definitions for Chat Session, Message, Vector Embedding, Knowledge Base Chunk, and User Preferences with validation rules and relationships.

4. **Quickstart Guide** (quickstart.md): Setup instructions including prerequisites, environment configuration, API endpoints, and deployment instructions with OpenAI ChatKit SDK integration.

5. **API Contracts** (contracts/):
   - chat-api.yaml: OpenAPI specification for chat, translation, personalization, and health endpoints
   - rag-api.yaml: OpenAPI specification for RAG-specific functionality (search, embeddings, indexing)

6. **Agent Context Update**: Updated CLAUDE.md with new technology stack (Python 3.11, Node.js 20+, FastAPI, OpenAI Agents SDK, Cohere, Qdrant, Neon Postgres).

The plan addresses all requirements including code audit, SDK migration to OpenAI Agents SDK with Gemini bridge, feature parity for RAG, translation and personalization endpoints, and unified Cohere embeddings. The constitution check passed with all requirements satisfied.

## Outcome

Planning phase completed successfully with all required artifacts created. The implementation plan provides a clear roadmap for the surgical refactor, with identified files for consolidation and clear migration path to the target 5-file backend structure. Ready to proceed to task generation phase.

## Evaluation

The planning phase successfully delivered all required artifacts with comprehensive coverage of the technical requirements. The architecture aligns with the specified tech stack and maintains compatibility with existing Docusaurus frontend while upgrading to OpenAI Agents SDK with Gemini integration.