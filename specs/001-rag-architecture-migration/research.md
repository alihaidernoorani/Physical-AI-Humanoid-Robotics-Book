# Research: RAG Chatbot Architecture Migration

## Overview
This research document addresses technical decisions and best practices for migrating the existing integrated RAG chatbot to a revised architecture that reorganizes frontend code, replaces the embedding provider with Cohere, and replaces the OpenAI Chat API with the OpenAI Agents SDK using a Gemini model.

## Decision: Frontend Directory Restructure
**Rationale**: Moving all Docusaurus-related files to a dedicated `/frontend` directory improves project organization, maintainability, and separation of concerns. This follows modern web application architecture patterns and makes it clearer which files belong to the frontend vs backend.

**Implementation approach**:
- Move `docusaurus.config.ts`, `package.json`, `sidebars.ts`, `tsconfig.json` to `/frontend`
- Move `docs/` directory to `/frontend/docs`
- Move existing `/frontend/src` to `/frontend/src`
- Update all import paths and build configurations to reflect new structure
- Update deployment scripts to reference new paths

**Alternatives considered**:
- Keep current mixed structure (harder to maintain and understand)
- Split into more granular directories (over-engineering for this project)
- Use monorepo tools like Lerna or Nx (unnecessary complexity for this scale)

## Decision: Embedding Migration from Sentence Transformers to Cohere
**Rationale**: Cohere embeddings provide state-of-the-art semantic understanding and are well-suited for RAG applications. They offer better performance than MiniLM embeddings for complex semantic searches and are designed specifically for retrieval-augmented generation use cases.

**Implementation approach**:
- Replace Sentence Transformers with Cohere embedding service
- Update `embedding_service.py` to use Cohere API
- Add `COHERE_API_KEY` to environment variables
- Update settings.py to include Cohere configuration
- Ensure compatibility with Qdrant vector database
- Maintain same chunk size (300-500 tokens) and retrieval parameters
- Test retrieval accuracy against current implementation

**Alternatives considered**:
- OpenAI embeddings (cost concerns for large textbook)
- Custom-trained embeddings (overkill for this use case)
- Other transformer models (performance vs. accuracy trade-offs)
- Keep current MiniLM embeddings (doesn't meet migration requirements)

## Decision: Inference Migration from OpenAI Chat Completions to OpenAI Agents SDK with Gemini
**Rationale**: OpenAI Agents SDK provides better control over the reasoning process and allows for stricter grounding enforcement. Using Gemini-2.5-flash as specified in requirements offers competitive performance for RAG applications while meeting the architectural migration goals.

**Implementation approach**:
- Replace direct OpenAI ChatCompletion calls with OpenAI Agents SDK
- Configure Gemini-2.5-flash as the inference model
- Update `chat_service.py` to use new inference framework
- Maintain grounding behavior and safety mechanisms
- Preserve selected-text mode functionality
- Maintain backward-compatible API contracts
- Update environment variables for new model provider

**Alternatives considered**:
- Continue with OpenAI Chat Completions (doesn't meet migration requirements)
- Use LangChain (abstraction overhead, doesn't meet requirements)
- Custom agent framework (reinventing existing solutions)
- Different models (doesn't meet specified requirements)

## Decision: Qdrant Compatibility with Cohere Embeddings
**Rationale**: Qdrant is already integrated in the system and provides excellent performance for semantic search. Ensuring compatibility with Cohere embeddings maintains the existing vector database infrastructure while upgrading the embedding quality.

**Implementation approach**:
- Verify Cohere embedding dimensions are compatible with Qdrant
- Update embedding generation process to use Cohere vectors
- Test retrieval performance and accuracy with new embeddings
- Ensure no changes to metadata schema or indexing process
- Maintain top_k=5 and cosine similarity parameters

**Alternatives considered**:
- Switch to different vector database (unnecessary migration complexity)
- Modify Qdrant schema (breaks existing indexing and retrieval)

## Decision: Environment Configuration Management
**Rationale**: The migration introduces new environment variables for Cohere API and potentially Gemini access while maintaining existing configuration for Qdrant and other services.

**Implementation approach**:
- Add COHERE_API_KEY to settings
- Update .env template with new required variables
- Ensure backward compatibility for existing configuration
- Validate all required environment variables at startup
- Update documentation for new configuration requirements

**Alternatives considered**:
- Hardcode API keys (security risk)
- Use configuration files instead of environment variables (violates 12-factor app principles)

## Decision: Zero Functional Regression Strategy
**Rationale**: The migration must maintain all existing functionality including grounding behavior, safety mechanisms, refusal logic, and API contracts to ensure users experience no functional changes.

**Implementation approach**:
- Maintain all existing safety and refusal behavior
- Preserve selected-text-only mode functionality
- Keep existing textbook content and indexing semantics
- Maintain API contract compatibility
- Implement comprehensive testing to verify no regression
- Preserve user session and conversation state handling

**Alternatives considered**:
- Introduce breaking changes to improve functionality (violates requirements)
- Simplify safety mechanisms (violates constitution requirements)
- Change API contracts (breaks existing integrations)

## Decision: Build and Deployment Pipeline Updates
**Rationale**: The directory restructure and dependency changes require updates to build and deployment processes to ensure the application continues to function correctly after migration.

**Implementation approach**:
- Update package.json scripts to work from new frontend location
- Modify build configurations for new directory structure
- Update deployment scripts to reference new paths
- Ensure GitHub Pages deployment continues to work
- Update any CI/CD pipelines with new paths and dependencies

**Alternatives considered**:
- Separate build processes (unnecessary complexity)
- Different deployment strategy (maintains current approach is sufficient)

## Risk Analysis and Mitigation

### Primary Risks:
1. **Retrieval accuracy degradation** - Mitigation: Comprehensive testing against current implementation
2. **Functional regression** - Mitigation: Preserve all existing behavior and safety mechanisms
3. **Build/deployment failures** - Mitigation: Test in staging environment before production
4. **Performance degradation** - Mitigation: Monitor response times and throughput

### Backup Strategy:
- Maintain current implementation as backup branch during migration
- Implement gradual rollout if needed
- Ensure rollback capability if issues arise