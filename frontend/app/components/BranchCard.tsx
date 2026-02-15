'use client';

import { useState } from 'react';
import StabilityMeter from './StabilityMeter';
import RiskChip from './RiskChip';

interface BranchCardProps {
  branch: any;
}

export default function BranchCard({ branch }: BranchCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const topRisks = branch.risk_clusters?.slice(0, 2) || [];
  const topEvents = branch.key_events?.slice(0, 2) || [];
  const topFailure = branch.failure_triggers?.[0];
  const topMitigation = branch.mitigations?.[0];

  return (
    <div className="branch-card card">
      <div className="branch-header">
        <h3 className="branch-name">{branch.branch_name}</h3>
        <div className="branch-score">
          <StabilityMeter score={branch.final_stability_score || 0} size="sm" />
        </div>
      </div>

      <div className="branch-summary">
        {topRisks.length > 0 && (
          <div className="branch-section">
            <p className="section-label text-sm text-secondary">Top Risks</p>
            <div className="risk-chips">
              {topRisks.map((risk: any, idx: number) => (
                <RiskChip
                  key={idx}
                  tag={risk.tag}
                  severity={risk.severity}
                  severityLevel={risk.severity_level}
                />
              ))}
            </div>
          </div>
        )}

        {topEvents.length > 0 && (
          <div className="branch-section">
            <p className="section-label text-sm text-secondary">Key Events</p>
            <ul className="event-list">
              {topEvents.map((event: string, idx: number) => (
                <li key={idx} className="text-sm">{event}</li>
              ))}
            </ul>
          </div>
        )}

        {topFailure && (
          <div className="branch-section">
            <p className="section-label text-sm text-secondary">Failure Trigger</p>
            <p className="text-sm text-danger">{topFailure}</p>
          </div>
        )}

        {topMitigation && (
          <div className="branch-section">
            <p className="section-label text-sm text-secondary">Mitigation</p>
            <p className="text-sm text-success">{topMitigation}</p>
          </div>
        )}
      </div>

      <button
        className="expand-btn btn-secondary btn-sm"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {isExpanded ? '▲ Hide Details' : '▼ View Details'}
      </button>

      {isExpanded && (
        <div className="branch-details">
          {branch.narrative && (
            <div className="detail-section">
              <h4 className="detail-title">Narrative</h4>
              <p className="text-sm text-secondary">{branch.narrative}</p>
            </div>
          )}

          {branch.KPIs && (
            <div className="detail-section">
              <h4 className="detail-title">KPIs</h4>
              <div className="kpi-grid">
                {Object.entries(branch.KPIs).map(([key, value]) => (
                  <div key={key} className="kpi-item">
                    <span className="kpi-label text-xs text-tertiary">{key}</span>
                    <span className="kpi-value text-sm font-semibold">{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {branch.stress_points && branch.stress_points.length > 0 && (
            <div className="detail-section">
              <h4 className="detail-title">Stress Points</h4>
              <ul className="detail-list">
                {branch.stress_points.map((point: string, idx: number) => (
                  <li key={idx} className="text-sm">{point}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .branch-card {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .branch-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 1rem;
        }
        
        .branch-name {
          font-size: 1.125rem;
          font-weight: 600;
          flex: 1;
        }
        
        .branch-score {
          flex-shrink: 0;
        }
        
        .branch-summary {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        
        .branch-section {
          display: flex;
          flex-direction: column;
          gap: 0.375rem;
        }
        
        .section-label {
          font-weight: 500;
          margin-bottom: 0.125rem;
        }
        
        .risk-chips {
          display: flex;
          flex-wrap: wrap;
          gap: 0.375rem;
        }
        
        .event-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }
        
        .event-list li {
          padding-left: 1rem;
          position: relative;
        }
        
        .event-list li::before {
          content: '•';
          position: absolute;
          left: 0;
          color: var(--color-accent);
        }
        
        .expand-btn {
          width: 100%;
          margin-top: 0.5rem;
        }
        
        .branch-details {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          padding-top: 1rem;
          border-top: 1px solid var(--color-border-light);
        }
        
        .detail-section {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .detail-title {
          font-size: 0.875rem;
          font-weight: 600;
          color: var(--color-text-primary);
        }
        
        .kpi-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
          gap: 0.75rem;
        }
        
        .kpi-item {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          padding: 0.5rem;
          background: var(--color-bg-secondary);
          border-radius: var(--radius-sm);
        }
        
        .detail-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 0.375rem;
        }
        
        .detail-list li {
          padding-left: 1rem;
          position: relative;
        }
        
        .detail-list li::before {
          content: '→';
          position: absolute;
          left: 0;
          color: var(--color-accent);
        }
      `}</style>
    </div>
  );
}
