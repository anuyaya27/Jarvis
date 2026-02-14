"use client";

import { useMemo, useRef, useState } from "react";

const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function VoicePage() {
  const [useBrowserMic, setUseBrowserMic] = useState(true);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [result, setResult] = useState<any | null>(null);
  const [showJson, setShowJson] = useState(false);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const recognitionRef = useRef<any>(null);

  const speechSupported = useMemo(() => {
    if (typeof window === "undefined") return false;
    return Boolean((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition);
  }, []);

  function startListening() {
    setError("");
    if (!speechSupported) {
      setError("Web Speech API is not supported in this browser.");
      return;
    }
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-US";
    recognition.onstart = () => setListening(true);
    recognition.onresult = (event: any) => {
      const merged = Array.from(event.results)
        .map((r: any) => r[0]?.transcript || "")
        .join(" ")
        .trim();
      setTranscript(merged);
    };
    recognition.onerror = (event: any) => {
      setError(`Mic error: ${event.error || "unknown"}`);
    };
    recognition.onend = () => {
      setListening(false);
      recognitionRef.current = null;
    };
    recognitionRef.current = recognition;
    recognition.start();
  }

  function stopListening() {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
    setListening(false);
  }

  async function runSimulation() {
    setRunning(true);
    setError("");
    const resp = await fetch(`${backend}/simulate`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        transcript,
        constraints: { scenario_horizon: "next_quarter", branch_count_hint: 5 }
      })
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      setError(err?.error?.message || "Failed to run simulation.");
      setRunning(false);
      return;
    }
    const data = await resp.json();
    setResult(data || null);
    setRunning(false);
  }

  function scorePercent(value: number | undefined | null): number {
    const n = Number(value ?? 0);
    return Math.max(0, Math.min(100, n));
  }

  return (
    <div className="row">
      <div className="card" style={{ flex: 1, minWidth: 300 }}>
        <h2>Voice Console</h2>
        <label style={{ display: "block", marginBottom: 12 }}>
          <input
            type="checkbox"
            checked={useBrowserMic}
            onChange={(e) => {
              setUseBrowserMic(e.target.checked);
              setListening(false);
              setError("");
            }}
          />{" "}
          Use Browser Mic (Web Speech)
        </label>

        {!useBrowserMic && (
          <p>Sonic streaming not implemented yet. Enable Browser Mic for demo mode.</p>
        )}

        <div className="row">
          <button onClick={startListening} disabled={!useBrowserMic || listening}>Start Mic</button>
          <button onClick={stopListening} disabled={!useBrowserMic || !listening}>Stop Mic</button>
        </div>
        {error && <p style={{ color: "#b00020" }}>{error}</p>}
        <textarea rows={5} value={transcript} onChange={(e) => setTranscript(e.target.value)} />
        <div style={{ marginTop: 12 }}>
          <button onClick={runSimulation} disabled={!transcript || running}>
            {running ? "Running..." : "Run Simulation"}
          </button>
        </div>
      </div>
      <div className="card" style={{ flex: 1, minWidth: 300 }}>
        <h2>Simulation Dashboard</h2>
        {!result && <p>No result yet.</p>}
        {result && (
          <>
            <h3>Executive Summary</h3>
            <p>{result.executive_summary || "No executive summary returned."}</p>

            <h3>Recommended Path</h3>
            <p>
              <b>{result.recommended_path?.branch_name || "N/A"}:</b>{" "}
              {result.recommended_path?.reasoning || result.overall_recommendation}
            </p>

            <h3>Branches</h3>
            <div className="row">
              {(result.branches || []).map((branch: any) => (
                <div key={branch.branch_name} className="card" style={{ minWidth: 220, flex: 1 }}>
                  <div><b>{branch.branch_name}</b></div>
                  <div style={{ margin: "8px 0" }}>
                    Final Stability: {branch.final_stability_score ?? branch.stability_score ?? 0}
                  </div>
                  <div style={{ background: "#e5edf3", borderRadius: 8, height: 10, overflow: "hidden" }}>
                    <div
                      style={{
                        width: `${scorePercent(branch.final_stability_score ?? branch.stability_score)}%`,
                        background: "#0a6e4f",
                        height: "100%"
                      }}
                    />
                  </div>
                  <div style={{ marginTop: 8 }}>
                    {(branch.risk_clusters || []).slice(0, 3).map((risk: any, i: number) => (
                      <span
                        key={`${risk.tag}-${i}`}
                        style={{
                          display: "inline-block",
                          marginRight: 6,
                          marginBottom: 6,
                          padding: "2px 8px",
                          borderRadius: 999,
                          background: "#eef4ef",
                          fontSize: 12
                        }}
                      >
                        {risk.tag}:{risk.severity}
                      </span>
                    ))}
                  </div>
                  <ul>
                    {(branch.key_events || []).slice(0, 2).map((event: string, i: number) => (
                      <li key={i}>{event}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 10 }}>
              <label>
                <input type="checkbox" checked={showJson} onChange={(e) => setShowJson(e.target.checked)} /> Show JSON
              </label>
            </div>
            {showJson && <pre>{JSON.stringify(result, null, 2)}</pre>}
          </>
        )}
      </div>
    </div>
  );
}
