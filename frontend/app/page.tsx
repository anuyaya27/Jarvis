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

      <style jsx>{`
        .home-page {
          display: flex;
          flex-direction: column;
          gap: 4rem;
          padding: 2rem 0;
        }
        
        .hero {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          gap: 1.5rem;
          max-width: 800px;
          margin: 0 auto;
          padding: 3rem 1rem;
        }
        
        .hero-title {
          font-size: 3rem;
          font-weight: 700;
          background: linear-gradient(135deg, var(--color-accent), var(--color-success));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        
        .hero-subtitle {
          font-size: 1.25rem;
          color: var(--color-text-secondary);
          font-weight: 500;
        }
        
        .hero-description {
          font-size: 1rem;
          line-height: 1.6;
        }
        
        .hero-actions {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
        }
        
        .features {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 2rem;
        }
        
        .feature-card {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          gap: 1rem;
          padding: 2rem;
        }
        
        .feature-icon {
          font-size: 3rem;
        }
        
        .feature-title {
          font-size: 1.25rem;
          font-weight: 600;
        }
        
        .feature-description {
          line-height: 1.6;
        }
        
        @media (max-width: 768px) {
          .hero-title {
            font-size: 2rem;
          }
          
          .hero-subtitle {
            font-size: 1rem;
          }
          
          .hero-actions {
            flex-direction: column;
            width: 100%;
          }
          
          .hero-actions .btn {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
}
