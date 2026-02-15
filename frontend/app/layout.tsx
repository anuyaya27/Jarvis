import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Multiverse Copilot",
  description: "Voice-driven parallel reality decision engine for high-stakes business strategy",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <nav className="top-nav">
          <div className="nav-container">
            <div className="nav-brand">
              <Link href="/">
                <h1 className="brand-title">Multiverse Copilot</h1>
                <p className="brand-tagline">AI-Powered Strategy Simulation</p>
              </Link>
            </div>
            <div className="nav-links">
              <Link href="/voice" className="nav-link">
                Voice Console
              </Link>
              <Link href="/kb" className="nav-link">
                Knowledge Base
              </Link>
            </div>
          </div>
        </nav>
        <main className="main-content">
          {children}
        </main>
      </body>
    </html>
  );
}
