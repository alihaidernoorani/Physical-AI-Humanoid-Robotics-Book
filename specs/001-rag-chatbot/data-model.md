# Data Model: Integrated RAG Chatbot

## Overview
This document defines the data models for the RAG chatbot system, including entities for chat sessions, retrieved context, user queries, and generated responses.

## Entity: ChatSession
Represents a conversation between a user and the chatbot, maintaining context and mode settings.

**Fields**:
- `id` (string): Unique identifier for the session
- `user_id` (string, optional): Identifier for authenticated user
- `created_at` (datetime): Timestamp when session was created
- `updated_at` (datetime): Timestamp of last interaction
- `mode` (enum): "full_text" or "selected_text" - determines retrieval scope
- `metadata` (object): Additional session-specific data

**Validation rules**:
- `id` must be unique
- `mode` must be one of the allowed values
- `created_at` must be before `updated_at`

## Entity: RetrievedContext
Text chunks retrieved from the textbook that serve as the basis for generating responses.

**Fields**:
- `id` (string): Unique identifier for the context chunk
- `session_id` (string): Reference to the chat session
- `chunk_text` (string): The actual text content retrieved
- `similarity_score` (float): Cosine similarity score (0.0-1.0)
- `source_module` (string): Module name from textbook
- `source_chapter` (string): Chapter title
- `source_section` (string): Section path
- `source_page` (string, optional): Page reference if available
- `retrieved_at` (datetime): Timestamp when retrieved

**Validation rules**:
- `similarity_score` must be between 0.0 and 1.0
- `source_module`, `source_chapter`, `source_section` must match textbook structure
- `chunk_text` must not exceed 500 tokens

## Entity: UserQuery
The input question from the user, potentially associated with selected text for focused mode.

**Fields**:
- `id` (string): Unique identifier for the query
- `session_id` (string): Reference to the chat session
- `query_text` (string): The user's question
- `selected_text` (string, optional): Text highlighted by user (for selected_text mode)
- `query_mode` (enum): "full_text" or "selected_text"
- `timestamp` (datetime): When the query was submitted

**Validation rules**:
- `query_text` must not be empty
- `query_mode` must match the session mode
- `selected_text` is required when mode is "selected_text"

## Entity: GeneratedResponse
The chatbot's answer based on retrieved context, with proper attribution to source material.

**Fields**:
- `id` (string): Unique identifier for the response
- `session_id` (string): Reference to the chat session
- `query_id` (string): Reference to the original query
- `response_text` (string): The generated response
- `citations` (array): List of source references used
- `grounding_confidence` (float): Confidence in grounding (0.0-1.0)
- `generated_at` (datetime): Timestamp when response was generated
- `response_metadata` (object): Additional response-specific data

**Validation rules**:
- `response_text` must be grounded in provided context
- `citations` must reference actual retrieved context items
- `grounding_confidence` must be between 0.0 and 1.0

## Entity: TextbookChunk
Represents a chunk of textbook content in the vector database with associated metadata.

**Fields**:
- `id` (string): Unique identifier (stable across updates)
- `content` (string): The text content of the chunk
- `module_name` (string): Module name (e.g., "The Robotic Nervous System (ROS 2)")
- `chapter_title` (string): Chapter title
- `section_path` (string): Full path to section (e.g., "module-1/chapter-2/section-3")
- `content_type` (enum): "chapter", "section", "subsection", "paragraph"
- `embedding_vector` (array): Vector representation of the content
- `token_count` (integer): Number of tokens in the chunk
- `created_at` (datetime): When the chunk was indexed
- `updated_at` (datetime): When the chunk was last updated

**Validation rules**:
- `id` must be stable and persistent
- `content` must be between 300-500 tokens
- `module_name` must match the fixed 4-module structure
- `embedding_vector` must match the expected dimension for the embedding model

## Relationships
- ChatSession 1 --- * UserQuery (one session to many queries)
- ChatSession 1 --- * GeneratedResponse (one session to many responses)
- ChatSession 1 --- * RetrievedContext (one session to many retrieved contexts)
- UserQuery 1 --- 1 GeneratedResponse (one query to one response)
- RetrievedContext * --- * GeneratedResponse (many retrieved contexts to many responses via citations)