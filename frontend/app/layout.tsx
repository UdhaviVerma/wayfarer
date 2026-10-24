import "./globals.css";
import Link from "next/link";
import { ReactNode } from "react";

import { ThemeToggle } from "@/components/theme-toggle";
import { ThemeProvider } from "@/components/theme-provider";

export const metadata = {
  title: "Wayfarer | Global Developer Relocation Advisor",
  description: "AI-powered relocation advisor for developers",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <div className="mx-auto min-h-screen max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <header className="mb-8 flex items-center justify-between">
              <Link href="/" className="text-xl font-semibold">Wayfarer</Link>
              <nav className="flex items-center gap-3">
                <Link href="/dashboard" className="text-sm">Dashboard</Link>
                <Link href="/pricing" className="text-sm">Pricing</Link>
                <Link href="/faq" className="text-sm">FAQ</Link>
                <Link href="/blog" className="text-sm">Blog</Link>
                <ThemeToggle />
              </nav>
            </header>
            {children}
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
