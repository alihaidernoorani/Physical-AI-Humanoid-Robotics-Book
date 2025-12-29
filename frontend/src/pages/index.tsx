import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        {/* T063: Textbook intro paragraph */}
        <p className={styles.heroDescription}>
          A comprehensive guide to building intelligent humanoid robots using ROS 2,
          simulation environments, NVIDIA Isaac, and Vision-Language-Action models.
          From neural architectures to real-world deployment.
        </p>
      </div>
    </header>
  );
}

{/* T064: Module cards component */}
function ModuleCards() {
  const modules = [
    {
      title: 'Module 1: The Robotic Nervous System',
      subtitle: 'ROS 2',
      description: 'Master the communication infrastructure for humanoid robots with nodes, topics, services, and actions.',
      link: '/docs/ros2-nervous-system/intro',
      chapters: 5,
    },
    {
      title: 'Module 2: The Digital Twin',
      subtitle: 'Gazebo & Unity',
      description: 'Build high-fidelity simulation environments for testing robot behaviors before real-world deployment.',
      link: '/docs/digital-twin/intro',
      chapters: 5,
    },
    {
      title: 'Module 3: The AI-Robot Brain',
      subtitle: 'NVIDIA Isaac',
      description: 'Implement perception, navigation, and edge inference using NVIDIA Isaac ROS and Jetson platforms.',
      link: '/docs/ai-robot-brain/intro',
      chapters: 4,
    },
    {
      title: 'Module 4: Vision-Language-Action',
      subtitle: 'VLA',
      description: 'Integrate voice commands, LLM reasoning, and robotic actions for natural human-robot interaction.',
      link: '/docs/vla/intro',
      chapters: 5,
    },
  ];

  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <Heading as="h2" className={styles.modulesHeading}>
          Course Modules
        </Heading>
        <div className={styles.moduleGrid}>
          {modules.map((module, idx) => (
            <Link key={idx} to={module.link} className={styles.moduleCard}>
              <div className={styles.moduleCardHeader}>
                <span className={styles.moduleNumber}>Module {idx + 1}</span>
                <span className={styles.chapterCount}>{module.chapters} chapters</span>
              </div>
              <h3 className={styles.moduleCardTitle}>{module.subtitle}</h3>
              <p className={styles.moduleCardDescription}>{module.description}</p>
            </Link>
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
      <HomepageHeader />
      <main>
        <ModuleCards />
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
