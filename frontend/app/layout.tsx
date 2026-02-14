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
        <style jsx>{`
          .top-nav {
            background: var(--color-bg-primary);
            border-bottom: 1px solid var(--color-border-light);
            box-shadow: var(--shadow-sm);
            position: sticky;
            top: 0;
            z-index: 100;
          }
          
          .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
          }
          
          .nav-brand {
            display: flex;
            flex-direction: column;
            gap: 0.125rem;
          }
          
          .brand-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--color-text-primary);
            margin: 0;
          }
          
          .brand-tagline {
            font-size: 0.75rem;
            color: var(--color-text-tertiary);
            margin: 0;
          }
          
          .nav-links {
            display: flex;
            gap: 0.5rem;
          }
          
          .nav-link {
            padding: 0.5rem 1rem;
            font-size: 0.9375rem;
            font-weight: 500;
            color: var(--color-text-secondary);
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
          }
          
          .nav-link:hover {
            color: var(--color-text-primary);
            background: var(--color-bg-secondary);
          }
          
          .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
          }
          
          @media (max-width: 640px) {
            .nav-container {
              flex-direction: column;
              align-items: flex-start;
              gap: 1rem;
            }
            
            .nav-links {
              width: 100%;
            }
            
            .nav-link {
              flex: 1;
              text-align: center;
            }
            
            .main-content {
              padding: 1.5rem 1rem;
            }
          }
        `}</style>
      </body>
    </html>
  );
}
