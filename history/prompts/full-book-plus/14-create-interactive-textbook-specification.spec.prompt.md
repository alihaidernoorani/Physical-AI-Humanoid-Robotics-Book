---
id: 14
title: Create Interactive Textbook Specification
stage: spec
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: full-book-plus
branch: 001-full-book-plus
user: Claude
command: /sp.specify
labels: [spec, textbook, authentication, translation, personalization]
links:
  spec: specs/001-full-book-plus/spec.md
  plan: null
  tasks: null
  adr: null
files:
 - specs/001-full-book-plus/spec.md
 - specs/001-full-book-plus/checklists/requirements.md
tests:
 - spec completeness validation
 - requirement clarity check
 - acceptance criteria verification
---

## Prompt

full-book-plus

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
- **Compatibility**: Must deploy cleanly to GitHub Pages (static only)

---

### Not Building
- **RAG chatbot** — will be implemented in a separate spec (`rag-chatbot`)
- **FastAPI, Qdrant, or Neon backend logic** — not part of this phase
- **Full Urdu content pre-generation** — translation is on-demand, not pre-rendered
- **Server-side personalization** — all logic must be client-side
- **Code examples or CLI tutorials** — textbook remains conceptual (no labs)
- **Vendor comparisons or ethical deep dives** — only brief "Ethical & Safety" subsections
- **Custom Docusaurus theme from scratch** — only override styles via CSS

---

### Success Criteria
- Book deploys to GitHub Pages
- Auth, personalization, and Urdu buttons appear and function
- Subagent and Skill follow Claude Code's native structure
- All 21 chapters readable, styled, and metadata-compliant
- No broken links or layout issues
- Implementation adheres to `constitution.md` governance

## Response snapshot

Created a comprehensive specification for the interactive Physical AI & Humanoid Robotics textbook. The specification includes:

- User Scenarios & Testing with 4 prioritized user stories covering core textbook access, personalization, Urdu translation, and enhanced reading experience
- Functional Requirements with 14 specific capabilities covering auth, personalization, translation, UI improvements, and deployment constraints
- Key Entities defining Learner Profile, Textbook Chapter, Personalization Settings, and Urdu Translation
- Success Criteria with 10 measurable outcomes including content accessibility, performance metrics, and deployment requirements

The specification follows the template structure and includes a quality checklist to validate completeness. All requirements are testable and technology-agnostic as required.

## Outcome

- ✅ Impact: Complete specification created for interactive textbook with auth, personalization, and Urdu translation
- 🧪 Tests: Spec completeness and quality validation completed
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Specification addresses all key requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements properly captured
- Graders run and results (PASS/FAIL): PASS - specification meets all quality criteria
- Prompt variant (if applicable): Feature specification prompt
- Next experiment (smallest change to try): Proceed to planning phase