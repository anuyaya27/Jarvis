'use client';

import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

interface Document {
  name: string;
  size: number;
  status: 'uploading' | 'success' | 'error';
}

interface SearchResult {
  chunk_text: string;
  metadata: any;
  score: number;
}

export default function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const newDocs: Document[] = Array.from(files).map((file) => ({
      name: file.name,
      size: file.size,
      status: 'uploading',
    }));

    setDocuments((prev) => [...prev, ...newDocs]);

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch(`${API_BASE}/kb/upload`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Upload failed: ${response.statusText}`);
        }

        setDocuments((prev) =>
          prev.map((doc) =>
            doc.name === file.name ? { ...doc, status: 'success' } : doc
          )
        );
      } catch (err) {
        setDocuments((prev) =>
          prev.map((doc) =>
            doc.name === file.name ? { ...doc, status: 'error' } : doc
          )
        );
      }
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsSearching(true);
    setError(null);
    setResults([]);

    try {
      const response = await fetch(`${API_BASE}/kb/search?q=${encodeURIComponent(query)}`);

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError(err.message || 'An error occurred during search.');
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="kb-page">
      <div className="page-header">
        <h1>Knowledge Base</h1>
        <p className="text-secondary">
          Upload documents and search your organization's knowledge
        </p>
      </div>

      <div className="kb-layout">
        {/* Upload Section */}
        <div className="upload-section card">
          <div className="card-header">
            <h3 className="card-title">Upload Documents</h3>
          </div>
          <div className="upload-area">
            <input
              type="file"
              id="file-upload"
              multiple
              accept=".pdf,.txt,.md,.docx"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-upload" className="upload-dropzone">
              <div className="upload-icon">📁</div>
              <p className="upload-text">Click to upload or drag and drop</p>
              <p className="upload-hint text-xs text-tertiary">
                PDF, TXT, MD, DOCX (max 10MB each)
              </p>
            </label>
          </div>

          {documents.length > 0 && (
            <div className="documents-list">
              <h4 className="list-title text-sm font-semibold">Uploaded Documents</h4>
              {documents.map((doc, idx) => (
                <div key={idx} className="document-item">
                  <div className="doc-info">
                    <span className="doc-name text-sm truncate">{doc.name}</span>
                    <span className="doc-size text-xs text-tertiary">
                      {(doc.size / 1024).toFixed(1)} KB
                    </span>
                  </div>
                  <span
                    className={`badge ${
                      doc.status === 'success'
                        ? 'badge-success'
                        : doc.status === 'error'
                        ? 'badge-danger'
                        : 'badge-info'
                    }`}
                  >
                    {doc.status === 'uploading' && '⏳ Uploading'}
                    {doc.status === 'success' && '✓ Ready'}
                    {doc.status === 'error' && '✗ Failed'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Search Section */}
        <div className="search-section card">
          <div className="card-header">
            <h3 className="card-title">Search Knowledge</h3>
          </div>
          <div className="search-input-group">
            <input
              type="text"
              className="input"
              placeholder="Enter your query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              disabled={isSearching}
            />
            <button
              className="btn btn-primary"
              onClick={handleSearch}
              disabled={isSearching || !query.trim()}
            >
              {isSearching ? 'Searching...' : '🔍 Search'}
            </button>
          </div>

          {error && (
            <div className="alert alert-error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {results.length > 0 && (
            <div className="results-list">
              <h4 className="list-title text-sm font-semibold">
                {results.length} result{results.length !== 1 ? 's' : ''} found
              </h4>
              {results.map((result, idx) => (
                <div key={idx} className="result-card card">
                  <div className="result-header">
                    <span className="badge badge-info">
                      Score: {result.score.toFixed(2)}
                    </span>
                  </div>
                  <p className="result-text text-sm">{result.chunk_text}</p>
                  {result.metadata && Object.keys(result.metadata).length > 0 && (
                    <div className="result-meta">
                      {Object.entries(result.metadata).map(([key, value]) => (
                        <span key={key} className="meta-item text-xs text-tertiary">
                          {key}: {String(value)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .kb-page {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        
        .page-header {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .kb-layout {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
        }
        
        .upload-section,
        .search-section {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .upload-area {
          margin-bottom: 0.5rem;
        }
        
        .upload-dropzone {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 3rem 2rem;
          border: 2px dashed var(--color-border);
          border-radius: var(--radius-lg);
          background: var(--color-bg-secondary);
          cursor: pointer;
          transition: all 0.2s ease;
        }
        
        .upload-dropzone:hover {
          border-color: var(--color-accent);
          background: var(--color-bg-primary);
        }
        
        .upload-icon {
          font-size: 3rem;
          margin-bottom: 0.5rem;
        }
        
        .upload-text {
          font-weight: 500;
          margin-bottom: 0.25rem;
        }
        
        .upload-hint {
          margin: 0;
        }
        
        .documents-list,
        .results-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        
        .list-title {
          margin-bottom: 0.25rem;
        }
        
        .document-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0.75rem;
          background: var(--color-bg-secondary);
          border-radius: var(--radius-md);
          gap: 1rem;
        }
        
        .doc-info {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          flex: 1;
          min-width: 0;
        }
        
        .search-input-group {
          display: flex;
          gap: 0.75rem;
        }
        
        .search-input-group input {
          flex: 1;
        }
        
        .result-card {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          padding: 1rem;
        }
        
        .result-header {
          display: flex;
          align-items: center;
          justify-content: flex-end;
        }
        
        .result-text {
          line-height: 1.6;
        }
        
        .result-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          padding-top: 0.5rem;
          border-top: 1px solid var(--color-border-light);
        }
        
        .meta-item {
          padding: 0.25rem 0.5rem;
          background: var(--color-bg-secondary);
          border-radius: var(--radius-sm);
        }
        
        @media (max-width: 1024px) {
          .kb-layout {
            grid-template-columns: 1fr;
          }
        }
        
        @media (max-width: 640px) {
          .search-input-group {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
}
