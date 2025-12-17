# Quickstart: Integrated RAG Chatbot

## Overview
This guide provides a quick setup and deployment process for the RAG chatbot integrated with the Physical AI & Humanoid Robotics textbook.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for Docusaurus frontend)
- Docker (for local vector database)
- OpenAI API key
- Qdrant vector database instance

## Local Development Setup

### 1. Clone and Initialize
```bash
git clone <repository-url>
cd <repository-name>
npm install  # For Docusaurus frontend
pip install -r backend/requirements.txt  # For backend dependencies
```

### 2. Environment Configuration
Create `.env` file in backend directory:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
NEON_DB_URL=your_neon_database_url
QDRANT_API_KEY=your_qdrant_api_key_if_needed
EMBEDDING_MODEL=all-MiniLM-L6-v2  # or other sentence-transformers model
```

### 3. Start Vector Database
```bash
# Using Docker
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

# Or use Qdrant cloud service
```

### 4. Index Textbook Content
```bash
cd backend
python -m src.services.embedding_service --index-textbook
```

### 5. Start Backend API
```bash
cd backend
uvicorn src.api.main:app --reload --port 8000
```

### 6. Start Frontend
```bash
cd frontend
npm run start
```

## API Usage Examples

### Basic Chat Query
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-token" \
  -d '{
    "query": "What is ROS 2?",
    "mode": "full_text"
  }'
```

### Selected Text Mode
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-token" \
  -d '{
    "query": "Explain the concepts mentioned here",
    "mode": "selected_text",
    "selected_text": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications..."
  }'
```

### Content Retrieval Only
```bash
curl -X POST http://localhost:8000/api/v1/chat/retrieve \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-token" \
  -d '{
    "query": "control systems in robotics",
    "top_k": 5
  }'
```

## Frontend Integration
The chat interface is available as a React component that can be integrated into any Docusaurus page:

```jsx
import ChatInterface from './components/ChatInterface/ChatWindow';

function MyPage() {
  return (
    <div>
      <main>Page content here</main>
      <ChatInterface />
    </div>
  );
}
```

## Testing
Run backend tests:
```bash
cd backend
pytest tests/
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Deployment
1. Build frontend: `npm run build`
2. Deploy backend to serverless platform (AWS Lambda, Vercel, etc.)
3. Ensure vector database is accessible from deployed backend
4. Configure environment variables for production
5. Set up CDN for frontend assets