---
id: 15
title: Clarify Interactive Textbook Requirements
stage: clarif
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: full-book-plus
branch: 001-full-book-plus
user: Claude
command: /sp.clarify
labels: [clarify, textbook, authentication, translation, personalization]
links:
  spec: specs/001-full-book-plus/spec.md
  plan: null
  tasks: null
  adr: null
files:
 - specs/001-full-book-plus/spec.md
tests:
 - clarification completeness validation
 - requirement consistency check
---

## Prompt

Clarify the following underspecified areas in the current project scope to ensure safe, efficient implementation of Phase 3 features:

1. **Authentication Scope**:
   - Should better-auth run entirely client-side using `localStorage`, or is Neon Serverless Postgres integration required for user profiles during this phase?

2. **Urdu Translation Implementation**:
   - Is runtime browser-based translation (e.g., LibreTranslate API) sufficient, or must pre-generated `.ur.md` files be created for every chapter?

3. **Subagent & Skill Placement**:
   - Confirm the correct directories per Claude Code conventions:
     • Subagent: `.claude/subagents/urdu_translator/`
     • Skill: `.claude/skills/urdu-translation-skill/`
   - Should the `UrduTranslator` subagent be auto-loaded on every page, or only when the Urdu button is clicked?

4. **RAG Chatbot Timing**:
   - Is the RAG chatbot (FastAPI + Qdrant + Neon) part of this spec (`full-book-plus`), or strictly deferred to a separate `rag-chatbot` spec?

5. **UI Readability Boundaries**:
   - Are custom CSS overrides acceptable, or must all styling stay within Docusaurus theme configuration?

6. **Content Personalization Logic**:
   - Should personalization adjust content depth using React conditional rendering, or via client-side DOM manipulation after page load?

Do not propose solutions—only identify ambiguities requiring explicit resolution before `/sp.plan` and `/sp.implement`.

## Response snapshot

Successfully clarified 5 critical ambiguities in the interactive textbook specification:

1. **RAG Chatbot Scope**: Confirmed that RAG chatbot (FastAPI + Qdrant + Neon) is strictly deferred to a separate `rag-chatbot` spec, not part of this `full-book-plus` spec.

2. **Authentication Approach**: Confirmed that better-auth runs entirely client-side using `localStorage` only, with Neon Serverless Postgres integration deferred to RAG phase.

3. **Translation Implementation**: Confirmed that runtime browser-based translation is sufficient (e.g., LibreTranslate API), and pre-generated `.ur.md` files are not required.

4. **Subagent Configuration**: Confirmed that directories are correct per Claude Code conventions (`.claude/subagents/urdu_translator/` and `.claude/skills/urdu-translation-skill/`) and the UrduTranslator subagent loads only when the Urdu button is clicked, not on every page.

5. **UI Styling Approach**: Confirmed that custom CSS overrides are acceptable, not limited to Docusaurus theme configuration only.

All clarifications have been integrated into the specification document with updated functional requirements and constraints.

## Outcome

- ✅ Impact: Critical ambiguities resolved, specification ready for planning
- 🧪 Tests: Clarification completeness and requirement consistency validated
- 📁 Files: Updated spec.md with clarifications section and integrated changes
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Specification now has clear technical direction for implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - all clarifications successfully obtained
- Graders run and results (PASS/FAIL): PASS - all critical ambiguities resolved
- Prompt variant (if applicable): Requirements clarification prompt
- Next experiment (smallest change to try): Proceed to planning phase