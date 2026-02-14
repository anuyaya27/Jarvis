"use client";

import { useMemo, useRef, useState } from "react";

const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function VoicePage() {
  const [useBrowserMic, setUseBrowserMic] = useState(true);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [result, setResult] = useState("");
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
    const resp = await fetch(`${backend}/simulate`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        transcript,
        constraints: { scenario_horizon: "next_quarter", branch_count_hint: 5 }
      })
    });
    const data = await resp.json();
    setResult(JSON.stringify(data, null, 2) || "");
    setRunning(false);
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
        <h2>Simulation JSON</h2>
        <pre>{result || "No result yet."}</pre>
      </div>
    </div>
  );
}
