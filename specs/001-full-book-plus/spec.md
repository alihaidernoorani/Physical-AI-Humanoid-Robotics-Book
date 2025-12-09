# Feature Specification: Interactive Physical AI & Humanoid Robotics Textbook

**Feature Branch**: `001-full-book-plus`
**Created**: 2025-12-09
**Status**: Draft
**Input**: User description: "full-book-plus

Generate a complete, interactive Docusaurus textbook for *Physical AI & Humanoid Robotics* that includes:

1. **Full chapter content** for all 21 chapters (already drafted — verify and preserve)
2. **better-auth integration**:
   - Signup modal with 3 background questions:
     • Software experience (Beginner/Intermediate/Advanced)
     • Hardware setup (e.g., Jetson Orin, RTX GPU)
     • Learning style preference
   - Store profile in `localStorage` (client-side MVP acceptable)
3. **Personalization button** at top of every chapter:
   - Adjusts content depth/examples based on user profile
4. **"Translate to Urdu" button** at top of every chapter:
   - Triggers a **Claude Code Subagent** named `UrduTranslator`
   - The Subagent loads a **reusable Skill** called `urdu-translation-skill`
   - Skill uses a lightweight translation method (e.g., LibreTranslate API or browser-based)
   - Renders Urdu with RTL (right-to-left) layout
5. **UI Readability Improvements**:
   - Better typography, spacing, and visual callouts for "Key Takeaways" and "Ethical Notes"
   - Mobile-responsive Docusaurus theme
6. **Preserve frontmatter**: `personalization: true`, `translation: ur` in every `.md` file

**Subagent & Skill Placement**:
- Subagent `UrduTranslator` must be defined in:
  `.claude/subagents/urdu_translator/agent.md`
- Skill `urdu-translation-skill` must be implemented in:
  `.claude/skills/urdu-translation-skill/`
- Skill must include:
  - `skill.yaml` (metadata)
  - `implementation.js` or `implementation.ts` (logic)
  - Clear interface for input (chapter text) and output (Urdu text)
