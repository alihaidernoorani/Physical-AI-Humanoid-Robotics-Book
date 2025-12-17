# Implementation Tasks: RAG Chatbot Architecture Migration

**Feature**: RAG Chatbot Architecture Migration
**Branch**: `001-rag-architecture-migration`
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Created**: 2025-12-17

## Task Format
Each task follows the format: `[ ] T### [P] [US#] Description with file path`
- `[P]` = Parallelizable task (different files, no dependencies)
- `[US#]` = User Story label (for user story phases only)

## Phase 1: Setup and Project Initialization

- [ ] T001 Create `/frontend` directory structure in project root
- [ ] T002 Identify all frontend-related files and assets that need migration
- [ ] T003 Update project root gitignore to exclude frontend build artifacts from new location
- [ ] T004 Set up initial frontend directory structure with src/, docs/, and config files

## Phase 2: Foundational Tasks

- [ ] T010 Install Cohere SDK dependency in backend requirements.txt
- [ ] T011 Install OpenAI Agents SDK dependency in backend requirements.txt
- [ ] T012 Update settings.py to include Cohere and Google API configuration
- [ ] T013 Create environment variable validation for new configuration
- [ ] T014 Update backend dependencies to support Gemini inference

## Phase 3: User Story 1 - Continue using RAG chatbot without functional regression [P1]

### Tests for User Story 1
- [ ] T020 [P] [US1] Create regression tests to verify chatbot responses remain equivalent to previous implementation
- [ ] T021 [P] [US1] Create tests to verify grounding behavior preservation
- [ ] T022 [P] [US1] Create tests to verify safety and refusal mechanisms remain intact

### Models for User Story 1
- [ ] T030 [P] [US1] Update embedding_service.py to support Cohere embedding vectors
- [ ] T031 [P] [US1] Update TextChunk model in data model to accommodate Cohere vector dimensions

### Services for User Story 1
- [ ] T040 [US1] Update embedding_service.py to use Cohere API instead of Sentence Transformers
- [ ] T041 [US1] Update retrieval_service.py to work with Cohere embeddings in Qdrant
- [ ] T042 [US1] Update chat_service.py to use OpenAI Agents SDK with Gemini-2.5-flash
- [ ] T043 [US1] Preserve grounding behavior and refusal logic in updated chat service
- [ ] T044 [US1] Ensure selected-text-only mode functionality remains intact in chat service

### Endpoints for User Story 1
- [ ] T050 [US1] Update chat API endpoints to work with new inference framework
- [ ] T051 [US1] Verify API contracts remain backward compatible
- [ ] T052 [US1] Test chat query endpoint with new inference pipeline

## Phase 4: User Story 2 - Access frontend from new directory structure [P2]

### Tests for User Story 2
- [ ] T060 [P] [US2] Create tests to verify all frontend assets load correctly from new structure
- [ ] T061 [P] [US2] Create UI interaction tests for frontend functionality verification

### Frontend Migration
- [ ] T070 [P] [US2] Move docusaurus.config.ts to `/frontend/docusaurus.config.ts`
- [ ] T071 [P] [US2] Move package.json to `/frontend/package.json`
- [ ] T072 [P] [US2] Move sidebars.ts to `/frontend/sidebars.ts`
- [ ] T073 [P] [US2] Move tsconfig.json to `/frontend/tsconfig.json`
- [ ] T074 [P] [US2] Move docs/ directory to `/frontend/docs/`
- [ ] T075 [P] [US2] Move existing `/frontend/src` to `/frontend/src` (reorganize if needed)

### Build Configuration Updates
- [ ] T080 [US2] Update frontend package.json scripts to work from new location
- [ ] T081 [US2] Update docusaurus.config.ts to reference docs from new location
- [ ] T082 [US2] Update import paths in frontend components to reflect new structure
- [ ] T083 [US2] Update any absolute paths in frontend code to work with new structure
- [ ] T084 [US2] Update deployment configuration for GitHub Pages from new structure

## Phase 5: User Story 3 - Experience chatbot responses from new inference framework [P3]

### Tests for User Story 3
- [ ] T090 [P] [US3] Create tests to verify responses are generated via OpenAI Agents SDK
- [ ] T091 [P] [US3] Create tests to verify Gemini model is used for inference
- [ ] T092 [P] [US3] Create tests to verify quality and safety standards are maintained

