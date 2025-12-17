# Configuration Guide: RAG Chatbot Architecture Migration

This document outlines the new configuration requirements after the architecture migration to use Cohere embeddings and Gemini inference.

## Environment Variables

The following environment variables are required for the new architecture:

### Required Variables
- `COHERE_API_KEY`: Your Cohere API key for generating embeddings
- `GEMINI_API_KEY`: Your Google API key for Gemini inference
- `QDRANT_URL`: URL for your Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if using cloud version)

### Optional Variables
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: "textbook_chunks")
- `NEON_DB_URL`: URL for Neon Postgres database (if using)
- `DEBUG`: Enable debug mode (default: false)

## Architecture Changes

### Embedding Service
- Now uses Cohere's embedding API instead of Sentence Transformers
- Vector dimension: 1024 (previously 384 with Sentence Transformers)
- Model: `embed-english-v3.0`

### Inference Service
- Uses Gemini-2.5-flash via OpenAI-compatible interface
- Access through `GEMINI_API_KEY`

### Directory Structure
- Frontend files moved to `/frontend` directory
- Docusaurus configuration and content now in `/frontend`
- Backend remains in `/backend`

## Migration Steps

1. Update environment variables with new API keys
2. Re-index content using the updated indexing script
3. Verify Qdrant collection is configured for 1024-dimensional vectors
4. Test chat functionality with new inference pipeline

## Re-indexing Content

To re-index your textbook content with the new Cohere embeddings:

```bash
cd backend
python index_textbook.py
```

This will extract content from `frontend/docs`, generate Cohere embeddings, and store them in Qdrant.