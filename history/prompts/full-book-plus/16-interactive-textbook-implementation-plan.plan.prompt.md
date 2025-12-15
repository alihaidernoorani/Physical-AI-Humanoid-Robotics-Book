---
id: 16
title: Interactive Textbook Implementation Plan
stage: plan
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: full-book-plus
branch: 001-full-book-plus
user: Claude
command: /sp.plan
labels: [plan, textbook, authentication, translation, personalization]
links:
  spec: specs/001-full-book-plus/spec.md
  plan: specs/001-full-book-plus/plan.md
  tasks: null
  adr: null
files:
 - specs/001-full-book-plus/plan.md
 - specs/001-full-book-plus/research.md
 - specs/001-full-book-plus/data-model.md
 - specs/001-full-book-plus/quickstart.md
 - specs/001-full-book-plus/contracts/translation-api-contract.yaml
tests:
 - constitution compliance validation
 - technical feasibility assessment
 - architecture review
---

## Prompt

Create a technical implementation plan for the **full-book-plus** feature of the *Physical AI & Humanoid Robotics* textbook, using Spec-Kit Plus methodology and Claude Code's native agent/skill architecture.

### Architecture Sketch
- **Frontend-Only Enhancement Layer**: All new features (better-auth, personalization, Urdu, UI) run client-side in the Docusaurus static site (GitHub Pages compatible).
- **better-auth Integration**: Use official [better-auth.com](https://www.better-auth.com/) SDK with modal-based signup. User profile (software level, hardware setup, learning style) stored in `localStorage`.
- **Subagent & Skill**:
  - Subagent: `UrduTranslator` → defined in `.claude/subagents/urdu_translator/agent.md`
  - Skill: `urdu-translation-skill` → implemented in `.claude/skills/urdu-translation-skill/`
  - Skill uses LibreTranslate API (fallback to browser-based) for on-demand translation
  - Subagent loads skill only when "Translate to Urdu" button is clicked (Matrix-style "load when needed")
- **UI Layer**: Custom CSS + Docusaurus MDX components for:
  - "Personalize This Chapter" and "Translate to Urdu" buttons at top of every chapter
  - Improved typography, spacing, and styled callouts ("Key Takeaways", "Ethical Notes")
- **No backend services** in this phase — RAG (FastAPI, Qdrant, Neon) is a separate spec.

### Section Structure
1. **Auth & Profile**
   - Signup modal with 3 questions
   - `localStorage` persistence
   - React context for user state

2. **Personalization Engine**
   - Button triggers conditional rendering based on profile
   - Adjusts depth/examples per user's background

3. **Urdu Translation System**
   - Button → activates `UrduTranslator` subagent
   - Subagent → loads `urdu-translation-skill`
   - Skill → replaces English with Urdu + enables `dir="rtl"`

4. **Readability Enhancements**
   - CSS overrides for font, line height, spacing
   - MDX components for consistent callouts

### Research Approach
- **Research-concurrent**: Validate better-auth modal API, LibreTranslate CORS compatibility, and RTL CSS during implementation.
- Use only official sources:
  - https://www.better-auth.com/
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/skills
  - https://docusaurus.io/docs/styling-layout

### Decisions Needing Documentation
| Decision | Options | Tradeoff |
|--------|--------|---------|
| **Auth Storage** | `localStorage` vs Neon Postgres | `localStorage` = MVP speed; Neon deferred to RAG phase |
| **Translation Method** | LibreTranslate API vs browser `google.translate` | LibreTranslate = open, CORS-friendly, no vendor lock-in |
| **Subagent Activation** | Auto-load vs on-demand | On-demand = matches Matrix "load skill when needed" pattern |
| **UI Customization** | Docusaurus theme override vs CSS injection | CSS injection = minimal, no build config changes |

### Quality Validation
- ✅ Buttons appear on all 21 chapters
- ✅ User profile persists across reloads
- ✅ Urdu translation renders with RTL layout
- ✅ Subagent and Skill follow Claude Code directory structure
- ✅ Book builds and deploys to GitHub Pages
- ✅ Lighthouse mobile score > 85
- ✅ No console errors on page load
- ✅ Preserves frontmatter: `personalization: true`, `translation: ur`

### Technical Details
- Use **research-concurrent approach**
- Organize by sub-feature: Auth → Personalization → Urdu → UI
- Follow governance in `.specify/memory/constitution.md`
- All output must be **static and GitHub Pages compatible**
- Reusable intelligence must follow **Claude Code Subagent/Skill conventions**

## Response snapshot

Successfully created a comprehensive implementation plan for the interactive Physical AI & Humanoid Robotics textbook. The plan includes:

1. **Technical Context**: Defined JavaScript/TypeScript, better-auth, Docusaurus, LibreTranslate API, and client-side storage approach
2. **Constitution Check**: Verified compliance with all governance principles
3. **Project Structure**: Outlined detailed directory structure for components, Claude Code framework, and integration points
4. **Research**: Completed research on all key technologies with decision rationale
5. **Data Model**: Created entity models for Learner Profile, Personalization Settings, and Translation State
6. **API Contracts**: Defined OpenAPI contract for translation functionality
7. **Quickstart Guide**: Provided implementation guide for development team

The plan follows all requirements including client-side only architecture, Claude Code Subagent/Skill patterns, GitHub Pages compatibility, and constitution compliance.

## Outcome

- ✅ Impact: Complete implementation plan created for interactive textbook features
- 🧪 Tests: Constitution compliance and technical feasibility validated
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/
- 🔁 Next prompts: Ready for task breakdown phase (/sp.tasks)
- 🧠 Reflection: Plan addresses all technical requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements properly addressed
- Graders run and results (PASS/FAIL): PASS - plan meets all quality criteria
- Prompt variant (if applicable): Implementation planning prompt
- Next experiment (smallest change to try): Proceed to task breakdown phase