### Inference Framework Migration
- [ ] T100 [US3] Replace OpenAI ChatCompletion calls with OpenAI Agents SDK
- [ ] T101 [US3] Configure Gemini-2.5-flash as the inference model in the agents framework
- [ ] T102 [US3] Update chat_service.py to use new inference framework while preserving grounding
- [ ] T103 [US3] Ensure safety and refusal behavior is maintained with new model
- [ ] T104 [US3] Test response generation quality with new inference framework

## Phase 6: Integration and Validation

### Embedding Provider Migration
- [ ] T110 Remove Sentence Transformers dependencies from backend
- [ ] T111 Update embedding generation process to use Cohere vectors
- [ ] T112 Verify Qdrant compatibility with Cohere embeddings
- [ ] T113 Test retrieval accuracy with new Cohere embeddings
- [ ] T114 Re-index or validate embeddings in Qdrant with Cohere vectors

### Environment Configuration
- [ ] T120 Update .env template with new Cohere and Google API variables
- [ ] T121 Validate all environment variables for new architecture components
- [ ] T122 Update documentation for new configuration requirements

### Cross-Cutting Validation
- [ ] T130 Verify selected-text-only mode still functions after all migrations
- [ ] T131 Run backend build and fix any errors or warnings
- [ ] T132 Run frontend build and fix any errors or warnings
- [ ] T133 Test complete RAG flow from query to response with new architecture
- [ ] T134 Verify no regression in functionality compared to previous implementation

## Phase 7: Polish & Cross-Cutting Concerns

### Quality Assurance
- [ ] T140 Run all backend tests and ensure they pass
- [ ] T141 Run all frontend tests and ensure they pass
- [ ] T142 Perform end-to-end integration tests
- [ ] T143 Verify response quality and safety standards meet requirements
- [ ] T144 Test retrieval accuracy against previous implementation

### Documentation and Finalization
- [ ] T150 Update README with new directory structure information
- [ ] T151 Update quickstart guide with new setup instructions
- [ ] T152 Update API documentation if needed
- [ ] T153 Verify application builds and runs with zero errors and zero warnings
- [ ] T154 Confirm all functional requirements (FR-001 through FR-012) are met

## Dependencies

### User Story Completion Order
- User Story 1 (P1 - Continue using RAG chatbot) must be completed before User Story 3 (P3 - New inference framework)
- User Story 2 (P2 - Frontend restructure) can be completed in parallel with other stories
- All foundational tasks (Phase 2) must be completed before user story phases

### Critical Path
1. Foundational tasks (Phase 2)
2. User Story 1 (P1) - Core RAG functionality migration
3. User Story 2 (P2) - Frontend restructure
4. User Story 3 (P3) - Inference framework migration
5. Integration and validation (Phase 6)
6. Polish and finalization (Phase 7)

## Parallel Execution Examples

### Parallel Tasks within User Story 1
- T020, T021, T022 (tests) can run in parallel
- T030, T031 (models) can run in parallel
- T040, T041, T042, T043, T044 (services) can work on different files

### Parallel Tasks within User Story 2
- T070, T071, T072, T073, T074 (file moves) can happen in parallel
- T080, T081, T082, T083 (configuration updates) can work on different files

### Parallel Tasks within User Story 3
- T090, T091, T092 (tests) can run in parallel
- T100, T101, T102, T103, T104 (inference updates) can work on different components

## Implementation Strategy

### MVP Scope
- Focus on User Story 1 first: Core RAG functionality with Cohere embeddings and OpenAI Agents SDK
- Ensure grounding behavior and safety mechanisms are preserved
- Basic frontend migration to new directory structure

### Incremental Delivery
1. Complete foundational setup and dependencies
2. Implement Cohere embedding service with Qdrant compatibility
3. Migrate frontend files to new directory structure
4. Integrate OpenAI Agents SDK with Gemini model
5. Validate and test complete functionality
6. Polish and finalize all components

### Risk Mitigation
- Maintain backward compatibility throughout migration
- Implement comprehensive testing to catch regressions early
- Keep current implementation as backup during migration
- Test in staging environment before production deployment