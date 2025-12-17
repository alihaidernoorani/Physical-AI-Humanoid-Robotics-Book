# Research: RAG Agent Upgrade

## Inventory & Audit of Current Backend Structure

### Files to Keep (Aligned with Target 5-File Structure)
- `backend/main.py` - Entry point and router mounting (already exists)
- `backend/src/config.py` - Environment variable management (already exists)
- `backend/src/api/rag.py` - RAG-specific logic (exists, needs updates)
- `backend/src/api/v1/chat.py` - Chat endpoints (exists, needs updates)
- `backend/src/services/gemini_service.py` - Gemini integration (exists)
- `backend/src/services/cohere_service.py` - Cohere embeddings (exists)
- `backend/src/services/qdrant_service.py` - Qdrant vector database (exists)

### Files to Consolidate/Merge
- `backend/src/api/v1/chat.py` - Contains chat, translation, personalization endpoints (needs consolidation)
- `backend/src/services/chat_service.py` - Chat business logic (needs consolidation)
- `backend/src/services/retrieval_service.py` - Retrieval logic (needs consolidation)
- `backend/src/api/rag.py` - RAG logic (needs consolidation)

### Files to Delete (Redundant/Circular Import Risk)
- `backend/src/config/settings.py` - Duplicate configuration file (merge with config.py)
- `backend/src/api/main.py` - Duplicate main API file (likely redundant with main.py)
- Various service files that duplicate functionality

### Identified Circular Imports
- Need to check for circular imports between api/rag.py and services/
- Need to check for circular imports between config files

## Technology Research & Best Practices

### OpenAI Agents SDK with Gemini Integration
- OpenAI Agents SDK can work with Gemini through compatible base URLs
- Requires setting custom base URL to bridge to Gemini API
- Need to ensure proper model configuration for gemini-2.5-flash

### Cohere Embeddings Integration
- Cohere's embed-multilingual-v3.0 is ideal for multilingual textbook content
- Need to standardize all embedding operations to use this model
- Qdrant supports Cohere embeddings natively

### Selected-Text Logic Implementation
- High-priority context handler needed for selected text from Docusaurus frontend
- Should override general RAG when selected_text parameter is provided
- Implementation requires modifying the chat endpoint to accept and prioritize selected context

## Recommended Implementation Approach

### Phase 1: Audit & Cleanup
1. Catalog all backend files and identify redundancies
2. Remove duplicate configuration files
3. Resolve circular imports
4. Create consolidated service architecture

### Phase 2: SDK Migration
1. Update chat logic to use OpenAI Agents SDK with Gemini bridge
2. Standardize all embeddings to Cohere embed-multilingual-v3.0
3. Ensure Qdrant compatibility with new embedding model

### Phase 3: Feature Enhancement
1. Implement selected-text context handler
2. Ensure feature parity for translation and personalization
3. Test end-to-end functionality