# Research Summary: RAG Backend & Frontend Integration

## Decision: Migration from OpenAI to OpenAI Agents SDK with Gemini-2.5-flash
**Rationale**: The plan requires replacing OpenAI API calls with OpenAI Agents SDK using Gemini-2.5-flash. This provides better agent capabilities for RAG applications while leveraging Google's advanced multimodal model.

**Alternatives considered**:
- Continuing with OpenAI GPT models
- Using Anthropic Claude models
- Using open-source models like Llama 3

## Decision: Cohere Embeddings over MiniLM
**Rationale**: The plan specifies migrating embeddings to Cohere instead of the constitution's default MiniLM embeddings. Cohere embeddings typically provide better semantic understanding for RAG applications.

**Alternatives considered**:
- OpenAI embeddings
- Sentence transformers (MiniLM)
- Hugging Face embedding models

## Decision: Environment Configuration Strategy
**Rationale**: All API keys (Qdrant, Neon Postgres, Cohere, Gemini) must be securely loaded from environment variables. This ensures security and deployment flexibility.

**Alternatives considered**:
- Hardcoded values (rejected for security)
- Configuration files (rejected for version control risks)

## Decision: Dual Retrieval Mode Implementation
**Rationale**: Implementing both full-book and per-page selected-text retrieval modes provides flexibility for different user scenarios. The backend needs to support both modes with proper metadata filtering.

**Alternatives considered**:
- Single retrieval mode only (rejected for limited functionality)

## Decision: Metadata Schema for RAG Indexing
**Rationale**: Proper metadata inclusion for RAG indexing must follow the constitution requirements: module, chapter, subsection, source_type, source_origin. This enables proper grounding and citation capabilities.

**Alternatives considered**:
- Minimal metadata (rejected for insufficient tracking)
- Custom metadata schema (rejected for non-compliance with constitution)

## Technical Architecture Findings

### Backend Components
- FastAPI application with endpoints for RAG queries
- Integration with Cohere for embedding generation
- OpenAI Agents SDK with Gemini-2.5-flash for chat completions
- Qdrant vector database for semantic search
- Neon Postgres for metadata and personalization

### Frontend Integration Points
- React chat interface components
- API service layer for secure communication
- Dual mode selection (full-book vs per-page)
- Selected text capture functionality

### Security Considerations
- Environment variable validation and error handling
- API key rotation strategies
- Rate limiting and monitoring
- Input sanitization for RAG queries

## Implementation Approach
1. Audit existing FastAPI backend for current architecture
2. Implement Cohere embedding integration
3. Replace OpenAI API calls with OpenAI Agents SDK using Gemini
4. Update frontend to communicate with new backend endpoints
5. Implement dual retrieval mode functionality
6. Ensure proper metadata handling for grounding