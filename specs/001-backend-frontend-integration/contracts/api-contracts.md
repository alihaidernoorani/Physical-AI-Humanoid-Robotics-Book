# API Contracts: Backend-Frontend Integration

## Chat Endpoint Contract

### POST /chat
**Description**: Process user queries and return responses from the RAG system

**Request**:
```json
{
  "query": "string (user's question or message)",
  "context": "string (optional context for the query)",
  "mode": "string (optional RAG mode - 'per_page', 'global', etc.)"
}
```

**Response**:
```json
{
  "response": "string (AI-generated response)",
  "sources": [
    {
      "title": "string (source title)",
      "url": "string (source URL)",
      "excerpt": "string (relevant excerpt)"
    }
  ],
  "success": "boolean (whether the operation was successful)"
}
```

**Error Responses**:
- 400: Bad Request - Missing required fields
- 500: Internal Server Error - Backend processing failed

## Translation Endpoint Contract

### POST /translate
**Description**: Translate content to Urdu language

**Request**:
```json
{
  "text": "string (text to translate)",
  "target_language": "string (default: 'ur' for Urdu)"
}
```

**Response**:
```json
{
  "original_text": "string (original input text)",
  "translated_text": "string (translated text)",
  "target_language": "string (language code)",
  "success": "boolean (whether the operation was successful)"
}
```

**Error Responses**:
- 400: Bad Request - Missing required fields
- 500: Internal Server Error - Translation service failed

## Personalization Endpoint Contract

### POST /personalize
**Description**: Adjust content based on user preferences

**Request**:
```json
{
  "content": "string (content to personalize)",
  "user_level": "string (user expertise level: 'beginner', 'intermediate', 'advanced')",
  "preferences": "object (user preferences for personalization)"
}
```

**Response**:
```json
{
  "original_content": "string (original input content)",
  "personalized_content": "string (personalized content)",
  "user_level": "string (applied user level)",
  "success": "boolean (whether the operation was successful)"
}
```

**Error Responses**:
- 400: Bad Request - Missing required fields
- 500: Internal Server Error - Personalization service failed