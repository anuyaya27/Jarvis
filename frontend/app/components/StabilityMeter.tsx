interface StabilityMeterProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
}

export default function StabilityMeter({ score, size = 'md' }: StabilityMeterProps) {
  const getColor = (score: number) => {
    if (score >= 70) return 'success';
    if (score >= 50) return 'warning';
    return 'danger';
  };

  const sizes = {
    sm: { fontSize: '1.5rem', barHeight: '0.375rem' },
    md: { fontSize: '2.5rem', barHeight: '0.5rem' },
    lg: { fontSize: '3.5rem', barHeight: '0.75rem' },
  };

  const color = getColor(score);
  const currentSize = sizes[size];

  return (
    <div className="stability-meter">
      <div className="score-display" style={{ fontSize: currentSize.fontSize }}>
        <span className={`score-value text-${color}`}>{Math.round(score)}</span>
        <span className="score-max text-tertiary">/100</span>
      </div>
      <div className="progress" style={{ height: currentSize.barHeight }}>
        <div
          className={`progress-bar ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <style jsx>{`
        .stability-meter {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .score-display {
          font-weight: 700;
          line-height: 1;
        }
        
        .score-max {
          font-size: 0.6em;
          margin-left: 0.25rem;
        }
      `}</style>
    </div>
  );
}
