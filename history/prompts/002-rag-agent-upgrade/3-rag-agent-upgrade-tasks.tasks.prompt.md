---
id: 3
title: "rag-agent-upgrade-tasks"
stage: "tasks"
date_iso: "2025-12-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "rag-agent-upgrade"
branch: "002-rag-agent-upgrade"
user: "user"
command: "/sp.tasks # Integrated RAG & Agent Refactor"
labels: ["tasks", "rag", "upgrade", "ai", "agents", "architecture"]
links:
  spec: "specs/002-rag-agent-upgrade/spec.md"
  plan: "specs/002-rag-agent-upgrade/plan.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - specs/002-rag-agent-upgrade/tasks.md
tests_yaml: |
  - "task completeness validation"
  - "dependency validation"
  - "parallel execution validation"
---

# PHR: rag-agent-upgrade-tasks

## Prompt

```
# Integrated RAG & Agent Refactor

## T1 — Audit, Inventory & Cleanup

**Project Scan**
- Analyze all files in `backend/` and `frontend/` to identify existing chat logic.

**Inventory Report**
- Generate a Markdown list of:
  - **Files to KEEP** (aligned with the 5-file backend structure).
  - **Files to DELETE** (redundant logic or unused modules).
  - **Circular imports** and **broken absolute paths** to be fixed.

**Environment Setup**
- Verify that the following packages are listed in `requirements.txt`:
  - `openai-agents`
  - `openai-chatkit`
  - `cohere`
  - `qdrant-client`

---

## T2 — Backend Core: Agents & RAG Integration

**Gemini Bridge**
- Configure `app/agent.py` using `OpenAIChatCompletionsModel` with the Gemini OpenAI-compatible `base_url`.

**RAG Engine**
- Implement `app/rag.py` using:
  - **Cohere** for `embed-multilingual-v3.0` generation.
  - **Qdrant** for context retrieval.

**ChatKit Server**
- Implement `ChatKitServer` in `app/chat.py`.
- Override the `respond` method to call the **Agents SDK Runner**.

**State Management**
- Connect **Neon Postgres** to store conversation threads as required by the ChatKit protocol.

---

## T3 — Contextual Logic & Feature Endpoints

**Selected-Text Priority**
- In `agent.py`, check for `selected_text` in the request context and prioritize it over Qdrant retrieval.

**Additional Endpoints**
- Implement and test:
  - `/translate`
  - `/personalize`
  - Endpoints within the FastAPI app.

**Consolidation**
- Move all routing to `app/main.py`.
- Ensure that `uvicorn app.main:app` starts **without errors**.

---

## T4 — Docusaurus Frontend & Integration Test

**ChatKit UI**
- Replace custom chat logic with the `@openai/chatkit-react` widget (or equivalent script) in Docusaurus.

**Highlight Listener**
- Implement a React hook to capture `window.getSelection()` and pass it to the ChatKit session context.

**End-to-End Test**
- Verify that highlighting text in the book correctly influences the chatbot's response in the UI.
```

## Response

Generated comprehensive task list for the RAG Agent Upgrade feature following the specified 5-file backend structure:
- app/main.py: Entry point and router mounting
- app/agent.py: Agent SDK configuration and Gemini bridge
- app/rag.py: Cohere embedding logic and Qdrant retrieval
- app/chat.py: Endpoints (/chat, /translate, /personalize)
- app/config.py: Environment variable management

The tasks.md file contains 34 specific, actionable tasks organized across 7 phases:
1. Setup (T001-T005): Environment verification and audit
2. Foundational (T006-T010): 5-file backend structure implementation
3. [US1] RAG Chat Experience (T011-T018): Core RAG functionality with selected text priority
4. [US2] Multilingual Support (T019-T021): Translation endpoint implementation
5. [US3] Personalized Learning (T022-T024): Personalization endpoint implementation
6. Frontend Integration (T025-T028): ChatKit UI and selected text functionality
7. Polish & Cross-Cutting (T029-T034): Integration, testing, and optimization

Each task follows the required checklist format with proper IDs, story labels, and file paths. The implementation strategy focuses on the surgical refactor approach with clear dependencies between user stories and parallel execution opportunities identified.

## Outcome

Tasks generation phase completed successfully with a well-structured, actionable task list that follows the exact 5-file backend structure specified in the requirements. The tasks are organized by user story priority to enable independent implementation and testing while maintaining proper dependencies.

## Evaluation

The task list successfully addresses all requirements from the user prompt, including the specific 5-file backend structure, Gemini bridge configuration, Cohere embeddings, Qdrant integration, selected-text priority logic, and frontend ChatKit integration. The tasks are specific enough for LLM execution while maintaining appropriate dependencies and parallel execution opportunities.