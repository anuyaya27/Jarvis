"use client";

import { FormEvent, useState } from "react";

const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

type Match = { text: string; source: string; score: number };

export default function KBPage() {
  const [query, setQuery] = useState("");
  const [matches, setMatches] = useState<Match[]>([]);
  const [uploadStatus, setUploadStatus] = useState("");

  async function upload(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const input = form.elements.namedItem("doc") as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;
    const fd = new FormData();
    fd.append("file", input.files[0]);
    const resp = await fetch(`${backend}/kb/upload`, { method: "POST", body: fd });
    const data = await resp.json();
    setUploadStatus(`Uploaded doc_id=${data.doc_id}, chunks=${data.chunks}`);
    form.reset();
  }

  async function search() {
    const resp = await fetch(`${backend}/kb/query`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 })
    });
    const data = await resp.json();
    setMatches(data.matches || []);
  }

  return (
    <div className="row">
      <div className="card" style={{ flex: 1, minWidth: 300 }}>
        <h2>Knowledge Base</h2>
        <form onSubmit={upload}>
          <input type="file" name="doc" accept=".txt,.md,.pdf" />
          <div style={{ marginTop: 10 }}>
            <button type="submit">Upload</button>
          </div>
        </form>
        <p>{uploadStatus}</p>
      </div>
      <div className="card" style={{ flex: 1, minWidth: 300 }}>
        <h2>Semantic Search</h2>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search strategy context..." />
        <div style={{ marginTop: 10 }}>
          <button onClick={search} disabled={!query}>Search</button>
        </div>
        {matches.map((m, idx) => (
          <div key={idx} style={{ marginTop: 10, borderTop: "1px solid #e2e8ee", paddingTop: 10 }}>
            <div><b>{m.source}</b> ({m.score.toFixed(3)})</div>
            <div>{m.text}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

