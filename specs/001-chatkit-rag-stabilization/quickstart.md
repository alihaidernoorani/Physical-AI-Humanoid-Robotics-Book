# Quickstart: ChatKit + Docusaurus RAG Stabilization

**Date**: 2025-12-28
**Feature**: 001-chatkit-rag-stabilization
**Type**: Integration and deployment guide

## Overview

This guide provides quick setup instructions for the stabilized ChatKit + Docusaurus RAG system. The implementation focuses on reliable message display, correct HTTP status codes, and proper RAG retrieval from existing Qdrant data.

## Prerequisites

### Environment Setup
- Python 3.11+ with pip
- Node.js 20+ with npm
- Docusaurus project (already configured)
- Cohere API key
- Qdrant database access
- Hugging Face Space (for backend deployment)

### Required Environment Variables
```bash
# Backend (.env file)
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=textbook_rag
EMBEDDING_MODEL=embed-multilingual-v3.0
RELEVANCE_THRESHOLD=0.35
MAX_MESSAGE_LENGTH=2000
DATABASE_URL=your_neon_postgres_url
```

## Frontend Setup

### ChatKit Component Integration
1. Ensure ChatKit components are properly integrated in Docusaurus:
```jsx
// In your Docusaurus page or layout
import { ChatKit } from './components/ChatKit';

function Layout({children}) {
  return (
    <div>
      {children}
      <ChatKit />
    </div>
  );
}
```

### API Service Configuration
1. Verify payload contract in `frontend/src/services/api.js`:
```javascript
// Ensure request uses "message" field as required
const requestBody = {
  message: userMessage,        // Required field name per spec
  session_id: sessionId       // Optional, auto-generated if not provided
};
```

## Backend Setup

### FastAPI Server
1. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Configuration Validation
Verify the following configuration values in `backend/app/config.py`:
```python
# Required values per spec
relevance_threshold: float = 0.35  # RAG relevance threshold
max_message_length: int = 2000     # Maximum message length
embedding_model: str = "embed-multilingual-v3.0"  # Cohere model
```

## RAG System Setup

### Qdrant Collection
1. Verify collection exists with name `textbook_rag`
2. Ensure collection uses embed-multilingual-v3.0 compatible vectors (1024 dimensions)
3. Confirm existing textbook content is properly indexed

### Content Ingestion
If re-indexing is needed, use the ingestion script:
```bash
cd backend
python scripts/ingest_textbook.py --docs-path ../frontend/docs --dry-run
python scripts/ingest_textbook.py --docs-path ../frontend/docs
```

## Testing the Integration

### Message Flow Test
1. Send a test message through the ChatKit widget
2. Verify user message appears immediately (optimistic update)
3. Wait for assistant response
4. Verify assistant response appears without widget minimization
5. Confirm no page refresh was required

### API Contract Test
1. Use browser DevTools Network tab
2. Send a message and verify POST /api/v1/chat request
3. Confirm request body contains "message" field
4. Verify response contains expected fields: response, session_id, citations

### Error Handling Test
1. Send an empty message to trigger validation error
2. Verify backend returns HTTP 400 (not 500)
3. Check that frontend handles error gracefully

### RAG Retrieval Test
1. Ask: "What is the title of the first chapter?"
2. Verify response contains actual textbook content
3. Confirm citations reference proper sources

## API Endpoints

### Chat Endpoint
```
POST /api/v1/chat
Content-Type: application/json

Request:
{
  "message": "string (required)",
  "session_id": "string (optional)"
}

Response (200):
{
  "response": "string",
  "session_id": "string",
  "citations": "array",
  "response_time_ms": "number",
  "timestamp": "string"
}

Error Response (400):
{
  "detail": "string"
}
```

### Health Check
```
GET /api/v1/health

Response:
{
  "status": "healthy|unhealthy",
  "services": {
    "agent": "boolean",
    "rag": "boolean",
    "neon_db": "boolean"
  },
  "timestamp": "string"
}
```

## Troubleshooting

### Common Issues

1. **Messages don't appear immediately**:
   - Check frontend uses optimistic update pattern
   - Verify React state updates via setMessages(prev => [...prev, assistantMessage])

2. **400 errors converted to 500**:
   - Review backend exception handling in chat.py
   - Ensure HTTPException is re-thrown, not wrapped

3. **RAG returns no results**:
   - Verify Qdrant collection name is "textbook_rag"
   - Confirm relevance threshold is 0.35
   - Check Cohere model is embed-multilingual-v3.0

4. **Wrong payload fields**:
   - Confirm frontend sends "message" field
   - Verify backend expects { message: string, session_id: string }

## Verification Checklist

- [ ] User messages appear immediately without refresh
- [ ] Assistant responses appear without widget minimization
- [ ] Valid requests return HTTP 200
- [ ] Invalid requests return HTTP 400 (not 500)
- [ ] RAG retrieves content from Qdrant collection
- [ ] "What is the title of the first chapter?" returns correct answer
- [ ] Frontend uses correct payload contract ("message" field)
- [ ] React state updates with setMessages pattern
- [ ] No architectural changes made (only stability fixes)

## Deployment Notes

### Hugging Face Spaces
When deploying to Hugging Face Spaces:
1. Ensure environment variables are configured in Space settings
2. Verify Qdrant and Cohere API access from Space environment
3. Test message flow after deployment
4. Confirm health check endpoint is accessible

### Frontend Integration
For Docusaurus deployment:
1. ChatKit widget should appear as floating element
2. No page refresh should be needed for message display
3. Widget should maintain state between page navigations