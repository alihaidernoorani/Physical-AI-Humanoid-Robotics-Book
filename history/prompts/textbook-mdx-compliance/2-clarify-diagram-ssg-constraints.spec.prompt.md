---
id: 2
title: Clarify Diagram and SSG Constraints
stage: spec
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: textbook-mdx-compliance
branch: 001-textbook-mdx-compliance
user: system
command: /sp.clarify
labels: ["clarification", "diagrams", "mermaid", "ssg", "dark-mode", "regression-prevention"]
links:
  spec: specs/001-textbook-mdx-compliance/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-textbook-mdx-compliance/spec.md
tests:
  - null
---

## Prompt

Identify missing constraints, assumptions, and edge cases related to the UI/UX refactor of the Docusaurus textbook.

Clarify:
- Whether all diagram descriptions must become Mermaid diagrams
- Whether some conceptual diagrams should be converted to prose instead
- Expected Mermaid complexity level (simple vs detailed)
- Dark mode theming expectations for diagrams
- How to handle future content imports to avoid regression
- Any constraints related to static site generation (SSG)

Ask clarification questions and propose default assumptions where answers are missing.
Do not plan or implement yet.

## Response snapshot

Conducted 5 clarification questions with recommendations accepted:

**Q1: Diagram Conversion Strategy** → Mermaid-first with prose fallback for abstract concepts

**Q2: Mermaid Complexity Level** → Simple and readable (5-10 nodes, clear labels, mobile-optimized)

**Q3: Dark Mode Theming** → Automatic theme switching via Docusaurus Mermaid plugin

**Q4: Regression Prevention** → Build-time validation with automated artifact pattern checks

**Q5: SSG Constraints** → Strict static-only (all diagrams render at build time, no client-side JS for core content)

**New Requirements Added:**
- FR-DG-008 to FR-DG-010 (diagram complexity, prose fallback, SSG rendering)
- FR-DM-006 (automatic dark mode theming)
- FR-RP-001 to FR-RP-004 (regression prevention)
- FR-SSG-001 to FR-SSG-004 (static site constraints)
- SC-013 to SC-016 (new success criteria)

## Outcome

- Impact: Spec now has complete constraints for diagram handling, dark mode, regression prevention, and SSG compliance
- Tests: N/A (specification document)
- Files: spec.md updated with 14 new requirements and 4 new success criteria
- Next prompts: /sp.plan to define implementation approach
- Reflection: All recommendations accepted - defaults aligned with best practices for educational SSG sites

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify Docusaurus Mermaid plugin supports automatic theming
