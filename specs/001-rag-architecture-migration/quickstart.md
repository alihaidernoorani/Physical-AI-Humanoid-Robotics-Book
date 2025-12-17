# Quickstart Guide: RAG Chatbot Architecture Migration

## Overview
This guide helps developers understand and work with the migrated RAG chatbot architecture featuring Cohere embeddings, OpenAI Agents SDK with Gemini-2.5-flash, and reorganized frontend structure.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Qdrant vector database (running locally or accessible)
- Cohere API key
- Google AI API key (for Gemini-2.5-flash)

## Environment Setup

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

### 4. Environment Variables
Create `.env` files in both backend and frontend directories:

**Backend (.env):**
```env
# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=textbook_chunks

# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key

# Neon Postgres Configuration (if applicable)
NEON_DB_URL=your_neon_db_url

# Application Configuration
DEBUG=false
```

**Frontend (.env):**
```env
# Backend API URL
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application

### 1. Start Qdrant
```bash
# Option 1: Docker
docker run -p 6333:6333 -p 6334:6334 \
    -e QDRANT__SERVICE__API_KEY=your_api_key \
    --platform=linux/amd64 \
    qdrant/qdrant

# Option 2: If using existing Qdrant instance, ensure it's running
```

### 2. Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

### 3. Index Textbook Content (if needed)
```bash
cd backend
python index_textbook.py
```

### 4. Start Frontend
```bash
cd frontend
npm start
```

## Key Architecture Changes

### 1. Frontend Restructure
- All Docusaurus-related files moved to `/frontend` directory
- `docusaurus.config.ts`, `package.json`, `sidebars.ts`, `tsconfig.json` relocated
- `docs/` content now under `/frontend/docs`
- Frontend source code under `/frontend/src`

### 2. Embedding Service Migration
- Replaced Sentence Transformers with Cohere embeddings
- Updated `src/services/embedding_service.py` to use Cohere API
- Maintains same interface for compatibility with existing code

### 3. Inference Service Migration
- Replaced OpenAI ChatCompletions with OpenAI Agents SDK
- Using Gemini-2.5-flash model for response generation
- Preserves grounding behavior and safety mechanisms

## API Endpoints

### Chat API
- `POST /api/v1/chat/query` - Process user queries with RAG
- `GET /api/v1/chat/session/{session_id}` - Get session details
- `POST /api/v1/chat/session` - Create new session

### Health Check
- `GET /api/v1/health` - Check system health

### Textbook Content
- `GET /api/v1/textbook/modules` - List available modules
- `GET /api/v1/textbook/chapters/{module_name}` - List chapters in module

## Development Workflow

### Adding New Features
1. Update the backend services in `/backend/src/services`
2. Update API endpoints in `/backend/src/api`
3. Update frontend components in `/frontend/src/components`
4. Ensure all changes maintain backward compatibility

### Testing
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests (if applicable)
cd frontend
npm test
```

## Migration Checklist

### Before Deploying Migration
- [ ] Verify Cohere API key is properly configured
- [ ] Verify Google API key for Gemini is properly configured
- [ ] Test embedding generation with Cohere
- [ ] Test response generation with Gemini
- [ ] Verify frontend build works from new directory structure
- [ ] Test RAG functionality with new architecture
- [ ] Verify grounding and safety mechanisms still work
- [ ] Confirm API contracts remain backward compatible
- [ ] Test selected-text mode functionality
- [ ] Validate retrieval accuracy compared to previous implementation

### Post-Migration Verification
- [ ] All tests pass
- [ ] Application builds and runs without errors
- [ ] Chatbot responses maintain quality and safety
- [ ] Frontend operates correctly from new structure
- [ ] Embedding retrieval works with Cohere vectors
- [ ] Response generation works with OpenAI Agents SDK
- [ ] No functional regression in user experience