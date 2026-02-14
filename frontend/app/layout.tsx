import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <h1>Multiverse Copilot</h1>
          <p>Voice-driven parallel-reality decision engine powered by Amazon Nova.</p>
          <div className="row" style={{ marginBottom: 14 }}>
            <Link href="/voice">Voice Console</Link>
            <Link href="/kb">Knowledge Base</Link>
          </div>
          {children}
        </div>
      </body>
    </html>
  );
}

