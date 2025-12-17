# Tasks: Integrated RAG Chatbot

**Feature**: Integrated RAG Chatbot
**Feature Branch**: `001-rag-chatbot`
**Generated**: 2025-12-16
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Input**: Feature specification: Build and embed a Retrieval-Augmented Generation chatbot within the published textbook to answer questions grounded in book content or user-selected text.

## Implementation Strategy

This document outlines the implementation tasks for the RAG chatbot, organized by priority and dependencies. The approach follows an MVP-first strategy, with User Story 1 (core textbook Q&A) as the minimum viable product, followed by User Story 2 (selected text mode), and finally User Story 3 (UI integration).

## Dependencies

User stories completion order:
- User Story 1 (P1) must be completed before User Story 2 (P2) and User Story 3 (P3)
- User Story 2 (P2) can be developed in parallel with User Story 3 (P3) after User Story 1 is complete

## Parallel Execution Examples

Per user story:
- **User Story 1**: Textbook content preparation (T010-T015) can run in parallel with backend foundation (T020-T025)
- **User Story 2**: Selected text mode implementation (T040-T045) can run in parallel with guardrails (T050-T055)
- **User Story 3**: Frontend chat UI (T060-T065) can run in parallel with API integration (T070-T075)

## Phase 1: Setup Tasks

- [X] T001 Create project structure with backend/ and frontend/ directories per implementation plan
- [X] T002 Set up development environment with Python 3.11+, Node.js 18+, and required dependencies
- [X] T003 Configure Qdrant vector database connection and Neon Serverless Postgres connection
- [X] T004 Set up API documentation with FastAPI automatic docs
- [X] T005 Create initial configuration files and environment variable handling

## Phase 2: Foundational Tasks

- [X] T010 Set up project dependencies for backend (FastAPI, sentence-transformers, Qdrant, OpenAI, Neon Postgres)
- [X] T011 Set up project dependencies for frontend (React components for chat interface)
- [X] T012 Create base data models for ChatSession, RetrievedContext, UserQuery, and GeneratedResponse
- [X] T013 Implement database connection and session management for Neon Postgres
- [X] T014 Create API base structure with proper error handling and validation
- [X] T015 Set up testing framework (pytest for backend, Jest for frontend)

## Phase 3: User Story 1 - Chatbot answers questions from textbook content (P1)

- [X] T020 [P] Extract textbook content from docs/ directory modules (module-1 through module-4)
- [X] T021 [P] Implement text chunker utility to split content into 300-500 token chunks
- [X] T022 [P] [US1] Generate embeddings for all textbook content using all-MiniLM-L6-v2 model
- [X] T023 [P] [US1] Create Qdrant collection for textbook chunks with proper metadata schema
- [X] T024 [US1] Store textbook chunks in Qdrant with module, chapter, section metadata
- [X] T025 [US1] Implement similarity search in Qdrant to retrieve top-k relevant chunks
- [X] T030 [US1] Create chat service that retrieves context and generates responses
- [X] T031 [US1] Integrate OpenAI Agents for response generation from retrieved context
- [X] T032 [US1] Implement citation functionality to reference textbook sections
- [X] T033 [US1] Create /api/v1/chat endpoint for full-text mode queries
- [X] T034 [US1] Implement response validation to ensure grounding in context
- [X] T035 [US1] Test User Story 1: Verify responses are accurate and sourced from textbook content

## Phase 4: User Story 2 - Selected text mode for focused questioning (P2)

- [X] T040 [P] [US2] Create selected text mode endpoint that bypasses vector search
- [X] T041 [P] [US2] Implement logic to restrict answers to user-provided selected text only
- [X] T042 [US2] Update chat service to handle selected text mode requests
- [X] T043 [US2] Modify OpenAI Agent integration to work with selected text context
- [X] T044 [US2] Add selected text validation to ensure proper context length
- [X] T045 [US2] Test User Story 2: Verify responses are based exclusively on selected text
- [X] T050 [P] [US2] Implement guardrails to refuse answers when context is insufficient
- [X] T051 [US2] Add refusal handling for out-of-scope questions in both modes
- [X] T052 [US2] Create proper error responses when information is not available in context
- [X] T053 [US2] Implement confidence scoring for grounding verification
- [X] T054 [US2] Add logging for refused requests to track common question patterns
- [X] T055 [US2] Test guardrails: Verify system correctly refuses to answer when context unavailable

## Phase 5: User Story 3 - Embedded chat interface within textbook UI (P3)

- [X] T060 [P] [US3] Create React chat interface component with message history
- [X] T061 [P] [US3] Implement chat input area with mode toggle (full-text vs selected-text)
- [X] T062 [US3] Add text selection handler to capture user-highlighted content
- [X] T063 [US3] Create citation display component to show source references
- [X] T064 [US3] Implement chat window with responsive design for textbook pages
- [X] T065 [US3] Style chat interface to match textbook's Docusaurus theme
- [X] T070 [P] [US3] Integrate chat API calls with frontend service layer
- [X] T071 [P] [US3] Create session management in frontend to maintain conversation state
- [X] T072 [US3] Add mode switching functionality (full-text vs selected-text)
- [X] T073 [US3] Implement loading states and error handling in UI
- [X] T074 [US3] Add keyboard shortcuts for common chat actions
- [X] T075 [US3] Test User Story 3: Verify seamless integration without impacting textbook load times

## Phase 6: Testing and Validation

- [ ] T080 [P] Create unit tests for backend services (embedding, retrieval, chat)
- [ ] T081 [P] Create unit tests for frontend components (chat interface, text selection)
- [ ] T082 [P] Create integration tests for API endpoints
- [ ] T083 [P] Create RAG-specific validation tests for grounding accuracy
- [ ] T084 [P] Create performance tests to ensure <5s response times
- [ ] T085 [P] Create end-to-end tests covering all user stories
- [ ] T086 [P] Test accuracy on seeded questions with known answers
- [ ] T087 [P] Test refusal behavior when context is insufficient
- [ ] T088 [P] Test selected text mode accuracy (98% requirement)
- [ ] T089 [P] Test citation accuracy and proper source attribution

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T090 [P] Implement rate limiting (60 requests/min per user, 1000/min per IP)
- [ ] T091 [P] Add comprehensive logging and monitoring for production
- [ ] T092 [P] Create health check endpoint with dependency status reporting
- [ ] T093 [P] Add authentication middleware for API endpoints
- [ ] T094 [P] Optimize response caching to improve performance
- [ ] T095 [P] Create deployment configuration for serverless platforms
- [ ] T096 [P] Add error tracking and alerting for production issues
- [ ] T097 [P] Create documentation for API usage and frontend integration
- [ ] T098 [P] Create runbooks for common operational tasks
- [ ] T099 [P] Deploy system and validate stable operation with no hallucinations