---
id: 22
title: Analyze 500 error field name mismatch
stage: general
date: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: 001-chatwidget-stabilization
branch: 001-chatwidget-stabilization
user: Claude Sonnet 4.5
command: sp.analyze
labels: [analysis, 500-error, field-mismatch, frontend-backend, api]
links:
  spec: specs/001-chatwidget-stabilization/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/ChatKit/ChatKit.tsx (read)
  - frontend/src/services/api.js (read)
  - backend/app/chat.py (read)
  - backend/app/main.py (read)
tests:
  - N/A (analysis only)
---

## Prompt

/sp.analyze

Please analyze and recommend me a solution to the 500 internal server error. These are the logs from hugging face: INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
INFO:     10.16.30.4:3392 - "GET /?logs=container HTTP/1.1" 200 OK
INFO:     10.16.37.13:13022 - "GET /?logs=container HTTP/1.1" 200 OK
INFO:     10.16.30.4:39358 - "GET /api/v1/chat/history/test HTTP/1.1" 200 OK
INFO:     10.16.30.4:25117 - "GET /api/v1/chat/history/test HTTP/1.1" 200 OK
INFO:     10.16.37.13:49728 - "GET /api/v1/chat/history/test HTTP/1.1" 200 OK
INFO:     10.16.30.4:30649 - "POST /api/v1/chat/session HTTP/1.1" 200 OK
Error in chat endpoint: 400: Message is required
INFO:     10.16.37.13:10667 - "POST /api/v1/chat HTTP/1.1" 500 Internal Server Error
INFO:     10.16.30.4:54984 - "GET /api/v1/chat/history/test HTTP/1.1" 200 OK
...

## Response snapshot

### Root Cause Identified

**Field name mismatch between frontend and backend:**

| Component | Field Name Used | Expected by Backend |
|-----------|-----------------|---------------------|
| Frontend (ChatKit.tsx:124-126) | `query` | - |
| Backend (chat.py:39) | - | `message` |

### Code Evidence

**Frontend sends:**
```javascript
const response = await chatService.sendMessage({
  query: message,        // ❌ WRONG - sends "query"
  session_id: currentSessionId
});
```

**Backend expects:**
```python
message = request.get("message", "")  # ✅ Expects "message"
if not message:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Message is required"
    )
```

### Why 500 Instead of 400?

The 400 HTTPException is caught by the outer exception handler and re-raised as 500.

### Recommended Fix

Change `ChatKit.tsx` line 124-126:
```typescript
const response = await chatService.sendMessage({
  message: message,  // ✅ Use "message" to match backend
  session_id: currentSessionId
});
```

## Outcome

- Impact: Identified root cause of 500 error - field name mismatch (query vs message)
- Tests: N/A (analysis only)
- Files: Analyzed 4 files (ChatKit.tsx, api.js, chat.py, main.py)
- Next prompts: Implement the fix by changing `query` to `message` in ChatKit.tsx
- Reflection: Frontend-backend contract verification is critical for API integration

## Evaluation notes (flywheel)

- Failure modes observed: Field name inconsistency between frontend and backend
- Graders run and results (PASS/FAIL): N/A - analysis only
- Prompt variant (if applicable): Standard sp.analyze
- Next experiment (smallest change to try): Single-line fix in ChatKit.tsx:125
