import type { ReactNode } from 'react';
import styles from './styles.module.css';

interface TimelineBarProps {
  weekStart: number;
  weekEnd: number;
  totalWeeks?: number;
  accentColor: string;
  label?: string;
}

export default function TimelineBar({
  weekStart,
  weekEnd,
  totalWeeks = 13,
  accentColor,
  label,
}: TimelineBarProps): ReactNode {
  // Calculate position and width as percentages
  const startPercent = ((weekStart - 1) / totalWeeks) * 100;
  const widthPercent = ((weekEnd - weekStart + 1) / totalWeeks) * 100;

  const ariaLabel = `Module spans weeks ${weekStart} to ${weekEnd} of ${totalWeeks}`;

  return (
    <div className={styles.timelineContainer}>
      {label && <span className={styles.timelineLabel}>{label}</span>}
      <div
        className={styles.timelineTrack}
        role="progressbar"
        aria-valuenow={weekEnd}
        aria-valuemin={1}
        aria-valuemax={totalWeeks}
        aria-label={ariaLabel}
      >
        <div
          className={styles.timelineFill}
          style={{
            left: `${startPercent}%`,
            width: `${widthPercent}%`,
            backgroundColor: `var(${accentColor})`,
          }}
        />
      </div>
    </div>
  );
}