- Integration must follow **Claude Code Subagent/Skill patterns** as documented in [code.claude.com/docs](https://code.claude.com/docs/en/sub-agents)

---

### Constraints
- **Authentication**: Use better-auth client-side only; no custom backend/auth server
- **State**: User profiles stored in `localStorage`; Neon DB integration deferred to RAG phase
- **Translation**: No full i18n framework—use on-demand API or browser-based translation
- **Frontend**: Only React/Docusaurus MDX; no additional state libraries (e.g., Redux)
- **Responsiveness**: Must pass Lighthouse mobile audit (>85)
- **Performance**: Total JS bundle < 500 KB (excluding Docusaurus core)
- **Compatibility**: Must deploy cleanly to GitHub Pages (static only); all internal links must be relative for GitHub Pages compatibility

---

### Not Building
- **RAG chatbot** — strictly deferred to separate `rag-chatbot` spec (not part of this `full-book-plus` spec)
- **FastAPI, Qdrant, or Neon backend logic** — not part of this phase
- **Full Urdu content pre-generation** — translation is on-demand, not pre-rendered
- **Server-side personalization** — all logic must be client-side
- **Code examples or CLI tutorials** — textbook remains conceptual (no labs)
- **Vendor comparisons or ethical deep dives** — only brief "Ethical & Safety" subsections
- **Custom Docusaurus theme from scratch** — only override styles via CSS (custom CSS overrides are acceptable per clarification)

---

### Success Criteria
- Book deploys to GitHub Pages
- Auth, personalization, and Urdu buttons appear and function
- Subagent and Skill follow Claude Code's native structure
- All 21 chapters readable, styled, and metadata-compliant
- No broken links or layout issues
- Implementation adheres to `constitution.md` governance"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Access Interactive Textbook Content (Priority: P1)

As a learner, I want to access the Physical AI & Humanoid Robotics textbook with all 21 chapters available and properly formatted, so that I can engage with comprehensive educational content.

**Why this priority**: This is the core value proposition - without accessible textbook content, no other features provide value. This establishes the baseline functionality.

**Independent Test**: Can be fully tested by navigating through all textbook chapters and verifying content is readable, properly formatted, and all existing content is preserved.

**Acceptance Scenarios**:

1. **Given** I am on the textbook website, **When** I navigate to any chapter, **Then** I see properly formatted educational content with learning objectives, explanations, and key takeaways
2. **Given** I am viewing a textbook chapter, **When** I scroll through the content, **Then** the layout remains readable and responsive on both desktop and mobile devices

---

### User Story 2 - Personalize Learning Experience (Priority: P2)

As a learner, I want to create a profile with my background information so that the textbook content can be personalized to my experience level and learning preferences.

**Why this priority**: This significantly enhances the learning experience by adapting content to individual needs, making the textbook more effective for diverse audiences.

**Independent Test**: Can be fully tested by completing the signup modal, setting profile preferences, and verifying that personalization options are available on chapters.

**Acceptance Scenarios**:

1. **Given** I am a new visitor to the textbook, **When** I access the site, **Then** I can complete a signup modal with software experience, hardware setup, and learning style preferences
2. **Given** I have completed profile setup, **When** I view any chapter, **Then** I see a personalization button that allows me to adjust content depth based on my profile

---

### User Story 3 - Translate Content to Urdu (Priority: P3)

As a learner who prefers Urdu, I want to translate textbook content to Urdu with proper right-to-left layout so that I can access educational materials in my preferred language.

**Why this priority**: This expands accessibility to Urdu-speaking learners, significantly broadening the textbook's reach and impact.

**Independent Test**: Can be fully tested by using the Urdu translation button and verifying content is properly translated and displayed with RTL layout.

**Acceptance Scenarios**:

1. **Given** I am viewing any textbook chapter, **When** I click the "Translate to Urdu" button, **Then** the content is translated to Urdu with proper RTL layout
2. **Given** I have translated content to Urdu, **When** I navigate to another chapter, **Then** I can choose to maintain Urdu translation or switch back to English

---

### User Story 4 - Enhanced Reading Experience (Priority: P2)

As a learner, I want improved typography, spacing, and visual callouts for key content elements so that I can better engage with and retain educational material.

**Why this priority**: This directly impacts learning effectiveness by improving readability and highlighting important information like key takeaways and ethical notes.

**Independent Test**: Can be fully tested by viewing chapters and verifying improved typography, proper spacing, and prominent visual callouts for important sections.

**Acceptance Scenarios**:

1. **Given** I am viewing a textbook chapter, **When** I read through the content, **Then** I see improved typography and spacing that enhances readability
2. **Given** I am reading a chapter, **When** I encounter key takeaways or ethical notes, **Then** these sections are clearly highlighted with visual callouts

---

### Edge Cases

- What happens when a user has JavaScript disabled and cannot use the translation functionality?
- How does the system handle extremely long chapter content that might impact performance?
- What occurs when multiple users access the textbook simultaneously during peak usage?
- How does the personalization feature behave when a user updates their profile preferences?
- What happens if the Urdu translation service is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide access to all 21 chapters of the Physical AI & Humanoid Robotics textbook with simplified content using bullet points and formatting for improved readability
- **FR-002**: System MUST implement better-auth integration with a signup modal that collects software experience, hardware setup, and learning style preference
- **FR-003**: System MUST store user profile information in localStorage for client-side personalization (Neon Serverless Postgres integration deferred to RAG phase) - localStorage only
- **FR-004**: Users MUST be able to access a personalization button on every chapter that adjusts content depth based on their profile using React conditional rendering
- **FR-005**: Users MUST be able to translate textbook content to Urdu using a dedicated button on each chapter (on-demand browser-based translation, not pre-generated files)
- **FR-006**: System MUST render Urdu content with proper right-to-left (RTL) layout
- **FR-007**: System MUST implement Claude Code Subagent pattern for Urdu translation with UrduTranslator agent (loads only when Urdu button clicked, not on every page)
- **FR-008**: System MUST implement reusable Skill pattern for translation with urdu-translation-skill (stored in .claude/skills/urdu-translation-skill/ per Claude Code conventions)
- **FR-009**: System MUST improve typography, spacing, and visual callouts for "Key Takeaways" and "Ethical Notes" using custom CSS overrides as needed
- **FR-010**: System MUST maintain mobile-responsive design that passes Lighthouse mobile audit (>85)
- **FR-011**: System MUST preserve frontmatter metadata with `personalization: true` and `translation: ur` in every chapter file
- **FR-012**: System MUST maintain JS bundle size under 500 KB (excluding Docusaurus core)
- **FR-013**: System MUST deploy cleanly to GitHub Pages as a static site
- **FR-014**: System MUST provide proper error handling when translation services are unavailable

### Key Entities

- **Learner Profile**: User's background information including software experience level, hardware setup, and learning style preference stored in localStorage
- **Textbook Chapter**: Educational content unit containing learning objectives, conceptual explanations, key takeaways, and ethical notes
- **Personalization Settings**: Configuration that adjusts content depth and examples based on user profile preferences
- **Urdu Translation**: Converted content in Urdu language with proper RTL formatting and layout

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 21 chapters of the Physical AI & Humanoid Robotics textbook are accessible and properly formatted on the deployed site
- **SC-002**: Users can complete the signup modal with 3 background questions (software experience, hardware setup, learning style) in under 2 minutes
- **SC-003**: The personalization button appears and functions correctly on every chapter page, adjusting content based on user profile
- **SC-004**: The "Translate to Urdu" button appears and functions correctly on every chapter page with proper RTL layout
- **SC-005**: The deployed textbook passes Lighthouse mobile audit with a score of 85 or higher
- **SC-006**: The total JavaScript bundle size remains under 500 KB (excluding Docusaurus core)
- **SC-007**: The textbook deploys successfully to GitHub Pages without errors
- **SC-008**: All existing frontmatter metadata (`personalization: true`, `translation: ur`) is preserved in every chapter file
- **SC-009**: 95% of users can successfully navigate between chapters without broken links or layout issues
- **SC-010**: Claude Code Subagent and Skill patterns are properly implemented according to documentation standards

## Clarifications

### Session 2025-12-09

- Q: Should the RAG chatbot (FastAPI + Qdrant + Neon) be part of this spec or deferred to a separate `rag-chatbot` spec? → A: Deferred to separate `rag-chatbot` spec
- Q: Should better-auth run entirely client-side using `localStorage`, or is Neon Serverless Postgres integration required for user profiles during this phase? → A: Client-side only using `localStorage`
- Q: Is runtime browser-based translation sufficient, or must pre-generated `.ur.md` files be created for every chapter? → A: Runtime browser-based translation
- Q: Confirm correct directories per Claude Code conventions and subagent loading behavior? → A: Directories correct per Claude Code conventions AND subagent loads only when Urdu button clicked
- Q: Are custom CSS overrides acceptable, or must all styling stay within Docusaurus theme configuration? → A: Custom CSS overrides acceptable
- Q: Should chapters be rewritten for brevity or simplified with better formatting? → A: Simplify content with bullet points and formatting
- Q: Should internal links be relative for GitHub Pages compatibility? → A: Relative links throughout
- Q: Should user data be stored in localStorage or Neon Postgres? → A: localStorage only
- Q: Should personalization use React conditional rendering or Markdown variants? → A: React conditional rendering
- Q: Should translation be on-demand or pre-rendered? → A: On-demand browser-based translation
