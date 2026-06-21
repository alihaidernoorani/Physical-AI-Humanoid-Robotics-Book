import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import TimelineBar from '@site/src/components/TimelineBar';
import styles from './styles.module.css';

interface ModuleCardProps {
  moduleNumber: 1 | 2 | 3 | 4;
  title: string;
  subtitle: string;
  description: string;
  weekStart: number;
  weekEnd: number;
  link: string;
  accentColor: string;
}

export default function ModuleCard({
  moduleNumber,
  title,
  subtitle,
  description,
  weekStart,
  weekEnd,
  link,
  accentColor,
}: ModuleCardProps): ReactNode {
  const durationWeeks = weekEnd - weekStart + 1;
  const ariaLabel = `${title} - ${subtitle} - Weeks ${weekStart} to ${weekEnd}`;

  return (
    <Link
      to={link}
      className={styles.moduleCard}
      aria-label={ariaLabel}
      style={{
        borderLeftColor: `var(${accentColor})`,
      }}
    >
      <div className={styles.moduleCardHeader}>
        <span className={styles.moduleNumber}>Module {moduleNumber}</span>
        <span className={styles.durationBadge}>{durationWeeks} {durationWeeks === 1 ? 'week' : 'weeks'}</span>
      </div>
      <h3 className={styles.moduleCardTitle}>{subtitle}</h3>
      <p className={styles.moduleCardSubtitle}>{title}</p>
      <p className={styles.moduleCardDescription}>{description}</p>
      <TimelineBar
        weekStart={weekStart}
        weekEnd={weekEnd}
        totalWeeks={13}
        accentColor={accentColor}
        label={`Weeks ${weekStart}–${weekEnd}`}
      />
    </Link>
  );
}
