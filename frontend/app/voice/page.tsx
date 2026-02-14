'use client';

import { useState, useRef, useEffect } from 'react';
import StabilityMeter from '../components/StabilityMeter';
import RiskChip from '../components/RiskChip';
import BranchCard from '../components/BranchCard';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

interface SimulationResult {
  executive_summary?: string;
  recommended_path?: string;
  top_3_risks?: any[];
  branches?: any[];
  audit?: any;
}

export default function VoicePage() {
  const [isListening, setIsListening] = useState(false);
  const [micEnabled, setMicEnabled] = useState(true);
  const [transcript, setTranscript] = useState('');
  const [isSimulating, setIsSimulating] = useState(false);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showDebug, setShowDebug] = useState(false);

  const recognitionRef = useRef<any>(null);

  // Initialize Web Speech API
  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onresult = (event: any) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcriptPiece = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcriptPiece + ' ';
          } else {
            interimTranscript += transcriptPiece;
          }
        }

        setTranscript((prev) => prev + finalTranscript);
      };

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleListening = () => {
    if (!micEnabled) {
      alert('Sonic streaming not implemented yet. Using Web Speech API (mic toggle ON).');
      return;
    }

    if (!recognitionRef.current) {
      alert('Speech recognition not supported in this browser.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const handleSimulate = async () => {
    if (!transcript.trim()) {
      setError('Please provide a decision to simulate.');
      return;
    }

    setIsSimulating(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decision_text: transcript }),
      });

      if (!response.ok) {
        throw new Error(`Simulation failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred during simulation.');
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setTranscript('');
    setResult(null);
    setError(null);
    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  return (
    <div className="voice-page">
      <div className="page-header">
        <h1>Voice Console</h1>
        <p className="text-secondary">
          Speak or type your strategic decision to simulate parallel realities
        </p>
      </div>

      <div className="console-layout">
        {/* Command Bar */}
        <div className="command-bar card">
          <div className="command-header">
            <h3 className="card-title">Command Input</h3>
            <div className="mic-toggle">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={micEnabled}
                  onChange={(e) => setMicEnabled(e.target.checked)}
                />
                <span className="text-sm">Mic {micEnabled ? 'ON' : 'OFF'}</span>
              </label>
            </div>
          </div>

          <div className="input-area">
            <textarea
              className="input command-input"
              placeholder="e.g., Simulate acquiring Competitor X under a recession next quarter..."
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              rows={4}
              disabled={isSimulating}
            />
            <div className="input-controls">
              <button
                className={`btn btn-sm ${isListening ? 'btn-danger' : 'btn-secondary'}`}
                onClick={toggleListening}
                disabled={isSimulating}
              >
                {isListening ? '⏸ Stop' : '🎤 Start'}
              </button>
              {transcript && (
                <span className="text-xs text-tertiary">
                  {transcript.length} characters
                </span>
              )}
            </div>
          </div>

          <div className="action-buttons">
            <button
              className="btn btn-primary btn-lg"
              onClick={handleSimulate}
              disabled={isSimulating || !transcript.trim()}
            >
              {isSimulating ? 'Simulating...' : '▶ Simulate'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleReset}
              disabled={isSimulating}
            >
              Reset
            </button>
          </div>
        </div>

        {/* Results Dashboard */}
        {(isSimulating || result || error) && (
          <div className="dashboard">
            {error && (
              <div className="alert alert-error">
                <strong>Error:</strong> {error}
                <button className="btn btn-sm btn-secondary" onClick={handleSimulate}>
                  Retry
                </button>
              </div>
            )}

            {isSimulating && (
              <div className="loading-state">
                <div className="card">
                  <div className="skeleton skeleton-title" />
                  <div className="skeleton skeleton-text" />
                  <div className="skeleton skeleton-text" style={{ width: '80%' }} />
                </div>
                <div className="card">
                  <div className="skeleton skeleton-title" />
                  <div className="skeleton skeleton-text" />
                  <div className="skeleton skeleton-text" />
                </div>
                <div className="grid-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="card">
                      <div className="skeleton skeleton-title" />
                      <div className="skeleton skeleton-text" />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result && !isSimulating && (
              <>
                {/* Executive Summary */}
                {result.executive_summary && (
                  <div className="card summary-card">
                    <div className="card-header">
                      <h3 className="card-title">Executive Summary</h3>
                    </div>
                    <p className="card-body">{result.executive_summary}</p>
                  </div>
                )}

                {/* Recommended Path */}
                {result.recommended_path && (
                  <div className="card recommended-card">
                    <div className="card-header">
                      <h3 className="card-title">Recommended Path</h3>
                      <span className="badge badge-success">Best Choice</span>
                    </div>
                    <p className="card-body font-semibold">{result.recommended_path}</p>
                  </div>
                )}

                {/* Stability Overview */}
                {result.branches && result.branches.length > 0 && (
                  <div className="card stability-card">
                    <div className="card-header">
                      <h3 className="card-title">Stability Overview</h3>
                    </div>
                    <div className="stability-content">
                      <div className="stability-main">
                        <p className="text-sm text-secondary mb-2">Overall Stability Score</p>
                        <StabilityMeter
                          score={
                            result.branches.reduce(
                              (acc, b) => acc + (b.final_stability_score || 0),
                              0
                            ) / result.branches.length
                          }
                          size="lg"
                        />
                      </div>
                      <div className="branch-scores">
                        <p className="text-sm text-secondary mb-2">Branch Distribution</p>
                        {result.branches.map((branch, idx) => (
                          <div key={idx} className="branch-score-item">
                            <span className="text-sm truncate">{branch.branch_name}</span>
                            <span className="text-sm font-semibold">
                              {Math.round(branch.final_stability_score || 0)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Top Risks */}
                {result.top_3_risks && result.top_3_risks.length > 0 && (
                  <div className="card risks-card">
                    <div className="card-header">
                      <h3 className="card-title">Top Risks</h3>
                    </div>
                    <div className="risk-chips">
                      {result.top_3_risks.map((risk, idx) => (
                        <RiskChip
                          key={idx}
                          tag={risk.tag || risk}
                          severity={risk.severity}
                          severityLevel={risk.severity_level}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Branches Grid */}
                {result.branches && result.branches.length > 0 && (
                  <div className="branches-section">
                    <h2 className="section-title">Simulation Branches</h2>
                    <div className="branches-grid">
                      {result.branches.map((branch, idx) => (
                        <BranchCard key={idx} branch={branch} />
                      ))}
                    </div>
                  </div>
                )}

                {/* Debug JSON */}
                <div className="debug-section">
                  <button
                    className="btn btn-sm btn-secondary"
                    onClick={() => setShowDebug(!showDebug)}
                  >
                    {showDebug ? '▲ Hide' : '▼ View'} Raw JSON
                  </button>
                  {showDebug && (
                    <pre className="debug-json">
                      {JSON.stringify(result, null, 2)}
                    </pre>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>

      <style jsx>{`
        .voice-page {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        
        .page-header {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .console-layout {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        
        .command-bar {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .command-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        
        .mic-toggle {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .toggle-label {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          cursor: pointer;
        }
        
        .input-area {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .command-input {
          resize: vertical;
          font-family: inherit;
        }
        
        .input-controls {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        
        .action-buttons {
          display: flex;
          gap: 0.75rem;
          padding-top: 0.5rem;
        }
        
        .btn-danger {
          background: var(--color-danger);
          color: white;
        }
        
        .btn-danger:hover:not(:disabled) {
          background: #dc2626;
        }
        
        .dashboard {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        
        .loading-state {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        
        .grid-2 {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 1rem;
        }
        
        .summary-card,
        .recommended-card {
          border-left: 4px solid var(--color-accent);
        }
        
        .stability-card {
          border-left: 4px solid var(--color-success);
        }
        
        .stability-content {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
        }
        
        .branch-scores {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .branch-score-item {
          display: flex;
          justify-content: space-between;
          padding: 0.5rem;
          background: var(--color-bg-secondary);
          border-radius: var(--radius-sm);
          gap: 0.5rem;
        }
        
        .risks-card {
          border-left: 4px solid var(--color-warning);
        }
        
        .branches-section {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .section-title {
          font-size: 1.5rem;
          font-weight: 600;
          margin-top: 1rem;
        }
        
        .branches-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 1.5rem;
        }
        
        .debug-section {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-top: 1rem;
        }
        
        .debug-json {
          background: var(--color-bg-secondary);
          padding: 1rem;
          border-radius: var(--radius-md);
          overflow-x: auto;
          font-size: 0.75rem;
          line-height: 1.5;
          max-height: 400px;
          overflow-y: auto;
        }
        
        @media (max-width: 768px) {
          .stability-content {
            grid-template-columns: 1fr;
          }
          
          .branches-grid {
            grid-template-columns: 1fr;
          }
          
          .action-buttons {
            flex-direction: column;
          }
          
          .action-buttons button {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
}
