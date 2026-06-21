import type { ReactNode } from 'react';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

interface HeroSectionProps {
  title: string;
  tagline: string;
  description: string;
}

export default function HeroSection({ title, tagline, description }: HeroSectionProps): ReactNode {
  return (
    <header className={styles.hero} role="banner">
      <div className={styles.heroContainer}>
        <Heading as="h1" className={styles.heroTitle}>
          {title}
        </Heading>
        <p className={styles.heroTagline}>{tagline}</p>
        <p className={styles.heroDescription}>{description}</p>
      </div>
    </header>
  );
}
