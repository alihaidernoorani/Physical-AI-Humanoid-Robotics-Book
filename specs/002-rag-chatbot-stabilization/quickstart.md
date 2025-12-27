# Quickstart: RAG Chatbot Stabilization

**Feature**: 002-rag-chatbot-stabilization
**Date**: 2025-12-27

## Prerequisites

- Python 3.11+
- Node.js 20+
- Access to Cohere API (API key)
- Access to Qdrant Cloud (URL + API key)
- Access to Neon Postgres (connection string)

## Environment Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create `.env` file:
```env
COHERE_API_KEY=your-cohere-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION_NAME=textbook_rag
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
GEMINI_API_KEY=your-gemini-key
```

### Frontend

```bash
cd frontend
npm install
```

Create `.env` file:
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

## Running the Application

### 1. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend

```bash
cd frontend
npm start
```

### 3. Run Ingestion (one-time)

```bash
cd backend
python -m scripts.ingest_textbook --docs-path ../frontend/docs
```

## Verification Steps

### Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a ROS 2 topic?"}'
```

Expected: JSON response with `response`, `citations`, and `session_id`

### Test Health Endpoint

```bash
curl http://localhost:8000/api/health
```

Expected: `{"status": "healthy", "services": {"agent": true, "rag": true, "neon_db": true}}`

### Test UI Optimistic Updates

1. Open http://localhost:3000
2. Open browser DevTools Network tab
3. Send a message in chat
4. Verify: User message appears BEFORE network request completes

## Key Files Modified

| File | Purpose |
|------|---------|
| `backend/app/rag.py` | Add `input_type` to Cohere calls |
| `backend/app/services/db_manager.py` | New file: connection pooling + retry |
| `frontend/src/components/ChatInterface/ChatWindow.jsx` | Optimistic updates |
| `frontend/src/components/ChatInterface/ChatWindow.css` | Modern styling |
| `backend/scripts/ingest_textbook.py` | New file: batch ingestion |

## Troubleshooting

### Cohere API Error: "input_type required"
- Ensure `input_type` parameter is passed to all `embed()` calls
- Use `"search_query"` for queries, `"search_document"` for documents

### Database Connection Timeout
- Check `DATABASE_URL` includes `?sslmode=require`
- Verify Neon project is not paused (auto-pauses after inactivity)

### Qdrant Empty Results
- Run ingestion script first
- Verify collection exists: check Qdrant Cloud dashboard
- Check relevance threshold (0.7) isn't filtering all results
