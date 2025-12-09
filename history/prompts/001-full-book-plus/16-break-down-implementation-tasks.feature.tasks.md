---
id: 16
title: "Break Down Implementation Tasks"
stage: "tasks"
date: "2025-12-09"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "001-full-book-plus"
branch: "001-full-book-plus"
user: "DELL"
command: "/sp.tasks Break down the implementation plan into a clear, actionable checklist of tasks for the `full-book-plus` feature of the *Physical AI & Humanoid Robotics* textbook..."
labels: ["tasks", "breakdown", "planning", "docusaurus"]
links:
  spec: "/specs/001-full-book-plus/spec.md"
  plan: "/specs/001-full-book-plus/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "/specs/001-full-book-plus/tasks.md"
tests: []
---

## Prompt Text

```
Break down the implementation plan into a clear, actionable checklist of tasks for the `full-book-plus` feature of the *Physical AI & Humanoid Robotics* textbook.

**Scope**:
- Refactor existing chapter content for clarity and readability
- Fix navigation and internal linking
- Integrate better-auth with background questionnaire
- Implement personalization using React conditional rendering
- Add Urdu translation via Claude Code Subagent + Skill
- Improve UI/UX with GitHub Pages compatibility

**Requirements**:
- All tasks must be grouped into logical phases
- Preserve frontmatter (`personalization: true`, `translation: ur`) in every `.md` file
- Follow Claude Code conventions: Subagent in `.claude/subagents/`, Skill in `.claude/skills/`
- Use relative links only (e.g., `../02-digital-twin/intro.md`) for GitHub Pages compatibility
- Store user profile in `localStorage` (Neon DB deferred to RAG phase)

**Organize tasks into the following sections**:

---

### Content Refinement & Readability
- [ ] Simplify dense paragraphs in all 21 chapters (max 3–4 sentences per paragraph)
- [ ] Convert complex explanations into bullet points or numbered lists where appropriate
- [ ] Add 1–2 **diagram descriptions** per chapter (e.g., "Diagram: ROS 2 node communication flow")
- [ ] Add 1–2 **concrete examples** per chapter (e.g., "Example: VLA interpreting 'Clean the room'")
- [ ] Ensure every chapter ends with "Key Takeaways" and includes "Ethical & Safety Considerations"

### Navigation & Linking
- [ ] Add a prominent **"Start Learning →" button** to `docs/intro.md` linking to `01-ros2-nervous-system/intro.md`
- [ ] Fix all internal links using **relative paths** (e.g., `../02-digital-twin/intro.md`)
- [ ] Add "Next Chapter" and "Back to Module" navigation at the end of each chapter
- [ ] Validate all links with `npx docusaurus build` (no 404 errors)

### better-auth Integration
- [ ] Install `@better-auth/react` and `@better-auth/client` via npm
- [ ] Create a signup modal with 3 questions:
  - Software experience (Beginner/Intermediate/Advanced)
  - Hardware setup (e.g., Jetson Orin, RTX GPU)
  - Learning style preference
- [ ] Store user profile in `localStorage`
- [ ] Create `AuthContext` to expose profile to components
- [ ] Add login/signup controls to site header (non-intrusive)

### Personalization System
- [ ] Create a "Personalize This Chapter" button component (MDX-compatible)
- [ ] Add button to top of every chapter using Docusaurus layout
- [ ] Implement conditional rendering:
  - Skip basic ROS intro for advanced users
  - Highlight Jetson vs RTX examples based on hardware profile
  - Suggest capstone extensions based on learning style
- [ ] Ensure default content loads if user is not logged in

### Urdu Translation (Subagent + Skill)
- [ ] Create Subagent directory: `.claude/subagents/urdu_translator/`
- [ ] Define `agent.md` with activation trigger ("Translate to Urdu" button)
- [ ] Create Skill directory: `.claude/skills/urdu-translation-skill/`
- [ ] Implement `skill.yaml` with metadata and input/output schema
- [ ] Implement `implementation.js` using LibreTranslate API (with CORS fallback)
- [ ] Add "Translate to Urdu" button to top of every chapter
- [ ] On click:
  - Activate `UrduTranslator` subagent
  - Load `urdu-translation-skill`
  - Replace English text with Urdu
  - Set `document.dir = "rtl"` and `document.lang = "ur"`
- [ ] Add "Back to English" button to restore original content

### UI Readability Improvements
- [ ] Create `src/css/readability.css` with:
  - Body font size: 18px, line height: 1.7
  - Paragraph margin: 1.5em
  - Callout styles for "Key Takeaways" and "Ethical Notes"
- [ ] Ensure mobile responsiveness (test on iPhone SE, Android)
- [ ] Inject CSS via Docusaurus `stylesheets` config

### Final Validation
- [ ] Confirm all 21 chapters have:
  - Clear, scannable content
  - Diagram descriptions and examples
  - Personalization + Urdu buttons
  - Working relative links
- [ ] Test auth flow: signup → profile saved → personalization works
- [ ] Test Urdu flow: button → RTL layout → restore English
- [ ] Run `npm run build` → no errors
- [ ] Deploy to GitHub Pages and validate live site
- [ ] Achieve Lighthouse mobile score > 85

---

Output this as a clean, copy-pasteable checklist. Do not include explanations or commentary.
```

## Response Text

Successfully generated a comprehensive task breakdown for the `full-book-plus` feature implementation. The tasks.md file includes:

**Phase Organization**:
- Phase 1: Project Setup
- Phase 2: Foundational Components
- Phase 3: User Story 1 - Access Interactive Textbook Content (P1)
- Phase 4: User Story 2 - Personalize Learning Experience (P2)
- Phase 5: User Story 3 - Translate Content to Urdu (P3)
- Phase 6: User Story 4 - Enhanced Reading Experience (P2)
- Phase 7: Integration & Validation

**Key Features Implemented in Tasks**:
- Content refinement and readability improvements across all 21 chapters
- Navigation and linking with relative paths for GitHub Pages
- better-auth integration with localStorage profile storage
- Personalization system with React conditional rendering
- Urdu translation via Claude Code Subagent/Skill pattern
- UI/UX improvements with custom CSS

**Task Format Compliance**:
- All tasks follow the required checklist format with Task IDs (T001, T002, etc.)
- Parallelizable tasks marked with [P] flag
- User story-specific tasks marked with [US1], [US2], [US3], [US4] labels
- Dependencies and parallel execution opportunities documented
- Implementation strategy with MVP scope defined

## Outcome

Complete task breakdown ready for implementation. The 57 tasks are organized by user story priority and implementation phase, with clear dependencies and parallel execution opportunities identified. Each task is specific enough to be executed independently while contributing to the overall feature goals.