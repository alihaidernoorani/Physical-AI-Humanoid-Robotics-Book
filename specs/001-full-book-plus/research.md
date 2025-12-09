# Research: Interactive Physical AI & Humanoid Robotics Textbook

## Research Tasks Completed

### 1. better-auth Integration Research

**Decision**: Use better-auth client-side only with modal signup
**Rationale**: Aligns with requirement for client-side authentication and localStorage persistence. Better-auth provides a clean modal-based signup experience that can collect the required profile information (software experience, hardware setup, learning style).
**Implementation Approach**: Use better-auth's client-side SDK with custom modal for profile collection.

**Alternatives Considered**:
- Custom auth solution: More development time, less secure
- Auth0/Firebase: Would require backend integration, violating constraints

### 2. LibreTranslate API Compatibility Research

**Decision**: Use LibreTranslate API for on-demand translation
**Rationale**: Open source, CORS-friendly, no vendor lock-in. Supports Urdu translation and can be called from client-side JavaScript. Matches requirement for runtime browser-based translation.
**Implementation Approach**: Call LibreTranslate API endpoints directly from client-side when translation button is clicked.

**Alternatives Considered**:
- Google Translate API: Potential CORS issues, vendor lock-in
- Browser built-in translate: Limited control, inconsistent support
- Pre-generated files: Violates constraint of on-demand translation

### 3. Claude Code Subagent/Skill Architecture Research

**Decision**: Implement UrduTranslator subagent with urdu-translation-skill following Claude Code conventions
**Rationale**: Matches specified architecture pattern in feature requirements. Subagent loads skill only when needed, following Matrix-style "load when needed" pattern.
**Implementation Approach**: Create subagent in `.claude/subagents/urdu_translator/agent.md` and skill in `.claude/skills/urdu-translation-skill/` with proper interfaces.

**Alternatives Considered**:
- Direct function calls: Doesn't follow Claude Code conventions
- Auto-loaded components: Would impact performance, violating load-on-demand pattern

### 4. Docusaurus MDX Component Integration Research

**Decision**: Override Docusaurus theme components to add personalization and translation buttons
**Rationale**: Maintains compatibility with existing Docusaurus setup while adding required functionality. Can be done with custom CSS and React components.
**Implementation Approach**: Create custom MDX components that wrap existing Docusaurus components and add the required buttons.

**Alternatives Considered**:
- Fork Docusaurus theme: Too complex, harder to maintain
- Separate overlay components: Would be less integrated

### 5. RTL (Right-to-Left) Layout Research

**Decision**: Use CSS `dir="rtl"` attribute with Urdu-specific styling
**Rationale**: Standard approach for RTL languages in web development. Works well with modern browsers and maintains accessibility.
**Implementation Approach**: Apply RTL styling dynamically when Urdu translation is activated.

**Alternatives Considered**:
- Custom RTL implementation: More error-prone, reinventing standard approaches
- Separate Urdu pages: Would require pre-generated files, violating constraints

## Key Findings

1. **better-auth** supports client-side modal integration that can collect custom profile information
2. **LibreTranslate API** is CORS-compatible and supports Urdu translation
3. **Claude Code Subagent/Skill** framework can be implemented as specified
4. **Docusaurus** allows theme component overrides for custom functionality
5. **RTL layout** can be dynamically applied using standard web technologies

## Technical Validation

- All selected technologies are compatible with static site deployment to GitHub Pages
- Client-side only approach meets security and performance constraints
- Bundle size can stay under 500KB with proper code splitting
- Lighthouse mobile audit score should exceed 85 with optimized implementation