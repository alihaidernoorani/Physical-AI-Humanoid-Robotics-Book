# API Contracts: RAG Backend & Frontend Integration

## RAG Chat Endpoint
**Endpoint**: `POST /api/rag/chat`
**Description**: Process user queries and return contextually relevant responses based on textbook content

### Request
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

### Response (Success 200)
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

### Response (Error 400)
```json
{
  "error": "string",
  "details": "string"
}
```

---

## Embeddings Generation Endpoint
**Endpoint**: `POST /api/embeddings/generate`
**Description**: Generate embeddings for content indexing using Cohere

### Request
```json
{
  "content": "string (required)",
  "metadata": {
    "module": "string (required)",
    "chapter": "string (required)",
    "subsection": "string (required)",
    "source_type": "string (required)",
    "source_origin": "string (required)"
  }
}
```

### Response (Success 200)
```json
{
  "chunk_id": "string",
  "embedding": "array (vector embedding)",
  "metadata": {
    "module": "string",
    "chapter": "string",
    "subsection": "string",
    "source_type": "string",
    "source_origin": "string"
  }
}
```

---

## Content Indexing Endpoint
**Endpoint**: `POST /api/rag/index`
**Description**: Index content chunks in Qdrant vector database with metadata

### Request
```json
{
  "chunks": [
    {
      "content": "string (required)",
      "embedding": "array (required)",
      "metadata": {
        "module": "string (required)",
        "chapter": "string (required)",
        "subsection": "string (required)",
        "source_type": "string (required)",
        "source_origin": "string (required)",
        "page_reference": "string"
      }
    }
  ]
}
```

### Response (Success 200)
```json
{
  "indexed_count": "integer",
  "failed_count": "integer",
  "results": [
    {
      "chunk_id": "string",
      "status": "enum - 'success' or 'failed'",
      "error": "string (if failed)"
    }
  ]
}
```

---

## Personalization Settings Endpoint
**Endpoint**: `GET /api/user/settings`
**Description**: Retrieve user personalization settings

### Response (Success 200)
```json
{
  "user_id": "string",
  "learning_level": "enum - 'beginner', 'intermediate', 'advanced'",
  "preferred_language": "string",
  "last_accessed_module": "string",
  "custom_preferences": "object"
}
```

---

## Update Personalization Endpoint
**Endpoint**: `PUT /api/user/settings`
**Description**: Update user personalization settings

### Request
```json
{
  "learning_level": "enum - 'beginner', 'intermediate', 'advanced'",
  "preferred_language": "string",
  "custom_preferences": "object"
}
```

### Response (Success 200)
```json
{
  "success": "boolean",
  "updated_settings": "object (updated settings)"
}
```

---

## Translation Endpoint
**Endpoint**: `POST /api/translate`
**Description**: Translate content to specified language (Urdu support)

### Request
```json
{
  "text": "string (required)",
  "source_language": "string (default: 'en')",
  "target_language": "string (required, e.g., 'ur')",
  "use_cache": "boolean (default: true)"
}
```

### Response (Success 200)
```json
{
  "original_text": "string",
  "translated_text": "string",
  "source_language": "string",
  "target_language": "string",
  "from_cache": "boolean"
}
```

---

## Health Check Endpoint
**Endpoint**: `GET /api/health`
**Description**: Check the health status of backend services

### Response (Success 200)
```json
{
  "status": "string - 'healthy'",
  "services": {
    "qdrant": "boolean",
    "cohere": "boolean",
    "gemini": "boolean",
    "neon_db": "boolean"
  },
  "timestamp": "datetime"
}
```

---

## Error Response Format (Standard)
**Status Codes**: 400, 401, 403, 404, 500
```json
{
  "error": "string",
  "message": "string",
  "status_code": "integer",
  "timestamp": "datetime",
  "details": "object (optional)"
}
```

---

## Authentication
All endpoints require authentication via Bearer token in Authorization header:
```
Authorization: Bearer {token}
```

## Rate Limiting
All endpoints are subject to rate limiting:
- 100 requests per minute per IP
- 429 status code returned when limit exceeded

## Validation
All endpoints perform input validation:
- Content length limits
- Required field validation
- Format validation for IDs and keys
- Sanitization of user inputs