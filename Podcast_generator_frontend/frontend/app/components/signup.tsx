'use client'
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Link from "next/link";

const Signup = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      await axios.post("https://podcast-generator-qzhs.onrender.com/auth/signup", {
        name,
        email,
        password,
      });
      setSuccess("User registered successfully. Redirecting to login...");
      setTimeout(() => router.push("/login"), 1500);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Signup failed. Please try again."
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
          <h2 className="text-2xl font-semibold text-white mb-2">Create Account</h2>
          <p className="text-gray-300">Join thousands of creators making amazing podcasts</p>
        </div>

        {/* Signup Form */}
        <form
          onSubmit={handleSubmit}
          className="glass-effect-strong p-8 rounded-3xl shadow-2xl animate-scale-in"
        >
          <div className="space-y-6">
            <div>
              <label className="block mb-2 text-white font-medium">Full Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300"
                placeholder="Enter your full name"
              />
            </div>

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
                placeholder="Create a strong password"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-500/20 border border-red-500/30 rounded-xl text-red-200 text-sm animate-slide-up">
                {error}
              </div>
            )}

            {success && (
              <div className="p-3 bg-green-500/20 border border-green-500/30 rounded-xl text-green-200 text-sm animate-slide-up">
                {success}
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
                  Creating Account...
                </span>
              ) : (
                "Create Account"
              )}
            </button>
          </div>

          <div className="mt-6 text-center">
            <span className="text-gray-300">Already have an account? </span>
            <Link href="/login" className="text-gradient hover:text-gradient-purple transition-all duration-300 font-medium">
              Sign In
            </Link>
          </div>
        </form>

        {/* Benefits */}
        <div className="mt-6 glass-effect p-4 rounded-2xl animate-slide-up animate-delay-200">
          <p className="text-gray-300 text-sm text-center mb-3">What you get:</p>
          <div className="grid grid-cols-2 gap-2 text-xs text-gray-400">
            <div className="flex items-center gap-1">
              <span className="text-green-400">✓</span>
              Unlimited podcasts
            </div>
            <div className="flex items-center gap-1">
              <span className="text-green-400">✓</span>
              Multiple voices
            </div>
            <div className="flex items-center gap-1">
              <span className="text-green-400">✓</span>
              Custom tones
            </div>
            <div className="flex items-center gap-1">
              <span className="text-green-400">✓</span>
              High quality audio
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
