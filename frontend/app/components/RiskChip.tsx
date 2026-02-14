interface RiskChipProps {
  tag: string;
  severity?: string;
  severityLevel?: number;
}

export default function RiskChip({ tag, severity, severityLevel }: RiskChipProps) {
  const getVariant = () => {
    if (severityLevel !== undefined) {
      if (severityLevel >= 8) return 'danger';
      if (severityLevel >= 5) return 'warning';
      return 'info';
    }
    if (severity) {
      const s = severity.toLowerCase();
      if (s.includes('high') || s.includes('critical')) return 'danger';
      if (s.includes('medium') || s.includes('moderate')) return 'warning';
      return 'info';
    }
    return 'info';
  };

  const variant = getVariant();

  return (
    <span className={`badge badge-${variant}`}>
      {tag}
      {severityLevel !== undefined && ` (${severityLevel}/10)`}
    </span>
  );
}
