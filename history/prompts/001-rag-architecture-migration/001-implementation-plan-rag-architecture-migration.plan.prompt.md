---
id: "001"
title: "Implementation Plan RAG Architecture Migration"
stage: "plan"
date: "2025-12-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "rag-architecture-migration"
branch: "001-rag-architecture-migration"
user: "user"
command: "/sp.plan"
labels:
  - "architecture"
  - "migration"
  - "frontend"
  - "cohere"
  - "gemini"
  - "rag"
links:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
files:
  - /specs/001-rag-architecture-migration/plan.md
  - /specs/001-rag-architecture-migration/research.md
  - /specs/001-rag-architecture-migration/data-model.md
  - /specs/001-rag-architecture-migration/quickstart.md
  - /specs/001-rag-architecture-migration/contracts/chat-api.yaml
  - /specs/001-rag-architecture-migration/contracts/health-api.yaml
  - /specs/001-rag-architecture-migration/contracts/textbook-api.yaml
tests: []
prompt: |
  ---
  feature: rag-chatbot-architecture-migration
  ---

  This migration will proceed in controlled phases. First, frontend files will be identified, relocated into a `/frontend` directory, and all imports, build scripts, and paths updated accordingly. Second, the embedding layer will be refactored to use Cohere, including environment configuration, embedding generation, and compatibility with Qdrant. Third, the inference layer will be replaced by the OpenAI Agents SDK, removing direct Chat API usage and configuring Gemini-2.5-flash as the model. Existing RAG grounding, selected-text mode, refusal logic, and API contracts will be preserved throughout. After implementation, full builds and runtime tests will be executed to confirm zero regressions before marking completion.
response: |
  Implementation plan created for RAG Chatbot Architecture Migration. The plan includes:

  1. Technical Context: Documented current technologies (Python 3.11, TypeScript/JavaScript, FastAPI, Docusaurus, Qdrant, etc.) and migration targets (Cohere embeddings, OpenAI Agents SDK, Gemini-2.5-flash).

  2. Project Structure: Detailed both current structure (mixed frontend files in root) and target structure (frontend files consolidated in /frontend directory).

  3. Research: Created comprehensive research document covering frontend restructuring, embedding migration from Sentence Transformers to Cohere, inference migration to OpenAI Agents SDK with Gemini, Qdrant compatibility, environment configuration, zero regression strategy, and build pipeline updates.

  4. Data Model: Defined key entities (ChatSession, UserQuery, GeneratedResponse, RetrievedContext, TextChunk, ChatMode) with fields, relationships, and validation rules.

  5. API Contracts: Created contracts for Chat API, Health Check API, and Textbook Content API with detailed endpoints, request/response formats, and error handling.

  6. Quickstart Guide: Created comprehensive guide for developers to set up and run the migrated system.

  7. Agent Context: Updated CLAUDE.md with new technology stack information.
outcome: "Plan successfully created with all required artifacts: plan.md, research.md, data-model.md, quickstart.md, and API contracts in the contracts/ directory. The plan addresses all three phases of the migration: frontend restructure, embedding migration to Cohere, and inference migration to OpenAI Agents SDK with Gemini-2.5-flash. Zero functional regression is maintained throughout."
evaluation: "All required plan artifacts have been created and follow the template structure. The plan addresses the migration requirements while maintaining compliance with the project constitution. API contracts are properly defined with request/response formats. Data models are complete with validation rules. The quickstart guide provides clear instructions for developers."
---