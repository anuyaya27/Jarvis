"use client";

import { useState } from "react";

const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function VoicePage() {
  const [sessionId, setSessionId] = useState("");
  const [transcript, setTranscript] = useState("");
  const [result, setResult] = useState("");
  const [running, setRunning] = useState(false);

  async function startSession() {
    const resp = await fetch(`${backend}/voice/session`, { method: "POST" });
    const data = await resp.json();
    setSessionId(data.session_id);
  }

  async function sendMockVoiceChunk() {
    if (!sessionId) return;
    const ws = new WebSocket(`${backend.replace("http", "ws")}/voice/stream/${sessionId}`);
    ws.onopen = () => {
      ws.send(JSON.stringify({ audio_base64: btoa("fake-audio") }));
    };
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      setTranscript(d.final_transcript || d.partial_transcript || "");
      ws.close();
    };
  }

  async function runSimulation() {
    setRunning(true);
    const resp = await fetch(`${backend}/simulate`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        transcript,
        constraints: { scenario_horizon: "next_quarter", branch_count_hint: 5 }
      })
    });
    const data = await resp.json();
    setResult(JSON.stringify(data, null, 2));
    setRunning(false);
  }

  return (
    <div className="row">
      <div className="card" style={{ flex: 1, minWidth: 300 }}>
        <h2>Voice Console</h2>
        <div className="row">
          <button onClick={startSession}>Create Voice Session</button>
          <button onClick={sendMockVoiceChunk} disabled={!sessionId}>Push-to-Talk (Mock)</button>
        </div>
        <p><b>Session:</b> {sessionId || "not created"}</p>
        <textarea rows={5} value={transcript} onChange={(e) => setTranscript(e.target.value)} />
        <div style={{ marginTop: 12 }}>
          <button onClick={runSimulation} disabled={!transcript || running}>
            {running ? "Running..." : "Run Simulation"}
          </button>
        </div>
      </div>
      <div className="card" style={{ flex: 1, minWidth: 300 }}>
        <h2>Simulation JSON</h2>
        <pre>{result || "No result yet."}</pre>
      </div>
    </div>
  );
}

