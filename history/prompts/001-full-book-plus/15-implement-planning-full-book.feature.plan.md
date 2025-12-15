---
id: 15
title: "Implement Planning for Full Book Plus Feature"
stage: "plan"
date: "2025-12-09"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "001-full-book-plus"
branch: "001-full-book-plus"
user: "DELL"
command: "/sp.plan Create a technical implementation plan for the `full-book-plus` feature of the *Physical AI & Humanoid Robotics* textbook, incorporating the clarified requirements..."
labels: ["planning", "architecture", "docusaurus", "textbook"]
links:
  spec: "/specs/001-full-book-plus/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "/specs/001-full-book-plus/plan.md"
  - "/specs/001-full-book-plus/research.md"
  - "/specs/001-full-book-plus/data-model.md"
  - "/specs/001-full-book-plus/quickstart.md"
  - "/specs/001-full-book-plus/contracts/api-contracts.md"
  - "/specs/001-full-book-plus/contracts/skill-interface.yaml"
  - "/CLAUDE.md"
tests: []
---

## Prompt Text

```
Create a technical implementation plan for the `full-book-plus` feature of the *Physical AI & Humanoid Robotics* textbook, incorporating the clarified requirements:

- Content is simplified with bullet points, shorter paragraphs, and improved structure (not full rewrite)
- All internal links use relative paths for GitHub Pages compatibility
- A prominent "Start Learning →" button on `docs/intro.md` links to `01-ros2-nervous-system/intro.md`
- better-auth is integrated client-side with localStorage; signup modal asks 3 background questions
- Personalization uses React conditional rendering based on user profile (no server logic)
- Urdu translation is implemented via:
  - Subagent: `.claude/subagents/urdu_translator/agent.md`
  - Skill: `.claude/skills/urdu-translation-skill/` (using LibreTranslate API or browser fallback)
  - "Translate to Urdu" button triggers subagent and applies RTL layout
- UI improvements: custom CSS for typography, spacing, and callouts ("Key Takeaways", "Ethical Notes")
- All 21 chapters retain frontmatter: `personalization: true`, `translation: ur`

**Deliverables**:
- Architecture sketch (frontend-only, no backend)
- Section structure per enhancement
- Research approach (research-concurrent, using official docs only)
- Decisions with tradeoffs (e.g., localStorage vs Neon, LibreTranslate vs pre-rendered Urdu)
- Quality validation strategy (Lighthouse >85, no broken links, mobile responsive)

**Technical Details**:
- GitHub Pages compatible (static only)
- Uses Docusaurus MDX for React components in Markdown
- Follows constitution.md governance
- Reusable intelligence must follow Claude Code Subagent/Skill conventions
```

## Response Text

Successfully completed the technical implementation plan for the `full-book-plus` feature. The plan includes:

**Architecture**: Frontend-only implementation with Docusaurus, React, better-auth, and Claude Code Subagent/Skill pattern for Urdu translation.

**Deliverables Created**:
1. Implementation Plan (`plan.md`) - Complete technical architecture
2. Research Document (`research.md`) - Technology decisions and rationale
3. Data Model (`data-model.md`) - Entity relationships and validation rules
4. Quickstart Guide (`quickstart.md`) - Setup and development workflow
5. API Contracts (`contracts/`) - Interface specifications for all components
6. Agent Context Update - Updated CLAUDE.md with new technologies

**Key Technical Decisions**:
- Client-side only authentication with better-auth and localStorage
- React conditional rendering for personalization (not Markdown variants)
- LibreTranslate API for on-demand Urdu translation
- Custom CSS overrides for UI improvements (not full theme)
- Claude Code Subagent/Skill pattern for translation functionality

**Quality Validation Strategy**:
- Lighthouse mobile audit target >85
- Bundle size <500KB (excluding Docusaurus core)
- GitHub Pages compatibility with relative links
- Mobile-responsive design

All constitution compliance checks passed, ensuring scientific accuracy, academic clarity, reproducibility, and ethical standards are maintained.

## Outcome

Complete technical implementation plan ready for task breakdown and execution. All architectural decisions documented with trade-offs and alternatives considered.
