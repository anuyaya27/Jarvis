import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="home-page">
      <div className="hero">
        <h1 className="hero-title">Multiverse Copilot</h1>
        <p className="hero-subtitle">
          Voice-driven parallel reality decision engine for high-stakes business strategy
        </p>
        <p className="hero-description text-secondary">
          Simulate strategic decisions across multiple parallel realities, powered by Amazon Nova.
          Get executive summaries, risk analysis, and stability scores for each potential outcome.
        </p>
        <div className="hero-actions">
          <Link href="/voice" className="btn btn-primary btn-lg">
            Launch Voice Console
          </Link>
          <Link href="/kb" className="btn btn-secondary btn-lg">
            Knowledge Base
          </Link>
        </div>
      </div>

      <div className="features">
        <div className="feature-card card">
          <div className="feature-icon">🎤</div>
          <h3 className="feature-title">Voice-First Interface</h3>
          <p className="feature-description text-sm text-secondary">
            Speak your strategic decisions naturally and get instant simulations
          </p>
        </div>
        <div className="feature-card card">
          <div className="feature-icon">🌐</div>
          <h3 className="feature-title">Parallel Reality Engine</h3>
          <p className="feature-description text-sm text-secondary">
            Explore up to 6 different strategic branches with detailed outcomes
          </p>
        </div>
        <div className="feature-card card">
          <div className="feature-icon">📊</div>
          <h3 className="feature-title">Executive Analytics</h3>
          <p className="feature-description text-sm text-secondary">
            Get stability scores, risk assessments, and KPI projections
          </p>
        </div>
      </div>
    </div>
  );
}
