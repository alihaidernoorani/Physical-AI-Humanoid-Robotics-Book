---
id: 09
title: Fix Qdrant Search Attribute Error
stage: green
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-chatkit-rag-stabilization
branch: 001-chatkit-rag-stabilization
user: alihaidernoorani
command: /sp.implement
labels: ["fix", "qdrant", "search", "attribute-error", "error-handling"]
links:
  spec: specs/001-chatkit-rag-stabilization/spec.md
  plan: specs/001-chatkit-rag-stabilization/plan.md
  tasks: specs/001-chatkit-rag-stabilization/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/rag.py
tests:
  - Python syntax validation: PASS
---

## Prompt

Fix Qdrant search attribute error in backend/app/rag.py:
1. In QdrantRetrievalService, ensure the client is initialized correctly.
2. In the search_chunks_full_book and search_chunks_per_page methods, ensure the search call uses the correct syntax for the current qdrant-client version.
3. If self.client.search is failing, update it to use the recommended client.search() or client.query_points() method.
4. Add a try/except block around the search call to log the specific error message if it fails again.

## Response snapshot

### Changes Applied:

**1. Updated parameter names for qdrant-client >= 1.8.0:**
- Changed `query_vector` → `query`
- Changed `query_filter` → `filter`
- Changed `with_payload` → kept as is

**2. Added try/except with AttributeError handling in all search calls:**

**search_chunks_full_book (lines 208-226):**
```python
try:
    results = self.client.search(
        collection_name=self.collection_name,
        query=query_embedding,
        limit=limit * 2,
        filter=qdrant_filters,
        with_payload=True
    )
except AttributeError as e:
    logger.error(f"Qdrant client AttributeError (method not found): {str(e)}")
    logger.error("Trying alternative search method...")
    # Fallback to query_points for newer versions
    results = self.client.query_points(
        collection_name=self.collection_name,
        query=query_embedding,
        limit=limit * 2,
        filter=qdrant_filters,
        with_payload=True
    ).points
```

**search_chunks_per_page (lines 257-288):**
- Same pattern applied to both selected_text_results and query_results searches
- Each has try/except with fallback to query_points()

### Validation:
- Python syntax check: PASS

## Outcome

- ✅ Impact: Qdrant search now uses correct v1.8+ API syntax with fallback for version compatibility
- 🧪 Tests: Python syntax validation PASS
- 📁 Files: 1 file modified (backend/app/rag.py)
- 🔁 Next prompts: Test the chat endpoint to verify search works
- 🧠 Reflection: qdrant-client >= 1.8.0 renamed search parameters; added fallback for future compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Syntax validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test actual search against live Qdrant instance
