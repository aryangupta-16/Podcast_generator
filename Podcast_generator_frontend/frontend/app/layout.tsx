import "../styles/globals.css";
import type { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen font-inter">
        <header className="sticky top-0 z-30 w-full bg-white/80 backdrop-blur shadow-soft border-b border-gray-100">
          <div className="max-w-3xl mx-auto flex items-center gap-4 py-6 px-4 sm:px-8">
            <img src="/logo.svg" alt="AI Podcast Generator logo" className="w-10 h-10 rounded-2xl shadow-soft" />
            <div>
              <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">AI Podcast Generator</h1>
              <p className="text-gray-500 text-sm sm:text-base font-normal -mt-1">Turn any topic into a podcast with AI.</p>
            </div>
          </div>
        </header>
        <main className="flex flex-col items-center justify-center min-h-[70vh] px-4">
          {children}
        </main>
      </body>
    </html>
  );
}
