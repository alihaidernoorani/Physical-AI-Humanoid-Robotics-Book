# Quickstart: RAG Agent Upgrade

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose
- Access to Qdrant Cloud
- Access to Cohere API
- Access to Google AI (for Gemini)
- Neon Postgres account

## Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Physical-AI-Humanoid-Robotics-Textbook
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables:**
   Create `.env` file in backend directory:
   ```env
   # Qdrant Configuration
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=textbook_rag

   # Cohere Configuration
   COHERE_API_KEY=your_cohere_api_key
   EMBEDDING_MODEL=embed-multilingual-v3.0

   # Google AI (Gemini) Configuration
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.5-flash

   # Neon Postgres Configuration
   DATABASE_URL=your_neon_postgres_url

   # Application Configuration
   APP_ENV=development
   DEBUG=true
   ```

## Running the Application

### Backend (FastAPI)

1. **Start the backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Index the textbook content:**
   ```bash
   python index_textbook.py
   ```

### Frontend (Docusaurus)

1. **Start the frontend:**
   ```bash
   cd frontend
   npm run start
   ```

## API Endpoints

### Chat Endpoints
- `POST /api/v1/chat` - Main chat endpoint with RAG functionality
- `POST /api/v1/translate` - Translation endpoint
- `POST /api/v1/personalize` - Personalization endpoint
- `GET /api/v1/health` - Health check

### Request Examples

**Chat with selected text:**
```json
{
  "message": "Explain this concept in simpler terms",
  "selected_text": "Complex technical concept from the textbook...",
  "user_preferences": {
    "language": "en",
    "learning_level": "beginner"
  }
}
```

**Translation:**
```json
{
  "text": "Text to translate",
  "target_language": "ur"
}
```

## OpenAI ChatKit SDK Integration

The frontend chat interface is enhanced with OpenAI ChatKit SDK to provide a rich, interactive chat experience:

- Real-time message streaming
- Typing indicators
- Message history management
- Thread management for conversation continuity
- Error handling and retry mechanisms
- Custom styling and theming options

## Testing

1. **Backend tests:**
   ```bash
   cd backend
   pytest tests/
   ```

2. **Frontend tests:**
   ```bash
   cd frontend
   npm test
   ```

## Deployment

### Docker
```bash
docker-compose up -d
```

### Environment-specific configurations:
- For production, set `APP_ENV=production` and `DEBUG=false`
- Update API keys and database URLs for production
- Ensure Qdrant collection is properly configured for production use