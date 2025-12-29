---
id: 3
title: Create UI/UX Implementation Plan
stage: plan
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: textbook-mdx-compliance
branch: 001-textbook-mdx-compliance
user: system
command: /sp.plan
labels: ["implementation-plan", "architecture", "mermaid", "mobile-first", "dark-mode", "landing-page"]
links:
  spec: specs/001-textbook-mdx-compliance/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-textbook-mdx-compliance/plan.md
tests:
  - null
---

## Prompt

Create an architecture and design plan to satisfy the specified UI/UX requirements for the Docusaurus textbook.

The plan must include:
- Diagram architecture (Mermaid-only strategy)
- Content cleanup strategy for conversion artifacts
- Typography and dark mode design decisions
- Mobile responsiveness approach
- Introduction / landing page structure
- Files and directories impacted
- Explicit non-goals to prevent scope creep
- Safety considerations for static site generation

Do not break the plan into tasks.
Do not implement.

## Response snapshot

Created comprehensive implementation plan at `specs/001-textbook-mdx-compliance/plan.md` covering:

**5 Architecture Decisions:**
1. **Diagram Architecture**: Replace 62 custom `<Diagram>` components with native Mermaid (5-10 nodes max, mobile-optimized)
2. **Content Cleanup**: Remove 26 "Diagram Description:" artifacts + validation build checks
3. **Typography/Dark Mode**: Infima CSS variables, WCAG AA contrast (#e4e4e7 on #18181b), avoid pure white/black
4. **Mobile Responsiveness**: Mobile-first CSS, 320px minimum, horizontal scroll for diagrams
5. **Landing Page**: 2x2 module grid with textbook identity, responsive to single column on mobile

**Files Impacted:**
- Modify: docusaurus.config.ts, custom.css, readability.css, index.tsx, 21 MDX files
- Create: diagrams.css, validate-content.sh
- Delete: Diagram/ component directory

**12 Explicit Non-Goals** defined to prevent scope creep

**SSG Safety**: Build-time Mermaid rendering, artifact validation script, rollback strategy

## Outcome

- Impact: Complete architectural blueprint for UI/UX refactor ready for task generation
- Tests: N/A (planning document)
- Files: plan.md created with full architecture decisions
- Next prompts: /sp.tasks to generate actionable task list
- Reflection: Plan covers all user requirements with clear decisions and no ambiguity

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check PASSED
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate Mermaid plugin installation before implementation
