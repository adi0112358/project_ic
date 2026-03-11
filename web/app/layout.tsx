import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Project IC",
  description: "AI-assisted fungal infection classifier for type 2 diabetes"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main>
          <div className="container">
            <header className="header">
              <div className="brand">Project IC</div>
              <nav className="nav">
                <Link href="/">Home</Link>
                <Link href="/upload">Upload</Link>
                <Link href="/chat">Chat</Link>
              </nav>
            </header>
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
