import type {ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HeroSection from '@site/src/components/HeroSection';
import ModuleCard from '@site/src/components/ModuleCard';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function ModuleCards() {
  const modules = [
    {
      moduleNumber: 1 as const,
      title: 'The Robotic Nervous System',
      subtitle: 'ROS 2',
      description: 'Master the communication infrastructure for humanoid robots with nodes, topics, services, and actions.',
      weekStart: 1,
      weekEnd: 3,
      link: '/docs/ros2-nervous-system/intro',
      accentColor: '--module-1-accent',
    },
    {
      moduleNumber: 2 as const,
      title: 'The Digital Twin',
      subtitle: 'Gazebo & Unity',
      description: 'Build high-fidelity simulation environments for testing robot behaviors before real-world deployment.',
      weekStart: 4,
      weekEnd: 6,
      link: '/docs/digital-twin/intro',
      accentColor: '--module-2-accent',
    },
    {
      moduleNumber: 3 as const,
      title: 'The AI-Robot Brain',
      subtitle: 'NVIDIA Isaac',
      description: 'Implement perception, navigation, and edge inference using NVIDIA Isaac ROS and Jetson platforms.',
      weekStart: 7,
      weekEnd: 10,
      link: '/docs/ai-robot-brain/intro',
      accentColor: '--module-3-accent',
    },
    {
      moduleNumber: 4 as const,
      title: 'Vision-Language-Action',
      subtitle: 'VLA',
      description: 'Integrate voice commands, LLM reasoning, and robotic actions for natural human-robot interaction.',
      weekStart: 11,
      weekEnd: 13,
      link: '/docs/vla/intro',
      accentColor: '--module-4-accent',
    },
  ];

  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <Heading as="h2" className={styles.modulesHeading}>
          Course Modules
        </Heading>
        <div className={styles.moduleGrid}>
          {modules.map((module) => (
            <ModuleCard key={module.moduleNumber} {...module} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="A comprehensive textbook on Physical AI and Humanoid Robotics covering ROS 2, simulation, NVIDIA Isaac, and VLA models.">
      <HeroSection
        title={siteConfig.title}
        tagline={siteConfig.tagline}
        description="A comprehensive guide to building intelligent humanoid robots using ROS 2, simulation environments, NVIDIA Isaac, and Vision-Language-Action models. From neural architectures to real-world deployment."
      />
      <main>
        <ModuleCards />
      </main>
    </Layout>
  );
}
