# Implementation Tasks: Interactive Physical AI & Humanoid Robotics Textbook

## Feature Overview
Implement a complete, interactive Docusaurus textbook for *Physical AI & Humanoid Robotics* with enhanced features: better-auth integration with client-side localStorage for user profiles, personalization using React conditional rendering based on user background, on-demand Urdu translation via Claude Code Subagent/Skill pattern, and improved UI/UX with custom CSS overrides. The solution maintains all 21 chapters with simplified formatting for improved readability while ensuring GitHub Pages compatibility through static deployment and relative links.

**Feature**: 001-full-book-plus
**Branch**: 001-full-book-plus
**Input**: Feature specification from `/specs/001-full-book-plus/spec.md`

---

## Phase 1: Project Setup

- [x] T001 Create Claude Code directory structure for subagent and skill
- [x] T002 Install required dependencies: better-auth, docusaurus, react
- [x] T003 Initialize project configuration for GitHub Pages deployment

---

## Phase 2: Foundational Components

- [x] T004 Create base React components for authentication modal
- [x] T005 Set up localStorage utilities for profile management
- [x] T006 Create CSS foundation for improved typography and readability
- [x] T007 Set up Docusaurus theme overrides for custom components
- [x] T008 Create base API service utilities for translation
- [x] T009 [P] Update all chapter frontmatter to include `personalization: true` and `translation: ur`
- [x] T010 [P] Verify all existing chapter content is preserved and accessible

---

## Phase 3: User Story 1 - Access Interactive Textbook Content (P1)

**Goal**: Ensure all 21 chapters are available, properly formatted, and accessible with improved readability.

**Independent Test**: Navigate through all textbook chapters and verify content is readable, properly formatted, and all existing content is preserved.

- [ ] T011 [US1] [P] Simplify dense paragraphs in all 21 chapters (max 3–4 sentences per paragraph)
- [ ] T012 [US1] [P] Convert complex explanations into bullet points or numbered lists where appropriate
- [ ] T013 [US1] [P] Add 1–2 **diagram descriptions** per chapter (e.g., "Diagram: ROS 2 node communication flow")
- [ ] T014 [US1] [P] Add 1–2 **concrete examples** per chapter (e.g., "Example: VLA interpreting 'Clean the room'")
- [ ] T015 [US1] [P] Ensure every chapter ends with "Key Takeaways" and includes "Ethical & Safety Considerations"
- [x] T016 [US1] Add a prominent **"Start Learning →" button** to `docs/intro.md` linking to `01-ros2-nervous-system/intro.md`
- [x] T017 [US1] [P] Fix all internal links using **relative paths** (e.g., `../02-digital-twin/intro.md`)
- [x] T018 [US1] [P] Add "Next Chapter" and "Back to Module" navigation at the end of each chapter
- [ ] T019 [US1] Validate all links with `npx docusaurus build` (no 404 errors)

---

## Phase 4: User Story 2 - Personalize Learning Experience (P2)

**Goal**: Enable users to create a profile with background information so textbook content can be personalized to their experience level and learning preferences.

**Independent Test**: Complete the signup modal, set profile preferences, and verify that personalization options are available on chapters.

- [ ] T020 [US2] Install `@better-auth/react` and `@better-auth/client` via npm
- [ ] T021 [US2] Create a signup modal with 3 questions: software experience, hardware setup, learning style
- [ ] T022 [US2] Implement localStorage profile storage with validation
- [ ] T023 [US2] Create `AuthContext` to expose profile to components
- [ ] T024 [US2] Add login/signup controls to site header (non-intrusive)
- [ ] T025 [US2] Create a "Personalize This Chapter" button component (MDX-compatible)
- [ ] T026 [US2] Add personalization button to top of every chapter using Docusaurus layout
- [ ] T027 [US2] Implement conditional rendering to skip basic ROS intro for advanced users
- [ ] T028 [US2] Implement conditional rendering to highlight Jetson vs RTX examples based on hardware profile
- [ ] T029 [US2] Implement conditional rendering to suggest capstone extensions based on learning style
- [ ] T030 [US2] Ensure default content loads if user is not logged in

