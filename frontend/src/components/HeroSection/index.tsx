import type { ReactNode } from 'react';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

interface HeroSectionProps {
  title: string;
  tagline: string;
  description: string;
}

function AIGraphic(): ReactNode {
  return (
    <div className={styles.heroGraphic} aria-hidden="true">
      <svg viewBox="0 0 280 340" xmlns="http://www.w3.org/2000/svg" className={styles.aiSvg}>
        {/* Outer ambient rings */}
        <circle cx="140" cy="120" r="105" fill="none" stroke="rgba(56,189,248,0.08)" strokeWidth="1.5" />
        <circle cx="140" cy="120" r="88" fill="none" stroke="rgba(56,189,248,0.12)" strokeWidth="1" />

        {/* Neural network connections (behind nodes) */}
        {/* Input to hidden1 */}
        <line x1="50" y1="65" x2="105" y2="55" stroke="rgba(56,189,248,0.3)" strokeWidth="1"/>
        <line x1="50" y1="65" x2="105" y2="95" stroke="rgba(56,189,248,0.3)" strokeWidth="1"/>
        <line x1="50" y1="105" x2="105" y2="55" stroke="rgba(56,189,248,0.2)" strokeWidth="1"/>
        <line x1="50" y1="105" x2="105" y2="95" stroke="rgba(56,189,248,0.3)" strokeWidth="1"/>
        <line x1="50" y1="105" x2="105" y2="135" stroke="rgba(56,189,248,0.2)" strokeWidth="1"/>
        <line x1="50" y1="145" x2="105" y2="95" stroke="rgba(56,189,248,0.2)" strokeWidth="1"/>
        <line x1="50" y1="145" x2="105" y2="135" stroke="rgba(56,189,248,0.3)" strokeWidth="1"/>
        <line x1="50" y1="145" x2="105" y2="175" stroke="rgba(56,189,248,0.2)" strokeWidth="1"/>
        {/* Hidden1 to hidden2 */}
        <line x1="105" y1="55" x2="175" y2="70" stroke="rgba(129,140,248,0.35)" strokeWidth="1"/>
        <line x1="105" y1="55" x2="175" y2="120" stroke="rgba(129,140,248,0.2)" strokeWidth="1"/>
        <line x1="105" y1="95" x2="175" y2="70" stroke="rgba(129,140,248,0.3)" strokeWidth="1"/>
        <line x1="105" y1="95" x2="175" y2="120" stroke="rgba(129,140,248,0.35)" strokeWidth="1"/>
        <line x1="105" y1="135" x2="175" y2="120" stroke="rgba(129,140,248,0.3)" strokeWidth="1"/>
        <line x1="105" y1="135" x2="175" y2="170" stroke="rgba(129,140,248,0.3)" strokeWidth="1"/>
        <line x1="105" y1="175" x2="175" y2="120" stroke="rgba(129,140,248,0.2)" strokeWidth="1"/>
        <line x1="105" y1="175" x2="175" y2="170" stroke="rgba(129,140,248,0.35)" strokeWidth="1"/>
        {/* Hidden2 to output */}
        <line x1="175" y1="70" x2="230" y2="100" stroke="rgba(52,211,153,0.4)" strokeWidth="1.5"/>
        <line x1="175" y1="120" x2="230" y2="100" stroke="rgba(52,211,153,0.45)" strokeWidth="1.5"/>
        <line x1="175" y1="170" x2="230" y2="140" stroke="rgba(52,211,153,0.35)" strokeWidth="1.5"/>
        <line x1="175" y1="120" x2="230" y2="140" stroke="rgba(52,211,153,0.4)" strokeWidth="1.5"/>

        {/* Input layer nodes */}
        <circle cx="50" cy="65" r="6" fill="#38bdf8" className={styles.nodeA} />
        <circle cx="50" cy="105" r="6" fill="#38bdf8" className={styles.nodeB} />
        <circle cx="50" cy="145" r="6" fill="#38bdf8" className={styles.nodeA} />

        {/* Hidden layer 1 nodes */}
        <circle cx="105" cy="55" r="6" fill="#818cf8" className={styles.nodeB} />
        <circle cx="105" cy="95" r="6" fill="#818cf8" className={styles.nodeA} />
        <circle cx="105" cy="135" r="6" fill="#818cf8" className={styles.nodeB} />
        <circle cx="105" cy="175" r="6" fill="#818cf8" className={styles.nodeA} />

        {/* Hidden layer 2 nodes */}
        <circle cx="175" cy="70" r="6" fill="#a78bfa" className={styles.nodeA} />
        <circle cx="175" cy="120" r="6" fill="#a78bfa" className={styles.nodeB} />
        <circle cx="175" cy="170" r="6" fill="#a78bfa" className={styles.nodeA} />

        {/* Output nodes */}
        <circle cx="230" cy="100" r="8" fill="#34d399" className={styles.nodeB} />
        <circle cx="230" cy="140" r="8" fill="#34d399" className={styles.nodeA} />

        {/* Lines from neural net down to robot head */}
        <line x1="140" y1="196" x2="140" y2="178" stroke="rgba(56,189,248,0.5)" strokeWidth="1.5" strokeDasharray="4 3"/>
        <line x1="120" y1="196" x2="105" y2="175" stroke="rgba(129,140,248,0.35)" strokeWidth="1" strokeDasharray="3 4"/>
        <line x1="160" y1="196" x2="175" y2="170" stroke="rgba(167,139,250,0.35)" strokeWidth="1" strokeDasharray="3 4"/>

        {/* Robot body - ear panels */}
        <rect x="96" y="210" width="11" height="26" rx="4" fill="#1e40af"/>
        <rect x="173" y="210" width="11" height="26" rx="4" fill="#1e40af"/>
        <circle cx="101.5" cy="217" r="2.5" fill="#38bdf8"/>
        <circle cx="101.5" cy="228" r="2.5" fill="#38bdf8"/>
        <circle cx="178.5" cy="217" r="2.5" fill="#38bdf8"/>
        <circle cx="178.5" cy="228" r="2.5" fill="#38bdf8"/>

        {/* Robot head */}
        <rect x="107" y="196" width="66" height="55" rx="10" fill="#1e40af"/>

        {/* Antenna */}
        <rect x="136" y="180" width="8" height="18" rx="4" fill="#1e40af"/>
        <circle cx="140" cy="177" r="7" fill="none" stroke="#38bdf8" strokeWidth="1.5" opacity="0.5"/>
        <circle cx="140" cy="177" r="5" fill="#38bdf8" className={styles.antennaPulse}/>
        <circle cx="140" cy="177" r="2.5" fill="#ffffff" opacity="0.9"/>

        {/* Left eye */}
        <rect x="113" y="210" width="20" height="13" rx="4" fill="#0f172a"/>
        <rect x="115" y="212" width="16" height="9" rx="2.5" fill="#00d4ff" className={styles.eyeGlow}/>
        <rect x="118" y="214" width="10" height="5" rx="1.5" fill="#a5f3fc" opacity="0.6"/>

        {/* Right eye */}
        <rect x="147" y="210" width="20" height="13" rx="4" fill="#0f172a"/>
        <rect x="149" y="212" width="16" height="9" rx="2.5" fill="#00d4ff" className={styles.eyeGlow}/>
        <rect x="152" y="214" width="10" height="5" rx="1.5" fill="#a5f3fc" opacity="0.6"/>

        {/* Mouth grill */}
        <rect x="117" y="233" width="46" height="10" rx="4" fill="#0f172a"/>
        <rect x="121" y="236" width="7" height="4" rx="1.5" fill="#38bdf8"/>
        <rect x="132" y="236" width="7" height="4" rx="1.5" fill="#38bdf8"/>
        <rect x="143" y="236" width="7" height="4" rx="1.5" fill="#38bdf8"/>
        <rect x="154" y="236" width="5" height="4" rx="1.5" fill="#38bdf8" opacity="0.5"/>

        {/* Neck */}
        <rect x="128" y="251" width="24" height="12" rx="3" fill="#1e40af"/>

        {/* Shoulders / chest */}
        <rect x="90" y="263" width="100" height="45" rx="14" fill="#1d3461"/>
        <rect x="80" y="258" width="24" height="38" rx="8" fill="#1e40af"/>
        <rect x="176" y="258" width="24" height="38" rx="8" fill="#1e40af"/>

        {/* Chest panel */}
        <rect x="110" y="272" width="60" height="28" rx="6" fill="#0f172a"/>
        <circle cx="125" cy="282" r="5" fill="#38bdf8" opacity="0.8" className={styles.nodeA}/>
        <circle cx="140" cy="278" r="5" fill="#818cf8" opacity="0.8" className={styles.nodeB}/>
        <circle cx="155" cy="282" r="5" fill="#34d399" opacity="0.8" className={styles.nodeA}/>
        <line x1="125" y1="282" x2="140" y2="278" stroke="rgba(56,189,248,0.5)" strokeWidth="1"/>
        <line x1="140" y1="278" x2="155" y2="282" stroke="rgba(52,211,153,0.5)" strokeWidth="1"/>

        {/* Floating data particles */}
        <circle cx="60" cy="30" r="2" fill="#38bdf8" opacity="0.5" className={styles.floatA}/>
        <circle cx="220" cy="55" r="2" fill="#a78bfa" opacity="0.5" className={styles.floatB}/>
        <circle cx="30" cy="160" r="2" fill="#34d399" opacity="0.4" className={styles.floatA}/>
        <circle cx="255" cy="200" r="2" fill="#38bdf8" opacity="0.4" className={styles.floatB}/>
      </svg>
    </div>
  );
}

export default function HeroSection({ title, tagline, description }: HeroSectionProps): ReactNode {
  return (
    <header className={styles.hero} role="banner">
      <div className={styles.heroContainer}>
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <Heading as="h1" className={styles.heroTitle}>
              {title}
            </Heading>
            <p className={styles.heroTagline}>{tagline}</p>
            <p className={styles.heroDescription}>{description}</p>
          </div>
          <AIGraphic />
        </div>
      </div>
    </header>
  );
}
