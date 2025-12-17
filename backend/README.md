# RAG Backend API

Backend API for RAG chatbot with Cohere embeddings and Google Gemini-2.5-flash, designed for the Physical AI & Humanoid Robotics textbook.

## Features

- **RAG (Retrieval-Augmented Generation)**: Combines vector search with AI generation for accurate responses
- **Dual Retrieval Modes**:
  - Full-book: Search across the entire textbook
  - Per-page: Search only within selected text
- **Secure Environment Configuration**: All API keys loaded from environment variables
- **Rate Limiting**: 100 requests per minute per IP for chat endpoints
- **Authentication**: JWT-based authentication for all endpoints
- **Comprehensive Error Handling**: Detailed error messages and logging
- **Input Validation**: Sanitized and validated user inputs

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for containerized deployment)
- Qdrant vector database
- Cohere API key
- Google Gemini API key
- Neon Postgres database

## Installation

### Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Physical-AI-Humanoid-Robotics-Textbook/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Qdrant Configuration
QDRANT_URL=https://your-qdrant-instance.com
QDRANT_API_KEY=your-qdrant-api-key  # Optional if using unauthenticated instance

# AI Service Keys
COHERE_API_KEY=your-cohere-api-key
GEMINI_API_KEY=your-gemini-api-key

# Database Configuration
NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# Security
SECRET_KEY=your-super-secret-key-change-in-production

# Optional Configuration
DEBUG_MODE=false  # Set to true for development
```

## Running the Application

### Local Development

1. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Using Docker

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### RAG Chat Endpoint
- **URL**: `POST /api/rag/chat`
- **Description**: Process user queries and return contextually relevant responses based on textbook content
- **Request Body**:
  ```json
  {
    "query_text": "string (required)",
    "retrieval_mode": "enum (required) - 'full-book' or 'per-page'",
    "selected_text": "string (optional) - text selected by user in per-page mode",
    "metadata_filters": {
      "module": "string (optional)",
      "chapter": "string (optional)",
      "subsection": "string (optional)"
    }
  }
  ```
- **Response**:
  ```json
  {
    "response_id": "string",
    "response_text": "string",
    "citations": [
      {
        "chunk_id": "string",
        "module": "string",
        "chapter": "string",
        "subsection": "string",
        "page_reference": "string"
      }
    ],
    "confidence_score": "float (0.0-1.0)",
    "grounded_chunks": ["string (array of chunk IDs)"],
    "is_fallback": "boolean"
  }
  ```

### Validation Endpoint
- **URL**: `POST /api/rag/validate`
- **Description**: Validate a RAG query without processing it

### Statistics Endpoint
- **URL**: `GET /api/rag/stats`
- **Description**: Get statistics about the RAG system

### Health Check Endpoint
- **URL**: `GET /api/health`
- **Description**: Check the health status of backend services

## Authentication

All endpoints require authentication using Bearer tokens. Include the Authorization header in your requests:

```
Authorization: Bearer <your-jwt-token>
```

## Rate Limiting

The API implements rate limiting:
- Chat endpoints: 100 requests per minute per IP
- Retrieval endpoints: 200 requests per minute per IP
- Health check: 1000 requests per minute per IP

When rate limit is exceeded, the API returns a 429 status code with details.

## Development

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src
```

### Code Formatting

Format code with black:
```bash
black .
```

### Linting

Lint code with flake8:
```bash
flake8 .
```

## Deployment

### Production Deployment

For production deployment, use the Kubernetes configuration files in the `deploy/` directory.

1. Create Kubernetes secrets for your environment variables:
   ```bash
   kubectl create secret generic rag-secrets \
     --from-literal=qdrant-url=your-qdrant-url \
     --from-literal=qdrant-api-key=your-qdrant-api-key \
     --from-literal=cohere-api-key=your-cohere-api-key \
     --from-literal=gemini-api-key=your-gemini-api-key \
     --from-literal=neon-db-url=your-neon-db-url \
     --from-literal=secret-key=your-secret-key
   ```

2. Apply the deployment:
   ```bash
   kubectl apply -f deploy/prod-deployment.yml
   ```

### Environment Configuration for Production

For production deployments, ensure the following environment variables are properly set:
- Use strong, randomly generated SECRET_KEY
- Enable DEBUG_MODE only in development
- Use proper SSL certificates for HTTPS
- Configure proper CORS origins (not "*" in production)

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**: Ensure all required environment variables are set
2. **Connection Issues**: Verify that all external services (Qdrant, Cohere, Gemini) are accessible
3. **Rate Limiting**: If you're hitting rate limits during development, you can adjust them in the configuration
4. **Authentication**: Make sure you're including the Authorization header with a valid JWT token

### Logs

Check application logs for debugging information:
- In Docker: `docker-compose logs rag-backend`
- In Kubernetes: `kubectl logs deployment/rag-backend`

## Security

- All API keys are loaded from environment variables and never hardcoded
- JWT authentication required for all endpoints
- Input validation and sanitization on all user inputs
- Rate limiting to prevent abuse
- Secure CORS configuration (configured for development by default)

## Performance

- Uses efficient vector search for retrieval
- Implements caching where appropriate
- Optimized embedding generation
- Asynchronous request handling