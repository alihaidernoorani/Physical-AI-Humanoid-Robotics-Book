---
id: 001
title: rag-backend-integration-spec
stage: spec
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-backend-integration
branch: 001-rag-backend-integration
user: alihaidernoorani
command: /sp.specify
labels: [rag, backend, integration, specification]
links:
  spec: specs/001-rag-backend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-backend-integration/spec.md
  - specs/001-rag-backend-integration/checklists/requirements.md
tests:
  - spec validation completed
---

## Prompt

```
---
id: sp.specify.rag-backend-integration
name: "RAG Backend Fix & Frontend Integration"
description: >
  Ensure the backend services are fully functional, fix all existing issues,
  and properly integrate the frontend with the backend for the RAG chatbot.
  All environment variables must be correctly used and secured in the project.
version: "1.0.0"
---

## Objective
Refactor and fix backend code to:
- Fully integrate with the frontend React chat interface.
- Use Cohere for embeddings instead of OpenAI API.
- Use OpenAI Agents SDK for chat completions with Gemini-2.5-flash.
- Ensure the backend services, RAG indexing, and per-page selected-text retrieval function correctly.

## Environment Variables
All backend and frontend code must use the following environment variables securely:
- `QDRANT_API_KEY`
- `QDRANT_URL`
- `CLUSTER_ID`
- `COHERE_API_KEY`
- `GEMINI_API_KEY`
- `NEON_DB_URL`

## Scope of Work

### Backend Fixes
- Verify and fix FastAPI backend configuration.
- Ensure proper connection and authentication to Qdrant vector database.
- Migrate embedding generation from OpenAI API to Cohere embeddings API.
- Update chat service to use OpenAI Agents SDK with Gemini-2.5-flash chat completion model.
- Ensure per-page RAG mode retrieves chunks only from user-selected text when requested.
- Add metadata to all indexed chunks: module, chapter, subsection, source_type, source_origin.
- Implement proper error handling, logging, and validation.
- Verify Neon Serverless Postgres integration works for user personalization and translation endpoints.

### Frontend Integration
- Ensure React frontend calls backend endpoints correctly.
- Text selection for per-page RAG mode is properly captured and sent to backend.
- Citation display component works based on returned chunk metadata.
- API layer handles authentication and uses environment variables where needed.
- Responsive UI works with dual mode: full-book retrieval and selected-text-only retrieval.

### Testing
- Run full test suite to verify all backend endpoints respond correctly.
- Verify embedding generation with Cohere and retrieval with Qdrant.
- Test OpenAI Agents SDK calls with Gemini-2.5-flash for chat completions.
- Test per-page RAG mode with selected text to confirm correct grounding.
- End-to-end test: ask questions from the frontend and ensure responses are accurate and grounded.

## Success Criteria
- Backend endpoints fully functional without errors or warnings.
- Embeddings generated via Cohere correctly stored in Qdrant.
- OpenAI Agents SDK integration with Gemini model works as expected.
- Per-page selected-text retrieval functions correctly.
- Frontend successfully integrated and communicates with backend.
- All environment variables securely used without hardcoding keys in the codebase.
- Project passes all tests and is deployable.

## Deliverables
- Fixed and fully functional backend code.
- Frontend integrated with backend.
- Updated documentation explaining environment variable usage.
- End-to-end verified RAG chatbot feature.
```

## Response snapshot

Created comprehensive feature specification for RAG Backend Fix & Frontend Integration. The specification includes:

1. Three prioritized user stories covering core RAG functionality, environment configuration, and dual retrieval modes
2. Functional requirements focusing on semantic search, chat completion, and secure configuration
3. Key entities including RAG Query, Knowledge Chunk, Chat Response, and Environment Configuration
4. Measurable success criteria with specific metrics for system performance and reliability

The specification was validated against quality criteria and implementation-specific details were removed to maintain technology-agnostic requirements. A quality checklist was also created to ensure the specification meets all requirements before proceeding to planning phase.

## Outcome

- ✅ Impact: Created complete feature specification for RAG backend integration
- 🧪 Tests: Spec validation completed successfully
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan
- 🧠 Reflection: Specification is comprehensive and ready for planning

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A