---

## Phase 5: User Story 3 - Translate Content to Urdu (P3)

**Goal**: Enable Urdu-speaking learners to translate textbook content to Urdu with proper right-to-left layout.

**Independent Test**: Use the Urdu translation button and verify content is properly translated and displayed with RTL layout.

- [ ] T031 [US3] Create Subagent directory: `.claude/subagents/urdu_translator/`
- [ ] T032 [US3] Define `agent.md` with activation trigger ("Translate to Urdu" button)
- [ ] T033 [US3] Create Skill directory: `.claude/skills/urdu-translation-skill/`
- [ ] T034 [US3] Implement `skill.yaml` with metadata and input/output schema
- [ ] T035 [US3] Implement `implementation.js` using LibreTranslate API (with CORS fallback)
- [ ] T036 [US3] Add "Translate to Urdu" button to top of every chapter
- [ ] T037 [US3] Implement subagent activation when Urdu button is clicked
- [ ] T038 [US3] Implement skill loading for Urdu translation
- [ ] T039 [US3] Implement content replacement with Urdu text
- [ ] T040 [US3] Implement RTL layout with `document.dir = "rtl"` and `document.lang = "ur"`
- [ ] T041 [US3] Add "Back to English" button to restore original content
- [ ] T042 [US3] Implement error handling when translation services are unavailable

---

## Phase 6: User Story 4 - Enhanced Reading Experience (P2)

**Goal**: Improve typography, spacing, and visual callouts for key content elements to better engage learners and help retain educational material.

**Independent Test**: View chapters and verify improved typography, proper spacing, and prominent visual callouts for important sections.

- [ ] T043 [US4] Create `src/css/readability.css` with body font size: 18px, line height: 1.7
- [ ] T044 [US4] Add paragraph margin: 1.5em to readability.css
- [ ] T045 [US4] Create callout styles for "Key Takeaways" in readability.css
- [ ] T046 [US4] Create callout styles for "Ethical Notes" in readability.css
- [ ] T047 [US4] Ensure mobile responsiveness (test on iPhone SE, Android)
- [ ] T048 [US4] Inject CSS via Docusaurus `stylesheets` config

---

## Phase 7: Integration & Validation

- [ ] T049 Confirm all 21 chapters have clear, scannable content
- [ ] T050 Confirm all 21 chapters have diagram descriptions and examples
- [ ] T051 Confirm all 21 chapters have personalization + Urdu buttons
- [ ] T052 Confirm all 21 chapters have working relative links
- [ ] T053 Test auth flow: signup → profile saved → personalization works
- [ ] T054 Test Urdu flow: button → RTL layout → restore English
- [ ] T055 Run `npm run build` → verify no errors
- [ ] T056 Deploy to GitHub Pages and validate live site
- [ ] T057 Achieve Lighthouse mobile score > 85

---

## Dependencies

- User Story 1 (P1) must be completed before User Stories 2, 3, and 4 can be fully tested
- Foundational components (Phase 2) must be completed before any user story implementation
- Project setup (Phase 1) must be completed before any other phases

## Parallel Execution Opportunities

- Tasks T009-T019 (User Story 1) can be executed in parallel across different chapters
- Tasks T025-T030 (User Story 2) can be implemented once and applied to all chapters
- Tasks T036-T042 (User Story 3) can be implemented once and applied to all chapters
- Tasks T043-T048 (User Story 4) can be implemented once and applied site-wide

## Implementation Strategy

**MVP Scope**: Implement User Story 1 (P1) as the minimum viable product - ensure all 21 chapters are accessible with improved readability. This provides core value while deferring advanced features.

**Incremental Delivery**:
1. Phase 1-2: Foundation setup
2. Phase 3: Core content accessibility (MVP)
3. Phase 4: Personalization features
4. Phase 5: Urdu translation
5. Phase 6: UI enhancements
6. Phase 7: Integration and validation