# Quickstart Guide: RAG Backend & Frontend Integration

## Prerequisites

- Python 3.11+
- Node.js 20+
- Access to Cohere API
- Access to Gemini API (Google AI Studio)
- Qdrant vector database (local or cloud)
- Neon Postgres database

## Environment Setup

1. Create a `.env` file in the project root with the following variables:

```bash
# API Keys
COHERE_API_KEY=your_cohere_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Database URLs
QDRANT_URL=your_qdrant_url_here
NEON_DB_URL=your_neon_postgres_connection_string_here

# Optional: Qdrant API key if using cloud service
QDRANT_API_KEY=your_qdrant_api_key_here

# Debug settings
DEBUG_MODE=true
```

2. Create an `.env.example` file with the same structure but empty values for reference.

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
python main.py
```

The backend will start on `http://localhost:8000` by default.

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000` by default.

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Key Endpoints

### RAG Chat
- `POST /api/rag/chat` - Process user queries with RAG

### Embeddings
- `POST /api/embeddings/generate` - Generate embeddings using Cohere

### Content Indexing
- `POST /api/rag/index` - Index content in Qdrant

### User Settings
- `GET/PUT /api/user/settings` - Manage personalization settings

### Translation
- `POST /api/translate` - Translate content (Urdu support)

## Dual Retrieval Modes

The system supports two retrieval modes:

1. **Full-book mode**: Searches across the entire textbook content
2. **Per-page mode**: Searches only within selected text on the current page

To use per-page mode, include the `selected_text` parameter in your query.

## Troubleshooting

### Common Issues

1. **API Keys Not Loading**: Ensure `.env` file is in the correct location and has proper permissions
2. **Qdrant Connection**: Verify QDRANT_URL is correct and database is accessible
3. **Embedding Generation**: Check Cohere API key validity and rate limits
4. **Gemini Integration**: Verify Gemini API key and model access

### Health Check
Use the health endpoint to verify all services are accessible:
`GET /api/health`

## Development Workflow

1. Make changes to backend in the `backend/src/` directory
2. Make changes to frontend in the `frontend/src/` directory
3. Run tests to ensure functionality remains intact
4. Update API contracts if adding new endpoints
5. Update data models if changing data structures