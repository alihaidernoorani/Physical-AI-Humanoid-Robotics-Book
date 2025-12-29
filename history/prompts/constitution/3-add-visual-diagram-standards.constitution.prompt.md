---
id: 3
title: Add Visual and Diagram Standards
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-chatkit-rag-stabilization
user: system
command: /sp.constitution
labels: ["visual-standards", "diagrams", "mermaid", "mobile-first", "dark-mode", "typography"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Define project-wide quality standards for the Docusaurus technical textbook.

The constitution must enforce:
- Mermaid-first diagrams (no custom Diagram components)
- Every diagram must have a visible visual representation and a caption
- No conversion artifacts such as "Diagram Descriptions" or placeholder text
- Mobile-first readability (typography, spacing, overflow)
- Dark-mode optimized typography and contrast for long-form reading
- Textbook-style visual hierarchy (not API documentation style)
- Diagrams must be responsive and not overflow on mobile
- Introductory landing page is mandatory for the book

Prohibit:
- Diagram metadata without diagrams
- Placeholder or descriptive-only diagram text
- Custom diagram rendering components unless explicitly justified

Output only the constitution rules.
Do not plan or implement.

## Response snapshot

Updated constitution from v1.2.0 to v1.3.0 with the following additions:

**New Sections Added:**
1. **Landing Page Requirements** - Mandatory introductory landing page with module cards, textbook identity, and responsive design
2. **Visual Standards & Diagrams** - Mermaid-first policy, prohibited content (placeholder text, conversion artifacts), responsive diagram requirements
3. **Typography & Readability** - Mobile-first design (16px min, 1.5-1.7 line-height), dark-mode optimization (WCAG AA), textbook-style visual hierarchy
4. **Visual Quality Checklist** - Pre-acceptance verification checklist for diagrams, mobile readability, dark mode, and landing page

**Modified Sections:**
- Frontend (Docusaurus) - Added Mermaid native support, mobile-first responsive design, textbook-style hierarchy constraints
- Visual & Accessibility Standards - Expanded with alt text requirements and color accessibility
- Acceptance Criteria - Added diagram rendering, mobile verification, and dark mode criteria

## Outcome

- Impact: Constitution now enforces strict visual and diagram standards for educational textbook quality
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md updated
- Next prompts: Apply visual standards to existing content, audit diagrams for compliance
- Reflection: MINOR version bump appropriate - new principles added without breaking existing structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate existing content against new visual checklist
