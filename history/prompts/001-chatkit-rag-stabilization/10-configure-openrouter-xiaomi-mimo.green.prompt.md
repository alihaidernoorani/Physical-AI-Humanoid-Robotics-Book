---
id: 10
title: Configure OpenRouter with Xiaomi Mimo
stage: green
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-chatkit-rag-stabilization
branch: 001-chatkit-rag-stabilization
user: alihaidernoorani
command: /sp.implement
labels: ["llm", "openrouter", "xiaomi", "configuration", "litellm"]
links:
  spec: specs/001-chatkit-rag-stabilization/spec.md
  plan: specs/001-chatkit-rag-stabilization/plan.md
  tasks: specs/001-chatkit-rag-stabilization/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/config.py
  - backend/app/agent.py
tests:
  - Python syntax validation: PASS
---

## Prompt

Configure OpenRouter as the LLM provider using Xiaomi Mimo.

Scope:
- Backend LLM client configuration only
- Applies to the chat/agent service responsible for model inference

Implementation Steps:
- Update the LLM client to use OpenRouter as the base API endpoint: https://openrouter.ai/api/v1
- Configure the model identifier as: xiaomi/mimo-v2-flash:free
- Ensure the client (OpenAI / LiteLLM compatible) reads the API key from environment variables.
- Add required OpenRouter request headers:
  - HTTP-Referer: set to the deployed site URL or localhost during development
  - X-Title: set to "Textbook RAG"

Constraints:
- Do not modify frontend code.
- Do not change RAG retrieval or embedding logic.
- Preserve existing agent and conversation flow.
- Do not hardcode secrets or environment-specific values.

Validation:
- Chat requests successfully reach OpenRouter.
- Model responses are returned without authentication errors.
- No regression in existing chat session behavior.
- Errors are logged clearly if OpenRouter configuration fails.

## Response snapshot

### Changes Applied:

**1. config.py - Added OpenRouter Configuration:**
```python
# OpenRouter Configuration (for Xiaomi Mimo and other models)
openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
openrouter_model: str = os.getenv("OPENROUTER_MODEL", "xiaomi/mimo-v2-flash:free")
openrouter_site_url: str = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8000")
openrouter_app_title: str = os.getenv("OPENROUTER_APP_TITLE", "Textbook RAG")
```

**2. agent.py - Updated LiteLLM Model Configuration:**
- Changed from Gemini to OpenRouter/Xiaomi Mimo
- Model: `openrouter/{settings.openrouter_model}` (defaults to `xiaomi/mimo-v2-flash:free`)
- Added `base_url` for OpenRouter endpoint
- Added `extra_headers` with HTTP-Referer and X-Title

**3. Enhanced Error Handling:**
- Added OpenRouter-specific error detection
- Clear logging when API key or configuration is missing

### Validation:
- Python syntax check: PASS

### Environment Variables Required:
```
OPENROUTER_API_KEY=<your-api-key>
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1 (default)
OPENROUTER_MODEL=xiaomi/mimo-v2-flash:free (default)
OPENROUTER_SITE_URL=http://localhost:8000 (default)
OPENROUTER_APP_TITLE=Textbook RAG (default)
```

## Outcome

- ✅ Impact: LLM provider switched from Gemini to OpenRouter (Xiaomi Mimo)
- 🧪 Tests: Python syntax validation PASS
- 📁 Files: 2 files modified (config.py, agent.py)
- 🔁 Next prompts: Set OPENROUTER_API_KEY environment variable and test chat endpoint
- 🧠 Reflection: Leveraged existing LiteLLM infrastructure for OpenRouter compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Syntax validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with live OpenRouter API to verify model responses
