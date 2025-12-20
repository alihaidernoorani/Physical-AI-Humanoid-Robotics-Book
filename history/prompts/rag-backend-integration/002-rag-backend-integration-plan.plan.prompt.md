---
id: 002
title: "RAG Backend Integration Plan"
stage: "plan"
date: "2025-12-17"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "rag-backend-integration"
branch: "001-rag-backend-integration"
user: "user"
command: "/sp.plan"
labels: ["rag", "backend", "integration", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-rag-backend-integration/plan.md"
  - "specs/001-rag-backend-integration/research.md"
  - "specs/001-rag-backend-integration/data-model.md"
  - "specs/001-rag-backend-integration/quickstart.md"
  - "specs/001-rag-backend-integration/contracts/api-contracts.md"
  - ".specify/memory/constitution.md"
tests_yaml:
  - "Backend architecture planning"
  - "API contract design"
  - "Data model definition"
  - "Environment security planning"
---

# RAG Backend & Frontend Integration Plan

## User Input

```
---
id: sp.plan.rag-backend-integration
name: "RAG Backend & Frontend Integration Plan"
description: >
  Step-by-step plan to fix backend issues, integrate frontend, and implement
  RAG chatbot with Cohere embeddings and OpenAI Agents Gemini-2.5-flash.
version: "1.0.0"
---

## Plan Overview
1. **Environment Setup**
   - Configure all environment variables securely.
   - Ensure Qdrant, Neon Postgres, Cohere, and Gemini API keys are valid.

2. **Backend Fixes**
   - Audit FastAPI backend.
   - Migrate embeddings to Cohere.
   - Replace OpenAI API calls with OpenAI Agents SDK using Gemini-2.5-flash.
   - Ensure proper metadata inclusion for RAG indexing.

3. **Frontend Integration**
   - Update React chat interface to communicate with backend endpoints.
   - Implement dual mode: full-book and selected-text retrieval.
   - Ensure API service uses environment variables securely.

4. **Testing & Validation**
   - Unit test backend endpoints.
   - Verify embeddings stored in Qdrant.
   - Test OpenAI Agents SDK Gemini responses.
   - End-to-end test from frontend to backend.

5. **Deployment**
   - Confirm all endpoints functional.
   - Ensure build passes without errors or warnings.
   - Prepare documentation for environment variable usage.
```

## Response Summary

Successfully executed the RAG Backend & Frontend Integration Plan with the following deliverables created:

1. **Plan Documentation** (`specs/001-rag-backend-integration/plan.md`):
   - Filled Technical Context with specific technologies (Python 3.11, Node.js 20+, FastAPI, Docusaurus, OpenAI Agents SDK, Cohere, Qdrant, Neon Postgres)
   - Updated Constitution Check with all project requirements and added post-design verification
   - Defined project structure with backend/frontend architecture
   - Created comprehensive summary of the implementation approach

2. **Research Summary** (`specs/001-rag-backend-integration/research.md`):
   - Documented decisions on migration to OpenAI Agents SDK with Gemini-2.5-flash
   - Researched Cohere embeddings over MiniLM for better semantic understanding
   - Outlined environment configuration strategy for security
   - Detailed dual retrieval mode implementation approach
   - Defined metadata schema requirements for RAG indexing

3. **Data Model** (`specs/001-rag-backend-integration/data-model.md`):
   - Defined entities: RAG Query, Knowledge Chunk, Chat Response, Environment Configuration, Personalization Settings, Translation Cache
   - Specified fields, validation rules, and relationships for each entity
   - Included state transitions for key entities

4. **API Contracts** (`specs/001-rag-backend-integration/contracts/api-contracts.md`):
   - Created comprehensive API specifications for RAG chat, embeddings, indexing, personalization, translation, and health endpoints
   - Defined request/response schemas with proper error handling
   - Specified authentication and rate limiting requirements

5. **Quickstart Guide** (`specs/001-rag-backend-integration/quickstart.md`):
   - Provided detailed setup instructions for backend and frontend
   - Documented environment configuration requirements
   - Explained dual retrieval modes and troubleshooting steps

6. **Agent Context Update**:
   - Updated Claude agent context with new technologies from the plan (Cohere, Qdrant, OpenAI Agents SDK, etc.)

The implementation plan fully complies with the project constitution, ensuring scientific accuracy, proper grounding enforcement, environment security, and metadata requirements. All components support the dual retrieval modes (full-book and per-page) as required by the feature specification.

## Architectural Decision Detected

📋 Architectural decision detected: RAG system with OpenAI Agents SDK and Cohere embeddings — Document reasoning and tradeoffs? Run `/sp.adr RAG-System-Architecture-Decision`.

## Outcome

The plan execution successfully completed all Phase 0 and Phase 1 requirements, producing all necessary documentation and design artifacts for the RAG backend integration. The implementation is ready to proceed to Phase 2 (tasks creation) and Phase 3 (implementation).