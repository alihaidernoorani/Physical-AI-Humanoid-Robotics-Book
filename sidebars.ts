import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar configuration to match actual document IDs (without numeric prefixes)
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'ros2-nervous-system/intro',
        'ros2-nervous-system/ros2-nodes',
        'ros2-nervous-system/ros2-topics-services-actions',
        'ros2-nervous-system/writing-ros2-agents-python',
        'ros2-nervous-system/urdf-kinematic-modeling',
        'ros2-nervous-system/lifecycle-nodes-composition',
      ],
      link: {
        type: 'doc',
        id: 'ros2-nervous-system/intro',
      },
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'digital-twin/intro',
        'digital-twin/rigid-body-dynamics-gazebo',
        'digital-twin/sensor-simulation',
        'digital-twin/unity-high-fidelity-env',
        'digital-twin/synchronizing-gazebo-unity',
      ],
      link: {
        type: 'doc',
        id: 'digital-twin/intro',
      },
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'ai-robot-brain/intro',
        'ai-robot-brain/synthetic-data-generation',
        'ai-robot-brain/isaac-ros-gems',
        'ai-robot-brain/nav2-bipedal-navigation',
        'ai-robot-brain/edge-inference-jetson',
      ],
      link: {
        type: 'doc',
        id: 'ai-robot-brain/intro',
      },
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'vla/intro',
        'vla/voice-to-text-whisper',
        'vla/llm-task-decomposition',
        'vla/grounding-language-ros2',
        'vla/capstone-end-to-end',
      ],
      link: {
        type: 'doc',
        id: 'vla/intro',
      },
    },
  ],
};

export default sidebars;
