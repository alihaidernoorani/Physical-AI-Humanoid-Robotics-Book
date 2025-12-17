# Research: Integrated RAG Chatbot

## Overview
This research document addresses technical decisions and best practices for implementing the integrated RAG chatbot within the Physical AI & Humanoid Robotics textbook.

## Decision: RAG Architecture Pattern
**Rationale**: Retrieval-Augmented Generation is the optimal approach for providing accurate, textbook-grounded responses while preventing hallucinations. The architecture separates retrieval (finding relevant content) from generation (creating responses), allowing for strict grounding enforcement.

**Alternatives considered**:
- Pure generative models (high risk of hallucinations)
- Rule-based response systems (limited flexibility)
- Hybrid approaches with fallback mechanisms (increased complexity)

## Decision: Vector Database Selection - Qdrant
**Rationale**: Qdrant is lightweight, efficient, and designed for semantic search. It supports the required embedding similarity search and integrates well with Python ecosystems. It's also suitable for serverless deployment scenarios.

**Alternatives considered**:
- Pinecone (managed service, but adds external dependency)
- Weaviate (feature-rich but more complex setup)
- FAISS (Facebook's library, but requires more manual management)

## Decision: Embedding Model - Sentence Transformers (MiniLM)
**Rationale**: Based on the constitution requirements (line 72), MiniLM embeddings are specified for the project. These provide good semantic similarity with reasonable computational requirements and are well-suited for text chunks of 300-500 tokens.

**Alternatives considered**:
- OpenAI embeddings (cost concerns for large textbook)
- Custom-trained embeddings (overkill for this use case)
- Other transformer models (performance vs. accuracy trade-offs)

## Decision: Chunk Size - 300-500 tokens
**Rationale**: This range balances context richness with retrieval precision. It's large enough to maintain semantic coherence while small enough to ensure relevant retrieval. Aligns with constitution requirements (line 72).

**Alternatives considered**:
- Smaller chunks (risk of losing context)
- Larger chunks (reduced precision in retrieval)
- Variable sizes (increased complexity)

## Decision: OpenAI Agents SDK vs ChatKit
**Rationale**: OpenAI Agents SDK provides better control over the reasoning process and allows for stricter grounding enforcement. It's designed for complex reasoning tasks that require tools and function calling, which is suitable for RAG applications.

**Alternatives considered**:
- Direct OpenAI API calls (less control over grounding)
- LangChain (abstraction overhead)
- Custom agent framework (reinventing existing solutions)

## Decision: Full-book vs Selected-text Retrieval Modes
**Rationale**: Implementing both modes provides flexibility for different user needs. Full-book mode answers general questions, while selected-text mode provides focused responses to highlighted content. This dual approach satisfies both user stories 1 and 2.

**Alternatives considered**:
- Single mode only (limits functionality)
- Multiple selection modes (increased complexity)
- Context window-based selection (less intuitive for users)

## Decision: FastAPI Backend Framework
**Rationale**: FastAPI provides excellent performance, automatic API documentation, and strong typing. It's well-suited for serving ML models and handling concurrent requests. Integrates well with the Python ML ecosystem.

**Alternatives considered**:
- Flask (simpler but less performant)
- Django (overkill for API-only backend)
- Node.js/Express (different ecosystem than ML tools)

## Decision: Neon Serverless Postgres
**Rationale**: Serverless Postgres provides scalable, managed database services that integrate well with serverless deployments. It handles metadata, conversation state, and analytics without requiring server management.

**Alternatives considered**:
- SQLite (simpler but limited scalability)
- MongoDB (document-based but less structured for metadata)
- In-memory storage (not persistent)

## Decision: Docusaurus Frontend Integration
**Rationale**: Since the textbook is already built with Docusaurus, extending it with chat functionality provides seamless integration without disrupting the existing user experience. Maintains consistency with the current architecture.

**Alternatives considered**:
- Separate React application (increased complexity)
- iframe embedding (potential UX issues)
- Native mobile apps (scope expansion)

## Decision: Grounding Enforcement Strategy
**Rationale**: Implement a strict grounding policy where the system refuses to answer when information is not available in retrieved context. This enforces the constitution's requirement for no hallucinations (line 70) and maintains academic integrity.

**Alternatives considered**:
- Confidence scoring (still allows some hallucinations)
- Partial answers with uncertainty indicators (may still mislead)
- Fallback to external knowledge (violates grounding requirement)

## Decision: Metadata Schema for RAG Indexing
**Rationale**: Proper metadata schema ensures textbook structure is preserved in vector database. Includes module, chapter, subsection, and source type information for accurate citations and content organization.

**Schema includes**:
- module_name: Name of the textbook module
- chapter_title: Chapter title
- section_path: Full path to the content section
- content_type: Chapter, section, subsection, etc.
- page_reference: If applicable