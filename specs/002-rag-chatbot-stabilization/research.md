# Research: RAG Chatbot Stabilization

**Feature**: 002-rag-chatbot-stabilization
**Date**: 2025-12-27
**Status**: Complete

## Decision 1: Chunking Strategy

**Decision**: Markdown-aware splitting with fallback to recursive character splitting

**Rationale**:
- Markdown-aware splitting preserves semantic boundaries (headers, code blocks, paragraphs)
- Respects document structure which improves retrieval relevance
- Falls back to recursive character splitting for content without clear markdown structure
- Target chunk size: 500-1000 tokens (per spec clarification)

**Alternatives Considered**:
- Pure recursive character splitting: Simpler but may split mid-sentence or mid-concept
- Fixed-size splitting: Predictable but ignores semantic boundaries
- Sentence-based splitting: Good for prose but doesn't handle code blocks well

**Implementation Notes**:
- Use langchain's `MarkdownTextSplitter` or custom regex-based splitter
- Chunk overlap of 50-100 tokens to preserve context at boundaries
- Preserve frontmatter metadata for module/chapter/subsection extraction

## Decision 2: State Management for Optimistic Updates

**Decision**: Local React state with optimistic updates (no refetching)

**Rationale**:
- Messages array managed in component state provides immediate UI feedback
- User message added to state before API call (optimistic update)
- Bot response appended when API returns
- Error state replaces loading indicator on failure
- Simpler than server-state synchronization for single-session chat

**Alternatives Considered**:
- Refetch history on every message: Adds latency, contradicts optimistic update goal
- Global state (Redux/Zustand): Overkill for single-component chat state
- Server-sent events: Better for streaming but not required for this scope

**Implementation Notes**:
- Use `useState` for messages array
- Add user message immediately on submit
- Show loading state via separate `isLoading` boolean
- Append bot response or error message on API completion

## Decision 3: Database Connection Strategy

**Decision**: SQLAlchemy engine pooling with retry decorator

**Rationale**:
- SQLAlchemy's connection pooling handles connection reuse efficiently
- `tenacity` library provides clean retry logic with exponential backoff
- Supports SSL connections natively (required for Neon Postgres)
- Pooling reduces connection overhead vs raw psycopg2 connections

**Alternatives Considered**:
- Raw psycopg2 with manual retry: More control but reinvents connection pooling
- asyncpg: Better async performance but requires more complex setup
- No pooling: Creates new connection per request, inefficient

**Implementation Notes**:
- Configure pool_size=5, max_overflow=10 for moderate concurrency
- Use `pool_pre_ping=True` to detect stale connections
- Wrap operations in retry decorator: 3 retries, exponential backoff (1s, 2s, 4s)
- Graceful degradation: If DB unavailable, continue with RAG-only mode

## Decision 4: Cohere input_type Parameter

**Decision**: Dynamic input_type based on operation context

**Rationale**:
- Cohere embed-v3 models require `input_type` for optimal performance
- `search_query`: For user queries during retrieval (asymmetric search)
- `search_document`: For document chunks during ingestion
- Mismatched types degrade retrieval quality significantly

**Implementation Notes**:
- Add `input_type` parameter to embedding functions
- Ingestion script uses `input_type="search_document"`
- Query embedding uses `input_type="search_query"`
- Update existing `generate_single_embedding` and `generate_batch_embeddings`

## Decision 5: CSS Design System

**Decision**: CSS variables with "Modern Clean" design system

**Rationale**:
- CSS variables enable consistent theming without CSS-in-JS overhead
- Matches Docusaurus's existing CSS variable approach
- Easy to maintain and customize
- No additional dependencies required

**Design Tokens**:
- Font: `Inter, -apple-system, BlinkMacSystemFont, system-ui, sans-serif`
- Base text: 16px
- Primary accent: #2563eb (blue)
- User bubble: #2563eb background, white text
- Bot bubble: #f3f4f6 background, #1f2937 text
- Border radius: 16px for bubbles
- Spacing: 8px, 12px, 16px scale

## Decision 6: Relevance Threshold Implementation

**Decision**: Score-based filtering at retrieval time

**Rationale**:
- Qdrant returns similarity scores (0-1 for cosine)
- Filter results below 0.7 threshold before passing to LLM
- Prevents low-quality context from degrading responses
- Enables honest "no relevant information found" responses

**Implementation Notes**:
- Add score filtering in `search_chunks_full_book` and `search_chunks_per_page`
- Return empty list if no chunks pass threshold
- Chat endpoint handles empty context gracefully

## Research Sources

- Cohere Embed v3 Documentation: https://docs.cohere.com/reference/embed
- SQLAlchemy Connection Pooling: https://docs.sqlalchemy.org/en/20/core/pooling.html
- Tenacity Retry Library: https://tenacity.readthedocs.io/
- LangChain Text Splitters: https://python.langchain.com/docs/modules/data_connection/document_transformers/
- Qdrant Python Client: https://qdrant.tech/documentation/
