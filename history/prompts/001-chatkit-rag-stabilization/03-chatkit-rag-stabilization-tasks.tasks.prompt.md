---
id: 03
title: ChatKit RAG Stabilization Tasks Generated
stage: tasks
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-chatkit-rag-stabilization
branch: 001-chatkit-rag-stabilization
user: alihaidernoorani
command: /sp.tasks
labels: ["tasks", "chatkit", "rag", "stabilization", "frontend", "backend"]
links:
  spec: specs/001-chatkit-rag-stabilization/spec.md
  plan: specs/001-chatkit-rag-stabilization/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-chatkit-rag-stabilization/tasks.md
tests:
  - N/A (task generation phase)
---

## Prompt

"Frontend Chat Rendering & State Synchronization Fix"

## Context
- Backend chat session creation and message persistence are functional.
- Chat API returns valid JSON responses.
- **Bug:** Chat messages (user and assistant) do not render in the UI until the ChatKit widget is minimized and reopened.
- **Root Cause:** Suspected mutable state updates in React (preventing re-renders) or conditional rendering logic tied to the widget's mount cycle.

---

## 1. Frontend Rendering & State Tasks
- [ ] **Locate Core Component:** Open the main ChatKit React component (e.g., `ChatKit.tsx`, `ChatWindow.tsx`, or `useChat.ts`).
- [ ] **Audit State Pattern:** Identify the `messages` state variable (e.g., `useState<Message[]>([])`).
- [ ] **Implement Immutable User Updates:** Ensure user messages are added using the functional spread pattern:
  - `setMessages(prev => [...prev, newUserMessage]);`
  - *Verify no `.push()` or direct array mutations are used.*
- [ ] **Implement Immutable Assistant Updates:** In the API `.then()` or `await` block, append the assistant response using the same pattern:
  - `setMessages(prev => [...prev, assistantMessage]);`
- [ ] **Fix Rendering Dependency:** Ensure the message list display is not conditionally blocked by the "widget open" state or stored only in a local variable that resets on toggle.
- [ ] **Remove Remount Hacks:** Delete any logic that forces a component refresh or relies on `useEffect` with an empty dependency array to "see" new messages.

## 2. Frontend Contract Validation Tasks
- [ ] **Payload Mapping:** Verify the `fetch` call sends exactly `{"message": "..."}` and not `{"query": "..."}` to the backend.
- [ ] **Session Continuity:** Ensure `session_id` is captured from the first response and included in all subsequent requests to maintain context.
- [ ] **Response Parsing:** Confirm the code correctly accesses `data.answer` (or equivalent) from the JSON response before updating state.

## 3. UX & Error Visibility Tasks
- [ ] **Loading Feedback:** Add a simple `isLoading` state. Show a "Bot is typing..." indicator while the API request is in flight.
- [ ] **Transparent Errors:** Replace generic "Error" alerts with the actual `detail` provided by the FastAPI backend (e.g., `error.message` from the JSON body).
- [ ] **Stability:** Ensure a failed request (4xx/500) does not clear the existing message history or break the "Send" button.

---

## Acceptance Criteria
- [ ] User messages appear in the chat bubble list **immediately** upon clicking send.
- [ ] Assistant responses appear **automatically** as soon as the API call resolves.
- [ ] No minimize/reopen, refresh, or widget toggle is required to see conversation flow.

## Response snapshot

Generated comprehensive task breakdown for ChatKit + RAG stabilization:

**Branch**: `001-chatkit-rag-stabilization`

**Task Distribution** (45 total tasks):
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 4 tasks
- Phase 3 (US1 - P1): 13 tasks (Frontend rendering fix)
- Phase 4 (US2 - P2): 8 tasks (RAG retrieval)
- Phase 5 (US3 - P3): 6 tasks (HTTP status handling)
- Phase 6 (Polish): 10 tasks (Verification)

**Key Focus Areas**:
- US1 (P1): Fix immutable state updates in React (setMessages(prev => [...prev, msg]))
- US2 (P2): Align RAG to use correct model (embed-multilingual-v3.0) and threshold (0.35)
- US3 (P3): Preserve HTTP 400 status codes (no 4xx→500 conversion)

**Parallel Opportunities**:
- US2 and US3 can develop in parallel after US1 completion
- Multiple tasks within phases can execute in parallel ([P] markers)

**Success Criteria Coverage**:
- All 6 measurable outcomes from spec (SC-001 to SC-006) addressed
- MVP scope defined (US1 only) for incremental delivery

## Outcome

- ✅ Impact: Complete task breakdown for RAG stabilization implementation
- 🧪 Tests: N/A (task generation phase)
- 📁 Files: 1 file created (tasks.md)
- 🔁 Next prompts: `/sp.implement` to execute tasks
- 🧠 Reflection: Well-structured, prioritized task list with clear dependencies and parallel execution opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Task validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with Phase 3 (US1) tasks
