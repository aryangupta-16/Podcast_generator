"use client"
import "../styles/globals.css";
import type { ReactNode } from "react";
import Navbar from "./components/Navbar";
import { PayPalScriptProvider } from "@paypal/react-paypal-js";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="text-gray-900 min-h-screen font-inter relative">
        {/* Animated background elements */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-primary-400/20 to-secondary-400/20 rounded-full blur-3xl animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-accent-400/20 to-primary-400/20 rounded-full blur-3xl animate-float animate-delay-200"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-secondary-400/10 to-primary-400/10 rounded-full blur-3xl animate-pulse-glow"></div>
        </div>
        
        <main className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
          <PayPalScriptProvider options={{ clientId: "ASTr9NGLxso4SaQtugKYf3oqa-uM9Pni-C9wZX_zPsRnny_N1pfZthh5v37fmvkwHkELyc3l5qXXolJf", currency: "USD" }}>
            {children}
          </PayPalScriptProvider>
        </main>
      </body>
    </html>
  );
}
