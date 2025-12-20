# Implementation Tasks: RAG Agent Upgrade

**Feature**: RAG Agent Upgrade
**Branch**: `002-rag-agent-upgrade`
**Input**: Feature specification from `/specs/002-rag-agent-upgrade/spec.md`

## Implementation Strategy

This implementation follows a surgical refactor approach to upgrade the existing FastAPI and Docusaurus codebase to implement a production-ready RAG system using the OpenAI Agents SDK with Gemini-2.5-flash. The implementation follows the target 5-file backend structure:
- app/main.py: Entry point and router mounting
- app/agent.py: Agent SDK configuration and Gemini bridge
- app/rag.py: Cohere embedding logic and Qdrant retrieval
- app/chat.py: Endpoints (/chat, /translate, /personalize)
- app/config.py: Environment variable management

The implementation is organized into user story-driven phases to enable independent testing and incremental delivery.

**MVP Scope**: User Story 1 (RAG Chat Experience) with basic functionality - chat endpoint with RAG capabilities and selected text handling.

## Dependencies

- User Story 1 (P1) - RAG Chat Experience: Foundational backend services (config, agent, rag, chat)
- User Story 2 (P2) - Multilingual Support: Depends on User Story 1 (chat infrastructure)
- User Story 3 (P3) - Personalized Learning: Depends on User Story 1 (chat infrastructure)

## Parallel Execution Examples

- T001-T004 (Setup tasks) can run in parallel with T005-T008 (Backend structure tasks)
- T010-T012 (Agent & RAG tasks) can run in parallel with T013-T014 (Chat & UI tasks)

## Phase 1: Setup

### Goal
Initialize project structure and verify environment requirements

- [x] T001 Verify openai-chatkit is in requirements.txt (add if missing)
- [x] T002 Audit backend/ and frontend/ for existing chat logic files
- [x] T003 Generate inventory report of files to KEEP, DELETE, and consolidate
- [x] T004 Fix any circular imports and broken absolute paths identified
- [x] T005 Create app/ directory structure if it doesn't exist

## Phase 2: Foundational

### Goal
Establish core backend structure following the 5-file target structure

- [x] T006 Create/Update app/config.py with centralized environment variable management
- [x] T007 Create/Update app/main.py with entry point and router mounting
- [x] T008 Create/Update app/agent.py with OpenAI Agents SDK configuration for Gemini bridge AND ChatKit protocol-compliant conversation state management
- [x] T009 Create/Update app/rag.py with Cohere embed-multilingual-v3.0 and Qdrant retrieval
- [x] T010 Create/Update app/chat.py with all endpoints (/chat, /translate, /personalize)

## Phase 3: [US1] RAG Chat Experience

### Goal
Implement core RAG chat functionality with selected text priority handling

### Independent Test Criteria
Can be fully tested by submitting various questions about textbook content and verifying that the chatbot provides relevant, accurate responses with proper citations to source material.

- [x] T011 Configure OpenAIChatCompletionsModel with Gemini base URL in agent.py
- [x] T012 Implement Cohere embedding generation in rag.py using embed-multilingual-v3.0
- [x] T013 Implement Qdrant retrieval functionality in rag.py
- [x] T014 Connect Neon Postgres for conversation thread storage
- [x] T014a Verify Neon Postgres thread storage follows ChatKit protocol for conversation state management
- [x] T015 Implement /api/v1/chat endpoint in chat.py with proper selected_text handling
- [x] T016 Implement selected-text priority logic in agent.py that overrides general RAG when selected_text is provided
- [x] T017 Test RAG chat functionality with various textbook queries
- [x] T018 Verify selected text overrides general RAG when provided

## Phase 4: [US2] Multilingual Support

### Goal
Implement translation functionality for multilingual textbook content

### Independent Test Criteria
Can be tested by toggling between languages and verifying that content is accurately translated while maintaining technical accuracy.

- [x] T019 Implement /api/v1/translate endpoint in chat.py using Cohere translation capabilities
- [x] T020 Test translation functionality with textbook content in multiple languages
- [x] T021 Verify technical terminology preservation in translations

## Phase 5: [US3] Personalized Learning

### Goal
Implement content personalization based on user learning preferences

### Independent Test Criteria
Can be tested by adjusting personalization settings and verifying that explanations adapt in complexity and detail.

- [x] T022 Implement /api/v1/personalize endpoint in chat.py with learning level support (beginner, intermediate, advanced)
- [x] T023 Add personalization logic to adjust content complexity based on user preferences
- [x] T024 Test personalization functionality with different learning level preferences

## Phase 6: Frontend Integration

### Goal
Integrate OpenAI ChatKit UI and implement selected text functionality

- [ ] T025 Install @openai/chatkit-react in frontend dependencies
- [ ] T026 Replace custom chat logic with @openai/chatkit-react widget in Docusaurus
- [ ] T027 Implement React hook to capture window.getSelection() and pass to ChatKit session context
- [ ] T028 Test end-to-end functionality: highlighting text in book influences chatbot response in UI

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Final integration, testing, and optimization

- [x] T029 Verify all endpoints work: /chat, /translate, /personalize, /health
- [x] T030 Run integration test: highlight text → pass to chat → receive context-aware response
- [x] T031 Ensure FastAPI app launches with uvicorn and maintains compatibility with existing frontend
- [ ] T032 Verify code audit removes at least 90% of redundant files and circular imports
- [ ] T033 Confirm all vector operations use Cohere embed-multilingual-v3.0 with no performance degradation
- [x] T034 Verify uvicorn app.main:app starts without errors and follows 5-file structure