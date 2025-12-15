---
id: 14
title: "Clarify Underspecified Areas"
stage: "general"
date: "2025-12-09"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-full-book-plus"
user: "DELL"
command: "/sp.clarify Clarify the following underspecified areas in the current project scope to ensure safe and efficient implementation of the `full-book-plus` feature:..."
labels: ["clarification", "specification", "requirements"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files: []
tests: []
---

## Prompt Text

```
Clarify the following underspecified areas in the current project scope to ensure safe and efficient implementation of the `full-book-plus` feature:

1. **Content Refinement Scope**:
   - Should all 21 chapters be rewritten for brevity, or only simplified (e.g., break paragraphs, add bullet points)?
   - Are "diagram descriptions" sufficient (text-only), or must actual images/SVGs be generated?

2. **Navigation & Structure**:
   - Should the "Start Learning" button on `docs/intro.md` link directly to `01-ros2-nervous-system/intro.md`?
   - Should all internal links be relative (e.g., `../02-digital-twin/intro.md`) to ensure GitHub Pages compatibility?

3. **better-auth Implementation**:
   - Is `localStorage` sufficient for storing user background (software level, hardware, learning style), or must Neon Postgres be used?
   - Should the signup modal appear on first visit, or only when a personalization/Urdu button is clicked?

4. **Personalization Logic**:
   - Should content variants be pre-authored in Markdown (e.g., `<!-- BEGINNER -->...<!-- END -->`), or handled via React conditional rendering?

5. **Urdu Translation**:
   - Is on-demand browser-based translation (e.g., LibreTranslate API) acceptable, or must Urdu content be pre-rendered as `.ur.md` files?
   - Should the Subagent `UrduTranslator` live in `.claude/subagents/urdu_translator/` and the Skill in `.claude/skills/urdu-translation-skill/` per Claude Code conventions?

6. **UI Readability**:
   - Are CSS-only overrides acceptable, or must a full Docusaurus theme be created?
   - Should "Key Takeaways" and "Ethical Notes" use custom MDX components or standard Markdown admonitions?

7. **Frontmatter Preservation**:
   - Must `personalization: true` and `translation: ur` remain in every `.md` file after content updates?

Do not propose solutions—only identify ambiguities requiring explicit resolution before `/sp.plan` and `/sp.implement`.
```

## Response Text

Successfully completed clarification session for the `full-book-plus` feature. Asked and received answers to 5 critical questions:

1. Content refinement: Simplify content with bullet points and formatting (instead of rewriting for brevity)
2. Navigation structure: Use relative links throughout for GitHub Pages compatibility
3. Auth implementation: Use localStorage only for client-side MVP (not Neon Postgres)
4. Personalization logic: Use React conditional rendering (not Markdown variants)
5. Translation approach: Use on-demand browser-based translation (not pre-rendered files)

Updated the specification file at `/mnt/c/Users/DELL/Desktop/Physical-AI-Humanoid-Robotics-Textbook/specs/001-full-book-plus/spec.md` with all clarifications in the "Clarifications" section and incorporated the decisions into the functional requirements and constraints.

## Outcome

All critical ambiguities resolved. Specification now clearly defines implementation approach for content simplification, navigation structure, data storage, personalization logic, and translation method. Ready to proceed with `/sp.plan`.
