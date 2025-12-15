# Quickstart: Physical AI & Humanoid Robotics Textbook Blueprint

## Prerequisites
- Node.js 18+ installed
- Docusaurus v3.9 installed globally (`npm install -g @docusaurus/core`)
- Git for version control

## Setup Docusaurus Project
```bash
# Create new Docusaurus project
npx create-docusaurus@latest textbook-physical-ai --typescript throwaway

# Navigate to project directory
cd textbook-physical-ai

# Install dependencies
npm install
```

## Create the Module Structure
```bash
# Create module directories
mkdir -p docs/01-ros2-nervous-system
mkdir -p docs/02-digital-twin
mkdir -p docs/03-ai-robot-brain
mkdir -p docs/04-vla
```

## Generate Module Files
Create the following files with appropriate frontmatter:

### Module 1: The Robotic Nervous System (ROS 2)
- `docs/01-ros2-nervous-system/intro.md`
- `docs/01-ros2-nervous-system/01-ros2-nodes.md`
- `docs/01-ros2-nervous-system/02-ros2-topics-services-actions.md`
- `docs/01-ros2-nervous-system/03-writing-ros2-agents-python.md`
- `docs/01-ros2-nervous-system/04-urdf-kinematic-modeling.md`
- `docs/01-ros2-nervous-system/05-lifecycle-nodes-composition.md`

### Module 2: The Digital Twin (Gazebo & Unity)
- `docs/02-digital-twin/intro.md`
- `docs/02-digital-twin/01-rigid-body-dynamics-gazebo.md`
- `docs/02-digital-twin/02-sensor-simulation.md`
- `docs/02-digital-twin/03-unity-high-fidelity-env.md`
- `docs/02-digital-twin/04-synchronizing-gazebo-unity.md`

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- `docs/03-ai-robot-brain/intro.md`
- `docs/03-ai-robot-brain/01-synthetic-data-generation.md`
- `docs/03-ai-robot-brain/02-isaac-ros-gems.md`
- `docs/03-ai-robot-brain/03-nav2-bipedal-navigation.md`
- `docs/03-ai-robot-brain/04-edge-inference-jetson.md`

### Module 4: Vision-Language-Action (VLA)
- `docs/04-vla/intro.md`
- `docs/04-vla/01-voice-to-text-whisper.md`
- `docs/04-vla/02-llm-task-decomposition.md`
- `docs/04-vla/03-grounding-language-ros2.md`
- `docs/04-vla/04-capstone-end-to-end.md`

## Example File Structure with Frontmatter
```markdown
---
id: ros2-nodes
title: ROS 2 Nodes, Topics, Services, and Actions
description: Understanding the fundamental communication patterns in ROS 2
personalization: true
translation: ur
learning_outcomes:
  - Explain the role of nodes in ROS 2 architecture
  - Implement publisher-subscriber communication patterns
  - Create service-based request-response interactions
  - Use actions for goal-oriented communication
prerequisites:
  - Basic Python programming
  - Understanding of distributed systems
software_stack:
  - ROS 2 Humble Hawksbill
  - Python 3.10+
  - rclpy client library
hardware_recommendations:
  - NVIDIA Jetson AGX Orin Development Kit
  - Intel RealSense D455 Depth Camera
hardware_alternatives:
  - Raspberry Pi 4 with camera module (budget option)
  - Laptop with ROS 2 simulation environment
assessment_recommendations:
  - Practical exercise: Create a simple ROS 2 node
  - Quiz: Identify communication patterns in given scenarios
dependencies:
  - Module 0 (Course Introduction - if exists)
---

# ROS 2 Nodes, Topics, Services, and Actions

## Introduction
[Content will go here in later phases]

## Subtopic 1: Understanding ROS 2 Nodes
[Content will go here in later phases]

## Subtopic 2: Topic-Based Communication
[Content will go here in later phases]

## Summary
[Summary will go here in later phases]
```

## Create Category Configuration
Create `docs/_category_.json`:
```json
{
  "label": "Physical AI & Humanoid Robotics",
  "position": 1,
  "link": {
    "type": "generated-index",
    "description": "A comprehensive textbook on Physical AI and Humanoid Robotics"
  }
}
```

## Run the Development Server
```bash
# Start development server
npm start

# The site will be available at http://localhost:3000
```

## Deploy to GitHub Pages
1. Configure `docusaurus.config.js` with GitHub Pages settings
2. Run build command: `npm run build`
3. Deploy using GitHub Actions or manual process