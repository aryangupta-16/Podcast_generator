'use client'
import React, { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";
import Link from "next/link";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await axios.post("https://podcast-generator-qzhs.onrender.com/auth/login", {
        email,
        password,
      });
      Cookies.set("token", res.data?.access_token, { expires: 7000 });
      if (typeof window !== "undefined") {
        localStorage.setItem("credits", res.data?.credits);
      }
      router.push("/podcastFormPage");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Login failed. Please check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8 animate-slide-down">
          <Link href="/" className="inline-block mb-6">
            <h1 className="text-3xl font-bold text-gradient">Podcast Generator</h1>
          </Link>
          <h2 className="text-2xl font-semibold text-white mb-2">Welcome Back</h2>
          <p className="text-gray-300">Sign in to continue creating amazing podcasts</p>
        </div>

        {/* Login Form */}
        <form
          onSubmit={handleSubmit}
          className="glass-effect-strong p-8 rounded-3xl shadow-2xl animate-scale-in"
        >
          <div className="space-y-6">
            <div>
              <label className="block mb-2 text-white font-medium">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300"
                placeholder="Enter your email"
              />
            </div>
            
            <div>
              <label className="block mb-2 text-white font-medium">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300"
                placeholder="Enter your password"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-500/20 border border-red-500/30 rounded-xl text-red-200 text-sm animate-slide-up">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-button-gradient text-white py-3 rounded-xl font-semibold shadow-glow hover:shadow-glow-purple transition-all duration-300 hover-lift disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="spinner"></div>
                  Signing In...
                </span>
              ) : (
                "Sign In"
              )}
            </button>
          </div>

          <div className="mt-6 text-center">
            <span className="text-gray-300">Don't have an account? </span>
            <Link href="/signup" className="text-gradient hover:text-gradient-purple transition-all duration-300 font-medium">
              Create Account
            </Link>
          </div>
        </form>

        {/* Demo Credentials */}
        <div className="mt-6 glass-effect p-4 rounded-2xl animate-slide-up animate-delay-200">
          <p className="text-gray-300 text-sm text-center mb-2">Demo Credentials:</p>
          <div className="text-center text-xs text-gray-400 space-y-1">
            <div>Email: sb-4aju245416428@personal.example.com</div>
            <div>Password: K9pCPv+7</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
