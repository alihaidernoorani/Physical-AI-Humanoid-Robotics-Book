---
name: "chapter-refiner"
description: "Format and refine technical textbook chapters using a clear pedagogical structure. Improves clarity, flow, and learning effectiveness without changing course structure or technical meaning. Use when refining or preparing chapter content in .md or .mdx files."
version: "1.0.0"
---

# Chapter Refiner Skill

## When to Use This Skill

- Chapter content already exists but is unclear or poorly structured
- A chapter needs better learning flow and readability
- Content must be made easier to understand without changing scope
- Preparing chapters for quizzes, glossary, or interactivity
- Working with existing `.md` or `.mdx` chapter files

---

## How This Skill Works

1. **Understand chapter intent**
   - Identify the chapter goal and learning outcome
   - Confirm alignment with the locked course outline

2. **Organize content flow**
   - Ensure the chapter follows this order:
     - Introduction
     - Core concepts
     - Examples
     - Diagrams (where helpful)
     - Exercises or practice tasks
     - Short recap

3. **Improve explanations**
   - Rewrite unclear text in simple, direct language
   - Break complex ideas into small steps
   - Explain technical terms when first introduced

4. **Add learning support where needed**
   - Insert examples to clarify abstract ideas
   - Suggest diagrams where text is insufficient
   - Add simple exercises that reinforce explained concepts

5. **Ensure consistency**
   - Maintain consistent tone and terminology
   - Match depth and style across chapters

---

## Output Format

Provide:
- **Chapter Goal**: 1–2 sentences explaining what the learner will understand
- **Formatted Chapter Structure**:
  - Introduction
  - Concepts (with clear subsections)
  - Examples
  - Diagrams (described or referenced)
  - Exercises
  - Recap
- **Refined Explanations**: Clear, learner-friendly text
- **Added Learning Elements**: Examples, exercises, or diagram notes (if required)

---

## Example

**Input**: "Chapter explaining ROS 2 nodes and topics, but content feels dense"

**Output**:
- **Chapter Goal**: Understand how ROS 2 nodes communicate using topics
- **Formatted Structure**:
  1. Introduction: Why communication matters in robots
  2. Core Concepts:
     - What is a node?
     - What is a topic?
     - Publisher and subscriber model
  3. Example: Simple sensor-to-controller message flow
  4. Diagram: Node-topic communication diagram
  5. Exercise: Identify publishers and subscribers in a given system
  6. Recap: Key takeaways
- **Refined Explanations**: Simplified, step-by-step descriptions
- **Learning Elements Added**: Example scenario and practice exercise

---

## Rules This Skill Must Follow

- Do not rename chapters or sections
- Do not add new topics outside the outline
- Do not change technical meaning
- Do not introduce backend or UI code
- Improve understanding only, not scope

---

End of skill definition
