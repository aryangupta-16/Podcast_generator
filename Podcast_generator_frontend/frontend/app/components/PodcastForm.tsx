"use client"

import React, { useState } from "react";
import VoiceSelector from "./VoiceSelector";
import ToneSelector from "./ToneSelector";
import AudioPlayer from "./AudioPlayer";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import Cookies from "js-cookie";
import Navbar from "./Navbar";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

const DUMMY_VOICES = [
  { value: "fable", label: "Fable" },
  { value: "nova", label: "Nova" },
  { value: "echo", label: "Echo" },
  { value: "shimmer", label: "Shimmer" },
  { value: "onyx", label: "Onyx" },
  { value: "alloy", label: "Alloy" },
];
const DUMMY_TONES = [
  { value: "storytelling", label: "Storytelling" },
  { value: "entertaining", label: "Entertaining" },
  { value: "educational", label: "Educational" },
  { value: "conversational", label: "Conversational" },
  { value: "casual", label: "Casual" },
  { value: "professional", label: "Professional" },
];

const BACKEND_URL = "http://localhost:8000";

export default function PodcastForm() {
  const [topic, setTopic] = useState("");
  const [voice, setVoice] = useState(DUMMY_VOICES[0].value);
  const [tone, setTone] = useState(DUMMY_TONES[0].value);
  const [duration, setDuration] = useState(5);
  const [loading, setLoading] = useState(false);
  const [audioPath, setAudioPath] = useState<string | undefined>();

  const [creditsPopup, setCreditsPopup] = useState(false);
  const [credits, setCredits] = useState('');

  const [error,setError] = useState("");

  const handleCreditsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only update if the value is a valid number or empty string
    if (value === '' || /^\d+$/.test(value)) {
      setCredits(value);
    }
  };

  const token = Cookies.get("token");
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAudioPath(undefined);
    try {

      const headers = {
        Authorization: `Bearer ${token}`,
      }

      if(duration>1){
        // setError("Duration must be 1 minute");
        alert("keep duration 1 minute")
        console.log(error);
        return;
      }
      const res = await axios.post(
        `${BACKEND_URL}/api/v1/generate-podcast`,
        {
          topic,
          tone,
          voice,
          duration_minutes: duration,
        },
        { timeout: 180000, headers }
      );
      if (res.data && res.data.success && res.data.audio_file_path) {
        console.log(res.data.audio_file_path);
        console.log(res.data);
        setAudioPath(`${BACKEND_URL}/api/v1/download/${res.data.audio_file_path}`);
        toast.success("Podcast generated!");
      } else {
        toast.error("Failed to generate podcast. Try again.");
      }
    } catch (err: any) {
      toast.error("Error generating podcast. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAudioPath(undefined);
    setTopic("");
    setVoice(DUMMY_VOICES[0].value);
    setTone(DUMMY_TONES[0].value);
    setDuration(5);
  };

  return (
    <>
    <div className={`relative min-h-screen ${creditsPopup ? 'filter blur-sm' : ''} transition-all duration-300`}>

    <Navbar creditsPopup={creditsPopup} setCreditsPopup={setCreditsPopup}/>


    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Demo Credentials */}
      <div className="mb-8 glass-effect p-4 rounded-2xl animate-slide-up">
        <p className="text-white text-sm text-center mb-2">Demo Credentials:</p>
        <div className="text-center text-xs text-gray-300 space-y-1">
          <div>Email: sb-4aju245416428@personal.example.com</div>
          <div>Password: K9pCPv+7</div>
        </div>
      </div>

      <Toaster position="top-right" />
      
      <form
        className="w-full glass-effect-strong shadow-2xl rounded-3xl p-8 flex flex-col gap-8 animate-scale-in"
        onSubmit={handleSubmit}
      >
        {/* Header */}
        <div className="text-center mb-4">
          <h2 className="text-3xl font-bold text-white mb-2">Create Your Podcast</h2>
          <p className="text-gray-300">Transform any idea into a professional podcast episode</p>
        </div>

        {/* Topic Input */}
        <div className="flex flex-col gap-3">
          <label htmlFor="topic" className="font-semibold text-white text-lg">🎯 Podcast Topic</label>
          <input
            id="topic"
            type="text"
            required
            value={topic}
            onChange={e => setTopic(e.target.value)}
            placeholder="E.g. How AI will revolutionize the future of work"
            className="px-6 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 text-lg"
          />
        </div>

        {/* Voice and Tone Selectors */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <VoiceSelector voices={DUMMY_VOICES} value={voice} onChange={setVoice} />
          <ToneSelector tones={DUMMY_TONES} value={tone} onChange={setTone} />
        </div>

        {/* Duration Slider */}
        <div className="flex flex-col gap-4">
          <label htmlFor="duration" className="font-semibold text-white text-lg">⏱️ Duration: <span className="text-gradient font-bold">{duration} min</span></label>
          <div className="relative">
            <input
              id="duration"
              type="range"
              min={1}
              max={10}
              value={duration}
              onChange={e => setDuration(Number(e.target.value))}
              className="w-full h-3 bg-white/20 rounded-full appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, #0ea5e9 0%, #6366f1 ${(duration - 1) * 11.11}%, rgba(255,255,255,0.2) ${(duration - 1) * 11.11}%, rgba(255,255,255,0.2) 100%)`
              }}
            />
            <div className="flex justify-between text-xs text-gray-400 mt-2">
              <span>1 min</span>
              <span>10 min</span>
            </div>
          </div>
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          className="w-full py-4 rounded-2xl bg-button-gradient text-white font-bold text-lg shadow-glow hover:shadow-glow-purple transition-all duration-300 hover-lift disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >

          {loading ? (
            <span className="flex items-center justify-center gap-3">
              <div className="spinner"></div>
              Generating Your Podcast...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              🎙️ Generate Podcast
            </span>
          )}
        </button>

        { error && 
            <div className="text-red-500 text-sm">
            {error}
          </div>}
      </form>
      
      <AudioPlayer src={audioPath} isLoading={loading} onReset={audioPath ? handleReset : undefined} />
    </div>
    </div>

      {
        creditsPopup && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
            <div className="glass-effect-strong rounded-3xl p-8 shadow-2xl max-w-md w-full mx-4 animate-scale-in">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-2xl shadow-glow flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-2xl">💳</span>
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Add Credits</h3>
                <p className="text-gray-300">Purchase credits to generate more podcasts</p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-white font-medium mb-2">Amount (USD)</label>
                  <input 
                    type="text" 
                    inputMode="numeric"
                    pattern="[0-9]*"
                    value={credits}
                    onChange={handleCreditsChange}
                    placeholder="Enter amount" 
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300"
                  />
                </div>
                
                <div className="bg-white/5 rounded-xl p-4">
                  <PayPalButtons
                    style={{ 
                      layout: "vertical",
                      color: "blue",
                      shape: "pill",
                      label: "paypal"
                    }}
                    createOrder={(_, actions) => {
                      return fetch("http://localhost:8000/api/v1/orders", {
                        method: "POST",
                        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
                        body: JSON.stringify({ amount: `${credits}.00`, currency: "USD" }),
                      })
                        .then((res) => res.json())
                        .then((order) => order.id);
                    }}
                    onApprove={(data, actions) => {
                      return fetch(`http://localhost:8000/api/v1/orders/${data.orderID}/capture`, {
                        method: "POST",
                        headers: {Authorization: `Bearer ${token}` },
                      })
                        .then((res) => res.json())
                        .then((details) => {
                          console.log(details);
                          alert("Transaction completed by " + details.payer.name.given_name+ " "+ details.purchase_units[0].payments.captures[0].amount.value);
                          setCreditsPopup(false);
                          const storedCredits = localStorage.getItem("credits");
                          const addedCredits = Number(details.purchase_units[0].payments.captures[0].amount.value);
                          const newCredits = (storedCredits ? Number(storedCredits) : 0) + addedCredits;
                          localStorage.setItem("credits", newCredits.toString());
                          setCredits('');
                        });
                    }}
                  />
                </div>
                
                <button 
                  className="w-full py-3 glass-effect text-white rounded-xl font-semibold hover:bg-white/20 transition-all duration-300"
                  onClick={() => {
                    setCreditsPopup(false);
                    setCredits('');
                  }}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )
      }
    </>
  );
}

