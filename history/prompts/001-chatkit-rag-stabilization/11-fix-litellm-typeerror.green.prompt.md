---
id: 11
title: Fix LitellmModel TypeError - Remove extra_headers
stage: green
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-chatkit-rag-stabilization
branch: 001-chatkit-rag-stabilization
user: alihaidernoorani
command: /sp.implement
labels: ["fix", "litellm", "typeerror", "openrouter"]
links:
  spec: specs/001-chatkit-rag-stabilization/spec.md
  plan: specs/001-chatkit-rag-stabilization/plan.md
  tasks: specs/001-chatkit-rag-stabilization/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/agent.py
tests:
  - Python syntax validation: PASS
---

## Prompt

Fix TypeError in agent.py:
1. Open `backend/app/agent.py`.
2. Locate the `AgentSDKConfig.__init__` method (around line 24) where `LitellmModel` is being initialized.
3. Remove the `extra_headers` argument from the `LitellmModel(...)` call.
4. If you are using LiteLLM's standard library, move the OpenRouter headers ('HTTP-Referer' and 'X-Title') to the `completion()` function call instead of the constructor.
5. Ensure the `base_url` remains set to 'https://openrouter.ai/api/v1'.

## Response snapshot

### Changes Applied:

**Removed `extra_headers` from LitellmModel constructor:**

Before:
```python
self.model = LitellmModel(
    model=f"openrouter/{settings.openrouter_model}",
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    extra_headers={
        "HTTP-Referer": settings.openrouter_site_url,
        "X-Title": settings.openrouter_app_title,
    }
)
```

After:
```python
self.model = LitellmModel(
    model=f"openrouter/{settings.openrouter_model}",
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url
)
```

**Note**: The `extra_headers` parameter is not supported by LitellmModel constructor in this version. The headers are typically passed at the API call level if needed. For OpenRouter, the base_url and model configuration are sufficient for basic usage.

### Validation:
- Python syntax check: PASS

## Outcome

- ✅ Impact: Fixed TypeError by removing unsupported extra_headers parameter
- 🧪 Tests: Python syntax validation PASS
- 📁 Files: 1 file modified (backend/app/agent.py)
- 🔁 Next prompts: Test chat endpoint to verify OpenRouter integration works
- 🧠 Reflection: LitellmModel constructor doesn't accept extra_headers - removed to fix TypeError

## Evaluation notes (flywheel)

- Failure modes observed: TypeError on LitellmModel initialization with extra_headers
- Graders run and results (PASS/FAIL): Syntax validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): If headers are required, implement via LiteLLM's completion call context
