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
        <div className={styles.buttons}>
          <div className={styles.moduleButtons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/ros2-nervous-system/intro">
              Module 1: The Robotic Nervous System (ROS 2)
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="/docs/digital-twin/intro">
              Module 2: The Digital Twin (Gazebo & Unity)
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="/docs/ai-robot-brain/intro">
              Module 3: The AI-Robot Brain (NVIDIA Isaac™)
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="/docs/vla/intro">
              Module 4: Vision-Language-Action (VLA)
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
