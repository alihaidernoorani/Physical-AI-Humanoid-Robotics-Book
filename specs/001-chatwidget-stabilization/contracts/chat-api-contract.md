# Chat API Contract

## Overview
This document defines the API contract for the ChatWidget communication with the backend RAG service.

## Base URL
`https://alihaidernoorani-deploy-docusaurus-book.hf.space/api/v1`

## Endpoints

### Create Chat Session
`POST /chat/session`

#### Request
```json
{
  "timestamp": "2025-12-25T10:00:00.000Z",
  "metadata": {
    "type": "global-chat",
    "pageContext": "docs/introduction"
  }
}
```

#### Response
```json
{
  "session_id": "session-12345",
  "timestamp": "2025-12-25T10:00:00.000Z",
  "status": "success"
}
```

### Send Chat Message
`POST /chat`

#### Request
```json
{
  "query": "What is ROS 2?",
  "session_id": "session-12345",
  "context": {
    "current_page": "docs/ros2-basics",
    "referrer": "docs/introduction"
  }
}
```

#### Response
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is a set of software libraries and tools that help you build robot applications...",
  "citations": [
    "ROS 2 documentation",
    "Introduction to Robotics textbook"
  ],
  "session_id": "session-12345"
}
```

### Get Chat History
`GET /chat/history/{sessionId}`

#### Response
```json
{
  "session_id": "session-12345",
  "messages": [
    {
      "id": "msg-1",
      "text": "What is ROS 2?",
      "sender": "user",
      "timestamp": "2025-12-25T10:00:00.000Z"
    },
    {
      "id": "msg-2",
      "text": "ROS 2 (Robot Operating System 2) is a set of software libraries and tools that help you build robot applications...",
      "sender": "bot",
      "timestamp": "2025-12-25T10:00:01.000Z",
      "citations": [
        "ROS 2 documentation",
        "Introduction to Robotics textbook"
      ]
    }
  ]
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

### Common Error Codes
- `CHAT_SESSION_NOT_FOUND`: Session ID does not exist
- `RAG_QUERY_FAILED`: Backend RAG service failed to process query
- `REQUEST_TIMEOUT`: Request took too long to process
- `INVALID_INPUT`: Request body validation failed