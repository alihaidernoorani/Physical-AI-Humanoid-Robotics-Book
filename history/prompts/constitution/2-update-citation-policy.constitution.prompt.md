---
id: 2
title: Update Citation Policy
stage: constitution
date: 2025-12-14
surface: agent
model: sonnet
feature: none
branch: 001-textbook-mdx-compliance
user: Claude
command: /sp.constitution
labels: [constitution, citations, policy, verification]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - validate constitution completeness
---

## Prompt

Change Type: Policy Clarification (No Scope Change)

Task:
Update the constitution to remove all reader-facing citations and reference sections,
while preserving strict internal verification and zero-hallucination standards.

Rules:
- Do NOT rewrite the full document
- Do NOT change modules, structure, or architecture
- Verification is internal, not reader-facing
- The book must NOT include citations, references, or bibliographies

Enforcement:
- RAG answers must be generated only from retrieved chunks
- If grounding is insufficient, respond with uncertainty
- All indexed chunks must include metadata:
  module, chapter, subsection, source_type, source_origin

Output:
Only show added or modified sections.

## Response snapshot

The constitution has been successfully updated to remove reader-facing citations and reference sections while preserving strict internal verification and zero-hallucination standards. Key changes include:

1. Modified "Content Verification & Plagiarism Standards" to emphasize internal verification system and prohibit reader-facing citations and bibliographies.

2. Updated "Book Format & Deployment" to remove "Citations section" requirement and instead state "No citations sections or bibliographies visible to readers."

3. Changed "Content Constraints" to specify "(internal verification only)" and add "No reader-facing references or bibliographies allowed."

4. Enhanced the "Backend (FastAPI)" section to include requirements for RAG grounding enforcement:
   - RAG chatbot must only generate answers from retrieved chunks with proper grounding
   - If grounding is insufficient, respond with uncertainty rather than hallucinating
   - All indexed chunks must include metadata: module, chapter, subsection, source_type, source_origin

The version has been incremented from 1.1.0 to 1.2.0 to reflect these changes.

## Outcome

- ✅ Impact: Successfully updated constitution to remove reader-facing citations while preserving internal verification standards
- 🧪 Tests: Constitution validates successfully with new policy requirements
- 📁 Files: .specify/memory/constitution.md updated with citation policy changes
- 🔁 Next prompts: Constitution now enforces internal verification without reader-facing references
- 🧠 Reflection: Policy clarification successfully implemented while maintaining verification integrity

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Policy update completed successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - Policy update complete